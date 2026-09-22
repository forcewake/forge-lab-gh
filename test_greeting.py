"""Tests for the greeting module docstring header and polite_shout()."""

import greeting


def test_module_docstring_is_non_empty():
    """greeting must carry a non-empty module-level docstring header."""
    assert isinstance(greeting.__doc__, str)
    assert greeting.__doc__.strip()


def test_polite_shout_is_greet_uppercased_with_bang():
    """polite_shout(name) equals greet(name).upper() + '!' (never doubled)."""
    # greet() is a docstring-only stub returning None today; coerce to "" the
    # same way polite_shout does so the composition contract stays testable
    # without modifying greet().
    for name in ("Ada", "grace hopper", ""):
        expected = (greeting.greet(name) or "").upper()
        if not expected.endswith("!"):
            expected += "!"
        assert greeting.polite_shout(name) == expected


def test_polite_shout_is_uppercase_with_single_bang():
    """Every result is fully uppercased and ends with exactly one '!'."""
    for name in ("Ada", "grace hopper", ""):
        shouted = greeting.polite_shout(name)
        assert shouted.endswith("!")
        assert not shouted.endswith("!!")
        assert shouted == shouted.upper()
