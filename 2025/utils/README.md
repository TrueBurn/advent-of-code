# Advent of Code 2025 - Utility Library

Common utilities for solving Advent of Code puzzles, based on patterns from 2024 solutions.

## Quick Start

```python
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from utils import Grid, bfs, parse_grid
```

## Modules

### `grid.py` - Grid Operations (40% of AoC problems)

**Classes:**
- `Grid` - 2D grid wrapper with common operations
- `Direction` - Enum for cardinal/diagonal directions

**Functions:**
- `in_bounds(grid, row, col)` - Check if position is valid
- `get_neighbors(row, col, grid, diagonal=False)` - Get neighboring positions
- `manhattan_distance(pos1, pos2)` - Calculate Manhattan distance

**Constants:**
- `CARDINAL_DIRS` - [UP, RIGHT, DOWN, LEFT]
- `ALL_DIRS` - All 8 directions including diagonals

**Example Usage:**
```python
from utils import Grid, Direction, CARDINAL_DIRS

# Load grid from file
grid = Grid.from_file('input.txt')

# Find character positions
start = grid.find('S')
goals = grid.find_all('E')

# Get neighbors
neighbors = grid.get_neighbors(*start, diagonal=False)

# Iterate with directions
for direction in CARDINAL_DIRS:
    dr, dc = direction.value
    new_pos = (start[0] + dr, start[1] + dc)
    if grid.in_bounds(*new_pos):
        print(f"Can move {direction.name}")

# Direction operations
current_dir = Direction.UP
right_dir = current_dir.turn_right()  # Direction.RIGHT
opposite = current_dir.reverse()      # Direction.DOWN
```

### `search.py` - Search Algorithms (30% of AoC problems)

**Functions:**
- `bfs(start, get_neighbors, is_goal)` - Breadth-First Search
- `dfs(start, get_neighbors, is_goal)` - Depth-First Search
- `dijkstra(start, get_neighbors_with_cost, is_goal)` - Dijkstra's algorithm
- `a_star(start, get_neighbors_with_cost, heuristic, is_goal)` - A* algorithm
- `find_all_paths_bfs(start, get_neighbors, is_goal, max_length)` - Find all paths

**Example Usage:**
```python
from utils import bfs, dijkstra, a_star, Grid

grid = Grid.from_file('input.txt')
start = grid.find('S')
end = grid.find('E')

# BFS for unweighted shortest path
visited, goal, distances = bfs(
    start=start,
    get_neighbors=lambda pos: grid.get_neighbors(*pos),
    is_goal=lambda pos: pos == end
)
print(f"Shortest path: {distances[end]} steps")

# Dijkstra for weighted graphs
distances, goal, parents = dijkstra(
    start=start,
    get_neighbors_with_cost=lambda pos: [
        (neighbor, 1) for neighbor in grid.get_neighbors(*pos)
        if grid[neighbor] != '#'
    ],
    is_goal=lambda pos: pos == end
)

# A* with Manhattan distance heuristic
cost, path, g_scores = a_star(
    start=start,
    get_neighbors_with_cost=lambda pos: [
        (n, 1) for n in grid.get_neighbors(*pos) if grid[n] != '#'
    ],
    heuristic=lambda pos: abs(pos[0] - end[0]) + abs(pos[1] - end[1]),
    is_goal=lambda pos: pos == end
)
print(f"A* path length: {len(path)}, cost: {cost}")
```

### `parsing.py` - Input Parsing (100% of AoC problems)

**Functions:**
- `parse_grid(filename, converter=str)` - Parse 2D grid
- `parse_sections(filename)` - Split by blank lines
- `parse_ints(line, signed=True)` - Extract integers from string
- `parse_coords(line, pattern=None)` - Parse coordinate patterns
- `parse_lines(filename, strip=True, skip_empty=True)` - Parse lines
- `parse_blocks(filename)` - Parse blocks separated by blank lines
- `parse_graph(filename, directed=False, separator="-")` - Parse graph edges
- `parse_key_value(filename, separator=":")` - Parse key-value pairs
- `parse_csv(filename, delimiter=",", skip_header=False)` - Parse CSV

**Example Usage:**
```python
from utils import parse_grid, parse_sections, parse_ints, parse_coords

# Character grid
grid = parse_grid('input.txt')  # List[List[str]]

# Integer grid
grid = parse_grid('input.txt', int)  # List[List[int]]

# Multi-section input
sections = parse_sections('input.txt')
rules = sections[0].split('\n')
updates = sections[1].split('\n')

# Extract all integers from line
# "Position: x=10, y=-5, z=20"
coords = parse_ints(line, signed=True)  # [10, -5, 20]

# Parse coordinate patterns
# "p=10,20 v=-3,5"
px, py, vx, vy = parse_coords(line, r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)')
```

## Common Patterns

### Grid Problem Template
```python
from utils import Grid, Direction, CARDINAL_DIRS, bfs

grid = Grid.from_file('input.txt')
start = grid.find('S')
end = grid.find('E')

# BFS to find shortest path
visited, goal, distances = bfs(
    start=start,
    get_neighbors=lambda pos: [
        n for n in grid.get_neighbors(*pos)
        if grid[n] != '#'
    ],
    is_goal=lambda pos: pos == end
)

print(f"Part 1: {distances[end]}")
```

### Graph Problem Template
```python
from utils import parse_graph, bfs
from collections import defaultdict

# Parse graph edges
graph = parse_graph('input.txt', directed=False)

# Or build manually
graph = defaultdict(list)
for line in open('input.txt'):
    a, b = line.strip().split('-')
    graph[a].append(b)
    graph[b].append(a)

# BFS on graph
visited, goal, distances = bfs(
    start='start',
    get_neighbors=lambda node: graph[node],
    is_goal=lambda node: node == 'end'
)
```

### Dynamic Programming Template
```python
from functools import cache

@cache
def solve(state, depth):
    """Memoized recursive solution."""
    if depth == 0:
        return base_case(state)

    results = []
    for next_state in get_next_states(state):
        results.append(solve(next_state, depth - 1))

    return combine(results)
```

## Performance Tips

1. **Use `@cache` for expensive recursive functions** (Days 11, 19, 21)
2. **Pre-compute distances with BFS** when needed multiple times (Day 20)
3. **Use sets for visited tracking** - O(1) lookups
4. **Grid bounds checking** - do once, not per iteration
5. **Direction enums** - cleaner than tuple constants
6. **Early termination** - return as soon as goal is found

## Testing Utilities

```python
import unittest
from solution import part1, part2

class TestSolution(unittest.TestCase):
    def test_part1_example(self):
        result = part1('test_input.txt')
        self.assertEqual(result, expected_value)
```

## Historical Usage (2024)

- **Grid operations**: Days 4, 6, 8, 10, 12, 15, 16, 18, 20 (40%)
- **BFS**: Days 10, 18, 20, 21 (16%)
- **Dijkstra/A***: Days 9, 16 (8%)
- **DFS**: Days 10, 12 (8%)
- **Memoization**: Days 11, 19, 21 (12%)
- **Multi-section parsing**: Days 13, 15, 17, 24, 25 (20%)
