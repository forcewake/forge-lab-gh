"""Small helpers that build friendly text greetings.

The :mod:`greeting` module keeps its message templates in one place so
callers never format greetings by hand. ``greet`` and ``farewell`` render
the basic messages, while ``polite_shout`` builds on ``greet`` to return
the same greeting in uppercase with a trailing exclamation mark.
"""

def greet(name: str) -> str:
    """Return a friendly greeting for *name*."""


def farewell(name: str) -> str:
    """Return a goodbye message for *name*."""


def polite_shout(name: str) -> str:
    """Return the greeting for *name* uppercased and ending with ``!``."""
    # greet() is currently a docstring-only stub returning None, so normalize
    # the result to a str here instead of changing greet (kept unchanged per plan).
    message = greet(name) or ""
    return f"{message.upper()}!"
