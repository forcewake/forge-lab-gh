"""Tests for the stringutil helpers — cohort CU-11."""

import unittest

from stringutil import is_palindrome, squeeze, truncate


class SqueezeTest(unittest.TestCase):
    """squeeze collapses whitespace runs and strips the ends."""

    def test_collapses_multi_space_run(self) -> None:
        self.assertEqual(squeeze("too   many    spaces"), "too many spaces")

    def test_strips_leading_and_trailing_spaces(self) -> None:
        self.assertEqual(squeeze("   padded  string   "), "padded string")


class IsPalindromeTest(unittest.TestCase):
    """is_palindrome compares exact characters, with no folding."""

    def test_palindrome_is_true(self) -> None:
        self.assertTrue(is_palindrome("racecar"))

    def test_non_palindrome_is_false(self) -> None:
        self.assertFalse(is_palindrome("Racecar"))


class TruncateTest(unittest.TestCase):
    """truncate keeps at most limit leading characters."""

    def test_cuts_at_limit(self) -> None:
        self.assertEqual(truncate("truncated", 4), "trun")

    def test_negative_limit_yields_empty(self) -> None:
        self.assertEqual(truncate("truncated", -1), "")


if __name__ == "__main__":
    unittest.main()
