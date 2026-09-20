"""CU-04 seed HTTP client stub."""

from settings import DEFAULT_TIMEOUT_S


def attempt(endpoint: str) -> str:
    return f"GET {endpoint} timeout={DEFAULT_TIMEOUT_S}"
