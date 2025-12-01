import os
import unittest

from solution import part1, part2


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        with open("test_example.txt", "w") as f:
            f.write("""L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
""")

    def tearDown(self):
        for f in ["test_example.txt", "test_r1000.txt", "test_l68.txt",
                  "test_r48.txt", "test_r50.txt"]:
            if os.path.exists(f):
                os.remove(f)

    def test_example_part1(self):
        result = part1("test_example.txt")
        self.assertEqual(result, 3)

    def test_example_part2(self):
        result = part2("test_example.txt")
        self.assertEqual(result, 6)

    def test_r1000_from_50(self):
        # The problem mentions this edge case - R1000 from 50 crosses 0 ten times
        with open("test_r1000.txt", "w") as f:
            f.write("R1000\n")
        result = part2("test_r1000.txt")
        self.assertEqual(result, 10)

    def test_l68_from_50(self):
        with open("test_l68.txt", "w") as f:
            f.write("L68\n")
        result = part2("test_l68.txt")
        self.assertEqual(result, 1)

    def test_r48_from_50(self):
        with open("test_r48.txt", "w") as f:
            f.write("R48\n")
        result = part2("test_r48.txt")
        self.assertEqual(result, 0)

    def test_r50_from_50(self):
        with open("test_r50.txt", "w") as f:
            f.write("R50\n")
        result = part2("test_r50.txt")
        self.assertEqual(result, 1)


def run_tests():
    print("Running unit tests...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSolution)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()
