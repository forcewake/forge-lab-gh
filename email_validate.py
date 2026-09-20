"""Email validation (CU-06 seed: rejects every dotted domain)."""


def is_valid_email(value: str) -> bool:
    if value.count("@") != 1:
        return False
    local, _, domain = value.partition("@")
    return bool(local) and domain.isalpha()
