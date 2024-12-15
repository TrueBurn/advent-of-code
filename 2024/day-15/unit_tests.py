import unittest
from solution import Pos, parse_input, simulate_move, calculate_gps_sum, scale_map, simulate_move_wide, calculate_gps_sum_wide

class TestSolution(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None  # Show full diffs for grid comparisons
    
    def test_pos_addition(self):
        p1 = Pos(1, 2)
        p2 = Pos(-1, 3)
        result = p1 + p2
        self.assertEqual(result, Pos(0, 5))
    
    def test_parse_input(self):
        with open('test_input.txt', 'w') as f:
            f.write("#####\n#.@O#\n#####\n<>v^")
        
        grid, moves, robot_pos = parse_input('test_input.txt')
        self.assertEqual(len(grid), 3)
        self.assertEqual(moves, "<>v^")
        self.assertEqual(robot_pos, Pos(1, 2))
        
        import os
        os.remove('test_input.txt')
    
    # Part 1 Tests
    def test_simulate_move_basic(self):
        grid = [list(row) for row in [
            "#####",
            "#.@.#",
            "#####"
        ]]
        robot_pos = Pos(1, 2)
        
        grid, new_pos = simulate_move(grid, robot_pos, '>')
        self.assertEqual(new_pos, Pos(1, 3))
        self.assertEqual(grid[1][2], '.')
        self.assertEqual(grid[1][3], '@')
    
    def test_simulate_move_with_box(self):
        grid = [list(row) for row in [
            "#####",
            "#@O.#",
            "#####"
        ]]
        robot_pos = Pos(1, 1)
        
        grid, new_pos = simulate_move(grid, robot_pos, '>')
        self.assertEqual(new_pos, Pos(1, 2))
        self.assertEqual(grid[1][3], 'O')
    
    def test_calculate_gps_sum(self):
        grid = [list(row) for row in [
            "#####",
            "#.O.#",  # Box at (1,2) = 102
            "#O..#",  # Box at (2,1) = 201
            "#####"
        ]]
        self.assertEqual(calculate_gps_sum(grid), 303)
    
    # Part 2 Tests
    def test_scale_map(self):
        grid = [
            "###",
            "#O@",
            "###"
        ]
        expected = [
            ['#', '#', '#', '#', '#', '#'],
            ['#', '#', '[', ']', '@', '.'],
            ['#', '#', '#', '#', '#', '#']
        ]
        self.assertEqual(scale_map(grid), expected)
    
    def test_calculate_gps_sum_wide(self):
        grid = scale_map([
            "######",
            "#.O..#",  # Box at (1,2) becomes (1,4) after scaling (each cell becomes two)
            "#O...#",  # Box at (2,1) becomes (2,2) after scaling
            "######"
        ])
        # After scaling:
        # - First box '[' is at (1,4) = 104
        # - Second box '[' is at (2,2) = 202
        # Total = 306
        self.assertEqual(calculate_gps_sum_wide(grid), 306)
    
    def test_part2_example_first_moves(self):
        grid = [
            "#######",
            "#...#.#",
            "#.....#",
            "#..OO@#",
            "#..O..#",
            "#.....#",
            "#######"
        ]
        
        grid = scale_map(grid)
        robot_pos = Pos(3, 6 * 2)
        
        # First move down
        grid, robot_pos = simulate_move_wide(grid, robot_pos, 'v')
        expected1 = [
            "##############",
            "##......##..##",
            "##..........##",
            "##....[][]@.##",  # Robot moves with boxes
            "##....[]....##",
            "##..........##",
            "##############"
        ]
        self.assertEqual([''.join(row) for row in grid], expected1)
        
        # Second move down
        grid, robot_pos = simulate_move_wide(grid, robot_pos, 'v')
        expected2 = [
            "##############",
            "##......##..##",
            "##..........##",
            "##....[][]@.##",  # Robot stays with boxes
            "##....[]....##",
            "##..........##",
            "##############"
        ]
        self.assertEqual([''.join(row) for row in grid], expected2)

def run_tests():
    print("Running unit tests...")
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestSolution)
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    return result.wasSuccessful()

if __name__ == '__main__':
    run_tests()
