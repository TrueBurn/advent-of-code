def parse_input(filename):
    rules = []
    sequences = []
    is_rules = True

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                is_rules = False
                continue

            if is_rules:
                before, after = line.split('|')
                rules.append((int(before), int(after)))
            else:
                nums = [int(x) for x in line.split(',')]
                sequences.append(nums)

    return rules, sequences

def check_order(sequence, rules):
    for before, after in rules:
        if before in sequence and after in sequence:
            if sequence.index(before) > sequence.index(after):
                return False
    return True

def get_middle(sequence):
    return sequence[len(sequence) // 2]

def part_one(rules, sequences):
    total = 0
    for sequence in sequences:
        if check_order(sequence, rules):
            total += get_middle(sequence)
    return total

def order_sequence(sequence, rules):
    nums = sequence.copy()
    size = len(nums)

    for i in range(size):
        for j in range(size - i - 1):
            for before, after in rules:
                if nums[j] == after and nums[j+1] == before:
                    nums[j], nums[j+1] = nums[j+1], nums[j]
    return nums

def part_two(rules, sequences):
    total = 0
    for sequence in sequences:
        if not check_order(sequence, rules):
            ordered = order_sequence(sequence, rules)
            total += get_middle(ordered)
    return total

def main():
    print("Parsing input...")
    rules, sequences = parse_input('input.txt')

    print("\nProcessing Part 1...")
    result1 = part_one(rules, sequences)

    print("\nProcessing Part 2...")
    result2 = part_two(rules, sequences)

    # Final results display
    print("\n=== Final Results ===")
    print(f"Part 1: Sum of middle numbers from valid sequences: {result1}")
    print(f"Part 2: Sum of middle numbers from fixed sequences: {result2}")

if __name__ == "__main__":
    main()
