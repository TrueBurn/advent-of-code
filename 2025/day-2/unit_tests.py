"""
Unit tests for Day 2: Gift Shop
"""

import os
import sys
import unittest
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from solution import is_invalid_id, is_invalid_id_part2, parse_input, part1, part2  # noqa: E402


class TestDay2(unittest.TestCase):
    def setUp(self):
        """Create test input file"""
        self.test_file = "test_input.txt"
        with open(self.test_file, "w") as f:
            f.write(
                """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
"""
            )

    def tearDown(self):
        """Remove test file"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_is_invalid_id(self):
        """Test the invalid ID detection function"""
        # Valid invalid IDs (repeated sequences)
        self.assertTrue(is_invalid_id(11))  # "11" = "1" twice
        self.assertTrue(is_invalid_id(22))  # "22" = "2" twice
        self.assertTrue(is_invalid_id(55))  # "55" = "5" twice
        self.assertTrue(is_invalid_id(99))  # "99" = "9" twice
        self.assertTrue(is_invalid_id(6464))  # "6464" = "64" twice
        self.assertTrue(is_invalid_id(123123))  # "123123" = "123" twice
        self.assertTrue(is_invalid_id(1010))  # "1010" = "10" twice
        self.assertTrue(is_invalid_id(222222))  # "222222" = "222" twice
        self.assertTrue(is_invalid_id(446446))  # "446446" = "446" twice
        self.assertTrue(is_invalid_id(1188511885))  # "1188511885" = "11885" twice
        self.assertTrue(is_invalid_id(38593859))  # "38593859" = "3859" twice

        # Not invalid IDs
        self.assertFalse(is_invalid_id(101))  # Not a repeated sequence
        self.assertFalse(is_invalid_id(100))  # Not a repeated sequence
        self.assertFalse(is_invalid_id(1698522))  # Not a repeated sequence
        self.assertFalse(is_invalid_id(12))  # Different digits
        self.assertFalse(is_invalid_id(1234))  # Not repeated

    def test_example_part1(self):
        """Test Part 1 with the example input"""
        result = part1(self.test_file)
        self.assertEqual(result, 1227775554, "Example should sum to 1227775554")

    def test_parse_input(self):
        """Test input parsing"""
        ranges = parse_input(self.test_file)
        self.assertEqual(len(ranges), 11, "Should have 11 ranges")
        self.assertEqual(ranges[0], (11, 22), "First range should be (11, 22)")
        self.assertEqual(ranges[1], (95, 115), "Second range should be (95, 115)")

    def test_is_invalid_id_part2(self):
        """Test the invalid ID detection for Part 2 (at least twice)"""
        # Valid invalid IDs (repeated at least twice)
        self.assertTrue(is_invalid_id_part2(11))  # "11" = "1" twice
        self.assertTrue(is_invalid_id_part2(99))  # "99" = "9" twice
        self.assertTrue(is_invalid_id_part2(111))  # "111" = "1" three times
        self.assertTrue(is_invalid_id_part2(999))  # "999" = "9" three times
        self.assertTrue(is_invalid_id_part2(1010))  # "1010" = "10" twice
        self.assertTrue(is_invalid_id_part2(12341234))  # "1234" twice
        self.assertTrue(is_invalid_id_part2(123123123))  # "123" three times
        self.assertTrue(is_invalid_id_part2(1212121212))  # "12" five times
        self.assertTrue(is_invalid_id_part2(1111111))  # "1" seven times
        self.assertTrue(is_invalid_id_part2(565656))  # "56" three times
        self.assertTrue(is_invalid_id_part2(824824824))  # "824" three times
        self.assertTrue(is_invalid_id_part2(2121212121))  # "21" five times

        # Not invalid IDs
        self.assertFalse(is_invalid_id_part2(101))  # Not repeated
        self.assertFalse(is_invalid_id_part2(1698522))  # Not repeated
        self.assertFalse(is_invalid_id_part2(12))  # Different digits

    def test_example_part2(self):
        """Test Part 2 with the example input"""
        result = part2(self.test_file)
        self.assertEqual(result, 4174379265, "Example should sum to 4174379265")


def run_tests():
    """Run all tests and return success status"""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDay2)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()
