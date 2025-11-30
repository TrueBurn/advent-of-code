"""
Grid utilities for 2D grid-based problems.

Common patterns from AoC 2024: Days 4, 6, 8, 10, 12, 15, 16, 18, 20
"""

from enum import Enum
from typing import Callable, List, Optional, Tuple


class Direction(Enum):
    """Cardinal and diagonal directions."""

    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)
    UP_RIGHT = (-1, 1)
    UP_LEFT = (-1, -1)
    DOWN_RIGHT = (1, 1)
    DOWN_LEFT = (1, -1)

    def turn_right(self) -> "Direction":
        """Turn 90 degrees clockwise (cardinal directions only)."""
        turns = {
            Direction.UP: Direction.RIGHT,
            Direction.RIGHT: Direction.DOWN,
            Direction.DOWN: Direction.LEFT,
            Direction.LEFT: Direction.UP,
        }
        return turns[self]

    def turn_left(self) -> "Direction":
        """Turn 90 degrees counter-clockwise (cardinal directions only)."""
        turns = {
            Direction.UP: Direction.LEFT,
            Direction.LEFT: Direction.DOWN,
            Direction.DOWN: Direction.RIGHT,
            Direction.RIGHT: Direction.UP,
        }
        return turns[self]

    def reverse(self) -> "Direction":
        """Get opposite direction."""
        reverses = {
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.LEFT: Direction.RIGHT,
            Direction.RIGHT: Direction.LEFT,
            Direction.UP_RIGHT: Direction.DOWN_LEFT,
            Direction.DOWN_LEFT: Direction.UP_RIGHT,
            Direction.UP_LEFT: Direction.DOWN_RIGHT,
            Direction.DOWN_RIGHT: Direction.UP_LEFT,
        }
        return reverses[self]


# Common direction sets
CARDINAL_DIRS = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
ALL_DIRS = list(Direction)


def in_bounds(grid: List[List], row: int, col: int) -> bool:
    """
    Check if position is within grid bounds.

    Args:
        grid: 2D list representing the grid
        row: Row index
        col: Column index

    Returns:
        True if position is valid, False otherwise
    """
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def get_neighbors(
    row: int, col: int, grid: List[List], diagonal: bool = False
) -> List[Tuple[int, int]]:
    """
    Get valid neighboring positions.

    Args:
        row: Current row
        col: Current column
        grid: 2D list representing the grid
        diagonal: Include diagonal neighbors if True

    Returns:
        List of (row, col) tuples for valid neighbors
    """
    directions = ALL_DIRS if diagonal else CARDINAL_DIRS
    neighbors = []

    for direction in directions:
        dr, dc = direction.value
        new_row, new_col = row + dr, col + dc
        if in_bounds(grid, new_row, new_col):
            neighbors.append((new_row, new_col))

    return neighbors


def manhattan_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
    """
    Calculate Manhattan distance between two positions.

    Args:
        pos1: First position (row, col)
        pos2: Second position (row, col)

    Returns:
        Manhattan distance
    """
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


class Grid:
    """
    Grid wrapper with common operations.

    Example usage:
        grid = Grid.from_file('input.txt')
        start = grid.find('@')
        neighbors = grid.get_neighbors(start)
    """

    def __init__(self, data: List[List[str]]):
        """
        Initialize grid.

        Args:
            data: 2D list of characters
        """
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if data else 0

    @classmethod
    def from_file(cls, filename: str) -> "Grid":
        """
        Create grid from file.

        Args:
            filename: Path to input file

        Returns:
            Grid instance
        """
        with open(filename) as f:
            data = [list(line.strip()) for line in f if line.strip()]
        return cls(data)

    @classmethod
    def from_lines(cls, lines: List[str]) -> "Grid":
        """
        Create grid from list of strings.

        Args:
            lines: List of strings

        Returns:
            Grid instance
        """
        return cls([list(line) for line in lines])

    def in_bounds(self, row: int, col: int) -> bool:
        """Check if position is within bounds."""
        return 0 <= row < self.rows and 0 <= col < self.cols

    def get(self, row: int, col: int, default: Optional[str] = None) -> Optional[str]:
        """
        Get value at position with optional default.

        Args:
            row: Row index
            col: Column index
            default: Default value if out of bounds

        Returns:
            Character at position or default
        """
        if self.in_bounds(row, col):
            return self.data[row][col]
        return default

    def set(self, row: int, col: int, value: str) -> None:
        """Set value at position."""
        if self.in_bounds(row, col):
            self.data[row][col] = value

    def find(self, char: str) -> Optional[Tuple[int, int]]:
        """
        Find first occurrence of character.

        Args:
            char: Character to find

        Returns:
            (row, col) tuple or None if not found
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.data[row][col] == char:
                    return (row, col)
        return None

    def find_all(self, char: str) -> List[Tuple[int, int]]:
        """
        Find all occurrences of character.

        Args:
            char: Character to find

        Returns:
            List of (row, col) tuples
        """
        positions = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.data[row][col] == char:
                    positions.append((row, col))
        return positions

    def get_neighbors(
        self, row: int, col: int, diagonal: bool = False, condition: Optional[Callable] = None
    ) -> List[Tuple[int, int]]:
        """
        Get neighboring positions.

        Args:
            row: Current row
            col: Current column
            diagonal: Include diagonal neighbors
            condition: Optional function to filter neighbors

        Returns:
            List of (row, col) tuples
        """
        neighbors = get_neighbors(row, col, self.data, diagonal)
        if condition:
            neighbors = [n for n in neighbors if condition(self.get(*n))]
        return neighbors

    def print(self) -> None:
        """Print grid to console."""
        for row in self.data:
            print("".join(row))

    def copy(self) -> "Grid":
        """Create a deep copy of the grid."""
        return Grid([row[:] for row in self.data])

    def __getitem__(self, key: Tuple[int, int]) -> str:
        """Allow grid[row, col] syntax."""
        row, col = key
        return self.data[row][col]

    def __setitem__(self, key: Tuple[int, int], value: str) -> None:
        """Allow grid[row, col] = value syntax."""
        row, col = key
        self.data[row][col] = value

    def __str__(self) -> str:
        """String representation."""
        return "\n".join("".join(row) for row in self.data)
