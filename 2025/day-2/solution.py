"""
Advent of Code 2025 - Day 2: Gift Shop

Find invalid product IDs that are digit sequences repeated twice.
For example: 11 (1 twice), 6464 (64 twice), 123123 (123 twice)

Algorithm: String manipulation and pattern matching
Time Complexity: O(n * m) where n is ranges, m is IDs per range
Space Complexity: O(1)

Key Insights:
- Invalid ID has even length and first half equals second half
- No leading zeros allowed
- Check each ID in the ranges to find invalid ones
"""

import sys
from pathlib import Path
from typing import List, Tuple

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))


def is_invalid_id(num: int) -> bool:
    """
    Check if a number is an invalid ID (sequence repeated exactly twice).

    Args:
        num: The number to check

    Returns:
        True if the number is an invalid ID, False otherwise
    """
    s = str(num)
    # Must have even length to be repeated
    if len(s) % 2 != 0:
        return False

    # Split in half and check if both halves are equal
    mid = len(s) // 2
    return s[:mid] == s[mid:]


def is_invalid_id_part2(num: int) -> bool:
    """
    Check if a number is an invalid ID (sequence repeated at least twice).

    Args:
        num: The number to check

    Returns:
        True if the number is an invalid ID, False otherwise
    """
    s = str(num)
    length = len(s)

    # Try all possible pattern lengths (from 1 to length//2)
    for pattern_len in range(1, length // 2 + 1):
        # Check if the string length is divisible by pattern length
        if length % pattern_len == 0:
            pattern = s[:pattern_len]
            # Check if the entire string is made of this pattern repeated
            repeats = length // pattern_len
            if pattern * repeats == s and repeats >= 2:
                return True

    return False


def parse_input(input_file: str) -> List[Tuple[int, int]]:
    """
    Parse the input file and return list of ID ranges.

    Args:
        input_file: Path to the input file

    Returns:
        List of (start, end) tuples for each range
    """
    ranges = []
    with open(input_file) as f:
        content = f.read().strip()
        # Split by comma and parse each range
        for range_str in content.split(","):
            range_str = range_str.strip()
            if "-" in range_str:
                start, end = range_str.split("-")
                ranges.append((int(start), int(end)))
    return ranges


def part1(input_file: str) -> int:
    """
    Find and sum all invalid IDs in the given ranges.

    Args:
        input_file: Path to the input file

    Returns:
        Sum of all invalid IDs
    """
    ranges = parse_input(input_file)
    total = 0

    for start, end in ranges:
        for num in range(start, end + 1):
            if is_invalid_id(num):
                total += num

    return total


def part2(input_file: str) -> int:
    """
    Find and sum all invalid IDs in the given ranges (at least twice repetition).

    Args:
        input_file: Path to the input file

    Returns:
        Sum of all invalid IDs
    """
    ranges = parse_input(input_file)
    total = 0

    for start, end in ranges:
        for num in range(start, end + 1):
            if is_invalid_id_part2(num):
                total += num

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
