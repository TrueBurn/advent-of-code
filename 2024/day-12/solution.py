from typing import List, Set, Tuple
import time
import os
from collections import defaultdict

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_regions(grid: List[str], plant: str) -> List[Set[Tuple[int, int]]]:
    max_row, max_col = len(grid), len(grid[0])
    visited = set()
    regions = []
    
    for row in range(max_row):
        for col in range(max_col):
            if grid[row][col] == plant and (row, col) not in visited:
                region = set()
                stack = [(row, col)]
                
                while stack:
                    r, c = stack.pop()
                    if (r, c) in visited:
                        continue
                        
                    visited.add((r, c))
                    if grid[r][c] == plant:
                        region.add((r, c))
                        for dr, dc in [(0,1), (1,0), (-1,0), (0,-1)]:
                            nr, nc = r + dr, c + dc
                            if 0 <= nr < max_row and 0 <= nc < max_col:
                                stack.append((nr, nc))
                
                if region:
                    regions.append(region)
    
    return regions

def get_perimeter_and_sides(region: Set[Tuple[int, int]], max_row: int, max_col: int) -> Tuple[int, int]:
    perimeter = 0
    up, down, left, right = [], [], [], []
    
    for row, col in region:
        for dr, dc in [(0,1), (1,0), (-1,0), (0,-1)]:
            nr, nc = row + dr, col + dc
            if nr < 0 or nr >= max_row or nc < 0 or nc >= max_col or (nr, nc) not in region:
                perimeter += 1
                if dr == -1:
                    right.append((nc, nr))
                elif dr == 1:
                    left.append((nc, nr))
                elif dc == -1:
                    up.append((nr, nc))
                elif dc == 1:
                    down.append((nr, nc))
    
    sides = 0
    for points in [up, down, left, right]:
        if not points:
            continue
        points.sort()
        by_col = defaultdict(list)
        for r, c in points:
            by_col[c].append(r)
            
        for col_points in by_col.values():
            col_points.sort()
            sides += 1
            for i in range(len(col_points)-1):
                if abs(col_points[i] - col_points[i+1]) > 1:
                    sides += 1
    
    return perimeter, sides

def solve(grid: List[str]) -> Tuple[int, int]:
    max_row, max_col = len(grid), len(grid[0])
    total_cells = max_row * max_col
    processed = 0
    price1 = price2 = 0
    
    unique_plants = set(c for row in grid for c in row)
    for plant in unique_plants:
        regions = get_regions(grid, plant)
        for region in regions:
            perimeter, sides = get_perimeter_and_sides(region, max_row, max_col)
            area = len(region)
            price1 += area * perimeter
            price2 += area * sides
            
            processed += len(region)
            if processed % 1000 == 0:
                clear_console()
                print(f"Progress: {processed}/{total_cells} cells processed ({processed/total_cells:.1%})")
    
    return price1, price2

def parse_input(file_path: str) -> List[str]:
    with open(file_path) as f:
        return f.read().strip().split('\n')

def main():
    start_time = time.time()
    grid = parse_input('input.txt')
    
    solve_start = time.time()
    result1, result2 = solve(grid)
    solve_time = time.time() - solve_start
    total_time = time.time() - start_time
    
    clear_console()
    print("=== Final Results ===")
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")
    print(f"\nSolve time: {solve_time:.2f}s")
    print(f"Total time: {total_time:.2f}s")

if __name__ == "__main__":
    main()
