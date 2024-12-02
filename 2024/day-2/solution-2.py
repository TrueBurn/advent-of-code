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

    # Check first two numbers to determine if sequence should be increasing or decreasing
    increasing = sequence[1] > sequence[0]

    for i in range(1, len(sequence)):
        diff = sequence[i] - sequence[i-1]

        # Check if difference is between 1 and 3 (inclusive)
        if abs(diff) < 1 or abs(diff) > 3:
            return False

        # Check if sequence maintains increasing/decreasing pattern
        if increasing and diff < 0:
            return False
        if not increasing and diff > 0:
            return False

    return True

def is_safe_with_dampener(sequence):
    # First check if it's already safe without removing any number
    if is_safe_sequence(sequence):
        return True

    # Try removing each number one at a time
    for i in range(len(sequence)):
        # Create new sequence without the current number
        dampened_sequence = sequence[:i] + sequence[i+1:]
        if is_safe_sequence(dampened_sequence):
            return True

    return False

def count_safe_sequences_with_dampener(sequences):
    safe_count = 0
    for sequence in sequences:
        if is_safe_with_dampener(sequence):
            safe_count += 1
    return safe_count

def main():
    sequences = parse_input('input.txt')
    safe_count = count_safe_sequences_with_dampener(sequences)
    print(f"Number of safe sequences with Problem Dampener: {safe_count}")

if __name__ == "__main__":
    main()
