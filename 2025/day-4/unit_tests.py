"""
Advent of Code 2025 - Day 4: Printing Department
Unit Tests
"""

import os
import unittest

from solution import (
    count_accessible_rolls,
    part1,
    part2,
    remove_accessible_rolls_iteratively,
)


class TestDay4(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.test_input = "test_input.txt"
        # Create test input file with example from problem
        with open(self.test_input, "w") as f:
            f.write(
                """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""
            )

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_input):
            os.remove(self.test_input)

    def test_example_part1(self):
        """Test Part 1 with example input - should find 13 accessible rolls."""
        result = part1(self.test_input)
        self.assertEqual(result, 13, "Example should have 13 accessible rolls")

    def test_count_accessible(self):
        """Test the count_accessible_rolls function directly."""
        grid = [
            "..@@.@@@@.",
            "@@@.@.@.@@",
            "@@@@@.@.@@",
            "@.@@@@..@.",
            "@@.@@@@.@@",
            ".@@@@@@@.@",
            ".@.@.@.@@@",
            "@.@@@.@@@@",
            ".@@@@@@@@.",
            "@.@.@@@.@.",
        ]
        result = count_accessible_rolls(grid)
        self.assertEqual(result, 13)

    def test_example_part2(self):
        """Test Part 2 with example input - should remove 43 total rolls."""
        result = part2(self.test_input)
        self.assertEqual(result, 43, "Example should remove 43 rolls total")

    def test_remove_iteratively(self):
        """Test the remove_accessible_rolls_iteratively function directly."""
        grid = [
            "..@@.@@@@.",
            "@@@.@.@.@@",
            "@@@@@.@.@@",
            "@.@@@@..@.",
            "@@.@@@@.@@",
            ".@@@@@@@.@",
            ".@.@.@.@@@",
            "@.@@@.@@@@",
            ".@@@@@@@@.",
            "@.@.@@@.@.",
        ]
        result = remove_accessible_rolls_iteratively(grid)
        self.assertEqual(result, 43)


def run_tests():
    """Run all tests and return True if all pass."""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDay4)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()
