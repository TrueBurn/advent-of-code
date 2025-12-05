"""
Advent of Code 2025 - Day 5: Cafeteria

Part 1: Determine which ingredient IDs are fresh based on ID ranges.
Part 2: Count total unique IDs covered by all ranges.

Algorithm:
- Part 1: Range checking for each ID
- Part 2: Merge overlapping ranges, then count total IDs

Time Complexity:
- Part 1: O(n * m) where n is number of IDs, m is number of ranges
- Part 2: O(m log m) for sorting ranges + O(m) for merging

Space Complexity: O(n + m)

Key Insights:
- Part 1: Check if each ID falls within any range (inclusive)
- Part 2: Merge overlapping/adjacent ranges to avoid double-counting
- Ranges are inclusive on both ends
"""

import sys
from pathlib import Path
from typing import List, Tuple

# Add utils to path
sys.path.append(str(Path(__file__).parent.parent))


def parse_input(input_file: str) -> Tuple[List[Tuple[int, int]], List[int]]:
    """
    Parse the input file into ranges and ingredient IDs.

    Args:
        input_file: Path to the input file

    Returns:
        Tuple of (ranges, ingredient_ids)
        - ranges: List of (start, end) tuples
        - ingredient_ids: List of ingredient IDs to check
    """
    with open(input_file) as f:
        content = f.read()

    # Split by blank line
    sections = content.strip().split("\n\n")
    ranges_section = sections[0]
    ids_section = sections[1]

    # Parse ranges
    ranges = []
    for line in ranges_section.strip().split("\n"):
        start, end = line.split("-")
        ranges.append((int(start), int(end)))

    # Parse ingredient IDs
    ingredient_ids = []
    for line in ids_section.strip().split("\n"):
        ingredient_ids.append(int(line))

    return ranges, ingredient_ids


def is_fresh(ingredient_id: int, ranges: List[Tuple[int, int]]) -> bool:
    """Check if an ingredient ID is fresh (falls within any range)."""
    for start, end in ranges:
        if start <= ingredient_id <= end:
            return True
    return False


def merge_ranges(ranges: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Merge overlapping or adjacent ranges.

    Args:
        ranges: List of (start, end) tuples

    Returns:
        List of merged ranges
    """
    if not ranges:
        return []

    # Sort ranges by start position
    sorted_ranges = sorted(ranges)

    merged = [sorted_ranges[0]]

    for current_start, current_end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]

        # If current range overlaps or is adjacent to last range, merge them
        if current_start <= last_end + 1:
            # Merge by extending the end if needed
            merged[-1] = (last_start, max(last_end, current_end))
        else:
            # No overlap, add as separate range
            merged.append((current_start, current_end))

    return merged


def part1(input_file: str) -> int:
    """
    Count how many ingredient IDs are fresh.

    Args:
        input_file: Path to the input file

    Returns:
        Number of fresh ingredient IDs
    """
    ranges, ingredient_ids = parse_input(input_file)

    fresh_count = 0
    for ingredient_id in ingredient_ids:
        if is_fresh(ingredient_id, ranges):
            fresh_count += 1

    return fresh_count


def part2(input_file: str) -> int:
    """
    Count total number of unique IDs covered by all ranges.

    Args:
        input_file: Path to the input file

    Returns:
        Total number of fresh ingredient IDs
    """
    ranges, _ = parse_input(input_file)

    # Merge overlapping ranges to avoid double-counting
    merged = merge_ranges(ranges)

    # Count IDs in merged ranges (ranges are inclusive)
    total_count = 0
    for start, end in merged:
        total_count += end - start + 1

    return total_count


def main():
    """Main execution function."""
    from unit_tests import run_tests

    if run_tests():
        print("\nAll tests passed! Running actual solution...\n")
        result1 = part1("input.txt")
        print(f"Part 1: {result1}")
        print(f"Part 2: {part2('input.txt')}")
    else:
        print("\nTests failed! Please fix the issues before running the actual solution.")


if __name__ == "__main__":
    main()
