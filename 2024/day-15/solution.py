from dataclasses import dataclass
from typing import List, Dict, Set
from enum import Enum

class Cell(str, Enum):
    WALL = '#'
    EMPTY = '.'
    ROBOT = '@'
    BOX = 'O'
    BOX_LEFT = '['
    BOX_RIGHT = ']'

class Direction(str, Enum):
    UP = '^'
    RIGHT = '>'
    DOWN = 'v'
    LEFT = '<'

@dataclass(frozen=True)
class Pos:
    row: int
    col: int
    def __add__(self, other):
        return Pos(self.row + other.row, self.col + other.col)

DIRECTIONS = {
    Direction.UP: Pos(-1, 0),
    Direction.RIGHT: Pos(0, 1),
    Direction.DOWN: Pos(1, 0),
    Direction.LEFT: Pos(0, -1)
}

def parse_input(input_file: str) -> tuple[List[List[str]], str, Pos]:
    grid = []
    moves = []
    robot_pos = None
    
    with open(input_file) as f:
        for i, line in enumerate(f.readlines()):
            if line.startswith(Cell.WALL):
                row = list(line.strip())
                if Cell.ROBOT in row:
                    j = row.index(Cell.ROBOT)
                    robot_pos = Pos(i, j)
                    row[j] = Cell.EMPTY
                grid.append(row)
            else:
                moves.append(line.strip())
    
    return grid, ''.join(moves), robot_pos

def scale_map(grid: List[str]) -> List[List[str]]:
    scaled = []
    for row in grid:
        new_row = []
        for cell in row:
            if cell == Cell.WALL:
                new_row.extend([Cell.WALL, Cell.WALL])
            elif cell == Cell.BOX:
                new_row.extend([Cell.BOX_LEFT, Cell.BOX_RIGHT])
            elif cell == Cell.EMPTY:
                new_row.extend([Cell.EMPTY, Cell.EMPTY])
            elif cell == Cell.ROBOT:
                new_row.extend([Cell.ROBOT, Cell.EMPTY])
        scaled.append(new_row)
    return scaled

def simulate_move(grid: List[List[str]], robot_pos: Pos, move: str) -> tuple[List[List[str]], Pos]:
    dest = robot_pos + DIRECTIONS[move]
    
    if grid[dest.row][dest.col] == Cell.EMPTY:
        grid[robot_pos.row][robot_pos.col] = Cell.EMPTY
        grid[dest.row][dest.col] = Cell.ROBOT
        return grid, dest
    elif grid[dest.row][dest.col] == Cell.BOX:
        temp = dest
        while grid[temp.row][temp.col] == Cell.BOX:
            temp = temp + DIRECTIONS[move]
        if grid[temp.row][temp.col] == Cell.EMPTY:
            grid[dest.row][dest.col] = Cell.EMPTY
            grid[temp.row][temp.col] = Cell.BOX
            grid[robot_pos.row][robot_pos.col] = Cell.EMPTY
            grid[dest.row][dest.col] = Cell.ROBOT
            return grid, dest
    
    return grid, robot_pos

def calculate_gps_sum(grid: List[List[str]]) -> int:
    total = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == Cell.BOX:
                total += 100 * i + j
    return total

def part1(input_file: str) -> int:
    grid, moves, robot_pos = parse_input(input_file)
    
    for move in moves:
        grid, robot_pos = simulate_move(grid, robot_pos, move)
    
    return calculate_gps_sum(grid)

def simulate_move_wide(grid: List[List[str]], robot_pos: Pos, move: str) -> tuple[List[List[str]], Pos]:
    dest = robot_pos + DIRECTIONS[move]
    
    if grid[dest.row][dest.col] == Cell.EMPTY:
        grid[robot_pos.row][robot_pos.col] = Cell.EMPTY
        grid[dest.row][dest.col] = Cell.ROBOT
        return grid, dest
    elif grid[dest.row][dest.col] in [Cell.BOX_LEFT, Cell.BOX_RIGHT]:
        q = [dest]
        boxes = {dest}
        while q:
            current = q.pop()
            if grid[current.row][current.col] == Cell.BOX_LEFT:
                next_pos = Pos(current.row, current.col + 1)
            else:
                next_pos = Pos(current.row, current.col - 1)
            if next_pos not in boxes and grid[next_pos.row][next_pos.col] in [Cell.BOX_LEFT, Cell.BOX_RIGHT]:
                q.append(next_pos)
                boxes.add(next_pos)
            next_pos = Pos(current.row + DIRECTIONS[move].row, current.col + DIRECTIONS[move].col)
            if next_pos not in boxes and grid[next_pos.row][next_pos.col] in [Cell.BOX_LEFT, Cell.BOX_RIGHT]:
                q.append(next_pos)
                boxes.add(next_pos)
        
        spaces = set()
        for box in boxes:
            space = Pos(box.row + DIRECTIONS[move].row, box.col + DIRECTIONS[move].col)
            if space not in boxes:
                spaces.add(space)
                if grid[space.row][space.col] == Cell.WALL:
                    return grid, robot_pos
        
        if all(grid[space.row][space.col] == Cell.EMPTY for space in spaces):
            def push_distance(box):
                if move in (Direction.LEFT, Direction.RIGHT):
                    return abs(box.col - dest.col)
                return abs(box.row - dest.row)
            
            for box in sorted(boxes, key=push_distance, reverse=True):
                space = Pos(box.row + DIRECTIONS[move].row, box.col + DIRECTIONS[move].col)
                grid[box.row][box.col], grid[space.row][space.col] = \
                    grid[space.row][space.col], grid[box.row][box.col]
            
            grid[robot_pos.row][robot_pos.col] = Cell.EMPTY
            grid[dest.row][dest.col] = Cell.ROBOT
            return grid, dest
    
    return grid, robot_pos

def calculate_gps_sum_wide(grid: List[List[str]]) -> int:
    total = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == Cell.BOX_LEFT:
                total += 100 * i + j
    return total

def part2(input_file: str) -> int:
    grid, moves, robot_pos = parse_input(input_file)
    grid = scale_map(grid)
    robot_pos = Pos(robot_pos.row, robot_pos.col * 2)
    
    for move in moves:
        grid, robot_pos = simulate_move_wide(grid, robot_pos, move)
    
    return calculate_gps_sum_wide(grid)

def main():
    from unit_tests import run_tests
    
    if run_tests():
        print("\nAll tests passed! Running actual solution...\n")
        result1 = part1('input.txt')
        result2 = part2('input.txt')
        print(f"Part 1: {result1}")
        print(f"Part 2: {result2}")
    else:
        print("\nTests failed! Please fix the issues before running the actual solution.")

if __name__ == '__main__':
    main()
