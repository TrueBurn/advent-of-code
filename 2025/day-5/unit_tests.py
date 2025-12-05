"""
Unit tests for Day 5 solution.
"""

import os
import unittest

from solution import parse_input, part1, part2


class TestSolution(unittest.TestCase):
    """Test cases for Day 5 solution."""

    def setUp(self):
        """Set up test fixtures."""
        self.maxDiff = None
        self.test_file = "test_input.txt"

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_parse_input(self):
        """Test input parsing."""
        with open(self.test_file, "w") as f:
            f.write(
                """3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""
            )

        ranges, ids = parse_input(self.test_file)
        self.assertEqual(len(ranges), 4)
        self.assertEqual(ranges[0], (3, 5))
        self.assertEqual(ranges[1], (10, 14))
        self.assertEqual(len(ids), 6)
        self.assertEqual(ids, [1, 5, 8, 11, 17, 32])

    def test_part1_example(self):
        """Test Part 1 with example input."""
        with open(self.test_file, "w") as f:
            f.write(
                """3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""
            )

        result = part1(self.test_file)
        self.assertEqual(result, 3, "Should have 3 fresh ingredients (5, 11, 17)")

    def test_part2_example(self):
        """Test Part 2 with example input."""
        with open(self.test_file, "w") as f:
            f.write(
                """3-5
10-14
16-20
12-18

1
5
8
11
17
32
"""
            )

        result = part2(self.test_file)
        # Fresh IDs: 3,4,5,10,11,12,13,14,15,16,17,18,19,20 = 14 total
        self.assertEqual(result, 14, "Should have 14 total fresh IDs")


def run_tests():
    """Run all tests and return success status."""
    print("Running unit tests...")
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestSolution)
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()
