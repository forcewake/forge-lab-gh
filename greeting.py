"""CU-01 greeting module."""

__all__ = ["greet"]


def greet(name: str) -> str:
    """Return a greeting for ``name`` interpolated verbatim."""
    return f"Hello, {name}!"
