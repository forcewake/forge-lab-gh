"""Tests for services.billing.price (CU-09)."""

import os
import sys

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
)

from services.billing.price import discount_cents


def test_discount_is_floor_of_ten_percent():
    assert discount_cents(380) == 38


def test_discount_of_zero_is_zero():
    assert discount_cents(0) == 0


def test_discount_below_ten_cents_floors_to_zero():
    assert discount_cents(1) == 0
