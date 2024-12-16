from dataclasses import dataclass
from typing import List, Set, Dict, Tuple
from enum import Enum
import heapq

class Cell(str, Enum):
    WALL = '#'
    EMPTY = '.'
    START = 'S'
    END = 'E'

class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

@dataclass(frozen=True)
class State:
    row: int
    col: int
    direction: Direction

    def __lt__(self, other):
        return False

def parse_input(input_file: str) -> Tuple[List[List[str]], State, Tuple[int, int]]:
    grid = []
    start_pos = None
    end_pos = None
    
    with open(input_file) as f:
        for i, line in enumerate(f.readlines()):
            row = list(line.strip())
            if Cell.START in row:
                j = row.index(Cell.START)
                start_pos = (i, j)
                row[j] = Cell.EMPTY
            if Cell.END in row:
                j = row.index(Cell.END)
                end_pos = (i, j)
                row[j] = Cell.EMPTY
            grid.append(row)
    
    return grid, State(start_pos[0], start_pos[1], Direction.EAST), end_pos

def get_next_states(state: State, grid: List[List[str]]) -> List[Tuple[State, int]]:
    next_states = []
    rows, cols = len(grid), len(grid[0])
    row_offsets = [-1, 0, 1, 0]
    col_offsets = [0, 1, 0, -1]
    
    new_row = state.row + row_offsets[state.direction.value]
    new_col = state.col + col_offsets[state.direction.value]
    
    if (0 <= new_row < rows and 0 <= new_col < cols and 
        grid[new_row][new_col] != Cell.WALL):
        next_states.append((State(new_row, new_col, state.direction), 1))
    
    for new_direction in [
        Direction((state.direction.value - 1) % 4),
        Direction((state.direction.value + 1) % 4)
    ]:
        next_states.append((State(state.row, state.col, new_direction), 1000))
    
    return next_states

def manhattan_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def find_shortest_path(grid: List[List[str]], start_state: State, end_pos: Tuple[int, int]) -> int:
    queue = [(0, 0, start_state)]
    visited = set()
    g_scores = {start_state: 0}
    
    while queue:
        _, g_score, current = heapq.heappop(queue)
        
        if (current.row, current.col) == end_pos:
            return g_score
        
        if current in visited:
            continue
        
        visited.add(current)
        
        for next_state, cost in get_next_states(current, grid):
            new_g_score = g_score + cost
            
            if next_state not in g_scores or new_g_score < g_scores[next_state]:
                g_scores[next_state] = new_g_score
                f_score = new_g_score + manhattan_distance(
                    (next_state.row, next_state.col), 
                    end_pos
                )
                heapq.heappush(queue, (f_score, new_g_score, next_state))
    
    return float('inf')

def find_all_optimal_paths(grid: List[List[str]], start_state: State, end_pos: Tuple[int, int]) -> Set[Tuple[int, int]]:
    queue = [(0, 0, start_state, [(start_state.row, start_state.col)])]
    visited = set()
    g_scores = {start_state: 0}
    optimal_score = float('inf')
    optimal_paths = []
    
    while queue:
        _, g_score, current, path = heapq.heappop(queue)
        
        if g_score > optimal_score:
            continue
        
        if (current.row, current.col) == end_pos:
            if g_score < optimal_score:
                optimal_score = g_score
                optimal_paths = [path]
            elif g_score == optimal_score:
                optimal_paths.append(path)
            continue
        
        state_key = (current.row, current.col, current.direction)
        if state_key in visited and g_scores[current] > g_score:
            continue
        
        visited.add(state_key)
        g_scores[current] = g_score
        
        for next_state, cost in get_next_states(current, grid):
            new_g_score = g_score + cost
            
            if next_state not in g_scores or new_g_score <= g_scores[next_state]:
                g_scores[next_state] = new_g_score
                f_score = new_g_score + manhattan_distance(
                    (next_state.row, next_state.col), 
                    end_pos
                )
                new_path = path + [(next_state.row, next_state.col)]
                heapq.heappush(queue, (f_score, new_g_score, next_state, new_path))
    
    optimal_tiles = set()
    for path in optimal_paths:
        optimal_tiles.update(path)
    
    return optimal_tiles

def part1(input_file: str) -> int:
    grid, start_state, end_pos = parse_input(input_file)
    return find_shortest_path(grid, start_state, end_pos)

def part2(input_file: str) -> int:
    grid, start_state, end_pos = parse_input(input_file)
    optimal_tiles = find_all_optimal_paths(grid, start_state, end_pos)
    return len(optimal_tiles)

def main():
    from unit_tests import run_tests
    
    if run_tests():
        print("\nAll tests passed! Running actual solution...\n")
        result1 = part1('input.txt')
        result2 = part2('input.txt')
        print(f"Part 1: {result1}")
        print(f"Part 2: {result2}")
    else:
        print("\nTests failed! Please fix the issues before running the actual solution.")

if __name__ == '__main__':
    main()
