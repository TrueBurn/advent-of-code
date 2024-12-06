import re

def parse_input(filename):
    with open(filename, 'r') as f:
        content = f.read()
    return content

def find_multiplications(content, check_enabled=False):
    mul_pattern = r'mul\((\d{1,3}),(\d{1,3})\)'
    do_pattern = r'do\(\)'
    dont_pattern = r'don\'t\(\)'

    # Find all matches with positions
    muls = [(m.start(), int(m.group(1)), int(m.group(2)))
            for m in re.finditer(mul_pattern, content)]

    if not check_enabled:
        return [(n1, n2) for _, n1, n2 in muls]

    # Get control instructions
    dos = [m.start() for m in re.finditer(do_pattern, content)]
    donts = [m.start() for m in re.finditer(dont_pattern, content)]

    # Combine control instructions
    controls = [(pos, True) for pos in dos]
    controls.extend((pos, False) for pos in donts)
    controls.sort()

    # Process multiplications
    results = []
    enabled = True  # Start enabled
    for pos, num1, num2 in muls:
        # Update enabled state based on controls
        while controls and controls[0][0] < pos:
            enabled = controls[0][1]
            controls.pop(0)

        if enabled:
            results.append((num1, num2))

    return results

def part_one(content):
    muls = find_multiplications(content, check_enabled=False)
    return sum(x * y for x, y in muls)

def part_two(content):
    muls = find_multiplications(content, check_enabled=True)
    return sum(x * y for x, y in muls)

def main():
    print("Parsing input...")
    content = parse_input('input.txt')

    print("\nProcessing Part 1...")
    result1 = part_one(content)

    print("\nProcessing Part 2...")
    result2 = part_two(content)

    print("\n=== Final Results ===")
    print(f"Part 1: Sum of all multiplication results: {result1}")
    print(f"Part 2: Sum of enabled multiplication results: {result2}")

if __name__ == "__main__":
    main()
