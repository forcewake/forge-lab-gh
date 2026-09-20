"""Stdlib-only report of the running Python environment."""

import platform
import sys


def python_report() -> dict:
    """Return interpreter and OS details for the current environment.

    Both values are guaranteed non-empty strings: ``sys``-based fallbacks
    cover exotic setups where the ``platform`` helpers return empty results.
    """
    version_parts = sys.version.split()
    python = platform.python_version()
    if not python:
        python = version_parts[0] if version_parts else "unknown"
    system = platform.system() or sys.platform or "unknown"
    return {"python": python, "platform": system}
