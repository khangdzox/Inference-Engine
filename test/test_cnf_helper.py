import unittest
from cnf_helper import transform_to_cnf, bidirectional_elemination, implication_elemination, apply_de_morgan, apply_distributivity_or_over_and, get_previous_operand, get_following_operand, add_parentheses_around_operator, get_main_operator, simplify_parentheses, get_inside_parentheses

class TestTransformToCNF(unittest.TestCase):
    """
    Test transform_to_cnf.
    """
    def test_simple(self):
        # Test biconditional elemination
        sentence = ['a', '<=>', 'b']
        sentence = transform_to_cnf(sentence)
        self.assertEqual(sentence, [['~a', 'b'], ['~b', 'a']])

        # Test implication elemination
        sentence = ['a', '=>', 'b']
        sentence = transform_to_cnf(sentence)
        self.assertEqual(sentence, [['~a', 'b']])

        # Test De Morgan's Law
        sentence = ['~', '(', 'a', '&', 'b', ')']
        sentence = transform_to_cnf(sentence)
        self.assertEqual(sentence, [['~a', '~b']])

        # Test Distributivity of & over ||
        sentence = ['a', '||', '(', 'c', '&', 'd', '&', 'e', ')']
        sentence = transform_to_cnf(sentence)
        self.assertEqual(sentence, [['a', 'c'], ['a', 'd'], ['a', 'e']])

    def test_complex(self):
        sentence = ['(', 'a', '<=>', '(', 'c', '=>', '~', 'd', ')', ')', '&', 'b', '&', '(', 'b', '=>', 'a', ')']
        sentence = transform_to_cnf(sentence)
        self.assertEqual(sentence, [['~a', '~c', '~d'], ['c', 'a'], ['d', 'a'], ['b'], ['~b', 'a']])

class TestBidirectionalElemination(unittest.TestCase):
    """
    Test bidirectional_elemination.
    """
    def test_single(self):
        sentence = ['a', '<=>', 'b']
        sentence = bidirectional_elemination(sentence)
        self.assertEqual(sentence, ['(', '(', 'a', '=>', 'b', ')', '&', '(', 'b', '=>', 'a', ')', ')'])

    def test_multiple(self):
        sentence = ['a', '<=>', 'b', '<=>', 'c']
        sentence = bidirectional_elemination(sentence)

        # ((((a => b) & (b => a)) => c) & (c => ((a => b) & (b => a))))
        self.assertEqual(sentence, ['(', '(', '(', '(', 'a', '=>', 'b', ')', '&', '(', 'b', '=>', 'a', ')', ')', '=>', 'c', ')', '&', '(', 'c', '=>', '(', '(', 'a', '=>', 'b', ')', '&', '(', 'b', '=>', 'a', ')', ')', ')', ')'])

    def test_multiple_operands_with_single_operand(self):
        sentence = ['(', 'a', '||', 'b', ')', '<=>', 'c']
        sentence = bidirectional_elemination(sentence)
        # (((a || b ) => c) & (c => (a||b)))
        self.assertEqual(sentence, ['(', '(', '(', 'a', '||', 'b', ')', '=>', 'c', ')', '&', '(', 'c', '=>', '(', 'a', '||', 'b', ')', ')', ')'])

    def test_multiple_operands_with_multiple_operands(self):
        sentence = ['(', 'a', '||', 'b', ')', '<=>', '(', 'c', '||', 'd', ')']
        sentence = bidirectional_elemination(sentence)
        # (((a || b ) => (c || d)) & ((c || d) => (a||b)))
        self.assertEqual(sentence, ['(', '(', '(', 'a', '||', 'b', ')', '=>', '(', 'c', '||', 'd', ')', ')', '&', '(', '(', 'c', '||', 'd', ')', '=>', '(', 'a', '||', 'b', ')', ')', ')'])

    def test_single_operands_with_multiple_operands(self):
        sentence = ['a', '<=>', '(', 'b', '||', 'c', ')']
        sentence = bidirectional_elemination(sentence)
        # ((a => (b || c)) & ((b || c) => a))
        self.assertEqual(sentence, ['(', '(', 'a', '=>', '(', 'b', '||', 'c', ')', ')', '&', '(', '(', 'b', '||', 'c', ')', '=>', 'a', ')', ')'])

    def test_bidirectional_in_bidirectional(self):
        sentence = ['(', 'a', '<=>', 'b', ')', '<=>', '(', 'c', '<=>', 'd', ')']
        sentence = bidirectional_elemination(sentence)
        # ((((a => b) & (b => a)) => ((c => d) & (d => c))) & (((c => d) & (d => c)) => ((a => b) & (b => a))))
        self.assertEqual(sentence, ['(', '(', '(', '(', '(', 'a', '=>', 'b', ')', '&', '(', 'b', '=>', 'a', ')', ')', ')', '=>', '(', '(', '(', 'c', '=>', 'd', ')', '&', '(', 'd', '=>', 'c', ')', ')', ')', ')', '&', '(', '(', '(', '(', 'c', '=>', 'd', ')', '&', '(', 'd', '=>', 'c', ')', ')', ')', '=>', '(', '(', '(', 'a', '=>', 'b', ')', '&', '(', 'b', '=>', 'a', ')', ')', ')', ')', ')'])

