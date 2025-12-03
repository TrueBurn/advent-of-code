"""Unit tests for Day 3 solution."""

import os
import unittest

from solution import find_max_joltage, find_max_joltage_n_batteries, part1, part2


class TestDay3(unittest.TestCase):
    """Test cases for Day 3: Lobby."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_input = "test_input.txt"
        with open(self.test_input, "w") as f:
            f.write(
                """987654321111111
811111111111119
234234234234278
818181911112111
"""
            )

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_input):
            os.remove(self.test_input)

    def test_example_case(self):
        """Test the example from the problem description."""
        result = part1(self.test_input)
        self.assertEqual(result, 357, "Should sum to 357")

    def test_find_max_joltage_line1(self):
        """Test finding max joltage for first example line."""
        result = find_max_joltage("987654321111111")
        self.assertEqual(result, 98, "First line should produce 98")

    def test_find_max_joltage_line2(self):
        """Test finding max joltage for second example line."""
        result = find_max_joltage("811111111111119")
        self.assertEqual(result, 89, "Second line should produce 89")

    def test_find_max_joltage_line3(self):
        """Test finding max joltage for third example line."""
        result = find_max_joltage("234234234234278")
        self.assertEqual(result, 78, "Third line should produce 78")

    def test_find_max_joltage_line4(self):
        """Test finding max joltage for fourth example line."""
        result = find_max_joltage("818181911112111")
        self.assertEqual(result, 92, "Fourth line should produce 92")

    def test_simple_case(self):
        """Test a simple two-digit bank."""
        result = find_max_joltage("12")
        self.assertEqual(result, 12, "Two digit bank should return those digits")

    def test_reverse_order(self):
        """Test that we get max when digits are reversed."""
        result = find_max_joltage("21")
        self.assertEqual(result, 21, "Should be 21, not 12")

    def test_all_same_digit(self):
        """Test bank with all same digits."""
        result = find_max_joltage("5555")
        self.assertEqual(result, 55, "All 5s should produce 55")

    def test_part2_line1(self):
        """Test Part 2 with first example line."""
        result = find_max_joltage_n_batteries("987654321111111", 12)
        self.assertEqual(result, 987654321111, "First line should produce 987654321111")

    def test_part2_line2(self):
        """Test Part 2 with second example line."""
        result = find_max_joltage_n_batteries("811111111111119", 12)
        self.assertEqual(result, 811111111119, "Second line should produce 811111111119")

    def test_part2_line3(self):
        """Test Part 2 with third example line."""
        result = find_max_joltage_n_batteries("234234234234278", 12)
        self.assertEqual(result, 434234234278, "Third line should produce 434234234278")

    def test_part2_line4(self):
        """Test Part 2 with fourth example line."""
        result = find_max_joltage_n_batteries("818181911112111", 12)
        self.assertEqual(result, 888911112111, "Fourth line should produce 888911112111")

    def test_part2_example(self):
        """Test Part 2 with the full example."""
        result = part2(self.test_input)
        expected = 987654321111 + 811111111119 + 434234234278 + 888911112111
        self.assertEqual(result, expected, f"Part 2 should sum to {expected}")


def run_tests():
    """Run all tests and return True if all pass."""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDay3)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()
