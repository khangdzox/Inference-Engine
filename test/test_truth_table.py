import unittest
from truth_table import is_sentence_true

class TestIsSentenceTrue(unittest.TestCase):
    """
    Unit test for is_sentence_true() function.
    """
    def test_simple_sentence(self):
        self.assertTrue(is_sentence_true(['p'], {'p': True}))
        self.assertFalse(is_sentence_true(['p'], {'p': False}))

    def test_not(self):
        self.assertTrue(is_sentence_true(['~', 'p'], {'p': False}))
        self.assertFalse(is_sentence_true(['~', 'p'], {'p': True}))

    def test_or(self):
        self.assertTrue(is_sentence_true(['p', '||', 'q'], {'p': True, 'q': False}))
        self.assertTrue(is_sentence_true(['p', '||', 'q'], {'p': False, 'q': True}))
        self.assertTrue(is_sentence_true(['p', '||', 'q'], {'p': True, 'q': True}))
        self.assertFalse(is_sentence_true(['p', '||', 'q'], {'p': False, 'q': False}))

    def test_and(self):
        self.assertTrue(is_sentence_true(['p', '&', 'q'], {'p': True, 'q': True}))
        self.assertFalse(is_sentence_true(['p', '&', 'q'], {'p': True, 'q': False}))
        self.assertFalse(is_sentence_true(['p', '&', 'q'], {'p': False, 'q': True}))
        self.assertFalse(is_sentence_true(['p', '&', 'q'], {'p': False, 'q': False}))

    def test_implies(self):
        self.assertTrue(is_sentence_true(['p', '=>', 'q'], {'p': False, 'q': True}))
        self.assertTrue(is_sentence_true(['p', '=>', 'q'], {'p': True, 'q': True}))
        self.assertTrue(is_sentence_true(['p', '=>', 'q'], {'p': False, 'q': False}))
        self.assertFalse(is_sentence_true(['p', '=>', 'q'], {'p': True, 'q': False}))

    def test_iff(self):
        self.assertTrue(is_sentence_true(['p', '<=>', 'q'], {'p': True, 'q': True}))
        self.assertTrue(is_sentence_true(['p', '<=>', 'q'], {'p': False, 'q': False}))
        self.assertFalse(is_sentence_true(['p', '<=>', 'q'], {'p': True, 'q': False}))
        self.assertFalse(is_sentence_true(['p', '<=>', 'q'], {'p': False, 'q': True}))

    def test_parentheses(self):
        self.assertTrue(is_sentence_true(['(', 'p', ')'], {'p': True}))
        self.assertFalse(is_sentence_true(['(', 'p', '||', 'q', ')', '&', 'r'], {'p': False, 'q': True, 'r': False}))
        self.assertTrue(is_sentence_true(['(', 'p', '=>', 'q', ')', '<=>', '(', 'r', ')', '&', '~', 's'], {'p': False, 'q': True, 'r': True, 's': False}))
        self.assertFalse(is_sentence_true(['~', '(', 'A', '&', 'B', ')', '||', '(', 'C', '<=>', 'D', ')', '=>', 'E', '&', '(', 'F', '||', '~', 'G', ')'], {'A': True, 'B': False, 'C': False, 'D': True, 'E': True, 'F': False, 'G': True}))
        self.assertFalse(is_sentence_true(['(', 'A', '&', '(', 'B', '||', 'C', ')', ')', '=>', '(', 'D', '&', '(', 'E', '||', '~', 'F', ')', '<=>', '(', 'G', '||', 'H', ')', ')'], {'A': True, 'B': False, 'C': True, 'D': True, 'E': False, 'F': True, 'G': True, 'H': False}))


if __name__ == "__main__":
    unittest.main()
