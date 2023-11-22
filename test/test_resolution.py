import unittest
from resolution import resolve, resolution

class TestResolution(unittest.TestCase):
    def test_simple_true(self):
        kb = [['a', '=>', 'b'], ['b', '=>', 'c'], ['a']]
        query = ['c']
        self.assertTrue(resolution(kb, query))

    def test_simple_false(self):
        kb = [['a', '=>', 'b'], ['b', '&', 'd', '=>', 'c'], ['a'], [ '~', 'd']]
        query = ['c']
        self.assertFalse(resolution(kb, query))

    def test_complex_one(self):
        kb = [['p2', '=>', 'p3'], ['p3', '=>', 'p1'], ['c', '=>', 'e'], ['b', '&', 'e', '=>', 'f'], ['f', '&', 'g', '=>', 'h'], ['p1', '=>', 'd'], ['p1', '&', 'p3', '=>', 'c'], ['a'], ['b'], ['p2']]
        query = ['d']
        self.assertTrue(resolution(kb, query))

    def test_complex_two(self):
        kb = [['(', 'a', '<=>', '(', 'c', '=>', '~', 'd', ')', ')', '&', 'b', '&', '(', 'b', '=>', 'a', ')'], ['c'], ['~', 'f', '||', 'g']]
        query = ['~', 'd', '&', '(', '~', 'g', '=>', '~', 'f', ')']
        self.assertTrue(resolution(kb, query))

if __name__ == '__main__':
    unittest.main()