"""Compliment module.

Provides a small helper that returns a short praise line mentioning a
given topic, using only the standard library.
"""


def compliment(topic: str) -> str:
    """Return a short praise line mentioning the given topic.

    Args:
        topic: The subject to praise.

    Returns:
        A short compliment string that includes the topic.
    """
    return f"{topic} is absolutely wonderful — you did a great job with it!"
