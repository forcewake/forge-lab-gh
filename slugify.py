"""Slugify (CU-03 seed: underscores pass through)."""


def slugify(text: str) -> str:
    return text.strip().lower().replace(" ", "-")
