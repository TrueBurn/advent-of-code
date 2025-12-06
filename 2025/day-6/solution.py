"""
Advent of Code 2025 - Day 6: Trash Compactor

Algorithm: String parsing and column-based grouping
Time Complexity: O(n*m) where n is rows and m is max column width
Space Complexity: O(n*m)

Key Insights:
- Problems are arranged vertically in columns
- Problems are separated by full columns of spaces
- Need to identify column boundaries and group numbers with their operators
"""

import sys
from pathlib import Path
from typing import List, Tuple

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))


def parse_input(input_file: str) -> List[Tuple[List[int], str]]:
    """
    Parse the vertical math worksheet into problems.

    Each problem is a tuple of (numbers, operator).

    Args:
        input_file: Path to the input file

    Returns:
        List of problems as (numbers, operator) tuples
    """
    with open(input_file) as f:
        lines = [line.rstrip("\n") for line in f if line.strip()]

    if not lines:
        return []

    # Ensure all lines are the same length by padding with spaces
    max_len = max(len(line) for line in lines)
    lines = [line.ljust(max_len) for line in lines]

    # Find separator columns (columns where ALL rows have spaces)
    separator_cols = set(range(max_len))
    for line in lines:
        for col_idx in range(len(line)):
            if line[col_idx] != " ":
                separator_cols.discard(col_idx)

    # Find problem column ranges (non-separator columns grouped together)
    problem_ranges = []
    start_col = None

    for col_idx in range(max_len):
        if col_idx not in separator_cols:
            # Start of a problem or continuation
            if start_col is None:
                start_col = col_idx
        else:
            # Separator found, end the current problem if one exists
            if start_col is not None:
                problem_ranges.append((start_col, col_idx))
                start_col = None

    # Don't forget the last problem if it extends to the end
    if start_col is not None:
        problem_ranges.append((start_col, max_len))

    # Extract problems from each range
    problems = []
    for start, end in problem_ranges:
        numbers = []
        operator = None

        for line in lines:
            segment = line[start:end].strip()
            if not segment:
                continue

            # Check if this is an operator
            if segment in ("*", "+"):
                operator = segment
            else:
                # Try to parse as number
                try:
                    numbers.append(int(segment))
                except ValueError:
                    pass

        if numbers and operator:
            problems.append((numbers, operator))

    return problems


def solve_problems(numbers: List[int], operator: str) -> int:
    """Calculate the result of applying the operator to all numbers."""
    if operator == "*":
        result = 1
        for num in numbers:
            result *= num
        return result
    elif operator == "+":
        return sum(numbers)
    else:
        raise ValueError(f"Unknown operator: {operator}")


def part1(input_file: str) -> int:
    """
    Solve Part 1: Calculate the grand total of all problems.

    Args:
        input_file: Path to the input file

    Returns:
        Grand total (sum of all problem answers)
    """
    problems = parse_input(input_file)
    grand_total = 0

    for numbers, operator in problems:
        answer = solve_problems(numbers, operator)
        grand_total += answer

    return grand_total


def parse_input_part2(input_file: str) -> List[Tuple[List[int], str]]:
    """
    Parse the worksheet for Part 2 (cephalopod math - right-to-left reading).

    In cephalopod math, each character column (read top-to-bottom) forms a number,
    and we read columns right-to-left.

    Args:
        input_file: Path to the input file

    Returns:
        List of problems as (numbers, operator) tuples
    """
    with open(input_file) as f:
        lines = [line.rstrip("\n") for line in f if line.strip()]

    if not lines:
        return []

    # Ensure all lines are the same length by padding with spaces
    max_len = max(len(line) for line in lines)
    lines = [line.ljust(max_len) for line in lines]

    # Find separator columns (columns where ALL rows have spaces)
    separator_cols = set(range(max_len))
    for line in lines:
        for col_idx in range(len(line)):
            if line[col_idx] != " ":
                separator_cols.discard(col_idx)

    # Find problem column ranges
    problem_ranges = []
    start_col = None

    for col_idx in range(max_len):
        if col_idx not in separator_cols:
            if start_col is None:
                start_col = col_idx
        else:
            if start_col is not None:
                problem_ranges.append((start_col, col_idx))
                start_col = None

    if start_col is not None:
        problem_ranges.append((start_col, max_len))

    # Extract problems with cephalopod reading
    problems = []
    for start, end in problem_ranges:
        # Extract the text segments for this problem (preserving spacing)
        segments = []
        operator = None

        for line in lines:
            segment = line[start:end]
            stripped = segment.strip()

            if not stripped:
                continue

            # Check if this is an operator
            if stripped in ("*", "+"):
                operator = stripped
            else:
                # This is a number row - keep the segment with its spacing
                segments.append(segment)

        if not segments or not operator:
            continue

        # Find the maximum width
        width = max(len(seg.rstrip()) for seg in segments)

        # Strip trailing spaces from segments (keep them left-aligned)
        stripped_segments = [seg.rstrip() for seg in segments]

        # Read right-to-left by character position
        numbers = []
        for char_pos in range(width - 1, -1, -1):
            # Read this character position top-to-bottom
            digits = []
            for segment in stripped_segments:
                if char_pos < len(segment):
                    digits.append(segment[char_pos])

            # Form a number from these digits
            if digits:
                number_str = "".join(digits)
                try:
                    numbers.append(int(number_str))
                except ValueError:
                    pass

        if numbers and operator:
            problems.append((numbers, operator))

    return problems


def part2(input_file: str) -> int:
    """
    Solve Part 2: Calculate grand total using cephalopod math (right-to-left reading).

    Args:
        input_file: Path to the input file

    Returns:
        Grand total for Part 2
    """
    problems = parse_input_part2(input_file)
    grand_total = 0

    for numbers, operator in problems:
        answer = solve_problems(numbers, operator)
        grand_total += answer

    return grand_total


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
