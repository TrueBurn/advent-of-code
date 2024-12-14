from typing import List, Tuple, Set
import time
import os
import re
from contextlib import contextmanager
import queue

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def parse_input(input_file: str) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    robots = []
    pattern = r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)'
    
    with open(input_file) as f:
        for line in f:
            x, y, dx, dy = map(int, re.findall(pattern, line)[0])
            robots.append(((x, y), (dx, dy)))
    return robots

def move_robots(robots: List[Tuple[Tuple[int, int], Tuple[int, int]]], 
                width: int, height: int, seconds: int) -> List[Tuple[int, int]]:
    final_positions = []
    
    for (x, y), (dx, dy) in robots:
        final_x = ((x + dx * seconds) % width + width) % width
        final_y = ((y + dy * seconds) % height + height) % height
        final_positions.append((final_x, final_y))
    
    return final_positions

def count_quadrants(positions: List[Tuple[int, int]], width: int, height: int) -> int:
    quadrants = [0] * 4
    mid_x = width // 2
    mid_y = height // 2
    
    for x, y in positions:
        if x == mid_x or y == mid_y:
            continue
        quadrant = (0 if x < mid_x else 1) + (0 if y < mid_y else 2)
        quadrants[quadrant] += 1
    
    result = 1
    for q in quadrants:
        result *= q
    return result

def part1(input_file: str) -> int:
    robots = parse_input(input_file)
    final_positions = move_robots(robots, 101, 103, 100)
    return count_quadrants(final_positions, 101, 103)

def print_grid(positions: List[Tuple[int, int]], width: int, height: int) -> None:
    grid = [['.'] * width for _ in range(height)]
    for x, y in positions:
        grid[y][x] = '#'
    
    for y in range(height):
        print(f"{y:2d} {''.join(grid[y])}")

def find_christmas_tree(positions: List[Tuple[int, int]], width: int, height: int) -> bool:
    grid = [['.'] * width for _ in range(height)]
    for x, y in positions:
        grid[y][x] = '#'
    
    for center_y in range(10, height-20):
        for center_x in range(10, width-20):
            if grid[center_y][center_x] != '#':
                continue
            
            tree_found = True
            tree_height = 11
            
            for y_offset in range(tree_height):
                y = center_y + y_offset
                if y >= height:
                    tree_found = False
                    break
                
                width_at_row = min(1 + y_offset * 2, 11)
                start_x = center_x - width_at_row//2
                end_x = center_x + width_at_row//2 + 1
                
                for x in range(start_x, end_x):
                    if x < 0 or x >= width or grid[y][x] != '#':
                        tree_found = False
                        break
                
                if not tree_found:
                    break
            
            if tree_found:
                return True
    
    return False

def part2(input_file: str) -> int:
    robots = parse_input(input_file)
    width, height = 101, 103
    max_seconds = width * height
    confirmed_patterns = set()
    
    for second in range(0, max_seconds, 5):
        if second % 100 == 0:
            print(f"\rProgress: {second}/{max_seconds} ({second/max_seconds:.1%})", end='', flush=True)
        
        positions = move_robots(robots, width, height, second)
        positions = [(x % width, y % height) for x, y in positions]
        
        if second not in confirmed_patterns and find_christmas_tree(positions, width, height):
            confirmed_patterns.add(second)
            search_start = max(0, second - 4)
            search_end = min(max_seconds, second + 5)
            
            for detail_second in range(search_start, search_end):
                if detail_second == second:
                    continue
                    
                positions = move_robots(robots, width, height, detail_second)
                positions = [(x % width, y % height) for x, y in positions]
                
                if find_christmas_tree(positions, width, height):
                    return detail_second
            
            return second
    
    return -1

def main():
    input_file = "input.txt"
    start_time = time.time()
    
    solve_start = time.time()
    result1 = part1(input_file)
    part1_time = time.time() - solve_start
    
    solve_start = time.time()
    result2 = part2(input_file)
    part2_time = time.time() - solve_start
    
    total_time = time.time() - start_time
    
    clear_console()
    print("=== Final Results ===")
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")
    print(f"\nPart 1 time: {part1_time:.2f}s")
    print(f"Part 2 time: {part2_time:.2f}s")
    print(f"Total time: {total_time:.2f}s")

if __name__ == "__main__":
    main()
