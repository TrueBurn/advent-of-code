"""
Advent of Code 2025 - Day 7: Laboratories

Part 1 - Classical Tachyon Manifold:
  Algorithm: BFS-style beam simulation
  Count how many splitters are activated (each splitter counts once)

Part 2 - Quantum Tachyon Manifold:
  Algorithm: Recursive path counting with memoization
  Count all possible quantum timelines (unique paths through the manifold)
  When a particle hits a splitter, it creates two timelines (left and right)

Time Complexity: O(rows * cols) for both parts
Space Complexity: O(rows * cols) for tracking states and memoization

Key Insights:
- Part 1: Each splitter can only split once, regardless of how many beams hit it
- Part 2: Quantum splitting means counting all possible paths; memoization is crucial
"""

import sys
from collections import deque
from pathlib import Path
from typing import List, Tuple

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))


def parse_input(input_file: str) -> List[str]:
    """Parse the input file into a grid."""
    grid = []
    with open(input_file) as f:
        for line in f:
            line = line.rstrip()  # Keep trailing spaces if any, remove newline
            if line:
                grid.append(line)
    return grid


def find_start(grid: List[str]) -> Tuple[int, int]:
    """Find the starting position 'S' in the grid."""
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == "S":
                return (row, col)
    raise ValueError("No starting position 'S' found in grid")


def simulate_beams(grid: List[str], debug=False) -> int:
    """
    Simulate tachyon beam splitting and count total splits.

    All beams move downward. When a beam hits a splitter:
    - The beam stops
    - Two new beams start from the left and right cells of the splitter
    - Both new beams continue moving downward
    - Each splitter only splits once (first beam to hit it)
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    start_row, start_col = find_start(grid)

    # Queue of beams: (row, col) - all beams move downward
    beams = deque([(start_row, start_col)])

    # Track visited positions to avoid processing same beam multiple times
    visited = set()

    # Track which splitters have already been split
    split_splitters = set()

    split_count = 0

    while beams:
        row, col = beams.popleft()

        # Check if we've already processed a beam from this position
        if (row, col) in visited:
            continue
        visited.add((row, col))

        # Beam moves downward until it hits a splitter or exits
        current_row = row
        while current_row < rows:
            current_row += 1

            # Check if beam exits the grid
            if current_row >= rows:
                break

            cell = grid[current_row][col]

            if cell == "^":
                # Beam hits a splitter
                splitter_pos = (current_row, col)

                # Only count the split if this splitter hasn't been split before
                if splitter_pos not in split_splitters:
                    split_count += 1
                    split_splitters.add(splitter_pos)

                # Create two new beams from left and right of the splitter
                if col - 1 >= 0:
                    beams.append((current_row, col - 1))
                if col + 1 < cols:
                    beams.append((current_row, col + 1))

                # Original beam stops here
                break

    return split_count


def part1(input_file: str) -> int:
    """Count how many times the beam is split."""
    grid = parse_input(input_file)
    return simulate_beams(grid)


def count_timelines(grid: List[str], row: int, col: int, memo: dict) -> int:
    """
    Count the number of timelines (unique paths) from position (row, col) to exit.

    A quantum particle moves downward. When it hits a splitter:
    - The timeline splits into two: one going left, one going right
    - Both timelines continue moving downward from their new positions
    """
    # Check memoization
    if (row, col) in memo:
        return memo[(row, col)]

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    # Move down until we hit a splitter or exit
    current_row = row
    while current_row < rows:
        current_row += 1

        # Check if particle exits the grid - this completes 1 timeline
        if current_row >= rows:
            memo[(row, col)] = 1
            return 1

        current_col = col
        cell = grid[current_row][current_col]

        if cell == "^":
            # Hit a splitter - timeline splits into left and right
            left_timelines = 0
            right_timelines = 0

            # Left path: move to left position and continue down
            if current_col - 1 >= 0:
                left_timelines = count_timelines(grid, current_row, current_col - 1, memo)

            # Right path: move to right position and continue down
            if current_col + 1 < cols:
                right_timelines = count_timelines(grid, current_row, current_col + 1, memo)

            # Total timelines is sum of both paths
            total = left_timelines + right_timelines
            memo[(row, col)] = total
            return total

    # Should not reach here, but if we do, no timelines
    memo[(row, col)] = 0
    return 0


def part2(input_file: str) -> int:
    """Count the number of quantum timelines."""
    grid = parse_input(input_file)
    start_row, start_col = find_start(grid)

    memo = {}
    return count_timelines(grid, start_row, start_col, memo)


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
