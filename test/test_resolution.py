import unittest
from resolution import resolve, resolution

class TestResolve(unittest.TestCase):
    """
    Test resolve.
    """

    def test_resolve_part(self):
        self.assertEqual(set(resolve(['~a', 'b'], ['~b', 'c'])), {'~a', 'c'})
        self.assertEqual(set(resolve(['~a', 'b', 'c', '~d'], ['~a', '~b', '~c'])), {'~a', '~d'})

    def test_resolve_all(self):
        self.assertEqual(resolve(['~a', 'b'], ['a', '~b']), [])
        self.assertEqual(resolve(['~a', 'b', 'c', '~d'], ['a', '~b', '~c', 'd']), [])

    def test_resolve_none(self):
        self.assertEqual(set(resolve(['~a', 'b', 'c', '~d'], ['~a', '~d', '~e'])), {'~a', 'b', 'c', '~d', '~e'})
