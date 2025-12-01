"""
Day 1: Secret Entrance

Part 1: Count final positions at 0 after each rotation
Part 2: Count every time we pass through 0 during rotations

The trick for part 2 is handling large distances efficiently - instead of
simulating every single click, we calculate how many full cycles of 100 we
complete, then check if the remaining clicks cross 0.
"""

import sys
from functools import cache  # noqa: F401 - Template import
from pathlib import Path
from typing import List, Tuple

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))

# Utility imports - uncomment as needed
# from utils import Grid, Direction, CARDINAL_DIRS
# from utils import bfs, dfs, dijkstra, a_star
# from utils import parse_grid, parse_sections, parse_ints, parse_coords


def parse_input(input_file: str) -> List[Tuple[str, int]]:
    """Parse input into list of (direction, distance) tuples."""
    rotations = []
    with open(input_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            direction = line[0]
            distance = int(line[1:])
            rotations.append((direction, distance))
    return rotations


def part1(input_file: str) -> int:
    """Count how many times we end up at position 0 after a rotation."""
    rotations = parse_input(input_file)
    position = 50
    count = 0

    for direction, distance in rotations:
        if direction == "L":
            position = (position - distance) % 100
        else:
            position = (position + distance) % 100

        if position == 0:
            count += 1

    return count


def part2(input_file: str) -> int:
    """Count every time we pass through 0, including mid-rotation."""
    rotations = parse_input(input_file)
    position = 50
    count = 0

    for direction, distance in rotations:
        if direction == "L":
            # Each full cycle of 100 passes through 0 once
            full_cycles = distance // 100
            count += full_cycles

            # Check if the remaining distance crosses 0
            remaining = distance % 100
            if position > 0 and remaining >= position:
                count += 1

        else:  # Right
            full_cycles = distance // 100
            count += full_cycles

            remaining = distance % 100
            # Cross 0 when we wrap from 99 to 0
            if position > 0 and position + remaining >= 100:
                count += 1

        # Update position for next rotation
        if direction == "L":
            position = (position - distance) % 100
        else:
            position = (position + distance) % 100

    return count


def main():
    from unit_tests import run_tests

    if run_tests():
        print("\nAll tests passed! Running actual solution...\n")
        result1 = part1("input.txt")
        result2 = part2("input.txt")
        print(f"Part 1: {result1}")
        print(f"Part 2: {result2}")
    else:
        print("\nTests failed! Fix the issues first.")


if __name__ == "__main__":
    main()
