from collections import Counter

def parse_input(filename):
    left_list = []
    right_list = []

    with open(filename, 'r') as f:
        for line in f:
            # Skip empty lines
            line = line.strip()
            if not line:
                continue

            # Split each line into two numbers
            left, right = map(int, line.split())
            left_list.append(left)
            right_list.append(right)

    return left_list, right_list

def calculate_similarity_score(left_list, right_list):
    # Count occurrences in right list
    right_counts = Counter(right_list)

    # Calculate similarity score
    total_score = 0
    for num in left_list:
        # Multiply number by its count in right list (0 if not present)
        score = num * right_counts.get(num, 0)
        total_score += score

    return total_score

def main():
    left_list, right_list = parse_input('input.txt')
    answer = calculate_similarity_score(left_list, right_list)
    print(f"The similarity score is: {answer}")

if __name__ == "__main__":
    main()
