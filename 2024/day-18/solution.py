from typing import List, Set, Tuple, Optional
from collections import deque
from tqdm import tqdm

def parse_input(input_file: str) -> List[Tuple[int, int]]:
    corrupted = []
    with open(input_file) as f:
        for line in f:
            if not line.strip():
                continue
            x, y = map(int, line.strip().split(','))
            corrupted.append((x, y))
    return corrupted

def visualize_memory_space(corrupted: Set[Tuple[int, int]], visited: Set[Tuple[int, int]], grid_size: int) -> None:
    grid = [['.' for _ in range(grid_size)] for _ in range(grid_size)]
    for x, y in corrupted:
        grid[y][x] = '#'
    for x, y in visited:
        if grid[y][x] == '.':
            grid[y][x] = 'O'
    for row in grid:
        print(''.join(row))
    print()

def find_shortest_path(corrupted: List[Tuple[int, int]], grid_size: int = 71, debug: bool = False) -> int:
    corrupted_set = set(corrupted)
    start = (0, 0)
    end = (grid_size - 1, grid_size - 1)
    
    if debug:
        print("\nInitial grid:")
        visualize_memory_space(corrupted_set, set(), grid_size)
    
    queue = deque([(start, 0)])
    visited = {start}
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    
    while queue:
        pos, steps = queue.popleft()
        x, y = pos
        
        if debug and steps % 5 == 0:
            print(f"\nAfter {steps} steps:")
            visualize_memory_space(corrupted_set, visited, grid_size)
        
        if pos == end:
            if debug:
                print(f"\nFound path with {steps} steps:")
                visualize_memory_space(corrupted_set, visited, grid_size)
            return steps
        
        for dx, dy in directions:
            new_pos = (x + dx, y + dy)
            new_x, new_y = new_pos
            
            if (0 <= new_x < grid_size and 
                0 <= new_y < grid_size and 
                new_pos not in corrupted_set and 
                new_pos not in visited):
                queue.append((new_pos, steps + 1))
                visited.add(new_pos)
    
    if debug:
        print("\nNo path found!")
        visualize_memory_space(corrupted_set, visited, grid_size)
    return -1

def find_blocking_byte(corrupted: List[Tuple[int, int]], grid_size: int = 71, show_progress: bool = False) -> Optional[Tuple[int, int]]:
    if show_progress:
        pbar = tqdm(total=len(corrupted), desc="Finding blocking byte")
    
    for i, byte in enumerate(corrupted):
        if find_shortest_path(corrupted[:i + 1], grid_size) == -1:
            if show_progress:
                pbar.update(len(corrupted) - i)  # Update remaining progress
                pbar.close()
            return byte
        if show_progress:
            pbar.update(1)
    
    if show_progress:
        pbar.close()
    return None

def solve(corrupted: List[Tuple[int, int]], grid_size: int = 71, show_progress: bool = False) -> Tuple[int, str]:
    if show_progress:
        print("\nSolving Part 1...")
    part1_result = find_shortest_path(corrupted[:1024], grid_size)
    
    if show_progress:
        print("\nSolving Part 2...")
    blocking_byte = find_blocking_byte(corrupted, grid_size, show_progress)
    part2_result = f"{blocking_byte[0]},{blocking_byte[1]}" if blocking_byte else "No blocking byte found"
    
    return part1_result, part2_result

def main() -> None:
    from unit_tests import run_tests
    
    if run_tests():
        print("\nAll tests passed! Running actual solution...\n")
        corrupted = parse_input('input.txt')
        result1, result2 = solve(corrupted, show_progress=True)
        print(f"\nPart 1: {result1}")
        print(f"Part 2: {result2}")
    else:
        print("\nTests failed! Please fix the issues before running the actual solution.")

if __name__ == '__main__':
    main()
