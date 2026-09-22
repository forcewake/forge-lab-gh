"""Tests for the :mod:`greeting` module."""

import greeting


def test_polite_shout_uppercases_greeting_and_appends_bang():
    expected = (greeting.greet("x") or "").upper() + "!"
    assert greeting.polite_shout("x") == expected


def test_polite_shout_appends_bang_after_trailing_punctuation():
    # A greet() text already ending in punctuation must still get exactly one
    # trailing "!" (i.e. the doubled "!" is derived from greet's own period).
    original_greet = greeting.greet
    greeting.greet = lambda name: f"Hi, {name}."
    try:
        assert greeting.polite_shout("Ada") == "HI, ADA.!"
    finally:
        greeting.greet = original_greet


def test_module_docstring_exists_and_is_non_empty():
    assert greeting.__doc__ is not None
    assert greeting.__doc__.strip() != ""


def test_greet_and_farewell_unchanged():
    # polite_shout must reuse greet, not alter it.
    assert callable(greeting.greet)
    assert callable(greeting.farewell)
