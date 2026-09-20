"""Acceptance checks for the CU-01 greeting module.

Deviation note: the approved plan names only ``greeting.py``, but the repo
has no test suite, so ``pytest -q`` exits 5 ("no tests ran") and fails the
CI gate. These tests encode the predeclared acceptance cases so the gate
runs green; the module under test is unchanged.
"""

from greeting import greet


def test_greet_world() -> None:
    """greet('World') returns exactly ``Hello, World!``."""
    assert greet("World") == "Hello, World!"


def test_greet_forge() -> None:
    """greet('forge') returns exactly ``Hello, forge!``."""
    assert greet("forge") == "Hello, forge!"
