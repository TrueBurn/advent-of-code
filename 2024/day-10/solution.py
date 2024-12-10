import os
import time
from collections import deque

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def parse_input(filename):
    with open(filename, 'r') as f:
        return [list(map(int, line.strip())) for line in f if line.strip()]

def get_neighbors(grid, row, col):
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    neighbors = []

    for dr, dc in moves:
        r, c = row + dr, col + dc
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
            if grid[r][c] == grid[row][col] + 1:
                neighbors.append((r, c))
    return neighbors

def find_reachable_peaks(grid, start_row, start_col):
    peaks = set()
    queue = deque([(start_row, start_col)])
    seen = {(start_row, start_col)}

    while queue:
        row, col = queue.popleft()
        if grid[row][col] == 9:
            peaks.add((row, col))
            continue

        for nr, nc in get_neighbors(grid, row, col):
            if (nr, nc) not in seen:
                seen.add((nr, nc))
                queue.append((nr, nc))

    return len(peaks)

def find_trailheads(grid):
    trailheads = []
    rows, cols = len(grid), len(grid[0])

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                trailheads.append((r, c))

    return trailheads

def find_all_paths(grid, start_row, start_col):
    paths = []
    curr_path = [(start_row, start_col)]

    def dfs(row, col):
        if grid[row][col] == 9:
            paths.append(curr_path[:])
            return

        for nr, nc in get_neighbors(grid, row, col):
            if (nr, nc) not in curr_path:
                curr_path.append((nr, nc))
                dfs(nr, nc)
                curr_path.pop()

    dfs(start_row, start_col)
    return len(paths)

def part_one(grid):
    trailheads = find_trailheads(grid)
    total = len(trailheads)
    processed = 0

    scores = []
    for row, col in trailheads:
        score = find_reachable_peaks(grid, row, col)
        scores.append(score)

        processed += 1
        if processed % 10 == 0:
            clear_console()
            print(f"Progress: {processed}/{total} trailheads processed ({processed/total:.1%})")

    return sum(scores)

def part_two(grid):
    trailheads = find_trailheads(grid)
    total = len(trailheads)
    processed = 0

    ratings = []
    for row, col in trailheads:
        rating = find_all_paths(grid, row, col)
        ratings.append(rating)

        processed += 1
        if processed % 1 == 0:
            clear_console()
            print(f"Progress: {processed}/{total} trailheads processed ({processed/total:.1%})")
            print(f"Current trailhead rating: {rating}")

    return sum(ratings)

def main():
    start_time = time.time()
    grid = parse_input('input.txt')

    print("\n=== Part 1 ===")
    part1_start = time.time()
    result1 = part_one(grid)
    part1_time = time.time() - part1_start

    print("\n=== Part 2 ===")
    part2_start = time.time()
    result2 = part_two(grid)
    part2_time = time.time() - part2_start

    total_time = time.time() - start_time

    clear_console()
    print("=== Final Results ===")
    print(f"Part 1: {result1} (took {part1_time:.2f}s)")
    print(f"Part 2: {result2} (took {part2_time:.2f}s)")
    print(f"\nTotal time: {total_time:.2f}s")

if __name__ == "__main__":
    main()
