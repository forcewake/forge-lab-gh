"""Greeting helpers for the lab repo.

This module provides small functions that build friendly greetings and
farewells for a person's name.  It stays dependency-free so it can be
imported anywhere.  On top of :func:`greet` it offers :func:`polite_shout`,
which uppercases the greeting and adds an exclamation mark.
"""


def greet(name: str) -> str:
    """Return a friendly greeting for *name*."""


def farewell(name: str) -> str:
    """Return a goodbye message for *name*."""


def polite_shout(name: str) -> str:
    """Return the greet() message for *name*, uppercased with a trailing ``!``."""
    # greet() is a docstring-only stub that currently returns None; the plan
    # forbids changing greet(), so coerce its result to a string to keep this
    # composed helper total.  The trailing '!' is added only when missing, so
    # greet output that already ends with '!' is not doubled.
    text = (greet(name) or "").upper()
    if not text.endswith("!"):
        text += "!"
    return text
