from pathlib import Path
from collections import deque
from functools import lru_cache
from typing import List, Tuple, Set

def get_keypad_grids():
    KEYPAD = [
        ["7", "8", "9"],
        ["4", "5", "6"],
        ["1", "2", "3"],
        [" ", "0", "A"]
    ]
    
    DPAD = [
        [" ", "^", "A"],
        ["<", "v", ">"]
    ]
    
    return KEYPAD, DPAD

def find_position(grid: List[List[str]], value: str) -> Tuple[int, int]:
    for row_idx, row in enumerate(grid):
        if value in row:
            return (row.index(value), row_idx)
    return None

@lru_cache(maxsize=None)
def get_paths(start: str, end: str, grid_type: str) -> List[str]:
    KEYPAD, DPAD = get_keypad_grids()
    grid = KEYPAD if grid_type == "KEYPAD" else DPAD
    height, width = len(grid), len(grid[0])
    
    DIRECTIONS = {(0, 1): "v", (0, -1): "^", (1, 0): ">", (-1, 0): "<"}
    
    start_pos = find_position(grid, start)
    end_pos = find_position(grid, end)
    blank_pos = find_position(grid, " ")
    
    seen = {start_pos, blank_pos}
    queue = deque([(start_pos, [])])
    paths = []
    min_distance = float("inf")
    distance = 0
    
    while queue and distance <= min_distance:
        pos, path = queue.popleft()
        distance = len(path)
        
        if pos == end_pos:
            min_distance = distance
            paths.append("".join(path) + "A")
            continue
            
        for (dx, dy), direction in DIRECTIONS.items():
            new_x, new_y = pos[0] + dx, pos[1] + dy
            new_pos = (new_x, new_y)
            
            if (0 <= new_x < width and 
                0 <= new_y < height and 
                new_pos not in seen):
                queue.append((new_pos, path + [direction]))
        seen.add(pos)  # Add current position after checking neighbors
    
    return paths

@lru_cache(maxsize=None)
def min_length_dpad(sequence: str, depth: int) -> int:
    if depth == 0:
        return len(sequence)
    
    total = 0
    current = "A"
    
    for target in sequence:
        paths = get_paths(current, target, "DPAD")
        min_len = min(min_length_dpad(path, depth - 1) for path in paths)
        total += min_len
        current = target
    
    return total

def find_complexity(sequence: str, depth: int) -> int:
    current = "A"
    total = 0
    
    for target in sequence:
        paths = get_paths(current, target, "KEYPAD")
        min_len = min(min_length_dpad(path, depth) for path in paths)
        total += min_len
        current = target
    
    return total * int(sequence[:-1])

def parse_input(file_path: str) -> List[str]:
    with open(file_path) as f:
        return f.read().splitlines()

def solve(data: List[str], depth: int = 2) -> int:
    return sum(find_complexity(sequence, depth) for sequence in data)

def main():
    from unit_tests import run_tests
    
    if run_tests():
        print("\nAll tests passed! Running actual solution...\n")
        data = parse_input("input.txt")
        part1 = solve(data, depth=2)
        part2 = solve(data, depth=25)
        print(f"Part 1: {part1}")
        print(f"Part 2: {part2}")
    else:
        print("\nTests failed! Please fix the issues before running the actual solution.")

if __name__ == "__main__":
    main()
