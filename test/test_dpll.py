import unittest
from dpll import find_pure_symbol, find_unit_clause, is_clause_true

class TestFindPureSymbol(unittest.TestCase):
    """
    Test find_pure_symbol.
    """

    def test_empty_model(self):
        symbols = ['a', 'b', 'c']
        clauses = [['a', '~b'], ['~b', 'c'], ['~c', 'a']]
        model = {}
        self.assertEqual(find_pure_symbol(symbols, clauses, model), ('a', True))

    def test_with_model(self):
        symbols = ['a', 'b', 'c']
        clauses = [['a', '~b'], ['~b', 'c'], ['~c', '~a']]
        model = {'b': False}
        self.assertEqual(find_pure_symbol(symbols, clauses, model), ('a', False))

    def test_none(self):
        symbols = ['a', 'b', 'c']
        clauses = [['a', '~b'], ['b', 'c'], ['~c', '~a'], ['a']]
        model = {'b': False}
        self.assertEqual(find_pure_symbol(symbols, clauses, model), (None, False))

class TestFindUnitClause(unittest.TestCase):
    """
    Test find_unit_clause.
    """

    def test_single_element_clause(self):
        clauses = [['a', '~b'], ['~c'], ['c', 'a']]
        model = {}
        self.assertEqual(find_unit_clause(clauses, model), ('c', False))

    def test_unit_clause_1(self):
        clauses = [['a', '~b', 'c'], ['~b', 'c']]
        model = {'b': True, 'c': False}
        self.assertEqual(find_unit_clause(clauses, model), ('a', True))

    def test_unit_clause_2(self):
        clauses = [['a', '~b', 'c'], ['~b', 'c']]
        model = {'b': True}
        self.assertEqual(find_unit_clause(clauses, model), ('c', True))

    def test_none(self):
        clauses = [['a', '~b', 'c'], ['~b', 'c', 'd']]
        model = {'b': True}
        self.assertEqual(find_unit_clause(clauses, model), (None, False))

class TestIsClauseTrue(unittest.TestCase):
    """
    Test is_clause_true.
    """

    def test_true(self):
        self.assertTrue(is_clause_true(['a', '~b', 'c'], {'b': False}))

    def test_false(self):
        self.assertFalse(is_clause_true(['a', '~b', 'c'], {'a': False, 'b': True, 'c': False}))

    def test_none(self):
        self.assertIsNone(is_clause_true(['a', '~b', 'c'], {'a': False, 'c': False}))

if __name__ == '__main__':
    unittest.main()
