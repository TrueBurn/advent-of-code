import re

def parse_input(filename):
    with open(filename, 'r') as f:
        content = f.read()
    return content

def find_valid_multiplications_with_conditions(content):
    # Find all mul, do, and don't instructions with their positions
    mul_pattern = r'mul\((\d{1,3}),(\d{1,3})\)'
    do_pattern = r'do\(\)'
    dont_pattern = r'don\'t\(\)'

    # Find all matches
    mul_matches = [(m.start(), int(m.group(1)), int(m.group(2)))
                  for m in re.finditer(mul_pattern, content)]
    do_positions = [m.start() for m in re.finditer(do_pattern, content)]
    dont_positions = [m.start() for m in re.finditer(dont_pattern, content)]

    # Combine all control instructions (do/don't) with their positions and types
    controls = [(pos, True) for pos in do_positions]  # True for do()
    controls.extend((pos, False) for pos in dont_positions)  # False for don't()
    controls.sort()  # Sort by position

    # Process multiplications based on control state
    multiplications = []
    enabled = True  # Initially enabled

    for mul_pos, num1, num2 in mul_matches:
        # Update enabled state based on any controls before this multiplication
        while controls and controls[0][0] < mul_pos:
            enabled = controls[0][1]  # Set state based on do()/don't()
            controls.pop(0)

        # If multiplications are enabled, add this one to the list
        if enabled:
            multiplications.append((num1, num2))

    return multiplications

def calculate_total(multiplications):
    total = 0
    for num1, num2 in multiplications:
        result = num1 * num2
        total += result
    return total

def main():
    # Read and parse input
    content = parse_input('input.txt')

    # Find valid multiplications considering do/don't instructions
    multiplications = find_valid_multiplications_with_conditions(content)

    # Calculate total
    total = calculate_total(multiplications)

    print(f"Sum of enabled multiplication results: {total}")

if __name__ == "__main__":
    main()
