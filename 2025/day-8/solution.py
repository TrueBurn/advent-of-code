"""
Advent of Code 2025 - Day 8: Playground

Connect junction boxes in 3D space to form circuits.
Use Union-Find to track connected components.

Algorithm: Union-Find with sorted edge list
Time Complexity: O(n^2 log n) for sorting all pairs + O(n^2 * α(n)) for union-find
Space Complexity: O(n^2) for storing all distances

Key Insights:
- Classic Minimum Spanning Tree problem using Kruskal's algorithm
- Union-Find efficiently tracks connected components
- Sort all pairwise distances and connect 1000 closest pairs
- Track circuit sizes after connections complete
"""

import heapq
from typing import List, Tuple


class UnionFind:
    """Union-Find data structure for tracking connected components."""

    def __init__(self, n: int):
        """Initialize with n separate components."""
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n

    def find(self, x: int) -> int:
        """Find root of component containing x with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """
        Union components containing x and y.
        Returns True if they were in different components, False if already connected.
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            root_x, root_y = root_y, root_x

        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]

        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_x] += 1

        return True

    def get_component_sizes(self) -> List[int]:
        """Get sizes of all connected components."""
        roots = {}
        for i in range(len(self.parent)):
            root = self.find(i)
            if root not in roots:
                roots[root] = self.size[root]
        return list(roots.values())

    def count_components(self) -> int:
        """Count number of distinct connected components."""
        roots = set()
        for i in range(len(self.parent)):
            roots.add(self.find(i))
        return len(roots)


def parse_input(input_file: str) -> List[Tuple[int, int, int]]:
    """
    Parse junction box positions from input file.

    Args:
        input_file: Path to the input file

    Returns:
        List of (x, y, z) tuples representing junction box positions
    """
    positions = []
    with open(input_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            x, y, z = map(int, line.split(","))
            positions.append((x, y, z))
    return positions


def euclidean_distance(p1: Tuple[int, int, int], p2: Tuple[int, int, int]) -> float:
    """Calculate Euclidean distance between two 3D points."""
    return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2) ** 0.5


def part1(input_file: str, num_connections: int = 1000) -> int:
    """
    Connect the closest pairs of junction boxes and find largest circuits.

    Args:
        input_file: Path to the input file
        num_connections: Number of connections to make (default 1000)

    Returns:
        Product of three largest circuit sizes
    """
    positions = parse_input(input_file)
    n = len(positions)

    # Build list of all pairwise distances with junction box indices
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = euclidean_distance(positions[i], positions[j])
            edges.append((dist, i, j))

    # Sort by distance (smallest first) using heapq for efficiency
    heapq.heapify(edges)

    # Initialize Union-Find
    uf = UnionFind(n)

    # Try to connect the num_connections closest pairs
    # Count all attempts, not just successful ones
    for _ in range(min(num_connections, len(edges))):
        if edges:
            dist, i, j = heapq.heappop(edges)
            uf.union(i, j)  # May or may not succeed if already connected

    # Get all component sizes
    component_sizes = uf.get_component_sizes()

    # Find three largest components
    component_sizes.sort(reverse=True)

    return component_sizes[0] * component_sizes[1] * component_sizes[2]


def part2(input_file: str) -> int:
    """
    Connect junction boxes until all form a single circuit.

    Args:
        input_file: Path to the input file

    Returns:
        Product of X coordinates of the last two junction boxes connected
    """
    positions = parse_input(input_file)
    n = len(positions)

    # Build list of all pairwise distances with junction box indices
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = euclidean_distance(positions[i], positions[j])
            edges.append((dist, i, j))

    # Sort by distance (smallest first)
    edges.sort()

    # Initialize Union-Find
    uf = UnionFind(n)

    # Keep connecting until we have a single component
    last_i, last_j = -1, -1
    for dist, i, j in edges:
        if uf.union(i, j):
            last_i, last_j = i, j
            # Check if all boxes are now in one circuit
            if uf.count_components() == 1:
                break

    # Return product of X coordinates
    return positions[last_i][0] * positions[last_j][0]


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
