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

class TestResolve(unittest.TestCase):
    """
    Test resolve.
    """

    def test_resolve_part(self):
        self.assertEqual(set(resolve(['~a', 'b'], ['~b', 'c'])), {'~a', 'c'})
        self.assertEqual(set(resolve(['~a', 'b', 'c', '~d'], ['~a', '~b', '~c'])), {'~a', '~d'})

    def test_resolve_all(self):
        self.assertEqual(resolve(['~a', 'b'], ['a', '~b']), [])
        self.assertEqual(resolve(['~a', 'b', 'c', '~d'], ['a', '~b', '~c', 'd']), [])

    def test_resolve_none(self):
        self.assertEqual(set(resolve(['~a', 'b', 'c', '~d'], ['~a', '~d', '~e'])), {'~a', 'b', 'c', '~d', '~e'})

if __name__ == '__main__':
    unittest.main()
