"""CU-06 seed: the failing contract test. Fix the CODE, never this file."""

import unittest

from email_validate import is_valid_email


class EmailTest(unittest.TestCase):
    def test_plain_address_is_valid(self):
        self.assertTrue(is_valid_email("user@example.com"))

    def test_subdomain_is_valid(self):
        self.assertTrue(is_valid_email("user@mail.example.org"))

    def test_missing_at_is_invalid(self):
        self.assertFalse(is_valid_email("user-at-example.org"))

    def test_double_at_is_invalid(self):
        self.assertFalse(is_valid_email("a@@b.com"))


if __name__ == "__main__":
    unittest.main()
