"""
Advent of Code 2025 - Day 9: Movie Theater

Part 1: Find the largest rectangle using two red tiles as opposite corners.
Part 2: Rectangle can only contain red or green tiles (green = perimeter + interior of polygon).

Algorithm:
- Part 1: O(n^2) brute force checking all pairs
- Part 2: O(n^3) using segment-based validation for rectilinear polygon

Key Insights:
- Part 1: Any two tiles form corners, area = (|x2-x1|+1) * (|y2-y1|+1)
- Part 2: Polygon is rectilinear (axis-aligned edges). Precompute valid x-range
  for each y-segment, then check rectangles against these ranges in O(n).
"""

from typing import List, Tuple


def parse_input(input_file: str) -> List[Tuple[int, int]]:
    """Parse coordinate pairs from input file."""
    coords = []
    with open(input_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            x, y = map(int, line.split(","))
            coords.append((x, y))
    return coords


def part1(input_file: str) -> int:
    """Find the largest rectangle area using two red tiles as corners."""
    coords = parse_input(input_file)

    max_area = 0

    # Try all pairs of coordinates
    for i in range(len(coords)):
        for j in range(i + 1, len(coords)):
            x1, y1 = coords[i]
            x2, y2 = coords[j]

            # Calculate rectangle area (inclusive of endpoints)
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            area = width * height

            max_area = max(max_area, area)

    return max_area


def build_segment_ranges(
    polygon: List[Tuple[int, int]],
) -> Tuple[List[int], List[Tuple[int, int, int, int]]]:
    """
    Build y-segments with their valid x-ranges for a rectilinear polygon.

    Returns:
        y_values: Sorted unique y-coordinates
        segments: List of (y_lo, y_hi, x_min, x_max) for each y-segment
    """
    y_values = sorted(set(p[1] for p in polygon))

    # Build vertical edges: (x, y_min, y_max)
    v_edges = []
    for i in range(len(polygon)):
        p1, p2 = polygon[i], polygon[(i + 1) % len(polygon)]
        if p1[0] == p2[0]:  # Vertical edge
            v_edges.append((p1[0], min(p1[1], p2[1]), max(p1[1], p2[1])))

    # Compute interior x-range for each y-segment
    segments = []
    for i in range(len(y_values) - 1):
        y_lo, y_hi = y_values[i], y_values[i + 1]
        y_mid = (y_lo + y_hi) / 2

        # Find vertical edges that cross this y level
        crossings = sorted([x for (x, y_min, y_max) in v_edges if y_min < y_mid < y_max])
        if len(crossings) >= 2:
            segments.append((y_lo, y_hi, crossings[0], crossings[-1]))

    return y_values, segments


def is_rectangle_valid_fast(
    segments: List[Tuple[int, int, int, int]],
    x_min: int,
    x_max: int,
    y_min: int,
    y_max: int,
) -> bool:
    """Check if rectangle is entirely within the polygon using segment ranges."""
    for y_lo, y_hi, seg_x_min, seg_x_max in segments:
        # Check if this segment overlaps with rectangle's y-range
        if y_hi <= y_min or y_lo >= y_max:
            continue  # No overlap

        # Rectangle's x-range must be within segment's x-range
        if x_min < seg_x_min or x_max > seg_x_max:
            return False

    return True


def part2(input_file: str) -> int:
    """Find largest rectangle using only red and green tiles."""
    red_tiles = parse_input(input_file)

    # Build segment ranges for efficient rectangle validation
    y_values, segments = build_segment_ranges(red_tiles)

    max_area = 0

    # Try all pairs of red tiles as corners
    for i in range(len(red_tiles)):
        for j in range(i + 1, len(red_tiles)):
            c1, c2 = red_tiles[i], red_tiles[j]
            x_min, x_max = min(c1[0], c2[0]), max(c1[0], c2[0])
            y_min, y_max = min(c1[1], c2[1]), max(c1[1], c2[1])

            if is_rectangle_valid_fast(segments, x_min, x_max, y_min, y_max):
                area = (x_max - x_min + 1) * (y_max - y_min + 1)
                max_area = max(max_area, area)

    return max_area


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
