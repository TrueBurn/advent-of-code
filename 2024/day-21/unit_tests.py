import unittest
from solution import solve, find_complexity

EXAMPLE_INPUT = """029A
980A
179A
456A
379A"""

class TestDay21(unittest.TestCase):
    def test_complexity_values(self):
        test_cases = {
            "029A": 1972,  # 68 * 29
            "980A": 58800,  # 60 * 980
            "179A": 12172,  # 68 * 179
            "456A": 29184,  # 64 * 456
            "379A": 24256   # 64 * 379
        }
        
        for code, expected in test_cases.items():
            with self.subTest(code=code):
                result = find_complexity(code, depth=2)
                self.assertEqual(result, expected)

    def test_full_example(self):
        data = EXAMPLE_INPUT.strip().splitlines()
        result = solve(data, depth=2)
        self.assertEqual(result, 126384)

    def test_part2_depth(self):
        data = EXAMPLE_INPUT.strip().splitlines()
        part1 = solve(data, depth=2)
        part2 = solve(data, depth=25)
        self.assertNotEqual(part1, part2, "Part 2 should give different result with depth=25")

def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDay21)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()

if __name__ == '__main__':
    unittest.main()
