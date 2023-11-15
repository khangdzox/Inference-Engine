import unittest
from backward_chaining import backward_chaining_checking

class TestBackwardChaining(unittest.TestCase):
    """
    Unit test for backward_chaining() function.
    """
    def test_single(self):
        self.assertEqual(backward_chaining_checking([['p']], 'p'), (True, {'p'}))
        self.assertEqual(backward_chaining_checking([['p']], 'q'), (False, set()))

    def test_implication(self):
        self.assertEqual(backward_chaining_checking([['p', '=>', 'q'], ['p']], 'q'), (True, {'p', 'q'}))
        self.assertEqual(backward_chaining_checking([['p', '=>', 'q'], ['q']], 'p'), (False, set()))

    def test_sentences(self):
        self.assertEqual(
            backward_chaining_checking([['s', '&', 'p', '=>', 'q'], ['q', '=>', 'r'], ['s'], ['p']], 'r'),
            (True, {'s', 'p', 'q', 'r'}))

        self.assertEqual(
            backward_chaining_checking([['s', '&', 'p', '=>', 'q'], ['q', '=>', 'r'], ['s'], ['q']], 'p'),
            (False, set()))

    def test_cycle(self):
        self.assertEqual(
            backward_chaining_checking([['s', '&', 'p', '=>', 'p'], ['s', '&', 'q', '=>', 'p'], ['s'], ['q']], 'p'),
            (True, {'s', 'q', 'p'}))

        self.assertEqual(
            backward_chaining_checking([['p', '=>', 'q'], ['q', '=>', 'p']], 'p'),
            (False, set()))

        self.assertEqual(
            backward_chaining_checking([['s', '&', 'p', '=>', 'p'], ['s']], 'p'),
            (False, set()))

    def test_complex(self):
        self.assertEqual(
            backward_chaining_checking([['p2', '=>', 'p3'], ['p3', '=>', 'p1'], ['c', '=>', 'e'], ['b', '&', 'e', '=>', 'f'], ['f', '&', 'g', '=>', 'h'], ['p1', '=>', 'd'], ['p1', '&', 'p3', '=>', 'c'], ['a'], ['b'], ['p2']], 'd'),
            (True, {'p2', 'p3', 'p1', 'd'}))

if __name__ == "__main__":
    unittest.main()
