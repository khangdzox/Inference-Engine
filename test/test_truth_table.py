
import unittest
from truth_table import is_sentence_true, truth_table_checking

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

class TestTruthTableAlgorithm(unittest.TestCase):
    """
    Unit test for truth_table_checking() function.
    """
    def test_truth_table_checking(self):
        # Test case 1
        kb = [['p2', '=>', 'p3'], ['p3', '=>', 'p1'], ['c', '=>', 'e'], ['b', '&', 'e', '=>', 'f'], ['f', '&', 'g', '=>', 'h'], ['p1', '=>', 'd'], ['p1', '&', 'p3', '=>', 'c'], ['a'], ['b'], ['p2']]
        query = ['d']
        symbols = ['p2', 'p3', 'p1', 'c', 'e', 'b', 'f', 'g', 'h', 'd', 'a']
        result, count = truth_table_checking(kb, query, symbols)
        self.assertTrue(result)
        self.assertEqual(count, 3)

        # Test case 2
        kb = [['s', '&', 'p', '=>', 'p'], ['s', '&', 'q', '=>', 'p'], ['s'], ['q']]
        query = ['p']
        symbols = ['s', 'p', 'q']
        result, count = truth_table_checking(kb, query, symbols)
        self.assertTrue(result)
        self.assertEqual(count, 1)

        # Test case 3
        kb = [['a', '=>', 'b'], ['b']]
        query = ['a']
        symbols = ['a', 'b']
        result, count = truth_table_checking(kb, query, symbols)
        self.assertFalse(result)
        self.assertEqual(count, 2)

if __name__ == "__main__":
    unittest.main()
