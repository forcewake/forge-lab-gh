"""Tests for the :mod:`greeting` additions: ``polite_shout`` and the module docstring."""

import greeting


def test_polite_shout_uppercases_greet_text_and_appends_bang() -> None:
    # greet() currently returns None (docstring-only seed stub); polite_shout
    # normalizes that to "" rather than modifying greet().
    assert greeting.polite_shout("x") == (greeting.greet("x") or "").upper() + "!"


def test_polite_shout_appends_exactly_one_trailing_bang(monkeypatch) -> None:
    # The plan's "!!" risk, pinned precisely: the "!" is always appended, so
    # greet() text already ending in punctuation keeps it before the bang.
    monkeypatch.setattr(greeting, "greet", lambda name: f"Hello, {name}!")
    assert greeting.polite_shout("Ada") == "HELLO, ADA!!"

    monkeypatch.setattr(greeting, "greet", lambda name: f"Hello, {name}")
    assert greeting.polite_shout("Ada") == "HELLO, ADA!"


def test_module_docstring_header_is_present_and_effective() -> None:
    # A module docstring only becomes __doc__ when it is the first statement.
    assert isinstance(greeting.__doc__, str)
    assert greeting.__doc__.strip() != ""


def test_existing_functions_are_unchanged() -> None:
    # greet()/farewell() keep their seed behavior: callable, documented,
    # and returning None — polite_shout must not have altered them.
    assert greeting.greet("x") is None
    assert greeting.farewell("x") is None
    assert greeting.greet.__doc__ == "Return a friendly greeting for *name*."
    assert greeting.farewell.__doc__ == "Return a goodbye message for *name*."
