"""Sparkle module.

Provides a simple utility to wrap text in sparkle emoji.
"""


def sparkle(text: str) -> str:
    """Return the given text wrapped in sparkle emoji on both sides.

    Args:
        text: The input text to wrap.

    Returns:
        The text surrounded by a sparkle emoji on each side.
    """
    return f"✨{text}✨"
