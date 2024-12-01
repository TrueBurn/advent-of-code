import os

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

def calculate_total_distance(left_list, right_list):
    # Sort both lists
    left_sorted = sorted(left_list)
    right_sorted = sorted(right_list)

    # Calculate total distance
    total_distance = 0
    for l, r in zip(left_sorted, right_sorted):
        distance = abs(l - r)
        total_distance += distance

    return total_distance

def main():
    left_list, right_list = parse_input('input.txt')
    answer = calculate_total_distance(left_list, right_list)
    print(f"The total distance between the lists is: {answer}")

if __name__ == "__main__":
    main()
