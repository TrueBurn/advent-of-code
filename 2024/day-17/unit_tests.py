import unittest
from solution import parse_input, run_program, self_generate

class TestSolution(unittest.TestCase):
    def test_example1(self):
        program = [2, 6]
        output, _, b, _ = run_program(program, a=0, b=0, c=9)
        self.assertEqual(b & 7, 1)
    
    def test_example2(self):
        program = [5, 0, 5, 1, 5, 4]
        output, _, _, _ = run_program(program, a=10)
        self.assertEqual(','.join(map(str, output)), "0,1,2")
    
    def test_example3(self):
        program = [0, 1, 5, 4, 3, 0]
        output, _, _, _ = run_program(program, a=2024)
        self.assertEqual(','.join(map(str, output)), "4,2,5,6,7,7,7,7,3,1,0")
    
    def test_example4(self):
        program = [1, 7]
        output, _, b, _ = run_program(program, a=0, b=29)
        self.assertEqual(b & 7, 2)
    
    def test_example5(self):
        program = [4, 0]
        output, _, b, _ = run_program(program, a=0, b=2024, c=43690)
        self.assertEqual(b & 7, 2)
    
    def test_full_example(self):
        with open('test_input.txt', 'w') as f:
            f.write("Register A: 729\nRegister B: 0\nRegister C: 0\n\nProgram: 0,1,5,4,3,0")
        
        registers, program = parse_input('test_input.txt')
        output, _, _, _ = run_program(
            program,
            a=registers.get('A', 0),
            b=registers.get('B', 0),
            c=registers.get('C', 0)
        )
        
        import os
        os.remove('test_input.txt')
        
        self.assertEqual(','.join(map(str, output)), "4,6,3,5,6,3,5,2,1,0")
    
    def test_part2_example(self):
        program = [0, 3, 5, 4, 3, 0]
        result = self_generate(program)
        self.assertEqual(result, 117440)
        
        output, _, _, _ = run_program(program, a=result)
        self.assertEqual(','.join(map(str, output)), "0,3,5,4,3,0")
        
        for a in range(1, result):
            output, _, _, _ = run_program(program, a=a)
            if ','.join(map(str, output)) == "0,3,5,4,3,0":
                self.fail(f"Found lower solution: {a}")

def run_tests():
    print("Running unit tests...")
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestSolution)
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    return result.wasSuccessful()

if __name__ == '__main__':
    run_tests()
