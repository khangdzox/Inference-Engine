import unittest

def premise(sentence: list[str]) -> list[str]:
    """
    Return a list of symbol in the sentence's premise

    Args:
        sentence (list[str]): the sentence in Horn form

    Returns:
        list[str]: the list of symbol
    """
    result = []
    for symbol in sentence:
        if symbol == "&":
            continue
        if symbol == "=>":
            break
        result.append(symbol)
    return result

def conclusion(sentence: list[str]) -> str:
    """
    Return the symbol in the sentence's conclusion

    Args:
        sentence (list[str]): the sentence in Horn form

    Returns:
        str: the symbol
    """
    return sentence[-1]

# Unit test

class TestPremise(unittest.TestCase):
    """
    Unit test for premise() function.
    """
    def test_single(self):
        self.assertEqual(premise(['p']), ['p'])

    def test_sentence(self):
        self.assertEqual(premise(['p', '=>', 'q']), ['p'])
        self.assertEqual(premise(['s', '&', 'p', '=>', 'q']), ['s', 'p'])

class TestConclusion(unittest.TestCase):
    """
    Unit test for conclusion() function.
    """
    def test_single(self):
        self.assertEqual(conclusion(['p']), 'p')

    def test_sentence(self):
        self.assertEqual(conclusion(['p', '=>', 'q']), 'q')
        self.assertEqual(conclusion(['s', '&', 'p', '=>', 'k']), 'k')

if __name__ == "__main__":
    unittest.main()
