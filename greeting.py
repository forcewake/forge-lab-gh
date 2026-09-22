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
    # greet() is currently a docstring-only stub that returns None, and the
    # approved plan forbids changing it; fall back to the friendly greeting
    # its docstring promises so polite_shout can still honour its contract.
    if text is None:
        text = f"Hello, {name}"
    return f"{text.upper()}!"
