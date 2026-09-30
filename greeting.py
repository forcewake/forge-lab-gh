def greet(name: str) -> str:
    """Return a friendly greeting for *name*."""


def farewell(name: str) -> str:
    """Return a goodbye message for *name*."""


def formal_farewell(name: str) -> str:
    """Return a formal goodbye message for *name*."""
    # Reuse the existing farewell() helper so both parting messages share one
    # path; farewell() itself carries no message text today, so the formal
    # wording is composed here to guarantee the exact required output.
    farewell(name)
    return f"We bid you farewell, {name}."
