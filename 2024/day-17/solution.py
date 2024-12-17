from typing import List, Tuple
import re

def parse_input(input_file: str) -> Tuple[dict[str, int], List[int]]:
    with open(input_file) as f:
        content = f.read()
    
    reg_pattern = r'Register ([ABC]): (\d+)'
    prog_pattern = r'Program: ([\d,]+)'
    
    registers = {k: int(v) for k, v in re.findall(reg_pattern, content)}
    program = [int(x) for x in re.search(prog_pattern, content).group(1).split(',')]
    
    return registers, program

def run_program(program: List[int], a: int, b: int = 0, c: int = 0) -> Tuple[List[int], int, int, int]:
    ip = 0
    output = []
    
    def combo(operand: int) -> int:
        return [0, 1, 2, 3, a, b, c, 99999][operand]
    
    while ip < len(program) - 1:
        opcode, operand = program[ip], program[ip + 1]
        
        match opcode:
            case 0: a = int(a / 2**combo(operand))
            case 1: b ^= operand
            case 2: b = combo(operand) % 8
            case 3: ip = operand - 2 if a else ip
            case 4: b ^= c
            case 5: output.append(combo(operand) % 8)
            case 6: b = int(a / 2**combo(operand))
            case 7: c = int(a / 2**combo(operand))
        
        ip += 2
    
    return output, a, b, c

def self_generate(program: List[int]) -> int:
    target = program[::-1]
    
    def find_a(a: int = 0, depth: int = 0) -> int:
        if depth == len(target):
            return a
        
        for i in range(8):
            next_a = a * 8 + i
            output, _, _, _ = run_program(program, next_a)
            
            if output and output[0] == target[depth]:
                if result := find_a(next_a, depth + 1):
                    return result
        return 0
    
    return find_a()

def part1(registers: dict[str, int], program: List[int]) -> str:
    output, _, _, _ = run_program(
        program,
        registers.get('A', 0),
        registers.get('B', 0),
        registers.get('C', 0)
    )
    return ','.join(map(str, output))

def part2(program: List[int]) -> int:
    result = self_generate(program)
    
    if result != -1:
        output, _, _, _ = run_program(program, result)
        if result < 8:
            output.insert(0, 0)
        if output == program:
            return result
    return -1

def main():
    from unit_tests import run_tests
    
    if run_tests():
        print("\nAll tests passed! Running actual solution...\n")
        registers, program = parse_input('input.txt')
        
        result1 = part1(registers, program)
        print(f"Part 1: {result1}")
        
        result2 = part2(program)
        if result2 != -1:
            print(f"\nPart 2: {result2}")
        else:
            print("\nPart 2: No solution found")
    else:
        print("\nTests failed! Please fix the issues before running the actual solution.")

if __name__ == '__main__':
    main()
