def parse_input(filename):
    equations = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            test_value, numbers = line.split(':')
            test_value = int(test_value)
            numbers = [int(x) for x in numbers.split()]
            equations.append((test_value, numbers))

    return equations

def evaluate_expression(numbers, operators):
    values = [numbers[0]]
    for i, op in enumerate(operators):
        if op == '+':
            values[-1] += numbers[i + 1]
        elif op == '*':
            values[-1] *= numbers[i + 1]
        else:  # op == '||'
            values[-1] = int(str(values[-1]) + str(numbers[i + 1]))
    return values[0]

def can_make_value(test_value, numbers, include_concat=False):
    if len(numbers) == 1:
        return test_value == numbers[0]

    operators_needed = len(numbers) - 1
    possible_ops = ['+', '*', '||'] if include_concat else ['+', '*']
    num_ops = 3 if include_concat else 2

    # Try all possible operator combinations
    for i in range(num_ops ** operators_needed):
        operators = []
        temp = i
        for _ in range(operators_needed):
            operators.append(possible_ops[temp % num_ops])
            temp //= num_ops

        try:
            result = evaluate_expression(numbers, operators)
            if result == test_value:
                return True
        except:
            # Skip combinations that might cause overflow
            continue

    return False

def part_one(equations):
    total = 0
    for test_value, numbers in equations:
        if can_make_value(test_value, numbers, include_concat=False):
            total += test_value
    return total

def part_two(equations):
    total = 0
    for test_value, numbers in equations:
        if can_make_value(test_value, numbers, include_concat=True):
            total += test_value
    return total

def main():
    print("Parsing input...")
    equations = parse_input('input.txt')

    print("\nProcessing Part 1...")
    result1 = part_one(equations)

    print("\nProcessing Part 2...")
    result2 = part_two(equations)

    print("\n=== Final Results ===")
    print(f"Part 1: Sum of valid equation test values (+ and *): {result1}")
    print(f"Part 2: Sum of valid equation test values (including ||): {result2}")

if __name__ == "__main__":
    main()
