"""
Unit tests for Day 11 solution.
"""

import os
import unittest
from textwrap import dedent

from solution import find_all_paths, parse_input, part1, part2


class TestSolution(unittest.TestCase):
    """Test cases for Day 11 solution."""

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
                dedent(
                    """\
                    aaa: you hhh
                    you: bbb ccc
                    bbb: ddd eee
                    """
                )
            )

        result = parse_input(self.test_file)
        self.assertEqual(result["aaa"], ["you", "hhh"])
        self.assertEqual(result["you"], ["bbb", "ccc"])
        self.assertEqual(result["bbb"], ["ddd", "eee"])

    def test_part1_example(self):
        """Test Part 1 with example input from problem."""
        with open(self.test_file, "w") as f:
            f.write(
                dedent(
                    """\
                    aaa: you hhh
                    you: bbb ccc
                    bbb: ddd eee
                    ccc: ddd eee fff
                    ddd: ggg
                    eee: out
                    fff: out
                    ggg: out
                    hhh: ccc fff iii
                    iii: out
                    """
                )
            )

        result = part1(self.test_file)
        self.assertEqual(result, 5, "Example should have 5 paths from 'you' to 'out'")

    def test_find_all_paths(self):
        """Test the path finding function directly."""
        # Build simple graph
        graph = {"you": ["bbb", "ccc"], "bbb": ["out"], "ccc": ["out"]}

        paths = find_all_paths(graph, "you", "out")
        self.assertEqual(len(paths), 2, "Should find 2 paths: you->bbb->out and you->ccc->out")

    def test_find_all_paths_with_cycle_avoidance(self):
        """Test that cycles are properly avoided."""
        # Graph with potential cycle
        graph = {"you": ["a", "b"], "a": ["out"], "b": ["c"], "c": ["you", "out"]}

        paths = find_all_paths(graph, "you", "out")
        # Should find: you->a->out and you->b->c->out (but not cycle back through you)
        self.assertEqual(len(paths), 2)

    def test_part2_example(self):
        """Test Part 2 with example input from problem."""
        with open(self.test_file, "w") as f:
            f.write(
                dedent(
                    """\
                    svr: aaa bbb
                    aaa: fft
                    fft: ccc
                    bbb: tty
                    tty: ccc
                    ccc: ddd eee
                    ddd: hub
                    hub: fff
                    eee: dac
                    dac: fff
                    fff: ggg hhh
                    ggg: out
                    hhh: out
                    """
                )
            )

        result = part2(self.test_file)
        self.assertEqual(result, 2, "Example should have 2 paths that visit both dac and fft")


def run_tests():
    """Run all tests and return success status."""
    print("Running unit tests...")
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestSolution)
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()
