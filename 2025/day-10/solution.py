"""
Advent of Code 2025 - Day 10: Factory

Part 1: XOR toggling (binary) - brute force 2^n subsets
Part 2: Addition (counters) - mixed integer linear programming (MILP)

Key Insight Part 1: Pressing button twice cancels out, so each button 0 or 1 times.
Key Insight Part 2: Button presses must be integers - use MILP not LP relaxation.
"""

import re
import sys
from pathlib import Path
from typing import List, Set, Tuple, Union

import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint

sys.path.append(str(Path(__file__).parent.parent))


def parse_machine(
    line: str, include_joltage: bool = False
) -> Union[Tuple[List[bool], List[Set[int]]], Tuple[List[bool], List[Set[int]], List[int]]]:
    """Parse a machine line into target state, buttons, and optionally joltage."""
    # Extract indicator light diagram [...]
    indicator_match = re.search(r"\[([.#]+)\]", line)
    indicator = indicator_match.group(1)
    target = [c == "#" for c in indicator]

    # Extract button wiring schematics (...)
    button_matches = re.findall(r"\(([0-9,]+)\)", line)
    buttons = []
    for match in button_matches:
        indices = {int(x) for x in match.split(",")}
        buttons.append(indices)

    if include_joltage:
        # Extract joltage requirements {...}
        joltage_match = re.search(r"\{([0-9,]+)\}", line)
        joltage = [int(x) for x in joltage_match.group(1).split(",")]
        return target, buttons, joltage

    return target, buttons


def parse_input(input_file: str) -> List[str]:
    """Parse input file into list of machine lines."""
    with open(input_file) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


def min_presses_for_machine(target: List[bool], buttons: List[Set[int]]) -> int:
    """Find minimum button presses to achieve target state (Part 1 - XOR)."""
    n_lights = len(target)
    n_buttons = len(buttons)

    # If target is all off, 0 presses needed
    if not any(target):
        return 0

    min_presses = float("inf")

    # Try all 2^n_buttons combinations
    for mask in range(1 << n_buttons):
        state = [False] * n_lights
        presses = 0

        for i in range(n_buttons):
            if mask & (1 << i):
                presses += 1
                for light_idx in buttons[i]:
                    if light_idx < n_lights:
                        state[light_idx] = not state[light_idx]

        if state == target:
            min_presses = min(min_presses, presses)

    return min_presses if min_presses != float("inf") else -1


def min_presses_part2(buttons: List[Set[int]], targets: List[int]) -> int:
    """Find minimum button presses for joltage counters (Part 2 - addition)."""
    n_buttons = len(buttons)
    n_counters = len(targets)

    # If all targets are 0, no presses needed
    if all(t == 0 for t in targets):
        return 0

    # Build constraint matrix A where A[j][i] = 1 if button i affects counter j
    A_eq = np.zeros((n_counters, n_buttons))
    for i, btn in enumerate(buttons):
        for j in btn:
            if j < n_counters:
                A_eq[j][i] = 1

    # Objective: minimize sum of x_i (all coefficients = 1)
    c = np.ones(n_buttons)

    # Constraints: Ax = targets (equality)
    b_eq = np.array(targets, dtype=float)
    constraints = LinearConstraint(A_eq, b_eq, b_eq)

    # Bounds: x_i >= 0, no upper bound
    bounds = Bounds(lb=0, ub=np.inf)

    # All variables must be integers
    integrality = np.ones(n_buttons)  # 1 = integer variable

    result = milp(c, constraints=constraints, bounds=bounds, integrality=integrality)

    if result.success:
        return int(round(sum(result.x)))
    else:
        return -1


def part1(input_file: str) -> int:
    """Find total minimum button presses for all machines (indicator lights)."""
    lines = parse_input(input_file)
    total = 0

    for line in lines:
        target, buttons = parse_machine(line)
        presses = min_presses_for_machine(target, buttons)
        total += presses

    return total


def part2(input_file: str) -> int:
    """Find total minimum button presses for all machines (joltage counters)."""
    lines = parse_input(input_file)
    total = 0

    for line in lines:
        _, buttons, joltage = parse_machine(line, include_joltage=True)
        presses = min_presses_part2(buttons, joltage)
        total += presses

    return total


def main():
    """Main execution function."""
    from unit_tests import run_tests

    if run_tests():
        print("\nAll tests passed! Running actual solution...\n")
        result1 = part1("input.txt")
        result2 = part2("input.txt")
        print(f"Part 1: {result1}")
        print(f"Part 2: {result2}")
    else:
        print("\nTests failed! Please fix the issues before running the actual solution.")


if __name__ == "__main__":
    main()
