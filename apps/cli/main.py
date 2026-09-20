"""CU-10 seed CLI banner (must route through the shared helper)."""

from packages.shared.strings import shout


def banner(name: str) -> str:
    return f"== {shout(name)} =="
