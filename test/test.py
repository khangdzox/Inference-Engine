import unittest
from truth_table import truth_table_checking
from forward_chaining import forward_chaining_checking
from backward_chaining import backward_chaining_checking
from resolution import resolution_checking
from dpll import dpll_checking

class TestTruthTableChecking(unittest.TestCase):
    """
    Test truth_table_checking.
    """
    # Horn-form knowledge base
    # TELL
    # p2 => p3; p3 => p1; c => e; b&e => f; f&g => h; p1 => d; p1&p3 => c; a; b; p2;
    # ASK
    # d
    def test_case_1(self):
        kb = [['p2', '=>', 'p3'], ['p3', '=>', 'p1'], ['c', '=>', 'e'], ['b', '&', 'e', '=>', 'f'], ['f', '&', 'g', '=>', 'h'], ['p1', '=>', 'd'], ['p1', '&', 'p3', '=>', 'c'], ['a'], ['b'], ['p2']]
        query = ['d']
        symbols = ['p2', 'p3', 'p1', 'c', 'e', 'b', 'f', 'g', 'h', 'd', 'a']
        result, count = truth_table_checking(kb, query, symbols)
        self.assertTrue(result)
        self.assertEqual(count, 3)

    # General knowledge base
    # TELL
    # (a <=> (c => ~d)) & b & (b => a); c; ~f || g;
    # ASK
    # d
    def test_case_2(self):
        kb = [['(', 'a', '<=>', '(', 'c', '=>', '~', 'd', ')', ')', '&', 'b', '&', '(', 'b', '=>', 'a', ')'], ['c'], ['~', 'f', '||', 'g']]
        query = ['d']
        symbols = ['a', 'c', 'd', 'b', 'f', 'g']
        result, _ = truth_table_checking(kb, query, symbols)
        self.assertFalse(result)

    # General knowledge base
    # TELL
    # (a <=> (c => ~d)) & b & (b => a); c; ~f || g;
    # ASK
    # ~d & (~g => ~f)
    def test_case_3(self):
        kb = [['(', 'a', '<=>', '(', 'c', '=>', '~', 'd', ')', ')', '&', 'b', '&', '(', 'b', '=>', 'a', ')'], ['c'], ['~', 'f', '||', 'g']]
        query = ['~', 'd', '&', '(', '~', 'g', '=>', '~', 'f', ')']
        symbols = ['a', 'c', 'd', 'b', 'f', 'g']
        result, count = truth_table_checking(kb, query, symbols)
        self.assertTrue(result)
        self.assertEqual(count, 3)

    # Horn-form knowledge base
    # TELL
    # x => y; y => z; z => w; a&b => x; c&d => a; w&e => c; ~b
    # ASK
    # e
    def test_case_4(self):
        kb = [['x', '=>', 'y'], ['y', '=>', 'z'], ['z', '=>', 'w'], ['a', '&', 'b', '=>', 'x'], ['c', '&', 'd', '=>', 'a'], ['w', '&', 'e', '=>', 'c'], ['~', 'b']]
        query = ['e']
        symbols = ['x', 'y', 'z', 'w', 'a', 'b', 'c', 'd', 'e']
        result, _ = truth_table_checking(kb, query, symbols)
        self.assertFalse(result)

    # General knowledge base
    # TELL
    # p => q; q & r; s || ~t; u & v <=> p; r & w => s; ~u
    # ASK
    # t || ~v
    def test_case_5(self):
        kb = [['p', '=>', 'q'], ['q', '&', 'r'], ['s', '||', '~', 't'], ['u', '&', 'v', '<=>', 'p'], ['r', '&', 'w', '=>', 's'], ['~', 'u']]
        query = ['t', '||', '~', 'v']
        symbols = ['p', 'q', 'r', 's', 't', 'u', 'v', 'w']
        result, _ = truth_table_checking(kb, query, symbols)
        self.assertFalse(result)

