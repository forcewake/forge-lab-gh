"""Events-log analytics (CU-07 seed: reads only the first 100 lines)."""


def count_errors(path: str) -> int:
    with open(path, encoding="utf-8") as handle:
        head = handle.readlines()[:100]
    return sum(1 for line in head if line.startswith("ERROR"))
