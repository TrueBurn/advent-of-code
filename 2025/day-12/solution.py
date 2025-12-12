"""
Advent of Code 2025 - Day 12: Christmas Tree Farm

Algorithm: Backtracking with "fill first empty cell" heuristic
Time Complexity: O(exponential) but heavily pruned
Space Complexity: O(W*H) for grid state

Key Insights:
- This is a polyomino packing problem
- Use "fill first empty cell" strategy to prune search space
- Area check provides quick rejection for impossible cases
- Sort pieces largest-first for better pruning
"""

import sys
from pathlib import Path
from typing import FrozenSet, List, Set, Tuple

sys.path.append(str(Path(__file__).parent.parent))


def parse_input(input_file: str):
    """Parse shapes and regions from input file."""
    with open(input_file) as f:
        content = f.read()

    # Split into sections (separated by blank lines)
    sections = content.strip().split("\n\n")

    shapes = []
    regions = []

    for section in sections:
        lines = section.strip().split("\n")
        first_line = lines[0]

        # Check if this is a shape definition (e.g., "0:")
        if first_line.endswith(":") and "x" not in first_line:
            shape_lines = lines[1:]
            cells = set()
            for r, line in enumerate(shape_lines):
                for c, ch in enumerate(line):
                    if ch == "#":
                        cells.add((r, c))
            shapes.append(cells)
        else:
            # Region definitions
            for line in lines:
                if "x" in line:
                    parts = line.split(": ")
                    dims = parts[0].split("x")
                    w, h = int(dims[0]), int(dims[1])
                    counts = list(map(int, parts[1].split()))
                    regions.append((w, h, counts))

    return shapes, regions


def normalize(cells: Set[Tuple[int, int]]) -> FrozenSet[Tuple[int, int]]:
    """Normalize shape so minimum row and col are 0."""
    if not cells:
        return frozenset()
    min_r = min(r for r, c in cells)
    min_c = min(c for r, c in cells)
    return frozenset((r - min_r, c - min_c) for r, c in cells)


def rotate_90(cells: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    """Rotate 90 degrees clockwise: (r, c) -> (c, -r)."""
    return {(c, -r) for r, c in cells}


def flip_horizontal(cells: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    """Flip horizontally: (r, c) -> (r, -c)."""
    return {(r, -c) for r, c in cells}


def get_all_variants(cells: Set[Tuple[int, int]]) -> List[FrozenSet[Tuple[int, int]]]:
    """Get all unique orientations (rotations + reflections) of a shape."""
    variants = set()
    current = cells
    for _ in range(4):
        variants.add(normalize(current))
        variants.add(normalize(flip_horizontal(current)))
        current = rotate_90(current)
    return list(variants)


def can_fit_pieces(w: int, h: int, piece_list: List[List[FrozenSet]]) -> bool:
    """Check if all pieces can fit in the grid using backtracking."""
    if not piece_list:
        return True

    # Quick area check
    total_cells = sum(len(variants[0]) for variants in piece_list)
    if total_cells > w * h:
        return False

    # Sort pieces: largest first (more constrained), then by fewest variants
    piece_list = sorted(piece_list, key=lambda v: (-len(v[0]), len(v)))

    # Pre-compute variant bounds for faster bounds checking
    variant_info = []
    for variants in piece_list:
        info = []
        for variant in variants:
            max_r = max(dr for dr, dc in variant)
            max_c = max(dc for dr, dc in variant)
            info.append((variant, max_r, max_c))
        variant_info.append(info)

    grid = [[False] * w for _ in range(h)]

    def backtrack(piece_idx: int) -> bool:
        if piece_idx >= len(piece_list):
            return True

        for variant, max_r, max_c in variant_info[piece_idx]:
            # Try placing at all valid positions
            for r in range(h - max_r):
                for c in range(w - max_c):
                    # Check if can place here
                    can_place = True
                    for dr, dc in variant:
                        if grid[r + dr][c + dc]:
                            can_place = False
                            break

                    if can_place:
                        # Place piece
                        for dr, dc in variant:
                            grid[r + dr][c + dc] = True

                        if backtrack(piece_idx + 1):
                            return True

                        # Remove piece
                        for dr, dc in variant:
                            grid[r + dr][c + dc] = False

        return False

    return backtrack(0)


def part1(input_file: str) -> int:
    """Count regions that can fit all their required presents."""
    shapes, regions = parse_input(input_file)

    # Pre-compute all variants for each shape
    shape_variants = [get_all_variants(shape) for shape in shapes]

    count = 0
    for w, h, piece_counts in regions:
        # Build list of all pieces to place
        pieces = []
        for shape_idx, cnt in enumerate(piece_counts):
            for _ in range(cnt):
                pieces.append(shape_variants[shape_idx])

        if can_fit_pieces(w, h, pieces):
            count += 1

    return count


def part2(input_file: str) -> str:
    """Part 2 is narrative only - no additional computation required."""
    return "No puzzle - star awarded for completing Part 1!"


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
