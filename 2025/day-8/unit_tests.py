"""Unit tests for Day 8: Playground."""

import os
import unittest
from textwrap import dedent


class TestDay8(unittest.TestCase):
    """Test cases for Day 8 solution."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_file = "test_input.txt"

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_example_part1(self):
        """Test example from problem description."""
        with open(self.test_file, "w") as f:
            f.write(
                dedent(
                    """\
                    162,817,812
                    57,618,57
                    906,360,560
                    592,479,940
                    352,342,300
                    466,668,158
                    542,29,236
                    431,825,988
                    739,650,466
                    52,470,668
                    216,146,977
                    819,987,18
                    117,168,530
                    805,96,715
                    346,949,466
                    970,615,88
                    941,993,340
                    862,61,35
                    984,92,344
                    425,690,689
                    """
                )
            )

        from solution import part1

        # After 10 shortest connections, multiply sizes of 3 largest circuits (5, 4, 2)
        result = part1(self.test_file, num_connections=10)
        self.assertEqual(
            result,
            40,
            "Should get 40 from multiplying 5 * 4 * 2 (three largest circuits)",
        )

    def test_example_part2(self):
        """Test Part 2 example from problem description."""
        with open(self.test_file, "w") as f:
            f.write(
                dedent(
                    """\
                    162,817,812
                    57,618,57
                    906,360,560
                    592,479,940
                    352,342,300
                    466,668,158
                    542,29,236
                    431,825,988
                    739,650,466
                    52,470,668
                    216,146,977
                    819,987,18
                    117,168,530
                    805,96,715
                    346,949,466
                    970,615,88
                    941,993,340
                    862,61,35
                    984,92,344
                    425,690,689
                    """
                )
            )

        from solution import part2

        # Last connection to unify all: 216,146,977 and 117,168,530
        # Product of X coordinates: 216 * 117 = 25272
        result = part2(self.test_file)
        self.assertEqual(result, 25272, "Should get 25272 from multiplying X coords 216 * 117")


def run_tests():
    """Run all tests and return success status."""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDay8)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    unittest.main()
