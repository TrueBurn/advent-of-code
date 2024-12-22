import unittest
from solution import solve, generate_next_secret

EXAMPLE_INPUT_1 = """1
10
100
2024"""

EXAMPLE_INPUT_2 = """1
2
3
2024"""

class TestDay22(unittest.TestCase):
    def test_generate_next_secret(self):
        test_cases = {
            123: 15887950,
            15887950: 16495136,
            16495136: 527345
        }
        
        for initial, expected in test_cases.items():
            with self.subTest(initial=initial):
                result = generate_next_secret(initial)
                self.assertEqual(result, expected)

    def test_sequence_generation(self):
        secret = 123
        expected = [
            (123 % 10, 123),
            (0, 15887950),
            (6, 16495136),
            (5, 527345),
            (4, 704524)
        ]
        
        current = secret
        results = [(current % 10, current)]
        
        for _ in range(4):
            current = generate_next_secret(current)
            results.append((current % 10, current))
        
        self.assertEqual(results, expected)

    def test_example_input(self):
        part1, part2 = solve(EXAMPLE_INPUT_1)
        self.assertEqual(part1, 37327623)
        
        _, part2 = solve(EXAMPLE_INPUT_2)
        self.assertEqual(part2, 23)

def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDay22)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()

if __name__ == '__main__':
    unittest.main()
