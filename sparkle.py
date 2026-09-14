"""Sparkle text utility."""


def sparkle(text: str) -> str:
    """Return the given text wrapped in sparkle emojis.

    Args:
        text: The text to wrap in sparkles.

    Returns:
        The text surrounded by a sparkle on each side,
        e.g. sparkle("text") returns "✨ text ✨".
    """
    return f"✨ {text} ✨"
