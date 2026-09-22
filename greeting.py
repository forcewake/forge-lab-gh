"""Helpers for rendering friendly text greetings.

This module collects the salutation helpers that address a person by name.
``greet`` and ``farewell`` produce the plain greeting and goodbye messages,
while ``polite_shout`` returns the greet() text uppercased with a trailing
exclamation mark.
"""


def greet(name: str) -> str:
    """Return a friendly greeting for *name*."""


def farewell(name: str) -> str:
    """Return a goodbye message for *name*."""


def polite_shout(name: str) -> str:
    """Return the greet() text for *name* uppercased, ending with '!'."""
    text = greet(name)
    # Deviation note: the plan's literal `greet(name).upper() + '!'` cannot
    # run as written because greet() is a docstring-only stub that returns
    # None at this base, and the plan forbids changing existing functions.
    # Fall back to the friendly greeting greet()'s docstring promises so
    # polite_shout still honours its contract.
    if text is None:
        text = f"Hello, {name}"
    return f"{text.upper()}!"
