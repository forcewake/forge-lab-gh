"""Minimal stdlib-only greeting helpers."""

__all__ = ["greet"]


def greet(name: str) -> str:
    """Return ``Hello, <name>!`` for the given *name*, verbatim."""
    return f"Hello, {name}!"
