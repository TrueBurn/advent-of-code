import unittest
from solution import parse_input, find_connected_sets, find_lan_party

EXAMPLE_INPUT = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""

class TestDay23(unittest.TestCase):
    def test_parse_input(self):
        connections = parse_input(EXAMPLE_INPUT)
        self.assertIn(("kh", "tc"), connections)
        self.assertIn(("ka", "tb"), connections)
        self.assertEqual(len(connections), 32)

    def test_find_connected_sets(self):
        connections = parse_input(EXAMPLE_INPUT)
        sets = find_connected_sets(connections)
        
        expected_t_sets = {
            frozenset({"co", "de", "ta"}),
            frozenset({"co", "ka", "ta"}),
            frozenset({"de", "ka", "ta"}),
            frozenset({"qp", "td", "wh"}),
            frozenset({"tb", "vc", "wq"}),
            frozenset({"tc", "td", "wh"}),
            frozenset({"td", "wh", "yn"})
        }
        
        t_sets = {s for s in sets if any(c.startswith('t') for c in s)}
        self.assertEqual(t_sets, expected_t_sets)
        self.assertEqual(len(t_sets), 7)
    
    def test_find_lan_party(self):
        connections = parse_input(EXAMPLE_INPUT)
        result = find_lan_party(connections)
        self.assertEqual(result, "co,de,ka,ta")

def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDay23)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()

if __name__ == '__main__':
    unittest.main()
