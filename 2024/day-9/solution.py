import os

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def parse_input(filename):
    with open(filename, 'r') as f:
        return f.read().strip()

def get_disk_layout(input_str):
    input_str = input_str.strip()
    return [int(x) for x in input_str[::2]], [int(x) for x in input_str[1::2]]

def get_checksum(disk):
    total = 0
    for pos, fid in enumerate(disk):
        if fid != '.':
            total += pos * fid
    return total

def init_disk(files, spaces):
    disk = []
    for fid, size in enumerate(files):
        disk.extend([fid] * size)
        if fid < len(spaces):
            disk.extend(['.'] * spaces[fid])

    total_len = sum(files) + sum(spaces)
    disk.extend(['.'] * (total_len - len(disk)))
    return disk

def compact_left(disk):
    n = len(disk)
    empty_pos = []

    for i in range(n):
        if disk[i] == '.':
            empty_pos.append(i)

    if not empty_pos:
        return disk

    print("\nCompacting disk...")
    total_files = sum(1 for x in disk if x != '.')
    files_moved = 0

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

def find_file_spans(disk):
    spans = {}
    curr_id = None
    start = 0

    for i, fid in enumerate(disk):
        if fid != curr_id:
            if curr_id is not None and curr_id != '.':
                if curr_id not in spans:
                    spans[curr_id] = []
                spans[curr_id].append((start, i - start))
            curr_id = fid
            start = i

    if curr_id is not None and curr_id != '.':
        if curr_id not in spans:
            spans[curr_id] = []
        spans[curr_id].append((start, len(disk) - start))

    return spans

def find_empty_spans(disk):
    spans = []
    curr_len = 0
    start = 0

    for i, fid in enumerate(disk):
        if fid == '.':
            if curr_len == 0:
                start = i
            curr_len += 1
        else:
            if curr_len > 0:
                spans.append((start, curr_len))
            curr_len = 0

    if curr_len > 0:
        spans.append((start, curr_len))

    return spans

def get_file_map(input_str):
    return {i: int(x) for i, x in enumerate(input_str[::2])}

def get_space_map(input_str):
    return {i: int(x) for i, x in enumerate(input_str[1::2])}

def calc_file_position(files, spaces, space_left, target_space):
    pos = sum(size for f, size in files.items() if f <= target_space)
    pos += sum(size for s, size in spaces.items() if s < target_space)
    if space_left[target_space] != spaces[target_space]:
        pos += spaces[target_space] - space_left[target_space]
    return pos

def move_file(fid, files, spaces, space_left, disk_map):
    for i in range(fid):
        if files[fid] <= space_left[i]:
            pos = calc_file_position(files, spaces, space_left, i)
            space_left[i] -= files[fid]
            if fid - 1 in spaces:
                spaces[fid - 1] += files[fid]
                space_left[fid - 1] += files[fid]

            for x in range(pos, pos + files[fid]):
                disk_map[x] = fid
            files[fid] = 0
            return True
    return False

def finalize_disk_map(files, spaces):
    pos = 0
    disk_map = {}
    for fid in files:
        for _ in range(files[fid]):
            disk_map[pos] = fid
            pos += 1
        if fid in spaces:
            pos += spaces[fid]
    return disk_map

def part_one(input_str):
    print("Parsing disk layout...")
    files, spaces = get_disk_layout(input_str)

    print("Initializing disk...")
    disk = init_disk(files, spaces)

    final = compact_left(disk)

    print("\nCalculating checksum...")
    return get_checksum(final)

def part_two(input_str):
    print("Parsing disk layout...")
    files = get_file_map(input_str)
    spaces = get_space_map(input_str)
    space_left = get_space_map(input_str)
    disk_map = {}

    print("\nCompacting files...")
    total = len(files)
    processed = 0

    for fid in reversed(files):
        move_file(fid, files, spaces, space_left, disk_map)
        processed += 1
        if processed % 10 == 0:
            clear_console()
            print(f"Progress: {processed}/{total} files processed ({processed/total:.1%})")

    print("\nFinalizing disk map...")
    final_map = finalize_disk_map(files, spaces)
    disk_map.update(final_map)

    print("\nCalculating checksum...")
    checksum = 0
    for i in range(sum(int(x) for x in input_str)):
        if i in disk_map:
            checksum += i * disk_map[i]

    return checksum

def main():
    input_data = parse_input('input.txt')

    print(f"Input size: {len(input_data)} characters")

    print("\n=== Part 1 ===")
    result1 = part_one(input_data)

    print("\n=== Part 2 ===")
    result2 = part_two(input_data)

    clear_console()
    print("=== Final Results ===")
    print(f"Part 1: {result1}")
    print(f"Part 2: {result2}")

if __name__ == "__main__":
    main()
