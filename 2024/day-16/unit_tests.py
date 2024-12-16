import unittest
from solution import parse_input, find_shortest_path, State, Direction, part2

class TestSolution(unittest.TestCase):
    def test_small_example(self):
        grid = [
            "###############",
            "#.......#....E#",
            "#.#.###.#.###.#",
            "#.....#.#...#.#",
            "#.###.#####.#.#",
            "#.#.#.......#.#",
            "#.#.#####.###.#",
            "#...........#.#",
            "###.#.#####.#.#",
            "#...#.....#.#.#",
            "#.#.#.###.#.#.#",
            "#.....#...#.#.#",
            "#.###.#.#.#.#.#",
            "#S..#.....#...#",
            "###############"
        ]
        
        with open('test_input.txt', 'w') as f:
            f.write('\n'.join(grid))
        
        grid, start_state, end_pos = parse_input('test_input.txt')
        result = find_shortest_path(grid, start_state, end_pos)
        
        import os
        os.remove('test_input.txt')
        
        self.assertEqual(result, 7036)

    def test_small_example_part2(self):
        grid = [
            "###############",
            "#.......#....E#",
            "#.#.###.#.###.#",
            "#.....#.#...#.#",
            "#.###.#####.#.#",
            "#.#.#.......#.#",
            "#.#.#####.###.#",
            "#...........#.#",
            "###.#.#####.#.#",
            "#...#.....#.#.#",
            "#.#.#.###.#.#.#",
            "#.....#...#.#.#",
            "#.###.#.#.#.#.#",
            "#S..#.....#...#",
            "###############"
        ]
        
        with open('test_input.txt', 'w') as f:
            f.write('\n'.join(grid))
        
        grid, start_state, end_pos = parse_input('test_input.txt')
        result = part2('test_input.txt')
        
        import os
        os.remove('test_input.txt')
        
        self.assertEqual(result, 45)

def run_tests():
    print("Running unit tests...")
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestSolution)
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    return result.wasSuccessful()

if __name__ == '__main__':
    run_tests()
