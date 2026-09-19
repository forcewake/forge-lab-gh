"""Minimal stdlib-only greeting helpers."""


def greet(name: str) -> str:
    """Return ``Hello, <name>!`` for the given *name*, verbatim."""
    return f"Hello, {name}!"
