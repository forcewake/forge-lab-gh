"""Tests for the :mod:`greeting` additions: the module docstring header and ``polite_shout``."""

import pytest

import greeting


def test_polite_shout_returns_greet_text_uppercased_with_trailing_bang() -> None:
    # greet() is a docstring-only seed stub returning None, so its result is
    # normalized to "" the same way polite_shout normalizes it.
    for name in ("x", "Ada", "grace hopper"):
        assert greeting.polite_shout(name) == (greeting.greet(name) or "").upper() + "!"


def test_polite_shout_appends_exactly_one_trailing_bang(monkeypatch: pytest.MonkeyPatch) -> None:
    # Pins the plan's double-punctuation risk: the "!" is appended after whatever
    # greet() produced, never substituted for it.
    monkeypatch.setattr(greeting, "greet", lambda name: f"Hello, {name}!")
    assert greeting.polite_shout("Ada") == "HELLO, ADA!!"

    monkeypatch.setattr(greeting, "greet", lambda name: f"Hello, {name}")
    assert greeting.polite_shout("Ada") == "HELLO, ADA!"


def test_module_docstring_header_is_present() -> None:
    # Only a docstring placed as the module's first statement becomes __doc__.
    assert isinstance(greeting.__doc__, str)
    assert greeting.__doc__.strip() != ""


def test_existing_functions_are_unchanged() -> None:
    # polite_shout must not have altered the existing greet()/farewell() seed code.
    assert greeting.greet("x") is None
    assert greeting.farewell("x") is None
    assert greeting.greet.__doc__ == "Return a friendly greeting for *name*."
    assert greeting.farewell.__doc__ == "Return a goodbye message for *name*."
