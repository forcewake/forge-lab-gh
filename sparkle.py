"""Tiny sparkle helper used by the CI smoke tests."""


def sparkle(text: str) -> str:
    """Return *text* wrapped in sparkle emoji on both sides."""
    return f"✨{text}✨"
