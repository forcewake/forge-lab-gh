"""Billing prices (CU-09 seed)."""

PRICE_CENTS = {"espresso": 250, "latte": 380}


def price_cents(item: str) -> int:
    return PRICE_CENTS[item]
