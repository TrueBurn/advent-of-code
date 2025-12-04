"""
Advent of Code 2025 - Day 4: Printing Department

Count rolls of paper that can be accessed by forklifts.
A roll is accessible if it has fewer than 4 neighboring rolls in the 8 adjacent positions.

Algorithm: Grid traversal with neighbor counting
Time Complexity: O(rows * cols)
Space Complexity: O(rows * cols) for the grid
"""

from typing import List


def parse_input(input_file: str) -> List[str]:
    """Parse the input file into a list of strings representing the grid."""
    data = []
    with open(input_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data.append(line)
    return data


def count_accessible_rolls(grid: List[str]) -> int:
    """
    Count rolls that have fewer than 4 neighboring rolls in the 8 adjacent positions.

    Args:
        grid: List of strings representing the grid

    Returns:
        Number of accessible rolls
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    accessible = 0

    # All 8 directions: N, NE, E, SE, S, SW, W, NW
    directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == "@":
                # Count neighbors that are also rolls
                neighbor_count = 0
                for dr, dc in directions:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "@":
                        neighbor_count += 1

                # Accessible if fewer than 4 neighbors
                if neighbor_count < 4:
                    accessible += 1

    return accessible


def part1(input_file: str) -> int:
    """
    Solve Part 1: Count accessible rolls of paper.

    Args:
        input_file: Path to the input file

    Returns:
        Number of accessible rolls
    """
    grid = parse_input(input_file)
    return count_accessible_rolls(grid)


def remove_accessible_rolls_iteratively(grid: List[str]) -> int:
    """
    Repeatedly remove accessible rolls until no more can be removed.
    Count total rolls removed.

    Args:
        grid: List of strings representing the grid

    Returns:
        Total number of rolls removed
    """
    # Convert to list of lists so we can modify it
    grid = [list(row) for row in grid]
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    directions = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]

    total_removed = 0

    while True:
        # Find all accessible rolls (fewer than 4 neighbors)
        accessible_positions = []

        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == "@":
                    # Count neighbors that are also rolls
                    neighbor_count = 0
                    for dr, dc in directions:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "@":
                            neighbor_count += 1

                    # Accessible if fewer than 4 neighbors
                    if neighbor_count < 4:
                        accessible_positions.append((row, col))

        # If no accessible rolls, we're done
        if not accessible_positions:
            break

        # Remove all accessible rolls
        for row, col in accessible_positions:
            grid[row][col] = "."

        total_removed += len(accessible_positions)

    return total_removed


def part2(input_file: str) -> int:
    """
    Solve Part 2: Count total rolls that can be removed by iteratively
    removing accessible rolls.

    Args:
        input_file: Path to the input file

    Returns:
        Total number of rolls removed
    """
    grid = parse_input(input_file)
    return remove_accessible_rolls_iteratively(grid)


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
