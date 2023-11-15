import unittest
from forward_chaining import forward_chaining_checking

class TestForwardChaining(unittest.TestCase):
    """
    Unit test for forward_chaining() function.
    """
    def test_single(self):
        self.assertEqual(forward_chaining_checking([['p']], 'p'), (True, {'p'}))
        self.assertEqual(forward_chaining_checking([['p']], 'q'), (False, set()))

    def test_implication(self):
        self.assertEqual(forward_chaining_checking([['p', '=>', 'q'], ['p']], 'q'), (True, {'p', 'q'}))
        self.assertEqual(forward_chaining_checking([['p', '=>', 'q'], ['q']], 'p'), (False, set()))

    def test_sentences(self):
        self.assertEqual(
            forward_chaining_checking([['s', '&', 'p', '=>', 'q'], ['q', '=>', 'r'], ['s'], ['p']], 'r'),
            (True, {'s', 'p', 'q', 'r'}))

        self.assertEqual(
            forward_chaining_checking([['s', '&', 'p', '=>', 'q'], ['q', '=>', 'r'], ['s'], ['q']], 'p'),
            (False, set()))

    def test_cycle(self):
        self.assertEqual(
            forward_chaining_checking([['s', '&', 'p', '=>', 'p'], ['s', '&', 'q', '=>', 'p'], ['s'], ['q']], 'p'),
            (True, {'s', 'q', 'p'}))

        self.assertEqual(
            forward_chaining_checking([['p', '=>', 'q'], ['q', '=>', 'p']], 'p'),
            (False, set()))

        self.assertEqual(
            forward_chaining_checking([['s', '&', 'p', '=>', 'p'], ['s']], 'p'),
            (False, set()))

    def test_complex(self):
        self.assertEqual(
            forward_chaining_checking([['p2', '=>', 'p3'], ['p3', '=>', 'p1'], ['c', '=>', 'e'], ['b', '&', 'e', '=>', 'f'], ['f', '&', 'g', '=>', 'h'], ['p1', '=>', 'd'], ['p1', '&', 'p3', '=>', 'c'], ['a'], ['b'], ['p2']], 'd'),
            (True, {'a', 'b', 'p2', 'p3', 'p1', 'd'}))

if __name__ == "__main__":
    unittest.main()