class TestImplicationElemination(unittest.TestCase):
    """
    Test implication_elemination.
    """
    def test_single(self):
        sentence = ['a', '=>', 'b']
        sentence = implication_elemination(sentence)
        self.assertEqual(sentence, ['(', '~', 'a', '||', 'b', ')'])

    def test_multiple(self):
        sentence = ['a', '=>', 'b', '=>', 'c']
        sentence = implication_elemination(sentence)
        # (~(~a||b)) || c)
        self.assertEqual(sentence, ['(', '~', '(', '~', 'a', '||', 'b', ')', '||', 'c', ')'])
    def test_multiple_operands_with_single_operand(self):
        sentence = ['(', 'a', '||', 'b', ')', '=>', 'c']
        sentence = implication_elemination(sentence)
        # (~(a||b)) || c)
        self.assertEqual(sentence, ['(', '~', '(', 'a', '||', 'b', ')', '||', 'c', ')'])

    def test_multiple_operands_with_multiple_operands(self):
        sentence = ['(', 'a', '||', 'b', ')', '=>', '(', 'c', '||', 'd', ')']
        sentence = implication_elemination(sentence)
        # (~ (a || b) || (c || d))
        self.assertEqual(sentence, ['(', '~', '(', 'a', '||', 'b', ')', '||', '(', 'c', '||', 'd', ')', ')'])
    def test_single_operands_with_multiple_operands(self):
        sentence = ['a', '=>', '(', 'b', '||', 'c', ')']
        sentence = implication_elemination(sentence)
        # ((~a || (b || c)))
        self.assertEqual(sentence, ['(', '~', 'a', '||', '(', 'b', '||', 'c', ')', ')'])

    def test_bidirectional_in_bidirectional(self):
        sentence = ['(', 'a', '=>', 'b', ')', '=>', '(', 'c', '=>', 'd', ')']
        sentence = implication_elemination(sentence)
        # ((~(~a || b)) || (~c || d))
        self.assertEqual(sentence, ['(', '~', '(', '(', '~', 'a', '||', 'b', ')', ')', '||', '(', '(', '~', 'c', '||', 'd', ')', ')', ')'])

