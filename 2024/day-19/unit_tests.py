import unittest
from solution import parse_input, can_make_design, solve, TowelPattern, count_ways_to_make_design

class TestSolution(unittest.TestCase):
    def test_example(self):
        test_input = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""
        
        with open('test_input.txt', 'w') as f:
            f.write(test_input)
        
        patterns, designs = parse_input('test_input.txt')
        
        # Test specific cases from example
        self.assertTrue(can_make_design("brwrr", patterns))  # Can be made with br+wr+r
        self.assertTrue(can_make_design("bggr", patterns))   # Can be made with b+g+g+r
        self.assertTrue(can_make_design("gbbr", patterns))   # Can be made with gb+br
        self.assertTrue(can_make_design("rrbgbr", patterns)) # Can be made with r+rb+g+br
        self.assertFalse(can_make_design("ubwu", patterns))  # Impossible
        self.assertTrue(can_make_design("bwurrg", patterns)) # Can be made with bwu+r+r+g
        self.assertTrue(can_make_design("brgr", patterns))   # Can be made with br+g+r
        self.assertFalse(can_make_design("bbrgwb", patterns)) # Impossible
        
        # Test overall solution
        result1, _ = solve('test_input.txt')
        self.assertEqual(result1, 6)
        
        import os
        os.remove('test_input.txt')
    
    def test_edge_cases(self):
        # Test empty pattern
        self.assertTrue(can_make_design("", [], 0, {}))
        
        # Test single pattern exact match
        self.assertTrue(can_make_design("rgb", [TowelPattern("rgb")]))
        
        # Test impossible pattern
        self.assertFalse(can_make_design("xyz", [TowelPattern("rgb")]))
    
    def test_count_ways(self):
        test_input = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""
        
        with open('test_input.txt', 'w') as f:
            f.write(test_input)
        
        patterns, designs = parse_input('test_input.txt')
        
        # Test specific cases from example
        self.assertEqual(count_ways_to_make_design("brwrr", patterns), 2)   # 2 ways
        self.assertEqual(count_ways_to_make_design("bggr", patterns), 1)    # 1 way
        self.assertEqual(count_ways_to_make_design("gbbr", patterns), 4)    # 4 ways
        self.assertEqual(count_ways_to_make_design("rrbgbr", patterns), 6)  # 6 ways
        self.assertEqual(count_ways_to_make_design("bwurrg", patterns), 1)  # 1 way
        self.assertEqual(count_ways_to_make_design("brgr", patterns), 2)    # 2 ways
        
        # Test overall solution
        result1, result2 = solve('test_input.txt')
        self.assertEqual(result2, 16)  # Total ways = 2 + 1 + 4 + 6 + 1 + 2
        
        import os
        os.remove('test_input.txt')

def run_tests():
    print("Running unit tests...")
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestSolution)
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    return result.wasSuccessful()

if __name__ == '__main__':
    run_tests()
