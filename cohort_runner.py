"""In-memory cohort run executor with safe mid-run cancellation (CU-14).

A :class:`CohortRun` executes an ordered list of subtasks, one worker thread
per subtask, and transitions through ``pending -> running -> completed`` or
``failed``. A cancel request observed mid-run moves the run to
``cancel_requested``, stops launching new subtasks, gives the in-flight
subtask a grace period to cancel cooperatively, force-aborts it as a
fallback, then persists the terminal ``cancelled`` status with a timestamp
and whatever partial results were recorded.

Terminal state writes are idempotent: whichever of cancellation or natural
completion performs the first terminal transition wins, so a cancel racing a
finish can never produce an inconsistent final status. Only the standard
library is used; no new dependencies are introduced.
"""

from __future__ import annotations

import ctypes
import enum
import threading
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

__all__ = [
    "CancellationToken",
    "CohortRun",
    "CohortRunError",
    "InvalidRunStateError",
    "RunEvent",
    "RunStatus",
    "Subtask",
    "SubtaskAborted",
    "SubtaskCancelled",
    "TERMINAL_STATUSES",
]


class RunStatus(str, enum.Enum):
    """Lifecycle states of a cohort run, as reported to clients."""

    PENDING = "pending"
    RUNNING = "running"
    CANCEL_REQUESTED = "cancel_requested"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


TERMINAL_STATUSES: frozenset[RunStatus] = frozenset(
    {RunStatus.COMPLETED, RunStatus.FAILED, RunStatus.CANCELLED}
)


class CohortRunError(Exception):
    """Base class for cohort runner errors."""


class InvalidRunStateError(CohortRunError):
    """Raised when an operation is invalid for the run's current state."""


class SubtaskCancelled(Exception):
    """Raised by a subtask to report that it stopped cooperatively."""


class SubtaskAborted(BaseException):
    """Injected into a worker thread when cooperative cancellation times out.

    Derives from :class:`BaseException` so a subtask's broad ``except
    Exception`` handlers cannot swallow a forced abort.
    """


def _force_abort(thread: threading.Thread, exc_type: type[BaseException]) -> bool:
    """Best effort: raise ``exc_type`` inside ``thread`` and report delivery.

    CPython has no safe way to kill a thread, so this injects an asynchronous
    exception via ``PyThreadState_SetAsyncExc`` (stdlib ``ctypes``). The
    exception only lands between bytecodes, so a thread blocked inside a C
    call (for example ``time.sleep``) sees it once that call returns. On
    runtimes without the API the function reports failure and the caller
    falls back to abandoning the daemonized worker thread.
    """
    ident = thread.ident
    if ident is None:
        return False
    try:
        delivered = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_ulong(ident), ctypes.py_object(exc_type)
        )
    except Exception:  # non-CPython runtime without the C API
        return False
    if delivered > 1:  # defensive: reset any stray injections
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_ulong(ident), None)
        return False
    return delivered == 1


class CancellationToken:
    """Cooperative cancellation signal handed to every subtask invocation."""

    def __init__(self) -> None:
        self._event = threading.Event()

    @property
    def cancelled(self) -> bool:
        """Whether cancellation has been requested for the owning run."""
        return self._event.is_set()

    def cancel(self) -> None:
        """Signal the token; idempotent and safe to call from any thread."""
        self._event.set()

    def wait(self, timeout: float | None = None) -> bool:
        """Block until cancelled or ``timeout`` elapses; return cancelled."""
        return self._event.wait(timeout)


@dataclass(frozen=True)
class Subtask:
    """A single unit of cohort work.

    ``func`` receives the run's :class:`CancellationToken` and is expected to
    poll it (or ``wait`` on it) so that cancellation stays cooperative.
    """

    subtask_id: str
    func: Callable[[CancellationToken], Any]