class TestDeMorganLaw(unittest.TestCase):
    """
    Test de_morgan_law.
    """
    def test_single(self):
        sentence = ['~', '(', 'a', '&', 'b', ')']
        sentence = apply_de_morgan(sentence)
        self.assertEqual(sentence, ['(', '~', 'a', '||', '~', 'b', ')'])

        sentence = ['~', '(', 'a', '||', 'b', ')']
        sentence = apply_de_morgan(sentence)
        self.assertEqual(sentence, ['(', '~', 'a', '&', '~', 'b', ')'])

    def test_multiple(self):
        sentence = ['~', '(', 'a', '&', 'b', '&', 'c', ')']
        sentence = apply_de_morgan(sentence)
        self.assertEqual(sentence, ['(', '~', 'a', '||', '~', 'b', '||', '~', 'c', ')'])

        sentence = ['~', '(', 'a', '||', 'b', '||', 'c', ')']
        sentence = apply_de_morgan(sentence)
        self.assertEqual(sentence, ['(', '~', 'a', '&', '~', 'b', '&', '~', 'c', ')'])

    def test_nested(self):
        sentence = ['~', '(', 'a', '&', '(', 'b', '&', 'c', ')', ')']
        sentence = apply_de_morgan(sentence)
        self.assertEqual(sentence, ['(', '~', 'a', '||', '(', '~', 'b', '||', '~', 'c', ')', ')'])

        sentence = ['~', '(', '~', 'a', '||', '(', '~', 'b', '&', 'c', ')', ')']
        sentence = apply_de_morgan(sentence)
        self.assertEqual(sentence, ['(', 'a', '&', '(', 'b', '||', '~', 'c', ')', ')'])

    def test_no_parentheses(self):
        sentence = ['~', 'a', '&', 'b']
        sentence = apply_de_morgan(sentence)
        self.assertEqual(sentence, ['~', 'a', '&', 'b'])

        sentence = ['~', 'a', '||', 'b']
        sentence = apply_de_morgan(sentence)
        self.assertEqual(sentence, ['~', 'a', '||', 'b'])

    def test_with_before_operands_1(self):
        sentence = ['a', '&', '~', '(', 'b', '&', 'c', ')']
        sentence = apply_de_morgan(sentence)
        self.assertEqual(sentence, ['a', '&', '(', '~', 'b', '||', '~', 'c', ')'])

        sentence = ['a', '&', '~', '(', 'b', '||', 'c', ')']
        sentence = apply_de_morgan(sentence)
        self.assertEqual(sentence, ['a', '&', '(', '~', 'b', '&', '~', 'c', ')'])

    def test_with_before_operands_2(self):
        sentence = ['a', '&', '(','~', '(','b', '&', 'c', ')', ')']
        sentence = apply_de_morgan(sentence)
        self.assertEqual(sentence, ['a', '&', '(', '(', '~', 'b', '||', '~', 'c', ')', ')'])

        sentence = ['a', '&', '(','~', '(','b', '||', 'c', ')', ')']
        sentence = apply_de_morgan(sentence)
        self.assertEqual(sentence, ['a', '&', '(', '(', '~', 'b', '&', '~', 'c', ')', ')'])

class TestDistribute(unittest.TestCase):
    """
    Test distribute.
    """
    def test_single_with_multiple(self):
        sentence = ['a', '||', '(', 'b', '&', 'c', ')']
        sentence = apply_distributivity_or_over_and(sentence)
        self.assertEqual(sentence, ['(', 'a', '||', 'b', ')', '&', '(', 'a', '||', 'c', ')'])

    def test_multiple_with_single(self):
        sentence = ['(', 'a', '&', 'b', ')', '||', 'c']
        sentence = apply_distributivity_or_over_and(sentence)
        self.assertEqual(sentence, ['(', 'a', '||', 'c', ')', '&', '(', 'b', '||', 'c', ')'])

    def test_multiple_multiple_with_multiple(self):
        sentence = ['(', 'a', '&', 'b', ')', '||', '(', 'c', '&', 'd', ')', '||', '(', 'e', '&', 'f', ')']
        sentence = apply_distributivity_or_over_and(sentence)
        self.assertEqual(sentence, ['(', 'a', '||', 'c', '||', 'e', ')', '&', '(', 'b', '||', 'c', '||', 'e', ')', '&', '(', 'a', '||', 'd', '||', 'e', ')', '&', '(', 'b', '||', 'd', '||', 'e', ')', '&', '(', 'a', '||', 'c', '||', 'f', ')', '&', '(', 'b', '||', 'c', '||', 'f', ')', '&', '(', 'a', '||', 'd', '||', 'f', ')', '&', '(', 'b', '||', 'd', '||', 'f', ')'])

    def test_complex(self):
        sentence = ['(', 'a', '&', '(', 'b', '||', 'c', ')', ')', '||', '(', 'd', '&', 'e', ')']
        sentence = apply_distributivity_or_over_and(sentence)
        self.assertEqual(sentence, ['(', 'a', '||', 'd', ')', '&', '(', 'b', '||', 'c', '||', 'd', ')', '&', '(', 'a', '||', 'e', ')', '&', '(', 'b', '||', 'c', '||', 'e', ')'])

