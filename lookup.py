"""Word-list helpers (CU-08 seed)."""

_WORDS: list[str] = []


def _load(path: str) -> list[str]:
    if not _WORDS:
        with open(path, encoding="utf-8") as handle:
            _WORDS.extend(handle.read().split())
    return _WORDS


def lookup(path: str, word: str) -> bool:
    return word in _load(path)


def count_prefix(path: str, prefix: str) -> int:
    """Count the words in ``path`` that start with ``prefix`` (case-sensitive)."""
    with open(path, encoding="utf-8") as handle:
        words = handle.read().split()
    return sum(1 for word in words if word.startswith(prefix))
