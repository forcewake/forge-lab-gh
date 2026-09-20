"""Tests for the ratio helpers in ratios.py — CU-12."""

import unittest

from ratios import parse_ratio, ratio


class RatioTests(unittest.TestCase):
    def test_parse_ratio_returns_parts_as_floats(self) -> None:
        self.assertEqual(parse_ratio("3:4"), (3.0, 4.0))

    def test_parse_ratio_rejects_missing_separator(self) -> None:
        with self.assertRaises(ValueError):
            parse_ratio("34")

    def test_parse_ratio_rejects_extra_separator(self) -> None:
        with self.assertRaises(ValueError):
            parse_ratio("1:2:3")

    def test_ratio_divides_left_by_right(self) -> None:
        self.assertAlmostEqual(ratio("1:2"), 0.5)

    def test_ratio_propagates_zero_division(self) -> None:
        with self.assertRaises(ZeroDivisionError):
            ratio("1:0")


if __name__ == "__main__":
    unittest.main()