class TestGetPreviousOperand(unittest.TestCase):
    """
    Test get_previous_operand.
    """

    def test_single(self):
        sentence = ['a', '&', '(', 'b', '||', 'c', ')']
        self.assertEqual(get_previous_operand(sentence, 1), (0, 0))

    def test_parentheses(self):
        sentence = ['(', 'b', '||', 'c', ')', '&', 'a']
        self.assertEqual(get_previous_operand(sentence, 5), (0, 4))

    def test_with_not(self):
        sentence = ['~', 'b', '&', 'a']
        self.assertEqual(get_previous_operand(sentence, 2), (0, 1))

class TestGetFollowingOperand(unittest.TestCase):
    """
    Test get_following_operand.
    """

    def test_single(self):
        sentence = ['a', '&', '(', 'b', '||', 'c', ')']
        self.assertEqual(get_following_operand(sentence, 4), (5, 5))

    def test_parentheses(self):
        sentence = ['a', '&', '(', 'b', '||', 'c', ')']
        self.assertEqual(get_following_operand(sentence, 1), (2, 6))

    def test_negative_one(self):
        sentence = ['a', '&', '(', 'b', '||', 'c', ')']
        self.assertEqual(get_following_operand(sentence, -1), (0, 0))

        sentence = ['(', 'b', '||', 'c', ')', '&', 'a']
        self.assertEqual(get_following_operand(sentence, -1), (0, 4))

    def test_with_not(self):
        sentence = ['a', '&', '~', 'b']
        self.assertEqual(get_following_operand(sentence, 1), (2, 3))

        sentence = ['~', 'a', '&', 'b']
        self.assertEqual(get_following_operand(sentence, -1), (0, 1))

class TestAddParenthesesAroundOperator(unittest.TestCase):
    """
    Test add_parentheses_around_operator.
    """

    def test_single_operator(self):
        sentence = ['a', '&', 'b']
        self.assertEqual(add_parentheses_around_operator(sentence, '&'), ['(', 'a', '&', 'b', ')'])

        sentence = ['a', '&', 'b', '&', 'c']
        self.assertEqual(add_parentheses_around_operator(sentence, '&'), ['(', 'a', '&', 'b', '&', 'c', ')'])

    def test_multiple_operators(self):
        sentence = ['a', '&', 'b', '&', 'c', '||', 'd', '||', 'e', '&', 'f']
        self.assertEqual(add_parentheses_around_operator(sentence, '&'), ['(', 'a', '&', 'b', '&', 'c', ')', '||', 'd', '||', '(', 'e', '&', 'f', ')'])
        self.assertEqual(add_parentheses_around_operator(sentence, '||'), ['a', '&', 'b', '&', '(', 'c', '||', 'd', '||', 'e', ')', '&', 'f'])

    def test_already_have_parentheses(self):
        sentence = ['(', 'a', '&', 'b', ')']
        self.assertEqual(add_parentheses_around_operator(sentence, '&'), ['(', 'a', '&', 'b', ')'])

    def test_with_not(self):
        sentence = ['~', 'a', '&', 'b']
        self.assertEqual(add_parentheses_around_operator(sentence, '&'), ['(', '~', 'a', '&', 'b', ')'])

        sentence = ['~', '(', 'a', '&', 'b', ')', '&', 'c']
        self.assertEqual(add_parentheses_around_operator(sentence, '&'), ['(', '~', '(', 'a', '&', 'b', ')', '&', 'c', ')'])

