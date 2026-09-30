"""Tests for the greeting module."""

from greeting import farewell, formal_farewell, greet


def test_formal_farewell() -> None:
    """formal_farewell reuses farewell() and returns the exact formal wording."""
    assert formal_farewell("X") == "We bid you farewell, X."
    assert formal_farewell("Ada Lovelace") == "We bid you farewell, Ada Lovelace."


def test_existing_functions_unchanged() -> None:
    """The pre-existing helpers keep their original (stub) behavior."""
    assert greet("X") is None
    assert farewell("X") is None
