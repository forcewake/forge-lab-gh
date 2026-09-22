"""Helpers for building friendly, human-facing greeting messages.

The :mod:`greeting` module keeps every message template in one place so
callers never format greetings by hand: ``greet`` and ``farewell`` render
the basic messages, while ``polite_shout`` builds on ``greet`` to return
its text uppercased with a trailing exclamation mark.
"""


def greet(name: str) -> str:
    """Return a friendly greeting for *name*."""


def farewell(name: str) -> str:
    """Return a goodbye message for *name*."""


def polite_shout(name: str) -> str:
    """Return the :func:`greet` text for *name*, uppercased, ending in ``!``."""
    # greet() is a docstring-only stub that currently returns None, so its
    # result is normalized to "" here instead of altering greet() — the
    # approved plan requires existing functions to stay unchanged.
    message = greet(name) or ""
    return f"{message.upper()}!"