class TestGetMainOperator(unittest.TestCase):
    """
    Test get_main_operator.
    """

    def test_single_operator(self):
        sentence = ['a', '&', 'b']
        self.assertEqual(get_main_operator(sentence), '&')

        sentence = ['a', '||', 'b', '||', 'c']
        self.assertEqual(get_main_operator(sentence), '||')

    def test_multiple_operators(self):
        sentence = ['a', '&', 'b', '||', 'c']
        self.assertEqual(get_main_operator(sentence), None)

    def test_no_operator(self):
        sentence = ['a']
        self.assertEqual(get_main_operator(sentence), "")

    def test_single_operator_with_parentheses(self):
        sentence = ['(', 'a', '&', 'b', ')', '||', 'c']
        self.assertEqual(get_main_operator(sentence), '||')

        sentence = ['(', 'a', '&', 'b', ')', '&', '(', 'c', '||', 'd', ')']
        self.assertEqual(get_main_operator(sentence), '&')

    def test_multiple_operators_with_parentheses(self):
        sentence = ['(', 'a', '&', 'b', ')', '&', '(', 'c', '||', 'd', ')', '||', 'e']
        self.assertEqual(get_main_operator(sentence), None)

    def test_no_operator_with_parentheses(self):
        sentence = ['(', 'a', '&', 'b', ')']
        self.assertEqual(get_main_operator(sentence), '')

class TestSimplifyParentheses(unittest.TestCase):
    """
    Test simplify_parentheses.
    """

    def test_simple(self):
        sentence = ['(', 'a', '&', 'b', ')']
        self.assertEqual(simplify_parentheses(sentence), ['a', '&', 'b'])

    def test_nested(self):
        sentence = ['(', 'a', '&', '(', 'b', '&', 'c', ')', ')']
        self.assertEqual(simplify_parentheses(sentence), ['a', '&', 'b', '&', 'c'])

        sentence = ['(', 'a', '&', '(', '(', 'b', '&', 'c', ')', ')', ')']
        self.assertEqual(simplify_parentheses(sentence), ['a', '&', 'b', '&', 'c'])

        sentence = ['(', 'a', '&', '(', 'b', '&', '(', 'c', '&', 'd', ')', ')', ')']
        self.assertEqual(simplify_parentheses(sentence), ['a', '&', 'b', '&', 'c', '&', 'd'])

    def test_nested_with_not(self):
        sentence = ['~', '(', 'c', ')']
        self.assertEqual(simplify_parentheses(sentence), ['~', 'c'])

        sentence = ['(', '~', 'a', '&', '(', '~', '(', 'b', '&', 'c', ')', ')', ')']
        self.assertEqual(simplify_parentheses(sentence), ['~', 'a', '&', '~', '(', 'b', '&', 'c', ')'])

        sentence = ['(', 'a', '&', '~', '(', 'b', '&', '(', 'c', '&', '~', 'd', ')', ')', ')']
        self.assertEqual(simplify_parentheses(sentence), ['a', '&', '~', '(', 'b', '&', 'c', '&', '~', 'd', ')'])

    def test_no_parentheses(self):
        sentence = ['a', '&', 'b']
        self.assertEqual(simplify_parentheses(sentence), ['a', '&', 'b'])

    def test_different_operators(self):
        sentence = ['(', 'a', '&', 'b', ')', '||', '(', 'c', '||', 'd', ')']
        self.assertEqual(simplify_parentheses(sentence), ['(', 'a', '&', 'b', ')', '||', 'c', '||', 'd'])

    def test_complex(self):
        sentence = ['(', '(', '~', '(', '(', '~', 'c', '||', '~', 'd', ')', ')', '||', 'a', ')', ')']
        self.assertEqual(simplify_parentheses(sentence), ['~', '(', '~', 'c', '||', '~', 'd', ')', '||', 'a'])

class TestGetInsideParentheses(unittest.TestCase):
    """
    Test get_inside_parentheses.
    """

    def test_simple(self):
        sentence = ['(', 'a', '&', 'b', ')']
        self.assertEqual(get_inside_parentheses(sentence, 0, 4), (1, 3))

    def test_complex(self):
        sentence = ['(', 'a', '&', '(', 'b', '&', '(', 'c', '&', 'd', ')', ')', ')']
        self.assertEqual(get_inside_parentheses(sentence, 3, 11), (4, 10))

    def test_with_not(self):
        sentence = ['(', '~', '(', 'a', '&', 'b', ')', ')']
        self.assertEqual(get_inside_parentheses(sentence, 1, 6), (3, 5))

if __name__ == "__main__":
    unittest.main()
