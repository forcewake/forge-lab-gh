"""Tests for the greeting module."""

import greeting


def test_polite_shout_returns_uppercased_greet_with_exclamation():
    for name in ("ada", "grace", "linus"):
        assert greeting.polite_shout(name) == (
            (greeting.greet(name) or "").upper() + "!"
        )


def test_polite_shout_ends_with_single_exclamation():
    result = greeting.polite_shout("ada")
    assert result.endswith("!")
    assert not result.endswith("!!")


def test_module_has_docstring_header():
    assert isinstance(greeting.__doc__, str)
    assert greeting.__doc__.strip() != ""
