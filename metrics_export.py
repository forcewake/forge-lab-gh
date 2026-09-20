"""Render name/value pairs as CSV."""

from __future__ import annotations

import csv
import io
from typing import Iterable


def export_rows(rows: Iterable[tuple[str, object]]) -> str:
    """Return ``rows`` as CSV text with a ``name,value`` header and LF line endings."""
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(("name", "value"))
    writer.writerows(rows)
    return buffer.getvalue()
