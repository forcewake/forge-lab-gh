"""CU-04 seed HTTP client stub."""

from settings import DEFAULT_TIMEOUT_S, MAX_RETRIES


def attempt(endpoint: str) -> str:
    return f"GET {endpoint} timeout={DEFAULT_TIMEOUT_S} retries={MAX_RETRIES}"
