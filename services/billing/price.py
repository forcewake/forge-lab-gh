"""Billing prices (CU-09 seed)."""

PRICE_CENTS = {"espresso": 250, "latte": 380}


def price_cents(item: str) -> int:
    return PRICE_CENTS[item]


def discount_cents(subtotal_cents: int) -> int:
    """Return the integer floor of 10% of the subtotal."""
    return subtotal_cents // 10
