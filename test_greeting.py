"""Tests for the greeting module."""

import greeting
from greeting import greet, polite_shout


def test_module_docstring_is_present():
    """greeting.py must carry a non-empty module-level docstring."""
    assert isinstance(greeting.__doc__, str)
    assert greeting.__doc__.strip()


def test_polite_shout_uppercases_and_appends_exclamation():
    assert polite_shout("ada") == "HELLO, ADA!"
    assert polite_shout("Grace Hopper") == "HELLO, GRACE HOPPER!"


def test_polite_shout_always_ends_with_exclamation():
    assert polite_shout("x").endswith("!")


def test_polite_shout_builds_on_greet(monkeypatch):
    """polite_shout uppercases whatever greet() returns and appends '!'."""
    monkeypatch.setattr(greeting, "greet", lambda name: f"hi, {name}")
    assert polite_shout("world") == "HI, WORLD!"


def test_existing_functions_unchanged():
    """Pin the pre-existing stub behaviour the plan requires to stay as-is."""
    assert greet("world") is None
    assert greeting.farewell("world") is None
