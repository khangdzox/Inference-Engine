import unittest
from backward_chaining import backward_chaining_checking

class TestBackwardChaining(unittest.TestCase):
    """
    Unit test for backward_chaining() function.
    """
    def test_single(self):
        self.assertTrue(backward_chaining_checking([['p']], 'p'))
        self.assertFalse(backward_chaining_checking([['p']], 'q'))

    def test_implication(self):
        self.assertTrue(backward_chaining_checking([['p', '=>', 'q'], ['p']], 'q'))
        self.assertFalse(backward_chaining_checking([['p', '=>', 'q'], ['q']], 'p'))

    def test_sentences(self):
        self.assertTrue(backward_chaining_checking([['s', '&', 'p', '=>', 'q'], ['q', '=>', 'r'], ['s'], ['p']], 'r'))
        self.assertFalse(backward_chaining_checking([['s', '&', 'p', '=>', 'q'], ['q', '=>', 'r'], ['s'], ['q']], 'p'))

    def test_cycle(self):
        self.assertTrue(backward_chaining_checking([['s', '&', 'p', '=>', 'p'], ['s', '&', 'q', '=>', 'p'], ['s'], ['q']], 'p'))
        self.assertFalse(backward_chaining_checking([['p', '=>', 'q'], ['q', '=>', 'p']], 'p'))
        self.assertFalse(backward_chaining_checking([['s', '&', 'p', '=>', 'p'], ['s']], 'p'))

if __name__ == "__main__":
    unittest.main()