@dataclass(frozen=True)
class RunEvent:
    """A timestamped status/log event emitted by a run."""

    timestamp: float
    level: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize the event for clients and dashboards."""
        return {"timestamp": self.timestamp, "level": self.level, "message": self.message}


@dataclass
class _SubtaskOutcome:
    """Outcome recorded by a subtask worker thread.

    Defaults to ``aborted`` so a thread that dies from an injected
    :class:`SubtaskAborted` inside the worker handler is still reported as
    aborted instead of being silently lost.
    """

    state: str = "aborted"
    result: Any = None
    error: BaseException | None = None


class CohortRun:
    """Executes subtasks sequentially in worker threads with cancellation.

    The run owns its state machine and may be cancelled from another thread
    while :meth:`execute` or :meth:`start` is in flight.
    """

    def __init__(
        self,
        run_id: str,
        subtasks: Sequence[Subtask],
        *,
        grace_period: float = 5.0,
        poll_interval: float = 0.02,
        abort_join_timeout: float = 2.0,
    ) -> None:
        """Create a run that is ``pending`` until :meth:`execute` starts it.

        ``grace_period`` bounds how long an in-flight subtask may ignore the
        cooperative token before a forced abort is delivered;
        ``abort_join_timeout`` bounds how long the run waits for a worker to
        die from the forced abort before abandoning it.
        """
        self._run_id = run_id
        self._subtasks = tuple(subtasks)
        self._grace_period = grace_period
        self._poll_interval = poll_interval
        self._abort_join_timeout = abort_join_timeout
        self._lock = threading.RLock()
        self._status = RunStatus.PENDING
        self._results: dict[str, Any] = {}
        self._error: BaseException | None = None
        self._events: list[RunEvent] = []
        self._started_at: float | None = None
        self._finished_at: float | None = None
        self._cancel_event = threading.Event()
        self._token = CancellationToken()
        self._done = threading.Event()
        self._thread: threading.Thread | None = None
        self._worker_threads: list[threading.Thread] = []
        self._abandoned_threads: list[threading.Thread] = []
        self._log("info", f"run {run_id} created with {len(self._subtasks)} subtask(s)")

    @property
    def run_id(self) -> str:
        """Identifier of this run."""
        return self._run_id

    @property
    def status(self) -> RunStatus:
        """Current lifecycle status of the run."""
        with self._lock:
            return self._status

    @property
    def results(self) -> dict[str, Any]:
        """Results recorded so far, including partial results after cancel."""
        with self._lock:
            return dict(self._results)

    @property
    def error(self) -> BaseException | None:
        """The exception that failed the run, if any."""
        with self._lock:
            return self._error

    @property
    def events(self) -> tuple[RunEvent, ...]:
        """Status/log events emitted so far, oldest first."""
        with self._lock:
            return tuple(self._events)

    @property
    def started_at(self) -> float | None:
        """Wall-clock time the run entered ``running``, if it ever did."""
        with self._lock:
            return self._started_at

    @property
    def finished_at(self) -> float | None:
        """Wall-clock time the run reached a terminal status, if it has."""
        with self._lock:
            return self._finished_at

    @property
    def cancel_requested(self) -> bool:
        """Whether a cancellation has been requested for this run."""
        return self._cancel_event.is_set()

    def request_cancel(self) -> bool:
        """Mark the run cancel-requested; return True if this call did it.

        Transitions ``pending`` or ``running`` to ``cancel_requested`` and
        signals the in-flight subtask's token. A no-op returning ``False``
        when the run is already cancel-requested or has finished, so a cancel
        racing natural completion can never clobber a terminal status. The
        event is signalled under the state lock so that the run loop's
        between-subtask check and the status transition are one atomic step.
        """
        with self._lock:
            if self._status in TERMINAL_STATUSES or self._status is RunStatus.CANCEL_REQUESTED:
                return False
            self._cancel_event.set()
            self._token.cancel()
            self._status = RunStatus.CANCEL_REQUESTED
        self._log("info", f"run {self._run_id}: cancellation requested")
        return True

    def start(self) -> None:
        """Execute the run on a daemon background thread; return immediately."""
        with self._lock:
            if self._thread is not None:
                raise InvalidRunStateError(f"run {self._run_id} already started")
            if self._status in TERMINAL_STATUSES:
                raise InvalidRunStateError(
                    f"run {self._run_id} already finished ({self._status.value})"
                )
            self._thread = threading.Thread(
                target=self.execute, name=f"cohort-run-{self._run_id}", daemon=True
            )
        self._thread.start()

    def wait(self, timeout: float | None = None) -> bool:
        """Block until the run reaches a terminal state; True if it did."""
        return self._done.wait(timeout)

    def execute(self) -> RunStatus:
        """Run every subtask in order and return the final status.

        Raises :class:`InvalidRunStateError` if the run was already executed
        or finished; a run cancelled before start finalizes as ``cancelled``
        without launching any subtask.
        """
        with self._lock:
            if self._status is RunStatus.PENDING:
                self._status = RunStatus.RUNNING
                self._started_at = time.time()
            elif self._status is not RunStatus.CANCEL_REQUESTED:
                raise InvalidRunStateError(
                    f"run {self._run_id} cannot execute from status {self._status.value}"
                )
            cancelled_before_start = self._status is RunStatus.CANCEL_REQUESTED
        try:
            if cancelled_before_start:
                self._log("info", f"run {self._run_id}: cancelled before any subtask started")
            else:
                for spec in self._subtasks:
                    if self._cancel_event.is_set():
                        break
                    if not self._execute_subtask(spec):
                        break
            if self._cancel_event.is_set():
                self._finalize(RunStatus.CANCELLED)
            else:
                self._finalize(RunStatus.COMPLETED)
        except BaseException as exc:  # defensive: never leave the run dangling
            with self._lock:
                self._error = exc
            raise
        finally:
            with self._lock:
                terminal = self._status in TERMINAL_STATUSES
            if not terminal:
                self._finalize(
                    RunStatus.CANCELLED if self._cancel_event.is_set() else RunStatus.FAILED
                )
            self._release_resources()
        return self.status

    def to_dict(self) -> dict[str, Any]:
        """Serialize the run for clients and dashboards.

        ``status`` carries the machine-readable value, including
        ``cancel_requested`` and ``cancelled``; ``results`` holds whatever
        partial results were recorded before a cancellation.
        """
        with self._lock:
            return {
                "run_id": self._run_id,
                "status": self._status.value,
                "cancel_requested": self._cancel_event.is_set(),
                "started_at": self._started_at,
                "finished_at": self._finished_at,
                "subtasks_total": len(self._subtasks),
                "subtasks_completed": len(self._results),
                "results": dict(self._results),
                "error": repr(self._error) if self._error is not None else None,
                "events": [event.to_dict() for event in self._events],
            }

    def _execute_subtask(self, spec: Subtask) -> bool:
        """Run one subtask; return False when the run must stop launching work."""
        outcome = _SubtaskOutcome()
        worker = threading.Thread(
            target=self._subtask_target,
            args=(spec, outcome),
            name=f"{self._run_id}:{spec.subtask_id}",
            daemon=True,
        )
        with self._lock:
            self._worker_threads.append(worker)
        self._log("info", f"run {self._run_id}: launching subtask {spec.subtask_id}")
        worker.start()
        grace_deadline: float | None = None
        abort_deadline: float | None = None
        while True:
            worker.join(self._poll_interval)
            if not worker.is_alive():
                break
            if not self._cancel_event.is_set():
                continue
            now = time.monotonic()
            if grace_deadline is None:
                grace_deadline = now + self._grace_period
                self._log(
                    "info",
                    f"subtask {spec.subtask_id}: cancellation grace period "
                    f"of {self._grace_period:g}s started",
                )
            elif abort_deadline is None and now >= grace_deadline:
                abort_deadline = now + self._abort_join_timeout
                delivered = _force_abort(worker, SubtaskAborted)
                detail = "delivered" if delivered else "not supported on this runtime"
                self._log(
                    "warning",
                    f"subtask {spec.subtask_id} ignored cancellation for "
                    f"{self._grace_period:g}s; forced abort {detail}",
                )
            elif abort_deadline is not None and now >= abort_deadline:
                with self._lock:
                    self._abandoned_threads.append(worker)
                self._log(
                    "warning",
                    f"subtask {spec.subtask_id} worker thread abandoned after forced abort",
                )
                break
        if worker.is_alive():
            return False  # abandoned: stop launching work, never rejoin it
        self._apply_outcome(spec, outcome)
        if outcome.state == "failed":
            with self._lock:
                self._error = outcome.error
            self._finalize(RunStatus.FAILED)
            return False
        return True

    def _subtask_target(self, spec: Subtask, outcome: _SubtaskOutcome) -> None:
        """Worker-thread body: run ``spec`` and record its outcome."""
        try:
            outcome.result = spec.func(self._token)
            outcome.state = "completed"
        except SubtaskAborted:
            outcome.state = "aborted"
        except SubtaskCancelled:
            outcome.state = "cancelled"
        except Exception as exc:
            outcome.state = "failed"
            outcome.error = exc

    def _apply_outcome(self, spec: Subtask, outcome: _SubtaskOutcome) -> None:
        """Record one finished subtask's result and emit its status event."""
        if outcome.state == "completed":
            with self._lock:
                self._results[spec.subtask_id] = outcome.result
            self._log("info", f"run {self._run_id}: subtask {spec.subtask_id} completed")
        elif outcome.state == "cancelled":
            self._log("info", f"run {self._run_id}: subtask {spec.subtask_id} acknowledged cancellation")
        elif outcome.state == "aborted":
            self._log("warning", f"run {self._run_id}: subtask {spec.subtask_id} was force-aborted")
        else:
            self._log(
                "error",
                f"run {self._run_id}: subtask {spec.subtask_id} failed: {outcome.error!r}",
            )

    def _finalize(self, status: RunStatus) -> bool:
        """Transition to a terminal status exactly once; True on success.

        Idempotent against concurrent completion: the first terminal
        transition wins and any later call, including a cancel racing a
        natural finish, observes the already-final status unchanged.
        """
        with self._lock:
            if self._status in TERMINAL_STATUSES:
                return False
            self._status = status
            self._finished_at = time.time()
        self._log("info", f"run {self._run_id}: finished with status {status.value}")
        self._done.set()
        return True

    def _release_resources(self) -> None:
        """Reap finished worker threads and account for the worker slots.

        Abandoned threads are daemonized and can no longer affect the run;
        they are reported rather than joined, because joining a thread that
        ignores cancellation could block forever.
        """
        with self._lock:
            workers = list(self._worker_threads)
            abandoned = list(self._abandoned_threads)
        for worker in workers:
            if worker.is_alive() and worker not in abandoned:
                worker.join(self._abort_join_timeout)
        self._log(
            "info",
            f"run {self._run_id}: released {len(workers) - len(abandoned)} "
            f"worker slot(s); {len(abandoned)} abandoned",
        )

    def _log(self, level: str, message: str) -> None:
        """Append a status/log event for this run."""
        with self._lock:
            self._events.append(RunEvent(time.time(), level, message))
