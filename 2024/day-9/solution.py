import os
import time
import heapq

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def parse_input(filename):
    with open(filename, 'r') as f:
        return f.read().strip()

def split_disk_layout(input_str):
    input_str = input_str.strip()
    return [int(x) for x in input_str[::2]], [int(x) for x in input_str[1::2]]

def calc_disk_checksum(disk):
    return sum(pos * fid for pos, fid in enumerate(disk) if fid != '.')

def build_initial_disk(files, spaces):
    disk = []
    for fid, size in enumerate(files):
        disk.extend([fid] * size)
        if fid < len(spaces):
            disk.extend(['.'] * spaces[fid])

    total_len = sum(files) + sum(spaces)
    disk.extend(['.'] * (total_len - len(disk)))
    return disk

def move_files_left(disk):
    n = len(disk)
    empty_pos = [i for i in range(n) if disk[i] == '.']
    if not empty_pos:
        return disk

    files_moved = 0
    total_files = sum(1 for x in disk if x != '.')

    for i in range(n-1, -1, -1):
        if disk[i] != '.':
            if empty_pos and empty_pos[0] < i:
                disk[empty_pos[0]] = disk[i]
                disk[i] = '.'
                empty_pos.pop(0)
                empty_pos.append(i)
                files_moved += 1

                if files_moved % 1000 == 0:
                    clear_console()
                    print(f"Progress: {files_moved}/{total_files} files moved ({files_moved/total_files:.1%})")
    return disk

def part_one(input_str):
    files, spaces = split_disk_layout(input_str)
    disk = build_initial_disk(files, spaces)
    final = move_files_left(disk)
    return calc_disk_checksum(final)

def part_one_optimized(input_str):
    blocks = list(map(int, input_str[::2]))
    spaces = list(map(int, input_str[1::2])) + [0]

    disk = []
    for i, (block, space) in enumerate(zip(blocks, spaces)):
        disk.extend([i] * block)
        disk.extend(['.'] * space)

    empty = [i for i, val in enumerate(disk) if val == '.']

    for i in range(len(disk)-1, -1, -1):
        if disk[i] != '.' and empty and empty[0] < i:
            disk[empty[0]] = disk[i]
            disk[i] = '.'
            empty.pop(0)
            empty.append(i)

    return calc_disk_checksum(disk)

def part_two_optimized(input_str):
    blocks = list(map(int, input_str[::2]))
    spaces = list(map(int, input_str[1::2])) + [0]

    disk = [(pos, block, i) for i, (block, space) in enumerate(zip(blocks, spaces))
            for pos in [sum(blocks[:i]) + sum(spaces[:i])] if block]

    final = {}
    space_left = dict(enumerate(spaces))

    block_sums = [sum(blocks[:i]) for i in range(len(blocks) + 1)]
    space_sums = [sum(spaces[:i]) for i in range(len(spaces) + 1)]

    for pos, size, fid in reversed(disk):
        moved = False
        for i in range(fid):
            if size <= space_left[i]:
                offset = block_sums[i+1] + space_sums[i]
                if space_left[i] != spaces[i]:
                    offset += spaces[i] - space_left[i]

                space_left[i] -= size
                if fid - 1 in space_left:
                    space_left[fid - 1] += size

                final[fid] = (offset, size)
                moved = True
                break

        if not moved:
            final[fid] = (pos, size)

    return sum(fid * (pos * size + size * (size - 1) // 2)
              for fid, (pos, size) in final.items())

def part_two(input_str):
    files = {i: int(x) for i, x in enumerate(input_str[::2])}
    spaces = {i: int(x) for i, x in enumerate(input_str[1::2])}
    space_left = {i: int(x) for i, x in enumerate(input_str[1::2])}
    disk_map = {}

    total = len(files)
    processed = 0

    for fid in reversed(files):
        for i in range(fid):
            if files[fid] <= space_left[i]:
                pos = sum(size for f, size in files.items() if f <= i)
                pos += sum(size for s, size in spaces.items() if s < i)
                if space_left[i] != spaces[i]:
                    pos += spaces[i] - space_left[i]

                space_left[i] -= files[fid]
                if fid - 1 in spaces:
                    spaces[fid - 1] += files[fid]
                    space_left[fid - 1] += files[fid]

                for x in range(pos, pos + files[fid]):
                    disk_map[x] = fid
                files[fid] = 0
                break

        processed += 1
        if processed % 10 == 0:
            clear_console()
            print(f"Progress: {processed}/{total} files processed ({processed/total:.1%})")

    pos = 0
    for fid in files:
        for _ in range(files[fid]):
            disk_map[pos] = fid
            pos += 1
        if fid in spaces:
            pos += spaces[fid]

    checksum = 0
    for i in range(sum(int(x) for x in input_str)):
        if i in disk_map:
            checksum += i * disk_map[i]

    return checksum

def main():
    run_unoptimized = False
    start_time = time.time()
    input_data = parse_input('input.txt')

    if run_unoptimized:
        part1_start = time.time()
        result1 = part_one(input_data)
        part1_time = time.time() - part1_start

        part2_start = time.time()
        result2 = part_two(input_data)
        part2_time = time.time() - part2_start

    part1_opt_start = time.time()
    result1_opt = part_one_optimized(input_data)
    part1_opt_time = time.time() - part1_opt_start

    part2_opt_start = time.time()
    result2_opt = part_two_optimized(input_data)
    part2_opt_time = time.time() - part2_opt_start

    total_time = time.time() - start_time

    clear_console()
    print("=== Final Results ===")
    if run_unoptimized:
        print(f"Part 1: {result1} (took {part1_time:.2f}s)")
        print(f"Part 2: {result2} (took {part2_time:.2f}s)")
    print(f"Part 1 (Optimized): {result1_opt} (took {part1_opt_time:.2f}s)")
    print(f"Part 2 (Optimized): {result2_opt} (took {part2_opt_time:.2f}s)")
    print(f"\nTotal time: {total_time:.2f}s")

if __name__ == "__main__":
    main()
