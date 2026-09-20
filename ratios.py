"""Ratio helpers — CU-12 seed: documented behaviour, zero tests."""


def parse_ratio(text: str) -> tuple[float, float]:
    """Parse ``a:b`` into floats; ValueError for any other shape."""
    left, sep, right = text.partition(":")
    if not sep or not left or not right:
        raise ValueError(f"not a ratio: {text!r}")
    return float(left), float(right)


def ratio(text: str) -> float:
    """``a:b`` as a float; ZeroDivisionError propagates when b == 0."""
    a, b = parse_ratio(text)
    return a / b
