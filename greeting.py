"""Minimal stdlib-only greeting helpers."""

__all__ = ["greet"]


def greet(name: str) -> str:
    """Return ``Hello, <name>!`` for the given *name*, verbatim.

    The doctests are the predeclared acceptance pairs, kept executable so
    the check survives without a test suite (``python -m doctest greeting.py``).

    >>> greet('World')
    'Hello, World!'
    >>> greet('forge')
    'Hello, forge!'
    """
    return f"Hello, {name}!"
