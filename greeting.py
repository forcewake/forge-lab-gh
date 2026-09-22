"""Helpers for rendering friendly, human-facing greeting messages.

The :mod:`greeting` module keeps every message template in one place so
callers never format one by hand: :func:`greet` and :func:`farewell` render
the basic messages, while :func:`polite_shout` builds on :func:`greet` to
return its text uppercased with a trailing exclamation mark.
"""


def greet(name: str) -> str:
    """Return a friendly greeting for *name*."""


def farewell(name: str) -> str:
    """Return a goodbye message for *name*."""


def polite_shout(name: str) -> str:
    """Return the :func:`greet` message for *name*, uppercased, ending in ``!``."""
    # greet() is a docstring-only seed stub that currently returns None, so its
    # result is normalized to "" here instead of altering greet(): the approved
    # plan keeps every existing function unchanged.
    message = greet(name) or ""
    return message.upper() + "!"
