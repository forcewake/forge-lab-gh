"""Shipping rates (CU-09 seed: OUT OF SCOPE — must stay byte-identical)."""

FLAT_CENTS = 500


def shipping_cents(subtotal_cents: int) -> int:
    return FLAT_CENTS if subtotal_cents else 0
