"""Synthetic math operations for the forge 1.0 controlled CI-repair qualification."""


def double(x: int) -> int:
    """Return twice *x*.

    Repaired implementation for the controlled CI-repair qualification:
    the first candidate returned ``x + x + 1`` and failed the independent
    oracle ``tests/test_double_oracle.py`` in the forge ``unit`` job; this
    repair returns ``x + x`` so the oracle passes.
    """
    return x + x
