from collections import deque
from typing import List, Tuple, Dict
from tqdm import tqdm

def parse_input(input_text: str) -> Tuple[List[List[str]], Tuple[int, int], Tuple[int, int]]:
    grid = [list(line) for line in input_text.strip().split('\n')]
    start = end = None
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 'S':
                start = (i, j)
                grid[i][j] = '.'
            elif grid[i][j] == 'E':
                end = (i, j)
                grid[i][j] = '.'
    
    return grid, start, end

def precompute_distances(grid: List[List[str]], target: Tuple[int, int]) -> Dict[Tuple[int, int], int]:
    rows, cols = len(grid), len(grid[0])
    distances = {}
    queue = deque([(target, 0)])
    visited = {target}
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    while queue:
        pos, dist = queue.popleft()
        distances[pos] = dist
        
        for dr, dc in directions:
            new_pos = (pos[0] + dr, pos[1] + dc)
            if (0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols and 
                grid[new_pos[0]][new_pos[1]] == '.' and 
                new_pos not in visited):
                visited.add(new_pos)
                queue.append((new_pos, dist + 1))
    
    return distances

def find_cheats(grid: List[List[str]], start: Tuple[int, int], end: Tuple[int, int], max_cheat_time: int = 2, show_progress: bool = False) -> List[Tuple[Tuple[int, int], Tuple[int, int], int]]:
    rows, cols = len(grid), len(grid[0])
    distances_to_end = precompute_distances(grid, end)
    distances_from_start = precompute_distances(grid, start)
    
    if start not in distances_to_end:
        return []
        
    normal_time = distances_to_end[start]
    cheats = []
    valid_positions = {(i, j) for i in range(rows) for j in range(cols) if grid[i][j] == '.'}
    
    items = distances_from_start.items()
    if show_progress:
        items = tqdm(items)
    
    for start_pos, time_to_pos in items:
        for i in range(max(0, start_pos[0] - max_cheat_time), min(rows, start_pos[0] + max_cheat_time + 1)):
            for j in range(max(0, start_pos[1] - max_cheat_time), min(cols, start_pos[1] + max_cheat_time + 1)):
                end_pos = (i, j)
                if end_pos not in valid_positions or end_pos == start_pos:
                    continue
                
                cheat_length = abs(end_pos[0] - start_pos[0]) + abs(end_pos[1] - start_pos[1])
                if cheat_length > max_cheat_time:
                    continue
                
                if end_pos in distances_to_end:
                    total_time = time_to_pos + cheat_length + distances_to_end[end_pos]
                    time_saved = normal_time - total_time
                    if time_saved > 0:
                        cheats.append((start_pos, end_pos, time_saved))
    
    return cheats

def solve(input_text: str, show_progress: bool = False) -> Tuple[int, int]:
    grid, start, end = parse_input(input_text)
    
    cheats1 = find_cheats(grid, start, end, max_cheat_time=2, show_progress=show_progress)
    part1 = sum(1 for _, _, time_saved in cheats1 if time_saved >= 100)
    
    cheats2 = find_cheats(grid, start, end, max_cheat_time=20, show_progress=show_progress)
    part2 = sum(1 for _, _, time_saved in cheats2 if time_saved >= 100)
    
    return part1, part2

def main():
    from unit_tests import run_tests
    
    if run_tests():
        print("\nAll tests passed! Running actual solution...\n")
        with open('input.txt', 'r') as file:
            input_text = file.read()
        part1, part2 = solve(input_text, show_progress=True)
        print(f"Part 1: {part1}")
        print(f"Part 2: {part2}")
    else:
        print("\nTests failed! Please fix the issues before running the actual solution.")

if __name__ == '__main__':
    main()
