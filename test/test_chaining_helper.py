import unittest
from chaining_helper import premise, conclusion

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
