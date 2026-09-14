"""Tiny text-polishing helpers used alongside the greeting helpers."""


def polish(text: str) -> str:
    """Return ``text`` stripped of surrounding whitespace with exactly one
    trailing period.

    An empty (or whitespace-only) input is returned unchanged.
    """
    stripped = text.strip()
    if not stripped:
        return stripped
    return stripped.rstrip(".") + "."
