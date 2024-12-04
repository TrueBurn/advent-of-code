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

def has_xmas(grid, row, col, dx, dy):
    if not in_bounds(grid, row, col):
        return False

    if not (in_bounds(grid, row + 3*dx, col + 3*dy)):
        return False

    return (grid[row][col] == 'X' and
            grid[row + dx][col + dy] == 'M' and
            grid[row + 2*dx][col + 2*dy] == 'A' and
            grid[row + 3*dx][col + 3*dy] == 'S')

def count_xmas_patterns(grid):
    count = 0
    rows, cols = len(grid), len(grid[0])
    directions = [(0, 1), (1, 1), (1, 0), (1, -1),
                 (0, -1), (-1, -1), (-1, 0), (-1, 1)]

    for row in range(rows):
        for col in range(cols):
            for dx, dy in directions:
                if has_xmas(grid, row, col, dx, dy):
                    count += 1

    return count

def main():
    grid = parse_input('input.txt')
    result = count_xmas_patterns(grid)
    print(f"Found {result} occurrences of XMAS")

if __name__ == "__main__":
    main()
