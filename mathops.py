"""Synthetic math operations for the forge 1.0 controlled CI-repair qualification."""


def double(x: int) -> int:
    """Return twice *x* (intended contract).

    Deliberately wrong first candidate for the controlled CI-repair
    qualification: this returns ``x + x + 1`` so the independent oracle
    ``tests/test_double_oracle.py`` fails and supplies the CI test-failure
    evidence the later repair attempt requires. The repair is to return
    ``x + x``.
    """
    return x + x + 1
