# Independent oracle for the forge 1.0 controlled CI-repair qualification (synthetic).
from mathops import double


def test_double_three():
    assert double(3) == 6


def test_double_zero():
    assert double(0) == 0
