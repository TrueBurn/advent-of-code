"""
Unit tests for Day 0 solution.
"""

import unittest

from solution import parse_input, part1, part2  # noqa: F401 - Template imports


class TestSolution(unittest.TestCase):
    """Test cases for Day 0 solution."""

    def setUp(self):
        """Set up test fixtures."""
        self.maxDiff = None

    def test_parse_input(self):
        """Test input parsing."""
        # Create test input file
        with open("test_input.txt", "w") as f:
            f.write("test line 1\ntest line 2\n")

        result = parse_input("test_input.txt")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], "test line 1")

        # Clean up
        import os

        os.remove("test_input.txt")

    def test_part1_example(self):
        """Test Part 1 with example input."""
        # Add your test cases here
        pass

    def test_part2_example(self):
        """Test Part 2 with example input."""
        # Add your test cases here
        pass


def run_tests():
    """Run all tests and return success status."""
    print("Running unit tests...")
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestSolution)
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()
