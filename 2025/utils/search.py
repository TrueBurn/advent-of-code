"""
Search algorithm templates for pathfinding and graph traversal.

Common patterns from AoC 2024: Days 10, 16, 18, 20, 21
"""

import heapq
from collections import deque
from typing import Callable, Dict, List, Optional, Set, Tuple, TypeVar

T = TypeVar("T")


def bfs(
    start: T,
    get_neighbors: Callable[[T], List[T]],
    is_goal: Optional[Callable[[T], bool]] = None,
) -> Tuple[Set[T], Optional[T], Dict[T, int]]:
    """
    Breadth-First Search for unweighted graphs.

    Args:
        start: Starting node
        get_neighbors: Function that returns list of neighbors for a node
        is_goal: Optional function to check if node is the goal

    Returns:
        Tuple of (visited_set, goal_node_or_none, distances_dict)

    Example:
        visited, goal, distances = bfs(
            start=(0, 0),
            get_neighbors=lambda pos: grid.get_neighbors(*pos),
            is_goal=lambda pos: grid[pos] == 'E'
        )
    """
    queue = deque([start])
    visited = {start}
    distances = {start: 0}
    goal_node = None

    while queue:
        current = queue.popleft()

        if is_goal and is_goal(current):
            goal_node = current
            if goal_node:  # Stop at first goal
                break

        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)

    return visited, goal_node, distances


def dfs(
    start: T,
    get_neighbors: Callable[[T], List[T]],
    is_goal: Optional[Callable[[T], bool]] = None,
    visited: Optional[Set[T]] = None,
) -> Tuple[Set[T], Optional[T]]:
    """
    Depth-First Search for graph traversal.

    Args:
        start: Starting node
        get_neighbors: Function that returns list of neighbors for a node
        is_goal: Optional function to check if node is the goal
        visited: Optional set of already visited nodes (for recursion)

    Returns:
        Tuple of (visited_set, goal_node_or_none)

    Example:
        visited, goal = dfs(
            start=(0, 0),
            get_neighbors=lambda pos: grid.get_neighbors(*pos),
            is_goal=lambda pos: grid[pos] == 'E'
        )
    """
    if visited is None:
        visited = set()

    visited.add(start)

    if is_goal and is_goal(start):
        return visited, start

    for neighbor in get_neighbors(start):
        if neighbor not in visited:
            result_visited, goal = dfs(neighbor, get_neighbors, is_goal, visited)
            if goal:
                return result_visited, goal

    return visited, None


def dijkstra(
    start: T,
    get_neighbors_with_cost: Callable[[T], List[Tuple[T, int]]],
    is_goal: Optional[Callable[[T], bool]] = None,
) -> Tuple[Dict[T, int], Optional[T], Dict[T, Optional[T]]]:
    """
    Dijkstra's algorithm for weighted shortest path.

    Args:
        start: Starting node
        get_neighbors_with_cost: Function returning list of (neighbor, cost) tuples
        is_goal: Optional function to check if node is the goal

    Returns:
        Tuple of (distances_dict, goal_node_or_none, parent_dict)

    Example:
        distances, goal, parents = dijkstra(
            start=(0, 0),
            get_neighbors_with_cost=lambda pos: [
                (neighbor, 1) for neighbor in grid.get_neighbors(*pos)
            ],
            is_goal=lambda pos: pos == (9, 9)
        )
    """
    queue = [(0, start)]
    distances = {start: 0}
    parents = {start: None}
    visited = set()

    while queue:
        current_dist, current = heapq.heappop(queue)

        if current in visited:
            continue

        visited.add(current)

        if is_goal and is_goal(current):
            return distances, current, parents

        for neighbor, cost in get_neighbors_with_cost(current):
            new_dist = current_dist + cost

            if neighbor not in distances or new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                parents[neighbor] = current
                heapq.heappush(queue, (new_dist, neighbor))

    return distances, None, parents


def a_star(
    start: T,
    get_neighbors_with_cost: Callable[[T], List[Tuple[T, int]]],
    heuristic: Callable[[T], int],
    is_goal: Callable[[T], bool],
) -> Tuple[Optional[int], Optional[List[T]], Dict[T, int]]:
    """
    A* algorithm for weighted shortest path with heuristic.

    Args:
        start: Starting node
        get_neighbors_with_cost: Function returning list of (neighbor, cost) tuples
        heuristic: Heuristic function estimating cost to goal
        is_goal: Function to check if node is the goal

    Returns:
        Tuple of (path_cost_or_none, path_list_or_none, g_scores_dict)

    Example:
        cost, path, g_scores = a_star(
            start=(0, 0),
            get_neighbors_with_cost=lambda pos: [
                (n, 1) for n in grid.get_neighbors(*pos)
            ],
            heuristic=lambda pos: abs(pos[0] - 9) + abs(pos[1] - 9),
            is_goal=lambda pos: pos == (9, 9)
        )
    """
    # Priority queue: (f_score, g_score, node)
    queue = [(heuristic(start), 0, start)]
    g_scores = {start: 0}
    parents = {start: None}
    visited = set()

    while queue:
        f_score, g_score, current = heapq.heappop(queue)

        if current in visited:
            continue

        visited.add(current)

        if is_goal(current):
            # Reconstruct path
            path = []
            node = current
            while node is not None:
                path.append(node)
                node = parents[node]
            path.reverse()
            return g_score, path, g_scores

        for neighbor, cost in get_neighbors_with_cost(current):
            new_g_score = g_score + cost

            if neighbor not in g_scores or new_g_score < g_scores[neighbor]:
                g_scores[neighbor] = new_g_score
                f = new_g_score + heuristic(neighbor)
                parents[neighbor] = current
                heapq.heappush(queue, (f, new_g_score, neighbor))

    return None, None, g_scores


def find_all_paths_bfs(
    start: T,
    get_neighbors: Callable[[T], List[T]],
    is_goal: Callable[[T], bool],
    max_length: Optional[int] = None,
) -> List[List[T]]:
    """
    Find all paths from start to any goal using BFS.

    Args:
        start: Starting node
        get_neighbors: Function that returns list of neighbors
        is_goal: Function to check if node is a goal
        max_length: Optional maximum path length

    Returns:
        List of paths, where each path is a list of nodes

    Example:
        paths = find_all_paths_bfs(
            start=(0, 0),
            get_neighbors=lambda pos: grid.get_neighbors(*pos),
            is_goal=lambda pos: grid[pos] == '9',
            max_length=10
        )
    """
    queue = deque([(start, [start])])
    all_paths = []

    while queue:
        current, path = queue.popleft()

        if max_length and len(path) > max_length:
            continue

        if is_goal(current):
            all_paths.append(path)
            continue

        for neighbor in get_neighbors(current):
            if neighbor not in path:  # Avoid cycles
                queue.append((neighbor, path + [neighbor]))

    return all_paths
