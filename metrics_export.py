def export_rows(rows: list[tuple[str, int]]) -> str:
    """Return CSV text: a header line ``name,value``, then one ``name,value``
    line per row in the given order, every line terminated by ``\\n``.
    """
    lines = ["name,value"]
    for name, value in rows:
        lines.append(f"{name},{value}")
    return "\n".join(lines) + "\n"
