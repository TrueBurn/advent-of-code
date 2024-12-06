def parse_input(filename):
    grid = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            grid.append(list(line))
    return grid

def in_bounds(grid, r, c):
    return 0 <= r < len(grid) and 0 <= c < len(grid[0])

def check_xmas(grid, r, c, dr, dc):
    if not in_bounds(grid, r, c):
        return False

    # Check if we can fit XMAS in this direction
    if not all(in_bounds(grid, r + i*dr, c + i*dc) for i in range(4)):
        return False

    # Check if pattern matches XMAS
    return (grid[r][c] == 'X' and
            grid[r + dr][c + dc] == 'M' and
            grid[r + 2*dr][c + 2*dc] == 'A' and
            grid[r + 3*dr][c + 3*dc] == 'S')

def check_x_mas(grid, r, c):
    # Check if we have an 'A' at center
    if grid[r][c] != 'A':
        return False

    # Check diagonals for MAS (forward or backward)
    diagonals = [
        [(-1, -1), (1, 1)],   # top-left to bottom-right
        [(-1, 1), (1, -1)]    # top-right to bottom-left
    ]

    for d1, d2 in diagonals:
        # Check first diagonal
        has_mas1 = (in_bounds(grid, r + d1[0], c + d1[1]) and
                   in_bounds(grid, r - d1[0], c - d1[1]) and
                   ((grid[r + d1[0]][c + d1[1]] == 'M' and grid[r - d1[0]][c - d1[1]] == 'S') or
                    (grid[r + d1[0]][c + d1[1]] == 'S' and grid[r - d1[0]][c - d1[1]] == 'M')))

        # Check second diagonal
        has_mas2 = (in_bounds(grid, r + d2[0], c + d2[1]) and
                   in_bounds(grid, r - d2[0], c - d2[1]) and
                   ((grid[r + d2[0]][c + d2[1]] == 'M' and grid[r - d2[0]][c - d2[1]] == 'S') or
                    (grid[r + d2[0]][c + d2[1]] == 'S' and grid[r - d2[0]][c - d2[1]] == 'M')))

        if has_mas1 and has_mas2:
            return True

    return False

def part_one(grid):
    count = 0
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # right, down, diagonal-right, diagonal-left

    for r in range(rows):
        for c in range(cols):
            for dr, dc in directions:
                if check_xmas(grid, r, c, dr, dc):
                    count += 1
                # Check backwards
                if check_xmas(grid, r + 3*dr, c + 3*dc, -dr, -dc):
                    count += 1

    return count

def part_two(grid):
    count = 0
    rows, cols = len(grid), len(grid[0])

    for r in range(1, rows-1):  # Skip edges since we need space for MAS
        for c in range(1, cols-1):
            if check_x_mas(grid, r, c):
                count += 1

    return count

def main():
    print("Parsing input...")
    grid = parse_input('input.txt')
    print(f"Grid size: {len(grid)}x{len(grid[0])}")

    print("\nProcessing Part 1...")
    result1 = part_one(grid)

    print("\nProcessing Part 2...")
    result2 = part_two(grid)

    print("\n=== Final Results ===")
    print(f"Part 1: Found {result1} occurrences of XMAS")
    print(f"Part 2: Found {result2} X-MAS patterns")

if __name__ == "__main__":
    main()
