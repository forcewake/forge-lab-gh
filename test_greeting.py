"""Tests for the greeting module."""

import greeting


def test_polite_shout_returns_uppercased_greet_text(monkeypatch):
    """polite_shout returns greet()'s text uppercased and ending with '!'."""
    # greet() must stay unchanged per the issue, so the polite_shout()
    # contract is pinned against a stubbed greet() instead of the real one.
    calls = []

    def fake_greet(name: str) -> str:
        calls.append(name)
        return f"Hello, {name}"

    monkeypatch.setattr(greeting, "greet", fake_greet)

    assert greeting.polite_shout("world") == "HELLO, WORLD!"
    assert calls == ["world"]


def test_module_docstring_header():
    """greeting.py carries a non-empty module-level docstring header."""
    assert greeting.__doc__ is not None
    assert greeting.__doc__.strip()
