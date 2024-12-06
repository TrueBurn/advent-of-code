import os

def parse_input(filename):
    sequences = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            sequence = list(map(int, line.split()))
            sequences.append(sequence)
    return sequences

def is_safe_sequence(sequence):
    if len(sequence) < 2:
        return False

    increasing = sequence[1] > sequence[0]

    for i in range(1, len(sequence)):
        diff = sequence[i] - sequence[i-1]

        if abs(diff) < 1 or abs(diff) > 3:
            return False

        if increasing and diff < 0:
            return False
        if not increasing and diff > 0:
            return False

    return True

def check_with_dampener(sequence):
    if is_safe_sequence(sequence):
        return True

    for i in range(len(sequence)):
        dampened = sequence[:i] + sequence[i+1:]
        if is_safe_sequence(dampened):
            return True

    return False

def part_one(sequences):
    count = 0
    for sequence in sequences:
        if is_safe_sequence(sequence):
            count += 1
    return count

def part_two(sequences):
    count = 0
    for sequence in sequences:
        if check_with_dampener(sequence):
            count += 1
    return count

def main():
    print("Parsing input...")
    sequences = parse_input('input.txt')

    print("\nProcessing Part 1...")
    result1 = part_one(sequences)

    print("\nProcessing Part 2...")
    result2 = part_two(sequences)

    print("\n=== Final Results ===")
    print(f"Part 1: Found {result1} safe sequences")
    print(f"Part 2: Found {result2} sequences that can be made safe")

if __name__ == "__main__":
    main()
