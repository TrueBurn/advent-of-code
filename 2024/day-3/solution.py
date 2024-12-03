import re

def parse_input(filename):
    with open(filename, 'r') as f:
        content = f.read()
    return content

def find_valid_multiplications(content):
    # Regular expression to find mul(X,Y) patterns
    # Matches: mul(digits,digits) where digits are 1-3 characters long
    pattern = r'mul\((\d{1,3}),(\d{1,3})\)'

    # Find all matches in the content
    matches = re.finditer(pattern, content)

    multiplications = []
    for match in matches:
        # Extract the two numbers
        num1 = int(match.group(1))
        num2 = int(match.group(2))
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

    # Find all valid multiplications
    multiplications = find_valid_multiplications(content)

    # Calculate total
    total = calculate_total(multiplications)

    print(f"Sum of all multiplication results: {total}")

if __name__ == "__main__":
    main()
