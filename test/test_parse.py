import unittest
from parse import parse

class TestParse(unittest.TestCase):
    """
    Unit test for parse() function.
    """

    def test_parse(self):
        # Test case for the parse function with a sample input file
        test_kb, test_query, test_symbols = parse("data.txt")
        self.assertEqual(test_kb, [['p2', '=>', 'p3'], ['p3', '=>', 'p1'], ['c', '=>', 'e'], ['b', '&', 'e', '=>', 'f'], ['f', '&', 'g', '=>', 'h'], ['p1', '=>', 'd'], ['p1', '&', 'p3', '=>', 'c'], ['a'], ['b'], ['p2']])
        self.assertEqual(test_query, ['d'])
        self.assertEqual(set(test_symbols), {'h', 'c', 'b', 'p3', 'f', 'p1', 'e', 'g', 'd', 'a', 'p2'})

if __name__ == "__main__":
    unittest.main()
