import unittest
from solution import parse_schematic, can_fit, parse_input

EXAMPLE_INPUT = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""

class TestDay25(unittest.TestCase):
    def test_parse_schematic(self):
        lock = EXAMPLE_INPUT.split('\n\n')[0]
        n = parse_schematic(lock)
        self.assertTrue(n >= 0x7C0000000)
        
        key = EXAMPLE_INPUT.split('\n\n')[2]
        n = parse_schematic(key)
        self.assertTrue(n < 0x7C0000000)
    
    def test_can_fit(self):
        locks, keys = parse_input(EXAMPLE_INPUT)
        self.assertFalse(can_fit(locks[0], keys[0]))
        self.assertTrue(can_fit(locks[0], keys[2]))
    
    def test_full_example(self):
        locks, keys = parse_input(EXAMPLE_INPUT)
        valid_pairs = sum(1 for lock in locks for key in keys if can_fit(lock, key))
        self.assertEqual(valid_pairs, 3)

def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDay25)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()

if __name__ == '__main__':
    unittest.main()
