from solution import parse_input, can_fit_presents

test_input = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

12x5: 1 0 1 0 3 2
"""

with open("test3.txt", "w") as f:
    f.write(test_input)

shapes, regions = parse_input("test3.txt")

# This should fail - 3 of shape 4 plus 1 of shape 0, 1 of shape 2, 2 of shape 5
width, height, counts = regions[0]
print(f"Region: {width}x{height}")
print(f"Counts: {counts}")
print(f"Total presents: {sum(counts)}")

# Total area
total_area = 0
for idx, count in enumerate(counts):
    if count > 0:
        print(f"  Shape {idx}: {count} copies, area {len([c for r in shapes[idx] for c in r if c == '#'])}")
        total_area += count * len([c for r in shapes[idx] for c in r if c == '#'])

print(f"Total area needed: {total_area}")
print(f"Grid area: {width * height}")
print(f"Free space: {width * height - total_area}")

result = can_fit_presents(shapes, width, height, counts)
print(f"\nCan fit: {result}")
print(f"Expected: False")

import os
os.remove("test3.txt")
