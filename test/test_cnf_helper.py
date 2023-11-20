import unittest
from cnf_helper import *

class TestAndOrTransformation(unittest.TestCase):
    """
    Test and_or_transformation.

    Args:
        unittest (_type_): _description_
    """
    # def test_and_or_transformation(self):
    #     # Test biconditional elemination
    #     sentence = ['a', '<=>', 'b']
    #     sentence = and_or_tranformation(sentence)
    #     self.assertEqual(sentence, ['(', '~', 'a', '||', 'b', ')', '&', '(', '~', 'b', '||', 'a', ')'])

    #     # Test implication elemination
    #     sentence = ['a', '=>', 'b']
    #     sentence = and_or_tranformation(sentence)
    #     self.assertEqual(sentence, ['(', '~', 'a', '||', 'b', ')'])

    #     # Test De Morgan's Law
    #     sentence = ['~', '(', 'a', '&', 'b', ')']
    #     sentence = and_or_tranformation(sentence)
    #     self.assertEqual(sentence, ['(', '~', 'a', '||', '~', 'b', ')'])

    #     # Test Distributivity of & over ||
    #     sentence = ['a', '||', '(', 'c', '&', 'd', '&', 'e', ')']
    #     sentence = and_or_tranformation(sentence)
    #     print(sentence)
    #     self.assertEqual(sentence, ['(', 'a', '||', 'c', ')', '&', '(', 'a', '||', 'd', ')', '&', '(', 'a', '||', 'e', ')'])

class TestBidirectionalElemination(unittest.TestCase):
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
    def test_single(self):
        sentence = ['~', '(', 'a', '&', 'b', ')']
        sentence = de_morgan_law(sentence)
        self.assertEqual(sentence, ['(', '~', 'a', '||', '~', 'b', ')'])

        sentence = ['~', '(', 'a', '||', 'b', ')']
        sentence = de_morgan_law(sentence)
        self.assertEqual(sentence, ['(', '~', 'a', '&', '~', 'b', ')'])

    def test_multiple(self):
        sentence = ['~', '(', 'a', '&', 'b', '&', 'c', ')']
        sentence = de_morgan_law(sentence)
        self.assertEqual(sentence, ['(', '~', 'a', '||', '~', 'b', '||', '~', 'c', ')'])

        sentence = ['~', '(', 'a', '||', 'b', '||', 'c', ')']
        sentence = de_morgan_law(sentence)
        self.assertEqual(sentence, ['(', '~', 'a', '&', '~', 'b', '&', '~', 'c', ')'])

    def test_nested(self):
        sentence = ['~', '(', 'a', '&', '(', 'b', '&', 'c', ')', ')']
        sentence = de_morgan_law(sentence)
        self.assertEqual(sentence, ['(', '~', 'a', '||', '~', 'b', '||', '~', 'c', ')'])

        sentence = ['~', '(', 'a', '||', '(', 'b', '||', 'c', ')', ')']
        sentence = de_morgan_law(sentence)
        self.assertEqual(sentence, ['(', '~', 'a', '&', '~', 'b', '&', '~', 'c', ')'])

    def test_no_parentheses(self):
        sentence = ['~', 'a', '&', 'b']
        sentence = de_morgan_law(sentence)
        self.assertEqual(sentence, ['~', 'a', '&', 'b'])

        sentence = ['~', 'a', '||', 'b']
        sentence = de_morgan_law(sentence)
        self.assertEqual(sentence, ['~', 'a', '||', 'b'])

    def test_with_before_operands_1(self):
        sentence = ['a', '&', '~', '(', 'b', '&', 'c', ')']
        sentence = de_morgan_law(sentence)
        self.assertEqual(sentence, ['a', '&', '(', '~', 'b', '||', '~', 'c', ')'])

        sentence = ['a', '&', '~', '(', 'b', '||', 'c', ')']
        sentence = de_morgan_law(sentence)
        self.assertEqual(sentence, ['a', '&', '(', '~', 'b', '&', '~', 'c', ')'])

    def test_with_before_operands_2(self):
        sentence = ['a', '&', '(','~', '(','b', '&', 'c', ')', ')']
        sentence = de_morgan_law(sentence)
        self.assertEqual(sentence, ['a', '&', '(', '(', '~', 'b', '||', '~', 'c', ')', ')'])

        sentence = ['a', '&', '(','~', '(','b', '||', 'c', ')', ')']
        sentence = de_morgan_law(sentence)
        self.assertEqual(sentence, ['a', '&', '(', '(', '~', 'b', '&', '~', 'c', ')', ')'])

class TestDistribute(unittest.TestCase):
    def test_single_with_multiple(self):
        sentence = ['a', '||', '(', 'b', '&', 'c', ')']
        sentence = distribute(sentence)
        self.assertEqual(sentence, ['(', 'a', '||', 'b', ')', '&', '(', 'a', '||', 'c', ')'])

    def test_multiple_with_multiple(self):
        sentence = ['(', 'a', '&', 'b', ')', '||', '(', 'c', '&', 'd', ')'] 
        sentence = distribute(sentence)
        # ((a & b) || c) & ((a & b) || d))
        self.assertEqual(sentence, ['(', '(', 'a', '&', 'b', ')', '||', 'c', ')', '&', '(', '(', 'a', '&', 'b', ')', '||', 'd', ')'])

    def test_multiple_multiple_with_multiple(self):
        sentence = ['(', '(', 'a', '&', 'b', ')', '||', 'c', ')', '&', '(', '(', 'a', '&', 'b', ')', '||', 'd', ')', '||', '(', 'e', '&', 'f', ')']
        while ('||' in sentence) and (sentence[sentence.index('||') + 1] == '('):
            print("exist")
        sentence = distribute(sentence)
        print (sentence)
        # (((a & b) || c) & ((a & b) || d)) || e) & (((a & b) || c) & ((a & b) || d)) || f)
        # self.assertEqual(sentence, ['(', '(', 'a', '&', 'b', ')', '||', 'c', ')', '&', '(', '(', 'a', '&', 'b', ')', '||', 'd', ')', ')', '||', 'e', ')', '&', '(', '(', '(', '(', 'a', '&', 'b', ')', '||', 'c', ')', '&', '(', '(', 'a', '&', 'b', ')', '||', 'd', ')', ')', '||', 'f', ')'])

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
