from typing import List, Tuple
from time import perf_counter

def parse_schematic(schematic: str) -> int:
    n = 0
    for char in schematic:
        if char == '\n':
            continue
        n <<= 1
        if char == '#':
            n |= 1
    return n

def parse_input(input_text: str) -> Tuple[List[int], List[int]]:
    schematics = input_text.strip().split('\n\n')
    locks = []
    keys = []
    
    for schematic in schematics:
        n = parse_schematic(schematic)
        if n >= 0x7C0000000:
            locks.append(n)
        else:
            keys.append(n)
    
    return locks, keys

def can_fit(lock: int, key: int) -> bool:
    return not (lock & key)

def solve(input_text: str, track_performance: bool = False) -> Tuple[int, str]:
    if track_performance:
        start = perf_counter()
    
    locks, keys = parse_input(input_text)
    valid_pairs = sum(1 for lock in locks for key in keys if can_fit(lock, key))
    
    if track_performance:
        end = perf_counter()
        print(f"\nPerformance:")
        print(f"└─ Total: {(end-start):.3f} seconds")
    
    return valid_pairs, "Merry Christmas! 🎄"

def main():
    from unit_tests import run_tests
    
    if run_tests():
        print("\nAll tests passed! Running actual solution...\n")
        with open('input.txt', 'r') as file:
            input_text = file.read()
        part1, part2 = solve(input_text, track_performance=True)
        print(f"Part 1: {part1}")
        print(f"Part 2: {part2}")
    else:
        print("\nTests failed! Please fix the issues before running the actual solution.")

if __name__ == "__main__":
    main()
