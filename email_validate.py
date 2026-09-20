"""Email validation: dotted domains are valid, malformed ones are not."""

import re

# Dot-separated labels, each alphanumeric with optional inner hyphens, and at
# least two labels so a non-empty TLD is required.
_DOMAIN_RE = re.compile(
    r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)+\Z"
)


def is_valid_email(value: str) -> bool:
    if value.count("@") != 1:
        return False
    local, _, domain = value.partition("@")
    return bool(local) and _DOMAIN_RE.match(domain) is not None
