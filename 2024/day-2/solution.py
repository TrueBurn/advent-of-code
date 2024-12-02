import os

def parse_input(filename):
    sequences = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Convert line of numbers to list of integers
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

def count_safe_sequences(sequences):
    safe_count = 0
    for sequence in sequences:
        if is_safe_sequence(sequence):
            safe_count += 1
    return safe_count

def main():
    sequences = parse_input('input.txt')  # Changed to just input.txt
    safe_count = count_safe_sequences(sequences)
    print(f"Number of safe sequences: {safe_count}")

if __name__ == "__main__":
    main()
