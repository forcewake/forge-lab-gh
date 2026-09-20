"""CU-05 seed: the failing contract test. Fix the CODE, never this file."""

import unittest

from temperature import celsius_to_fahrenheit


class TemperatureTest(unittest.TestCase):
    def test_freezing(self):
        self.assertAlmostEqual(celsius_to_fahrenheit(0), 32)

    def test_boiling(self):
        self.assertAlmostEqual(celsius_to_fahrenheit(100), 212)

    def test_body_temperature(self):
        self.assertAlmostEqual(celsius_to_fahrenheit(37), 98.6)


if __name__ == "__main__":
    unittest.main()
