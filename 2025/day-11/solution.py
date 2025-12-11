"""
Advent of Code 2025 - Day 11: Reactor

Algorithm: DFS for finding all paths in a directed graph
Time Complexity: O(V + E) where V is vertices and E is edges
Space Complexity: O(V) for the recursion stack and visited set

Key Insights:
- Build adjacency list from device connections
- Use DFS to find all paths from 'you' to 'out'
- For Part 2: Count paths through required nodes using inclusion-exclusion
- Assume DAG for fast memoization
"""

import sys
from typing import Dict, List

# Increase recursion limit for deep graphs
sys.setrecursionlimit(100000)


def parse_input(input_file: str) -> Dict[str, List[str]]:
    """
    Parse the input file and build a graph adjacency list.

    Each line has format: "device: output1 output2 ..."
    Returns a dict mapping device name to list of outputs.
    """
    graph = {}
    with open(input_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Split on colon to get device and outputs
            device, outputs = line.split(":")
            device = device.strip()
            outputs = outputs.strip().split()

            graph[device] = outputs

    return graph


def find_all_paths(
    graph: Dict[str, List[str]], start: str, end: str, path: List[str] = None
) -> List[List[str]]:
    """
    Find all paths from start to end using DFS.

    Args:
        graph: Adjacency list representation of the graph
        start: Starting node
        end: Target node
        path: Current path (used for recursion)

    Returns:
        List of all paths from start to end
    """
    if path is None:
        path = []

    # Add current node to path
    path = path + [start]

    # Base case: reached the end
    if start == end:
        return [path]

    # If node has no outgoing edges, no path found
    if start not in graph:
        return []

    # Recursively explore all neighbors
    all_paths = []
    for neighbor in graph[start]:
        # Avoid cycles by checking if neighbor is already in path
        if neighbor not in path:
            paths = find_all_paths(graph, neighbor, end, path)
            all_paths.extend(paths)

    return all_paths


def part1(input_file: str) -> int:
    """
    Count all paths from 'you' to 'out'.
    """
    graph = parse_input(input_file)
    paths = find_all_paths(graph, "you", "out")
    return len(paths)


def count_paths_dag(graph: Dict[str, List[str]], start: str, end: str) -> int:
    """
    Count paths assuming DAG (no cycles). Super fast with memoization.
    If there ARE cycles that revisit nodes, this will still work but count them.
    """
    memo = {}

    def dfs(node: str) -> int:
        if node == end:
            return 1

        if node in memo:
            return memo[node]

        if node not in graph:
            return 0

        total = 0
        for neighbor in graph[node]:
            total += dfs(neighbor)

        memo[node] = total
        return total

    return dfs(start)


def remove_node_from_graph(graph: Dict[str, List[str]], node: str) -> Dict[str, List[str]]:
    """
    Create a new graph with the specified node removed.
    """
    new_graph = {}
    for src, dests in graph.items():
        if src == node:
            continue
        # Remove node from destination lists
        new_graph[src] = [d for d in dests if d != node]
    return new_graph


def part2(input_file: str) -> int:
    """
    Count all paths from 'svr' to 'out' that visit both 'dac' and 'fft'.

    Strategy: Use inclusion-exclusion principle
    Total visiting both = All paths - Skip dac - Skip fft + Skip both

    This works because: |A ∩ B| = |U| - |Ā| - |B̄| + |Ā ∩ B̄|
    where A = visit dac, B = visit fft
    """
    graph = parse_input(input_file)

    # Count all paths from svr to out (assuming DAG for speed)
    all_paths = count_paths_dag(graph, "svr", "out")

    # Count paths that skip dac (remove dac from graph)
    graph_no_dac = remove_node_from_graph(graph, "dac")
    skip_dac = count_paths_dag(graph_no_dac, "svr", "out")

    # Count paths that skip fft (remove fft from graph)
    graph_no_fft = remove_node_from_graph(graph, "fft")
    skip_fft = count_paths_dag(graph_no_fft, "svr", "out")

    # Count paths that skip both dac and fft
    graph_no_both = remove_node_from_graph(graph_no_dac, "fft")
    skip_both = count_paths_dag(graph_no_both, "svr", "out")

    # Inclusion-exclusion
    return all_paths - skip_dac - skip_fft + skip_both


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
