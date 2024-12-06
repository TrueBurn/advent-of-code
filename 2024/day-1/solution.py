from collections import Counter

def parse_input(filename):
    left_list = []
    right_list = []

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            left, right = map(int, line.split())
            left_list.append(left)
            right_list.append(right)

    return left_list, right_list

def calculate_total_distance(left_list, right_list):
    left_sorted = sorted(left_list)
    right_sorted = sorted(right_list)

    total = 0
    for l, r in zip(left_sorted, right_sorted):
        total += abs(l - r)

    return total

def calculate_similarity_score(left_list, right_list):
    right_counts = Counter(right_list)
    return sum(num * right_counts.get(num, 0) for num in left_list)

def part_one(left_list, right_list):
    return calculate_total_distance(left_list, right_list)

def part_two(left_list, right_list):
    return calculate_similarity_score(left_list, right_list)

def main():
    print("Parsing input...")
    left_list, right_list = parse_input('input.txt')

    print("\nProcessing Part 1...")
    result1 = part_one(left_list, right_list)

    print("\nProcessing Part 2...")
    result2 = part_two(left_list, right_list)

    print("\n=== Final Results ===")
    print(f"Part 1: Total distance between lists: {result1}")
    print(f"Part 2: Similarity score: {result2}")

if __name__ == "__main__":
    main()
