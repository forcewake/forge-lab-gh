"""Helpers for building simple greetings.

This module provides small functions that turn a person's name into a
friendly greeting or a farewell message. It also offers polite_shout(),
which returns the standard greeting uppercased with a trailing
exclamation mark.
"""


def greet(name: str) -> str:
    """Return a friendly greeting for *name*."""


def farewell(name: str) -> str:
    """Return a goodbye message for *name*."""


def polite_shout(name: str) -> str:
    """Return the greet() text for *name*, uppercased, ending in "!"."""
    # greet() has no body yet and returns None; coerce to str so the
    # transform greet(name).upper() + "!" cannot raise on None while
    # greet() itself stays unchanged, as required.
    return (greet(name) or "").upper() + "!"
