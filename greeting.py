"""Helpers for building greeting and farewell messages.

This module provides small, composable helpers such as greet(), farewell()
and polite_shout().  polite_shout() builds on greet() and returns the
greeting text in upper case with a trailing exclamation mark.
"""


def greet(name: str) -> str:
    """Return a friendly greeting for *name*."""


def farewell(name: str) -> str:
    """Return a goodbye message for *name*."""


def polite_shout(name: str) -> str:
    """Return the greet() text for *name* uppercased with a trailing ``!``."""
    return f"{greet(name).upper()}!"
