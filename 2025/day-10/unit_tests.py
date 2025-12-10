"""
Unit tests for Day 10: Factory solution.
"""

import os
import unittest
from textwrap import dedent

from solution import (
    parse_machine,
    min_presses_for_machine,
    min_presses_part2,
    part1,
    part2,
)


class TestSolution(unittest.TestCase):
    """Test cases for Day 10 solution."""

    def setUp(self):
        """Set up test fixtures."""
        self.maxDiff = None
        self.test_file = "test_input.txt"

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_parse_machine_line1(self):
        """Test parsing first example machine."""
        line = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
        target, buttons = parse_machine(line)
        self.assertEqual(target, [False, True, True, False])
        self.assertEqual(len(buttons), 6)
        self.assertEqual(buttons[0], {3})
        self.assertEqual(buttons[1], {1, 3})
        self.assertEqual(buttons[2], {2})
        self.assertEqual(buttons[3], {2, 3})
        self.assertEqual(buttons[4], {0, 2})
        self.assertEqual(buttons[5], {0, 1})

    def test_parse_machine_line2(self):
        """Test parsing second example machine."""
        line = "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}"
        target, buttons = parse_machine(line)
        self.assertEqual(target, [False, False, False, True, False])
        self.assertEqual(len(buttons), 5)
        self.assertEqual(buttons[0], {0, 2, 3, 4})

    def test_parse_machine_line3(self):
        """Test parsing third example machine."""
        line = "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"
        target, buttons = parse_machine(line)
        self.assertEqual(target, [False, True, True, True, False, True])
        self.assertEqual(len(buttons), 4)

    def test_min_presses_machine1(self):
        """Test minimum presses for first machine (should be 2)."""
        line = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
        target, buttons = parse_machine(line)
        result = min_presses_for_machine(target, buttons)
        self.assertEqual(result, 2, "First machine needs exactly 2 presses")

    def test_min_presses_machine2(self):
        """Test minimum presses for second machine (should be 3)."""
        line = "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}"
        target, buttons = parse_machine(line)
        result = min_presses_for_machine(target, buttons)
        self.assertEqual(result, 3, "Second machine needs exactly 3 presses")

    def test_min_presses_machine3(self):
        """Test minimum presses for third machine (should be 2)."""
        line = "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"
        target, buttons = parse_machine(line)
        result = min_presses_for_machine(target, buttons)
        self.assertEqual(result, 2, "Third machine needs exactly 2 presses")

    def test_part1_example(self):
        """Test Part 1 with all example machines (total should be 7)."""
        with open(self.test_file, "w") as f:
            f.write(
                dedent(
                    """\
                    [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
                    [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
                    [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
                    """
                )
            )
        result = part1(self.test_file)
        self.assertEqual(result, 7, "Total presses for all machines should be 7")

    def test_toggle_logic(self):
        """Test that toggling works correctly."""
        # Machine with all lights on target, press button that toggles all
        line = "[##] (0,1) {1}"
        target, buttons = parse_machine(line)
        # One button toggles both lights 0 and 1, target is both on
        # Pressing it once: off,off -> on,on = matches target
        result = min_presses_for_machine(target, buttons)
        self.assertEqual(result, 1)

    def test_already_correct(self):
        """Test machine that's already in correct state."""
        # Target is all off (.), lights start off, so 0 presses needed
        line = "[..] (0) (1) {1}"
        target, buttons = parse_machine(line)
        result = min_presses_for_machine(target, buttons)
        self.assertEqual(result, 0)

    # Part 2 tests
    def test_part2_machine1(self):
        """Test Part 2 minimum presses for first machine (should be 10)."""
        line = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
        _, buttons, joltage = parse_machine(line, include_joltage=True)
        result = min_presses_part2(buttons, joltage)
        self.assertEqual(result, 10, "First machine joltage needs 10 presses")

    def test_part2_machine2(self):
        """Test Part 2 minimum presses for second machine (should be 12)."""
        line = "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}"
        _, buttons, joltage = parse_machine(line, include_joltage=True)
        result = min_presses_part2(buttons, joltage)
        self.assertEqual(result, 12, "Second machine joltage needs 12 presses")

    def test_part2_machine3(self):
        """Test Part 2 minimum presses for third machine (should be 11)."""
        line = "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"
        _, buttons, joltage = parse_machine(line, include_joltage=True)
        result = min_presses_part2(buttons, joltage)
        self.assertEqual(result, 11, "Third machine joltage needs 11 presses")

    def test_part2_example(self):
        """Test Part 2 with all example machines (total should be 33)."""
        with open(self.test_file, "w") as f:
            f.write(
                dedent(
                    """\
                    [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
                    [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
                    [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
                    """
                )
            )
        result = part2(self.test_file)
        self.assertEqual(result, 33, "Total joltage presses should be 33")


def run_tests():
    """Run all tests and return success status."""
    print("Running unit tests...")
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestSolution)
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()
