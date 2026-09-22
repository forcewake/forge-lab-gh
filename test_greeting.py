"""Tests for the :mod:`greeting` additions: ``polite_shout`` and the module docstring header."""

import greeting


def test_polite_shout_uppercases_greet_text_and_appends_bang() -> None:
    # greet() is a docstring-only seed stub returning None; polite_shout builds
    # on greet() without modifying it, so the expected text normalizes None.
    assert greeting.polite_shout("x") == (greeting.greet("x") or "").upper() + "!"


def test_polite_shout_appends_exactly_one_trailing_bang(monkeypatch) -> None:
    # Pins the plan's double-punctuation risk: the "!" is always appended after
    # whatever greet() produced, never substituted.
    monkeypatch.setattr(greeting, "greet", lambda name: f"Hello, {name}!")
    assert greeting.polite_shout("Ada") == "HELLO, ADA!!"

    monkeypatch.setattr(greeting, "greet", lambda name: f"Hello, {name}")
    assert greeting.polite_shout("Ada") == "HELLO, ADA!"


def test_module_docstring_header_is_present() -> None:
    # A docstring only becomes __doc__ when it is the module's first statement.
    assert isinstance(greeting.__doc__, str)
    assert greeting.__doc__.strip() != ""


def test_existing_functions_are_unchanged() -> None:
    # greet()/farewell() keep their exact seed behavior; polite_shout must not
    # have altered them.
    assert greeting.greet("x") is None
    assert greeting.farewell("x") is None
    assert greeting.greet.__doc__ == "Return a friendly greeting for *name*."
    assert greeting.farewell.__doc__ == "Return a goodbye message for *name*."