class TestForwardChaining(unittest.TestCase):
    """
    Test forward_chaining_checking.
    """
    # Horn-form knowledge base
    # TELL
    # p2 => p3; p3 => p1; c => e; b&e => f; f&g => h; p1 => d; p1&p3 => c; a; b; p2;
    # ASK
    # d
    def test_case_1(self):
        kb = [['p2', '=>', 'p3'], ['p3', '=>', 'p1'], ['c', '=>', 'e'], ['b', '&', 'e', '=>', 'f'], ['f', '&', 'g', '=>', 'h'], ['p1', '=>', 'd'], ['p1', '&', 'p3', '=>', 'c'], ['a'], ['b'], ['p2']]
        query = 'd'
        result, inferred = forward_chaining_checking(kb, query)
        self.assertTrue(result)
        self.assertEqual(inferred, {'a', 'p3', 'p1', 'd', 'p2', 'b'})

    # Horn-form knowledge base
    # TELL
    # x => y; y => z; z => w; a&b => x; c&d => a; w&e => c; ~b
    # ASK
    # e
    def test_case_2(self):
        kb = [['x', '=>', 'y'], ['y', '=>', 'z'], ['z', '=>', 'w'], ['a', '&', 'b', '=>', 'x'], ['c', '&', 'd', '=>', 'a'], ['w', '&', 'e', '=>', 'c'], ['~', 'b']]
        query = 'e'
        result, _ = forward_chaining_checking(kb, query)
        self.assertFalse(result)

class TestBackwardChaining(unittest.TestCase):
    """
    Test backward_chaining_checking.
    """
    # Horn-form knowledge base
    # TELL
    # p2 => p3; p3 => p1; c => e; b&e => f; f&g => h; p1 => d; p1&p3 => c; a; b; p2;
    # ASK
    # d
    def test_case_1(self):
        kb = [['p2', '=>', 'p3'], ['p3', '=>', 'p1'], ['c', '=>', 'e'], ['b', '&', 'e', '=>', 'f'], ['f', '&', 'g', '=>', 'h'], ['p1', '=>', 'd'], ['p1', '&', 'p3', '=>', 'c'], ['a'], ['b'], ['p2']]
        query = 'd'
        result, inferred = backward_chaining_checking(kb, query)
        self.assertTrue(result)
        self.assertEqual(inferred, {'p2', 'p3', 'p1', 'd'})

    # Horn-form knowledge base
    # TELL
    # x => y; y => z; z => w; a&b => x; c&d => a; w&e => c; ~b
    # ASK
    # e
    def test_case_2(self):
        kb = [['x', '=>', 'y'], ['y', '=>', 'z'], ['z', '=>', 'w'], ['a', '&', 'b', '=>', 'x'], ['c', '&', 'd', '=>', 'a'], ['w', '&', 'e', '=>', 'c'], ['~', 'b']]
        query = 'e'
        result, _ = backward_chaining_checking(kb, query)
        self.assertFalse(result)

class TestResolutionChecking(unittest.TestCase):
    """
    Test resolution_checking.
    """
    # Horn-form knowledge base
    # TELL
    # p2 => p3; p3 => p1; c => e; b&e => f; f&g => h; p1 => d; p1&p3 => c; a; b; p2;
    # ASK
    # d
    def test_case_1(self):
        kb = [['p2', '=>', 'p3'], ['p3', '=>', 'p1'], ['c', '=>', 'e'], ['b', '&', 'e', '=>', 'f'], ['f', '&', 'g', '=>', 'h'], ['p1', '=>', 'd'], ['p1', '&', 'p3', '=>', 'c'], ['a'], ['b'], ['p2']]
        query = ['d']
        result = resolution_checking(kb, query)
        self.assertTrue(result)

    # General knowledge base
    # TELL
    # (a <=> (c => ~d)) & b & (b => a); c; ~f || g;
    # ASK
    # d
    def test_case_2(self):
        kb = [['(', 'a', '<=>', '(', 'c', '=>', '~', 'd', ')', ')', '&', 'b', '&', '(', 'b', '=>', 'a', ')'], ['c'], ['~', 'f', '||', 'g']]
        query = ['d']
        result = resolution_checking(kb, query)
        self.assertFalse(result)

    # General knowledge base
    # TELL
    # (a <=> (c => ~d)) & b & (b => a); c; ~f || g;
    # ASK
    # ~d & (~g => ~f)
    def test_case_3(self):
        kb = [['(', 'a', '<=>', '(', 'c', '=>', '~', 'd', ')', ')', '&', 'b', '&', '(', 'b', '=>', 'a', ')'], ['c'], ['~', 'f', '||', 'g']]
        query = ['~', 'd', '&', '(', '~', 'g', '=>', '~', 'f', ')']
        result = resolution_checking(kb, query)
        self.assertTrue(result)

    # Horn-form knowledge base
    # TELL
    # x => y; y => z; z => w; a&b => x; c&d => a; w&e => c; ~b
    # ASK
    # e
    def test_case_4(self):
        kb = [['x', '=>', 'y'], ['y', '=>', 'z'], ['z', '=>', 'w'], ['a', '&', 'b', '=>', 'x'], ['c', '&', 'd', '=>', 'a'], ['w', '&', 'e', '=>', 'c'], ['~', 'b']]
        query = ['e']
        result = resolution_checking(kb, query)
        self.assertFalse(result)

    # General knowledge base
    # TELL
    # p => q; q & r; s || ~t; u & v <=> p; r & w => s; ~u
    # ASK
    # t || ~v
    def test_case_5(self):
        kb = [['p', '=>', 'q'], ['q', '&', 'r'], ['s', '||', '~', 't'], ['u', '&', 'v', '<=>', 'p'], ['r', '&', 'w', '=>', 's'], ['~', 'u']]
        query = ['t', '||', '~', 'v']
        result = resolution_checking(kb, query)
        self.assertFalse(result)

