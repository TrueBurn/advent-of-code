"""
Input parsing utilities for common AoC patterns.

Common patterns from AoC 2024: All days
"""

import re
from typing import Any, Callable, List, Optional, Tuple


def parse_grid(filename: str, converter: Callable[[str], Any] = str) -> List[List[Any]]:
    """
    Parse file into 2D grid.

    Args:
        filename: Path to input file
        converter: Function to convert each character (default: str)

    Returns:
        2D list representing the grid

    Examples:
        # Character grid
        grid = parse_grid('input.txt')

        # Integer grid
        grid = parse_grid('input.txt', int)

        # Custom converter
        grid = parse_grid('input.txt', lambda c: c == '#')
    """
    with open(filename) as f:
        lines = [line.strip() for line in f if line.strip()]

    if converter == str:
        return [list(line) for line in lines]
    else:
        return [[converter(char) for char in line] for line in lines]


def parse_sections(filename: str) -> List[str]:
    """
    Parse file split by blank lines into sections.

    Args:
        filename: Path to input file

    Returns:
        List of section strings

    Example:
        sections = parse_sections('input.txt')
        for section in sections:
            process(section)
    """
    with open(filename) as f:
        content = f.read().strip()
    return content.split("\n\n")


def parse_ints(line: str, signed: bool = True) -> List[int]:
    """
    Extract all integers from a string.

    Args:
        line: Input string
        signed: Include negative numbers if True

    Returns:
        List of integers found in the string

    Example:
        # "Position: x=10, y=-5, z=20"
        coords = parse_ints(line, signed=True)  # [10, -5, 20]
    """
    pattern = r"-?\d+" if signed else r"\d+"
    return [int(x) for x in re.findall(pattern, line)]


def parse_coords(line: str, pattern: Optional[str] = None) -> Tuple[int, ...]:
    """
    Parse coordinates from a line using regex.

    Args:
        line: Input line
        pattern: Optional custom regex pattern (must have capture groups)

    Returns:
        Tuple of integers

    Examples:
        # "p=10,20 v=-3,5"
        pattern = r'p=(-?\\d+),(-?\\d+) v=(-?\\d+),(-?\\d+)'
        px, py, vx, vy = parse_coords(line, pattern)

        # "x=10, y=20"
        x, y = parse_coords(line)  # Uses default pattern for x=X, y=Y
    """
    if pattern is None:
        pattern = r"x=(-?\d+),?\s*y=(-?\d+)"

    match = re.search(pattern, line)
    if match:
        return tuple(int(x) for x in match.groups())
    return tuple()


def parse_lines(filename: str, strip: bool = True, skip_empty: bool = True) -> List[str]:
    """
    Parse file into list of lines.

    Args:
        filename: Path to input file
        strip: Strip whitespace from each line
        skip_empty: Skip empty lines

    Returns:
        List of lines

    Example:
        lines = parse_lines('input.txt')
        for line in lines:
            process(line)
    """
    with open(filename) as f:
        lines = f.readlines()

    if strip:
        lines = [line.strip() for line in lines]

    if skip_empty:
        lines = [line for line in lines if line]

    return lines


def parse_blocks(filename: str) -> List[List[str]]:
    """
    Parse file into list of blocks (separated by blank lines).

    Args:
        filename: Path to input file

    Returns:
        List of blocks, where each block is a list of lines

    Example:
        blocks = parse_blocks('input.txt')
        for block in blocks:
            for line in block:
                process(line)
    """
    sections = parse_sections(filename)
    return [section.split("\n") for section in sections]


def parse_graph(filename: str, directed: bool = False, separator: str = "-") -> dict:
    """
    Parse file into adjacency list graph.

    Args:
        filename: Path to input file
        directed: Create directed graph if True
        separator: Character(s) separating nodes in each line

    Returns:
        Dictionary mapping nodes to lists of neighbors

    Example:
        # Input: "A-B\nB-C\nA-C"
        graph = parse_graph('input.txt')
        # {'A': ['B', 'C'], 'B': ['A', 'C'], 'C': ['B', 'A']}
    """
    from collections import defaultdict

    graph = defaultdict(list)
    lines = parse_lines(filename)

    for line in lines:
        parts = line.split(separator)
        if len(parts) == 2:
            a, b = parts[0].strip(), parts[1].strip()
            graph[a].append(b)
            if not directed:
                graph[b].append(a)

    return dict(graph)


def parse_key_value(filename: str, separator: str = ":") -> dict:
    """
    Parse file with key-value pairs.

    Args:
        filename: Path to input file
        separator: Character(s) separating key from value

    Returns:
        Dictionary of key-value pairs

    Example:
        # Input: "name: John\nage: 30"
        data = parse_key_value('input.txt')
        # {'name': 'John', 'age': '30'}
    """
    data = {}
    lines = parse_lines(filename)

    for line in lines:
        if separator in line:
            key, value = line.split(separator, 1)
            data[key.strip()] = value.strip()

    return data


def parse_csv(filename: str, delimiter: str = ",", skip_header: bool = False) -> List[List[str]]:
    """
    Parse CSV-like file.

    Args:
        filename: Path to input file
        delimiter: Field delimiter
        skip_header: Skip first line if True

    Returns:
        List of rows, where each row is a list of fields

    Example:
        rows = parse_csv('input.txt', delimiter=',', skip_header=True)
        for row in rows:
            process(row)
    """
    lines = parse_lines(filename)

    if skip_header and lines:
        lines = lines[1:]

    return [line.split(delimiter) for line in lines]
