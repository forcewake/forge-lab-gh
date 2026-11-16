# Independent oracle for the forge 1.0 controlled CI-repair qualification (synthetic).
# Skipped until a candidate adds mathops.py, so unrelated candidates are not blocked.
import pytest

mathops = pytest.importorskip("mathops")


def test_double_three():
    assert mathops.double(3) == 6


def test_double_zero():
    assert mathops.double(0) == 0
