from shine import polish


def test_polish_strips_whitespace():
    assert polish("  hello  ") == "hello."


def test_polish_normalizes_trailing_periods():
    assert polish("hello") == "hello."
    assert polish("hello.") == "hello."
    assert polish("hello...") == "hello."


def test_polish_empty_input():
    assert polish("") == ""
    assert polish("   ") == ""
