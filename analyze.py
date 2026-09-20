"""Events-log analytics (CU-07 seed)."""


def count_errors(path: str) -> int:
    """Count lines prefixed with ``ERROR`` across the whole log file."""
    total = 0
    with open(path, encoding="utf-8") as handle:
        for line in handle:
            if line.startswith("ERROR"):
                total += 1
    return total
