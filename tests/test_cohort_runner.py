"""Tests for mid-run cancellation of :mod:`cohort_runner` (cohort CU-14)."""

from __future__ import annotations

import threading
import time

import pytest

from cohort_runner import (
    CancellationToken,
    CohortRun,
    InvalidRunStateError,
    RunStatus,
    Subtask,
    SubtaskCancelled,
)

JOIN_TIMEOUT = 10.0


def _quick(subtask_id: str, executed: list[str]) -> Subtask:
    """A subtask that records its execution and returns immediately."""

    def func(token: CancellationToken) -> str:
        executed.append(subtask_id)
        return f"{subtask_id}-result"

    return Subtask(subtask_id, func)


def test_cancel_before_start_executes_no_subtasks() -> None:
    executed: list[str] = []
    run = CohortRun("r1", [_quick("a", executed), _quick("b", executed)])

    assert run.request_cancel() is True
    assert run.status is RunStatus.CANCEL_REQUESTED

    assert run.execute() is RunStatus.CANCELLED
    assert executed == []
    assert run.results == {}
    assert run.started_at is None
    assert run.finished_at is not None
    assert run.status is RunStatus.CANCELLED


def test_cancel_mid_run_stops_new_work_and_preserves_partial_results() -> None:
    executed: list[str] = []
    started_b = threading.Event()

    def blocking_b(token: CancellationToken) -> str:
        executed.append("b")
        started_b.set()
        if token.wait(timeout=JOIN_TIMEOUT):
            raise SubtaskCancelled()
        return "b-result"

    run = CohortRun(
        "r2",
        [_quick("a", executed), Subtask("b", blocking_b), _quick("c", executed)],
        poll_interval=0.01,
    )
    worker = threading.Thread(target=run.execute, daemon=True)
    worker.start()

    assert started_b.wait(timeout=JOIN_TIMEOUT)
    assert run.request_cancel() is True
    worker.join(timeout=JOIN_TIMEOUT)

    assert run.status is RunStatus.CANCELLED
    assert executed == ["a", "b"], "subtask c must never be launched"
    assert run.results == {"a": "a-result"}, "partial results must be preserved"
    assert run.finished_at is not None
    assert any("cancellation requested" in event.message for event in run.events)


def test_forced_abort_after_grace_period_stops_the_run() -> None:
    executed: list[str] = []

    def stubborn(token: CancellationToken) -> str:
        executed.append("stubborn")
        while True:
            pass  # never polls the token, so cooperation cannot work

    run = CohortRun(
        "r3",
        [Subtask("stubborn", stubborn), _quick("after", executed)],
        grace_period=0.05,
        poll_interval=0.005,
        abort_join_timeout=0.05,
    )
    run.start()
    deadline = time.monotonic() + JOIN_TIMEOUT
    while (
        run.status is not RunStatus.RUNNING or "stubborn" not in executed
    ) and time.monotonic() < deadline:
        time.sleep(0.005)
    assert run.status is RunStatus.RUNNING, "cancel must arrive mid-run"

    assert run.request_cancel() is True
    assert run.wait(timeout=JOIN_TIMEOUT)

    assert run.status is RunStatus.CANCELLED
    assert executed == ["stubborn"], "subtask after must never be launched"
    warnings = [event.message for event in run.events if event.level == "warning"]
    assert any("forced abort" in message for message in warnings)


def test_cancel_racing_completion_is_consistent() -> None:
    """Each cancel racing a finish lands on exactly one terminal status."""
    for index in range(25):
        released = threading.Event()

        def racer(token: CancellationToken, index: int = index, released: threading.Event = released) -> str:
            released.set()
            return f"done-{index}"

        run = CohortRun(f"race-{index}", [Subtask("only", racer)], poll_interval=0.001)
        run.start()
        assert released.wait(timeout=JOIN_TIMEOUT)
        run.request_cancel()
        assert run.wait(timeout=JOIN_TIMEOUT)

        data = run.to_dict()
        assert data["status"] in {"completed", "cancelled"}
        assert data["finished_at"] is not None
        if data["status"] == "completed":
            assert data["results"] == {"only": f"done-{index}"}
            assert data["cancel_requested"] is False
            assert run.request_cancel() is False, "late cancel must be a no-op"
        else:
            assert data["cancel_requested"] is True
            assert run.status is RunStatus.CANCELLED


def test_cancel_after_finish_is_a_noop() -> None:
    executed: list[str] = []
    run = CohortRun("done", [_quick("a", executed)])
    assert run.execute() is RunStatus.COMPLETED
    finished_at = run.finished_at

    assert run.request_cancel() is False
    assert run.status is RunStatus.COMPLETED
    assert run.finished_at == finished_at
    with pytest.raises(InvalidRunStateError):
        run.execute()

    cancelled = CohortRun("done-cancelled", [_quick("a", [])])
    assert cancelled.request_cancel() is True
    assert cancelled.execute() is RunStatus.CANCELLED
    assert cancelled.request_cancel() is False
    assert cancelled.status is RunStatus.CANCELLED


def test_serialization_reports_cancelled_to_clients() -> None:
    executed: list[str] = []
    run = CohortRun("report", [_quick("a", executed)])
    assert run.to_dict()["status"] == "pending"

    assert run.request_cancel() is True
    assert run.to_dict()["status"] == "cancel_requested"

    assert run.execute() is RunStatus.CANCELLED
    data = run.to_dict()
    assert data["run_id"] == "report"
    assert data["status"] == "cancelled"
    assert data["cancel_requested"] is True
    assert data["finished_at"] is not None
    assert data["subtasks_completed"] == 0
    assert data["events"]


def test_subtask_failure_marks_run_failed_and_rejects_cancel() -> None:
    executed: list[str] = []

    def broken(token: CancellationToken) -> str:
        executed.append("broken")
        raise ValueError("boom")

    run = CohortRun("f1", [Subtask("broken", broken), _quick("after", executed)])
    assert run.execute() is RunStatus.FAILED
    assert executed == ["broken"]
    assert isinstance(run.error, ValueError)
    assert run.request_cancel() is False
    assert "boom" in run.to_dict()["error"]


def test_double_start_and_rerun_are_rejected() -> None:
    run = CohortRun("d1", [_quick("a", [])])
    run.start()
    with pytest.raises(InvalidRunStateError):
        run.start()
    assert run.wait(timeout=JOIN_TIMEOUT)
    assert run.status is RunStatus.COMPLETED
    with pytest.raises(InvalidRunStateError):
        run.start()
    with pytest.raises(InvalidRunStateError):
        run.execute()


def test_cancel_callback_reaches_cooperative_subtasks_via_token() -> None:
    observed: list[bool] = []

    def watcher(token: CancellationToken) -> bool:
        token.wait(timeout=JOIN_TIMEOUT)
        observed.append(token.cancelled)
        return "observed"

    run = CohortRun("token", [Subtask("watch", watcher)], poll_interval=0.01)
    worker = threading.Thread(target=run.execute, daemon=True)
    worker.start()
    run.request_cancel()
    worker.join(timeout=JOIN_TIMEOUT)

    assert observed == [True]
    assert run.status is RunStatus.CANCELLED
