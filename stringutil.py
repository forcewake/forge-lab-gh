"""String helpers — CU-11 seed: documented behaviour, zero tests."""


def squeeze(text: str) -> str:
    """Collapse every whitespace run into one space; strip both ends."""
    return " ".join(text.split())


def is_palindrome(text: str) -> bool:
    """True when *text* equals its reversal (exact characters, no folding)."""
    return text == text[::-1]


def truncate(text: str, limit: int) -> str:
    """At most *limit* leading characters; a negative limit yields ''."""
    return text[:limit] if limit >= 0 else ""