class TestDPLLChecking(unittest.TestCase):
    """
    Test dpll_checking.
    """
    # Horn-form knowledge base
    # TELL
    # p2 => p3; p3 => p1; c => e; b&e => f; f&g => h; p1 => d; p1&p3 => c; a; b; p2;
    # ASK
    def test_case_1(self):
        # d
        kb = [['p2', '=>', 'p3'], ['p3', '=>', 'p1'], ['c', '=>', 'e'], ['b', '&', 'e', '=>', 'f'], ['f', '&', 'g', '=>', 'h'], ['p1', '=>', 'd'], ['p1', '&', 'p3', '=>', 'c'], ['a'], ['b'], ['p2']]
        query = ['d']
        symbols = ['p2', 'p3', 'p1', 'c', 'e', 'b', 'f', 'g', 'h', 'd', 'a']
        result = dpll_checking(kb, query, symbols)
        self.assertTrue(result)

    # General knowledge base
    # TELL
    # (a <=> (c => ~d)) & b & (b => a); c; ~f || g;
    # ASK
    # d
    def test_case_2(self):
        kb = [['(', 'a', '<=>', '(', 'c', '=>', '~', 'd', ')', ')', '&', 'b', '&', '(', 'b', '=>', 'a', ')'], ['c'], ['~', 'f', '||', 'g']]
        query = ['d']
        symbols = ['a', 'c', 'd', 'b', 'f', 'g']
        result = dpll_checking(kb, query, symbols)
        self.assertFalse(result)

    # General knowledge base
    # TELL
    # (a <=> (c => ~d)) & b & (b => a); c; ~f || g;
    # ASK
    # ~d & (~g => ~f)
    def test_case_3(self):
        kb = [['(', 'a', '<=>', '(', 'c', '=>', '~', 'd', ')', ')', '&', 'b', '&', '(', 'b', '=>', 'a', ')'], ['c'], ['~', 'f', '||', 'g']]
        query = ['~', 'd', '&', '(', '~', 'g', '=>', '~', 'f', ')']
        symbols = ['a', 'c', 'd', 'b', 'f', 'g']
        result = dpll_checking(kb, query, symbols)
        self.assertTrue(result)

    # Horn-form knowledge base
    # TELL
    # x => y; y => z; z => w; a&b => x; c&d => a; w&e => c; ~b
    # ASK
    # e
    def test_case_4(self):
        kb = [['x', '=>', 'y'], ['y', '=>', 'z'], ['z', '=>', 'w'], ['a', '&', 'b', '=>', 'x'], ['c', '&', 'd', '=>', 'a'], ['w', '&', 'e', '=>', 'c'], ['~', 'b']]
        query = ['e']
        symbols = ['x', 'y', 'z', 'w', 'a', 'b', 'c', 'd', 'e']
        result = dpll_checking(kb, query, symbols)
        self.assertFalse(result)

    # General knowledge base
    # TELL
    # p => q; q & r; s || ~t; u & v <=> p; r & w => s; ~u
    # ASK
    # t || ~v
    def test_case_5(self):
        kb = [['p', '=>', 'q'], ['q', '&', 'r'], ['s', '||', '~', 't'], ['u', '&', 'v', '<=>', 'p'], ['r', '&', 'w', '=>', 's'], ['~', 'u']]
        query = ['t', '||', '~', 'v']
        symbols = ['p', 'q', 'r', 's', 't', 'u', 'v', 'w']
        result = dpll_checking(kb, query, symbols)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
