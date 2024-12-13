from typing import List, Tuple
import time
import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def parse_input(file_path: str) -> List[Tuple[int, int, int, int, int, int]]:
    machines = []
    with open(file_path) as f:
        lines = f.read().strip().split('\n\n')
        for machine in lines:
            lines = machine.split('\n')
            a_x = int(lines[0].split('X+')[1].split(',')[0])
            a_y = int(lines[0].split('Y+')[1])
            b_x = int(lines[1].split('X+')[1].split(',')[0])
            b_y = int(lines[1].split('Y+')[1])
            prize_x = int(lines[2].split('X=')[1].split(',')[0])
            prize_y = int(lines[2].split('Y=')[1])
            machines.append((a_x, a_y, b_x, b_y, prize_x, prize_y))
    return machines

def find_min_tokens(a_x: int, a_y: int, b_x: int, b_y: int, prize_x: int, prize_y: int, max_presses: int = 100) -> int:
    det = a_x * b_y - a_y * b_x
    if det == 0:
        return -1
        
    a = (prize_x * b_y - prize_y * b_x) / det
    b = (a_x * prize_y - a_y * prize_x) / det
    
    if a < 0 or b < 0 or not a.is_integer() or not b.is_integer() or a > max_presses or b > max_presses:
        return -1
        
    return int(3 * a + b)

def solve_part1(machines: List[Tuple[int, int, int, int, int, int]]) -> int:
    total_tokens = 0
    total_machines = len(machines)
    processed = 0
    
    for machine in machines:
        tokens = find_min_tokens(*machine)
        if tokens != -1:
            total_tokens += tokens
            
        processed += 1
        if processed % 10 == 0:
            clear_console()
            print("Part 1")
            print(f"Progress: {processed}/{total_machines} machines processed ({processed/total_machines:.1%})")
    
    return total_tokens

def solve_part2(machines: List[Tuple[int, int, int, int, int, int]]) -> int:
    offset = 10000000000000
    total_tokens = 0
    total_machines = len(machines)
    processed = 0
    
    for a_x, a_y, b_x, b_y, prize_x, prize_y in machines:
        tokens = find_min_tokens(a_x, a_y, b_x, b_y, prize_x + offset, prize_y + offset, float('inf'))
        if tokens != -1:
            total_tokens += tokens
            
        processed += 1
        if processed % 10 == 0:
            clear_console()
            print("Part 2")
            print(f"Progress: {processed}/{total_machines} machines processed ({processed/total_machines:.1%})")
    
    return total_tokens

def main():
    start_time = time.time()
    machines = parse_input('input.txt')
    
    solve_start = time.time()
    result1 = solve_part1(machines)
    part1_time = time.time() - solve_start
    
    solve_start = time.time()
    result2 = solve_part2(machines)
    part2_time = time.time() - solve_start
    
    total_time = time.time() - start_time
    
    clear_console()
    print("=== Final Results ===")
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")
    print(f"\nPart 1 time: {part1_time:.2f}s")
    print(f"Part 2 time: {part2_time:.2f}s")
    print(f"Total time: {total_time:.2f}s")

if __name__ == "__main__":
    main()
