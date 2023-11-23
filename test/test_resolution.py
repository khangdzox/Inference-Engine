import unittest
from resolution import resolve, resolution_checking

class TestResolution(unittest.TestCase):
    """
    Test resolution.
    """
    def test_simple_true(self):
        kb = [['a', '=>', 'b'], ['b', '=>', 'c'], ['a']]
        query = ['c']
        self.assertTrue(resolution_checking(kb, query))

    def test_simple_false(self):
        kb = [['a', '=>', 'b'], ['b', '&', 'd', '=>', 'c'], ['a'], [ '~', 'd']]
        query = ['c']
        self.assertFalse(resolution_checking(kb, query))

    def test_complex_one(self):
        kb = [['p2', '=>', 'p3'], ['p3', '=>', 'p1'], ['c', '=>', 'e'], ['b', '&', 'e', '=>', 'f'], ['f', '&', 'g', '=>', 'h'], ['p1', '=>', 'd'], ['p1', '&', 'p3', '=>', 'c'], ['a'], ['b'], ['p2']]
        query = ['d']
        self.assertTrue(resolution_checking(kb, query))

    def test_complex_two(self):
        kb = [['(', 'a', '<=>', '(', 'c', '=>', '~', 'd', ')', ')', '&', 'b', '&', '(', 'b', '=>', 'a', ')'], ['c'], ['~', 'f', '||', 'g']]
        query = ['~', 'd', '&', '(', '~', 'g', '=>', '~', 'f', ')']
        self.assertTrue(resolution_checking(kb, query))

    def test_complex_three(self):
        kb = [['(', 'a', '<=>', '(', 'c', '=>', '~', 'd', ')', ')', '&', 'b', '&', '(', 'b', '=>', 'a', ')'], ['c'], ['~', 'f', '||', 'g']]
        query = ['d']
        self.assertFalse(resolution_checking(kb, query))

class TestResolve(unittest.TestCase):
    """
    Test resolve.
    """

    def test_resolve_single(self):
        result = resolve(['~a', 'b'], ['~b', 'c'])
        self.assertEqual(set(result if result is not None else []), {'~a', 'c'})
        result = resolve(['~a', 'b', 'c', '~d'], ['~a', 'b', '~c'])
        self.assertEqual(set(result if result is not None else []), {'~a', 'b', '~d'})

    def test_resolve_multiple(self):
        self.assertIsNone(resolve(['b', 'c', '~d'], ['~a', '~b', '~c']))
        self.assertIsNone(resolve(['~a', 'b', 'c', '~d'], ['a', '~b', '~c', 'd']))

    def test_resolve_all(self):
        self.assertEqual(resolve(['~a'], ['a']), [])

    def test_resolve_nothing(self):
        self.assertIsNone(resolve(['~a', 'b', 'c', '~d'], ['~a', '~d', '~e']))

if __name__ == '__main__':
    unittest.main()
