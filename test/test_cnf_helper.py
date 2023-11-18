import unittest
from cnf_helper import *

class TestCnfHelper(unittest.TestCase):
    def test_and_or_transformation(self):
        # Test biconditional elemination
        sentence = ['a', '<=>', 'b']
        sentence = and_or_tranformation(sentence)
        self.assertEqual(sentence, [['(', '~', 'a', '||', 'b', ')'], '&', ['(', '~', 'b', '||', 'a', ')']])

        # Test implication elemination
        sentence = ['a', '=>', 'b']
        sentence = and_or_tranformation(sentence)
        self.assertEqual(sentence, [['(', '~', 'a', '||', 'b', ')']])

        # Test De Morgan's Law
        sentence = ['~', '(', 'a', '&', 'b', ')']
        sentence = and_or_tranformation(sentence)
        self.assertEqual(sentence, ['(', '~', 'a', '||', '~', 'b', ')'])

        # Test Distributivity of & over ||
        sentence = ['a', '||', '(', 'c', '&', 'd', '&', 'e', ')']
        sentence = and_or_tranformation(sentence)
        print(sentence)
        self.assertEqual(sentence, ['(', 'a', '||', 'c', ')', '&', '(', 'a', '||', 'd', ')', '&', '(', 'a', '||', 'e', ')'])