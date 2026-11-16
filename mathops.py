def double(x: int) -> int:
    # Deliberately wrong implementation for the controlled CI-repair qualification.
    # double(3) yields 7 and double(0) yields 1, so the independent oracle
    # tests/test_double_oracle.py fails in CI as intended.
    return x + x + 1
