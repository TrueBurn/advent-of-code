import os
from enum import Enum, auto
from multiprocessing import Pool, cpu_count

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

class Cell(Enum):
    WALL = auto()
    EMPTY = auto()

class Dir(Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)

def parse_input(filename):
    grid = []
    start = None

    with open(filename, 'r') as f:
        for r, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            row = []
            for c, char in enumerate(line):
                if char == "#":
                    row.append(Cell.WALL)
                elif char == "^":
                    row.append(Cell.EMPTY)
                    start = (r, c)
                else:
                    row.append(Cell.EMPTY)
            grid.append(row)

    return grid, start

def in_bounds(grid, r, c):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])

def move(grid, pos, direction):
    if not pos:
        return None, None, True

    r, c = pos
    dr, dc = direction.value
    new_r = r + dr
    new_c = c + dc

    if not in_bounds(grid, new_r, new_c):
        return None, None, True

    if grid[new_r][new_c] == Cell.WALL:
        turns = {
            Dir.UP: Dir.RIGHT,
            Dir.RIGHT: Dir.DOWN,
            Dir.DOWN: Dir.LEFT,
            Dir.LEFT: Dir.UP
        }
        return move(grid, pos, turns[direction])

    return (new_r, new_c), direction, False

def part_one(grid, start):
    visited = set()
    pos = start
    direction = Dir.UP

    while pos:
        visited.add(pos)
        pos, direction, exited = move(grid, pos, direction)
        if exited:
            break

    return len(visited)

def has_loop(grid, start, start_dir):
    slow = start
    slow_dir = start_dir
    fast = start
    fast_dir = start_dir

    steps = 0
    max_steps = len(grid) * len(grid[0]) * 4

    while steps < max_steps:
        slow, slow_dir, exit1 = move(grid, slow, slow_dir)
        if exit1:
            return False

        fast, fast_dir, exit2 = move(grid, fast, fast_dir)
        if exit2:
            return False
        fast, fast_dir, exit3 = move(grid, fast, fast_dir)
        if exit3:
            return False

        if slow == fast and slow_dir == fast_dir:
            return True

        steps += 1

    return False

def test_position(args):
    grid, start, pos = args
    r, c = pos

    if grid[r][c] == Cell.EMPTY and (r, c) != start:
        test_grid = [row[:] for row in grid]
        test_grid[r][c] = Cell.WALL
        if has_loop(test_grid, start, Dir.UP):
            return pos
    return None

def part_two(grid, start):
    empty = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == Cell.EMPTY:
                empty.append((r, c))

    args = [(grid, start, pos) for pos in empty]
    total = len(args)

    print("\nChecking potential positions...")

    with Pool(cpu_count()) as pool:
        results = []
        for i, result in enumerate(pool.imap_unordered(test_position, args)):
            if i % 100 == 0:
                clear_console()
                print(f"Progress - Part 2")
                print(f"Positions checked: {i}/{total} ({i/total:.1%})")
                print(f"Loop positions found: {len([r for r in results if r])}")
            if result:
                results.append(result)

    return len([r for r in results if r])

def main():
    print("Parsing input...")
    grid, start = parse_input('input.txt')
    print(f"Grid size: {len(grid)}x{len(grid[0])}")
    print(f"Starting position: {start}")

    print("\nProcessing Part 1...")
    result1 = part_one(grid, start)

    print("\nProcessing Part 2...")
    result2 = part_two(grid, start)

    # Final results display
    clear_console()
    print("=== Final Results ===")
    print(f"Part 1: Guard visited {result1} distinct positions")
    print(f"Part 2: Found {result2} positions that create loops")

if __name__ == "__main__":
    main()
