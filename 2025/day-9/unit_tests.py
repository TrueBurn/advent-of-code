"""Unit tests for Day 9: Movie Theater"""

import os
import unittest
from textwrap import dedent

from solution import parse_input, part1, part2


class TestDay9(unittest.TestCase):
    """Test cases for Day 9 solution."""

    def setUp(self):
        """Create test input file."""
        self.test_file = "test_input.txt"

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_parse_input(self):
        """Test parsing of coordinate input."""
        with open(self.test_file, "w") as f:
            f.write(
                dedent(
                    """\
                    7,1
                    11,1
                    2,3
                    """
                )
            )
        coords = parse_input(self.test_file)
        self.assertEqual(coords, [(7, 1), (11, 1), (2, 3)])

    def test_example_part1(self):
        """Test Part 1 with example from problem description."""
        with open(self.test_file, "w") as f:
            f.write(
                dedent(
                    """\
                    7,1
                    11,1
                    11,7
                    9,7
                    9,5
                    2,5
                    2,3
                    7,3
                    """
                )
            )
        result = part1(self.test_file)
        self.assertEqual(result, 50, "Largest rectangle should have area 50")

    def test_single_pair(self):
        """Test with just two tiles."""
        with open(self.test_file, "w") as f:
            f.write(
                dedent(
                    """\
                    0,0
                    2,3
                    """
                )
            )
        result = part1(self.test_file)
        # (2-0+1) * (3-0+1) = 3 * 4 = 12
        self.assertEqual(result, 12)

    def test_same_row(self):
        """Test tiles in same row."""
        with open(self.test_file, "w") as f:
            f.write(
                dedent(
                    """\
                    5,10
                    15,10
                    """
                )
            )
        result = part1(self.test_file)
        # (15-5+1) * (10-10+1) = 11 * 1 = 11
        self.assertEqual(result, 11)

    def test_same_column(self):
        """Test tiles in same column."""
        with open(self.test_file, "w") as f:
            f.write(
                dedent(
                    """\
                    5,10
                    5,20
                    """
                )
            )
        result = part1(self.test_file)
        # (5-5+1) * (20-10+1) = 1 * 11 = 11
        self.assertEqual(result, 11)

    def test_example_part2(self):
        """Test Part 2 with example from problem description."""
        with open(self.test_file, "w") as f:
            f.write(
                dedent(
                    """\
                    7,1
                    11,1
                    11,7
                    9,7
                    9,5
                    2,5
                    2,3
                    7,3
                    """
                )
            )
        result = part2(self.test_file)
        self.assertEqual(result, 24, "Largest valid rectangle should have area 24")


def run_tests():
    """Run all tests and return True if all pass."""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDay9)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()
