"""
Advent of Code 2025 - Day 3: Lobby

Find the maximum joltage from each battery bank by turning on exactly two batteries.
The joltage is the 2-digit number formed by the selected batteries (in order).

Key Insight:
- Try all possible pairs of batteries (i, j) where i < j
- The joltage is int(digit[i] + digit[j])
- Find the maximum for each bank and sum them all
"""

from typing import List


def parse_input(input_file: str) -> List[str]:
    """Parse the input file into a list of battery bank strings."""
    data = []
    with open(input_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data.append(line)
    return data


def find_max_joltage(bank: str) -> int:
    """
    Find the maximum joltage possible from a single battery bank.

    Args:
        bank: String of digits representing battery joltages

    Returns:
        Maximum joltage (2-digit number) possible from the bank
    """
    max_joltage = 0

    # Try all pairs of batteries (i, j) where i < j
    for i in range(len(bank)):
        for j in range(i + 1, len(bank)):
            # Form the 2-digit number from positions i and j
            joltage = int(bank[i] + bank[j])
            max_joltage = max(max_joltage, joltage)

    return max_joltage


def part1(input_file: str) -> int:
    """
    Solve Part 1: Find the total output joltage from all battery banks.

    Args:
        input_file: Path to the input file

    Returns:
        Sum of maximum joltages from all banks
    """
    banks = parse_input(input_file)
    total = 0

    for bank in banks:
        max_joltage = find_max_joltage(bank)
        total += max_joltage

    return total


def find_max_joltage_n_batteries(bank: str, num_batteries: int) -> int:
    """
    Find the maximum joltage by selecting exactly num_batteries batteries.

    Uses a greedy approach: at each position, select the largest digit
    that still leaves enough batteries for the remaining positions.

    Args:
        bank: String of digits representing battery joltages
        num_batteries: Number of batteries to select

    Returns:
        Maximum joltage (num_batteries-digit number) possible from the bank
    """
    n = len(bank)
    result = []
    start = 0

    for i in range(num_batteries):
        # How many more digits do we need after this one?
        remaining = num_batteries - i - 1
        # We can search up to this position (leaving enough for remaining digits)
        end = n - remaining

        # Find the maximum digit in the valid range
        max_digit = max(bank[start:end])
        # Find the first occurrence of this max digit
        max_idx = bank.index(max_digit, start)

        result.append(max_digit)
        start = max_idx + 1

    return int("".join(result))


def part2(input_file: str) -> int:
    """
    Solve Part 2: Find the total output joltage using 12 batteries per bank.

    Args:
        input_file: Path to the input file

    Returns:
        Sum of maximum 12-digit joltages from all banks
    """
    banks = parse_input(input_file)
    total = 0

    for bank in banks:
        max_joltage = find_max_joltage_n_batteries(bank, 12)
        total += max_joltage

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
