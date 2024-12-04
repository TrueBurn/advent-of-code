def parse_input(filename):
    grid = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            grid.append(list(line))
    return grid

def in_bounds(grid, row, col):
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])

def has_mas_diagonal(grid, row, col, dx, dy):
    if not in_bounds(grid, row, col) or grid[row][col] != 'A':
        return False

    r1, c1 = row + dx, col + dy
    r2, c2 = row - dx, col - dy

    if not (in_bounds(grid, r1, c1) and in_bounds(grid, r2, c2)):
        return False

    return ((grid[r1][c1] == 'M' and grid[r2][c2] == 'S') or
            (grid[r1][c1] == 'S' and grid[r2][c2] == 'M'))

def count_x_patterns(grid):
    count = 0
    rows, cols = len(grid), len(grid[0])

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] != 'A':
                continue

            if (has_mas_diagonal(grid, row, col, 1, 1) and
                has_mas_diagonal(grid, row, col, 1, -1)):
                count += 1

    return count

def main():
    grid = parse_input('input.txt')
    result = count_x_patterns(grid)
    print(f"Found {result} X-MAS patterns")

if __name__ == "__main__":
    main()
