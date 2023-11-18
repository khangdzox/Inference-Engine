import unittest
from cnf_helper import add_parentheses_around_operator, and_or_tranformation, get_main_operator, get_previous_operand, get_following_operand, simplify_parentheses

class TestAndOrTransformation(unittest.TestCase):
    """
    Test and_or_transformation.

    Args:
        unittest (_type_): _description_
    """
    def test_and_or_transformation(self):
        # Test biconditional elemination
        sentence = ['a', '<=>', 'b']
        sentence = and_or_tranformation(sentence)
        self.assertEqual(sentence, ['(', '~', 'a', '||', 'b', ')', '&', '(', '~', 'b', '||', 'a', ')'])

        # Test implication elemination
        sentence = ['a', '=>', 'b']
        sentence = and_or_tranformation(sentence)
        self.assertEqual(sentence, ['(', '~', 'a', '||', 'b', ')'])

        # Test De Morgan's Law
        sentence = ['~', '(', 'a', '&', 'b', ')']
        sentence = and_or_tranformation(sentence)
        self.assertEqual(sentence, ['(', '~', 'a', '||', '~', 'b', ')'])

        # Test Distributivity of & over ||
        sentence = ['a', '||', '(', 'c', '&', 'd', '&', 'e', ')']
        sentence = and_or_tranformation(sentence)
        print(sentence)
        self.assertEqual(sentence, ['(', 'a', '||', 'c', ')', '&', '(', 'a', '||', 'd', ')', '&', '(', 'a', '||', 'e', ')'])

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

    def test_multiple(self):
        sentence = ['(', 'a', '&', '(', 'b', '&', 'c', ')', ')']
        self.assertEqual(simplify_parentheses(sentence), ['a', '&', 'b', '&', 'c'])

    def test_nested(self):
        sentence = ['(', 'a', '&', '(', 'b', '&', '(', 'c', '&', 'd', ')', ')', ')']
        self.assertEqual(simplify_parentheses(sentence), ['a', '&', 'b', '&', 'c', '&', 'd'])

    def test_no_parentheses(self):
        sentence = ['a', '&', 'b']
        self.assertEqual(simplify_parentheses(sentence), ['a', '&', 'b'])

    def test_different_operators(self):
        sentence = ['(', 'a', '&', 'b', ')', '||', '(', 'c', '||', 'd', ')']
        self.assertEqual(simplify_parentheses(sentence), ['(', 'a', '&', 'b', ')', '||', 'c', '||', 'd'])
