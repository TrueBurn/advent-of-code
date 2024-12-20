import unittest
from solution import parse_input, find_cheats

EXAMPLE_INPUT = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""

class TestDay20(unittest.TestCase):
    def test_parse_input(self):
        grid, start, end = parse_input(EXAMPLE_INPUT)
        self.assertEqual(len(grid), 15)
        self.assertEqual(len(grid[0]), 15)
        self.assertEqual(start, (3, 1))
        self.assertEqual(end, (7, 5))

    def test_find_cheats_part1(self):
        grid, start, end = parse_input(EXAMPLE_INPUT)
        cheats = find_cheats(grid, start, end, max_cheat_time=2)
        
        cheats_by_savings = {
            2: 14, 4: 14, 6: 2, 8: 4, 10: 2, 12: 3,
            20: 1, 36: 1, 38: 1, 40: 1, 64: 1
        }
        
        counted_cheats = {}
        for cheat in cheats:
            time_saved = cheat[2]
            counted_cheats[time_saved] = counted_cheats.get(time_saved, 0) + 1
        
        for savings, count in cheats_by_savings.items():
            self.assertEqual(counted_cheats.get(savings, 0), count,
                           f"Expected {count} cheats saving {savings} picoseconds")

    def test_find_cheats_part2(self):
        grid, start, end = parse_input(EXAMPLE_INPUT)
        cheats = find_cheats(grid, start, end, max_cheat_time=20)
        
        # Test a few specific cases from part 2
        cheats_by_savings = {
            50: 32, 52: 31, 54: 29, 56: 39, 58: 25,
            60: 23, 62: 20, 64: 19, 66: 12, 68: 14,
            70: 12, 72: 22, 74: 4, 76: 3
        }
        
        counted_cheats = {}
        for cheat in cheats:
            time_saved = cheat[2]
            if time_saved >= 50:  # Only count cheats saving 50+ picoseconds
                counted_cheats[time_saved] = counted_cheats.get(time_saved, 0) + 1
        
        for savings, count in cheats_by_savings.items():
            self.assertEqual(counted_cheats.get(savings, 0), count,
                           f"Expected {count} cheats saving {savings} picoseconds")

def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDay20)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()

if __name__ == '__main__':
    unittest.main()
