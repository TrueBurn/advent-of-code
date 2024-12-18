import unittest
from solution import find_shortest_path, find_blocking_byte

class TestSolution(unittest.TestCase):
    def test_example_path(self):
        # Example grid:
        # ...#...
        # ..#..#.
        # ....#..
        # ...#..#
        # ..#..#.
        # .#..#..
        # #.#....
        corrupted = [
            (3,0), (5,1), (2,1),  # Row 0-1
            (4,2),                 # Row 2
            (3,3), (6,3),         # Row 3
            (2,4), (5,4),         # Row 4
            (1,5), (4,5),         # Row 5
            (0,6), (2,6)          # Row 6
        ]
        result = find_shortest_path(corrupted, grid_size=7, debug=False)
        self.assertEqual(result, 22)
    
    def test_no_path(self):
        corrupted = [(0,1), (1,0)]  # Block all paths from start
        self.assertEqual(find_shortest_path(corrupted, grid_size=2), -1)
    
    def test_direct_path(self):
        corrupted = []  # Empty grid
        self.assertEqual(find_shortest_path(corrupted, grid_size=2), 2)
    
    def test_single_path(self):
        corrupted = [(1,0), (0,1)]  # Only diagonal path possible
        self.assertEqual(find_shortest_path(corrupted, grid_size=2), -1)
    
    def test_blocking_byte(self):
        corrupted = [
            (3,0), (5,1), (2,1),  # Row 0-1
            (4,2),                 # Row 2
            (3,3), (6,3),         # Row 3
            (2,4), (5,4),         # Row 4
            (1,5), (4,5),         # Row 5
            (0,6), (2,6),         # Row 6
            (1,1), (6,1)          # Additional bytes including blocker
        ]
        blocking_byte = find_blocking_byte(corrupted, grid_size=7)
        self.assertEqual(blocking_byte, (6, 1))

def run_tests():
    print("Running unit tests...")
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestSolution)
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    return result.wasSuccessful()

if __name__ == '__main__':
    run_tests()
