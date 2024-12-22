from collections import defaultdict
from typing import Tuple
from time import perf_counter

def generate_next_secret(n: int) -> int:
    n ^= n * 64
    n %= 16777216

    n ^= n // 32
    n %= 16777216

    n ^= n * 2048
    n %= 16777216

    return n

def solve(input_text: str, track_performance: bool = False) -> Tuple[int, int]:
    data = [int(line) for line in input_text.splitlines()]
    
    if track_performance:
        start = perf_counter()
        
    final_numbers = data.copy()
    for _ in range(2000):
        final_numbers = [generate_next_secret(n) for n in final_numbers]
    part1 = sum(final_numbers)
    
    if track_performance:
        part1_time = perf_counter() - start
        start = perf_counter()
    
    sequences = defaultdict(int)
    for secret in data:
        last = secret % 10
        changes = []
        seen = set()
        
        for _ in range(2000):
            secret = generate_next_secret(secret)
            price = secret % 10
            diff = price - last
            last = price
            changes.append(diff)
            
            if len(changes) >= 4:
                seq = tuple(changes[-4:])
                if seq not in seen:
                    seen.add(seq)
                    sequences[seq] += price
    
    part2 = max(sequences.values())
    
    if track_performance:
        part2_time = perf_counter() - start
        print(f"\nPerformance:")
        print(f"├─ Part 1: {part1_time:.3f} seconds")
        print(f"├─ Part 2: {part2_time:.3f} seconds")
        print(f"└─ Total:  {part1_time + part2_time:.3f} seconds\n")
    
    return part1, part2

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
