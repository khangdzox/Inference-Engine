import unittest

operators = ['~', '||', '&', '=>', '<=>']

def is_sentence_true(sentence: list[str | bool], model: dict[str, bool]) -> bool:
    """
    Check if the sentence is true in the given model.

    Args:
        sentence (list[str | bool]): the propositional sentence to check.
        model (dict[str, bool]): the model with truth values for propositional variables.
    """
    # process parentheses
    temp_sentence = []
    parentheses_stack = []

    for index, symbol in enumerate(sentence):

        # if find opening parenthese then push its index to stack
        if symbol == "(":
            parentheses_stack.append(index)

        # if find closing parenthese then pop the last opening parenthese index from stack
        elif symbol == ")":
            p_index = parentheses_stack.pop()

            # if find match parentheses then evaluate the sub-sentence and and to temp_sentence
            if len(parentheses_stack) == 0:
                temp_sentence.append(is_sentence_true(sentence[p_index+1:index], model))

        # if in parentheses, don't add value to temp_sentence,
        # because the value between parentheses will be evaluated

        # if not in any parentheses then evaluate symbol and add to temp_sentence
        elif len(parentheses_stack) == 0 and isinstance(symbol, str):
            if symbol in operators:
                temp_sentence.append(symbol)
            else:
                temp_sentence.append(model[symbol])

    sentence = temp_sentence

    # process negation
    while '~' in sentence:
        index = sentence.index('~')
        sentence = sentence[:index] + [not sentence[index+1]] + sentence[index+2:]

    # process conjunction
    while '&' in sentence:
        index = sentence.index('&')
        sentence = sentence[:index-1] + [sentence[index-1] and sentence[index+1]] + sentence[index+2:]

    # process disjunction
    while '||' in sentence:
        index = sentence.index('||')
        sentence = sentence[:index-1] + [sentence[index-1] or sentence[index+1]] + sentence[index+2:]

    # process implication
    while '=>' in sentence:
        index = sentence.index('=>')
        sentence = sentence[:index-1] + [not sentence[index-1] or sentence[index+1]] + sentence[index+2:]

    # process equivalence
    while '<=>' in sentence:
        index = sentence.index('<=>')
        sentence = sentence[:index-1] + [sentence[index-1] == sentence[index+1]] + sentence[index+2:]

    if len(sentence) != 1:
        raise ValueError("Invalid sentence")

    return bool(sentence[0])

# Unit test

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
