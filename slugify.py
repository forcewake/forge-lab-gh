"""Slugify."""


def slugify(text: str) -> str:
    return text.strip().lower().replace(" ", "-").replace("_", "-")
