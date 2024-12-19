from typing import List, Tuple, Dict
from dataclasses import dataclass

@dataclass(frozen=True)
class TowelPattern:
    stripes: str
    
    def __len__(self) -> int:
        return len(self.stripes)

def parse_input(input_file: str) -> Tuple[List[TowelPattern], List[str]]:
    patterns = []
    designs = []
    parsing_patterns = True
    
    with open(input_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                parsing_patterns = False
                continue
            
            if parsing_patterns:
                patterns.extend(TowelPattern(p.strip()) for p in line.split(','))
            else:
                designs.append(line)
    
    return patterns, designs

def count_ways_to_make_design(design: str, patterns: List[TowelPattern], start_pos: int = 0, memo: Dict[int, int] = None) -> int:
    if memo is None:
        memo = {}
    
    if start_pos == len(design):
        return 1
    
    if start_pos in memo:
        return memo[start_pos]
    
    total_ways = sum(
        count_ways_to_make_design(design, patterns, start_pos + len(pattern), memo)
        for pattern in patterns
        if (start_pos + len(pattern) <= len(design) and 
            design[start_pos:start_pos + len(pattern)] == pattern.stripes)
    )
    
    memo[start_pos] = total_ways
    return total_ways

def can_make_design(design: str, patterns: List[TowelPattern], start_pos: int = 0, memo: Dict[int, bool] = None) -> bool:
    if memo is None:
        memo = {}
    
    if start_pos == len(design):
        return True
    
    if start_pos in memo:
        return memo[start_pos]
    
    memo[start_pos] = any(
        can_make_design(design, patterns, start_pos + len(pattern), memo)
        for pattern in patterns
        if (start_pos + len(pattern) <= len(design) and 
            design[start_pos:start_pos + len(pattern)] == pattern.stripes)
    )
    return memo[start_pos]

def solve(input_file: str) -> Tuple[int, int]:
    patterns, designs = parse_input(input_file)
    
    possible_count = sum(1 for design in designs if can_make_design(design, patterns))
    total_ways = sum(
        count_ways_to_make_design(design, patterns)
        for design in designs
        if can_make_design(design, patterns)
    )
    
    return possible_count, total_ways

def main() -> None:
    from unit_tests import run_tests
    
    if run_tests():
        print("\nAll tests passed! Running actual solution...\n")
        result1, result2 = solve('input.txt')
        print(f"Part 1: {result1}")
        print(f"Part 2: {result2}")
    else:
        print("\nTests failed! Please fix the issues before running the actual solution.")

if __name__ == '__main__':
    main()
