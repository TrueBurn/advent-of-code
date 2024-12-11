from functools import cache

def read_input(file_path):
    with open(file_path, 'r') as f:
        return [int(num) for line in f for num in line.split() if num]

@cache
def find_total(iterations, check_stone):
    if iterations == 0:
        return 1
    if check_stone == 0:
        return find_total(iterations - 1, 1)
    elif len(str(check_stone)) % 2 == 0:
        return (find_total(iterations - 1, int(str(check_stone)[:len(str(check_stone)) // 2])) +
                find_total(iterations - 1, int(str(check_stone)[len(str(check_stone)) // 2:])))
    else:
        return find_total(iterations - 1, check_stone * 2024)

def part_one(stones):
    return sum(find_total(25, stone) for stone in stones)

def part_two(stones):
    return sum(find_total(75, stone) for stone in stones)

if __name__ == "__main__":
    stones = read_input('input.txt')

    result_part_one = part_one(stones)
    print(f"Part 1: {result_part_one}")

    result_part_two = part_two(stones)
    print(f"Part 2: {result_part_two}")
