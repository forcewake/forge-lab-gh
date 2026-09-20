"""Render name/value pairs as CSV text."""

import csv
import io
from typing import Iterable, Tuple, Any

_HEADER = ["name", "value"]


def export_rows(rows: Iterable[Tuple[Any, Any]]) -> str:
    """Render ``rows`` as CSV with a ``name,value`` header and LF line endings.

    Args:
        rows: Iterable of ``(name, value)`` pairs; values are stringified by
            the :mod:`csv` writer.

    Returns:
        The CSV document as a string using ``\\n`` terminators.
    """
    # newline='' avoids platform-dependent newline translation (csv docs);
    # lineterminator='\n' overrides csv's default CRLF.
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(_HEADER)
    for row in rows:
        writer.writerow(row)
    return buffer.getvalue()
