import unittest
from unittest import mock
from parse import parse

class TestParse(unittest.TestCase):
    """
    Unit test for parse() function.
    """

    # mocking the file open function
    @mock.patch('builtins.open', mock.mock_open(read_data=
        """
        TELL
        p2 => p3; p3 => p1; c => e; b&e => f; f&g => h; p1 => d; p1&p3 => c; a; b; p2;

        ASK
        d
        """
    ) )
    def test_parse_1(self):
        # Test case for the parse function with a sample input file
        test_kb, test_query, test_symbols = parse("data.txt")
        self.assertEqual(test_kb, [['p2', '=>', 'p3'], ['p3', '=>', 'p1'], ['c', '=>', 'e'], ['b', '&', 'e', '=>', 'f'], ['f', '&', 'g', '=>', 'h'], ['p1', '=>', 'd'], ['p1', '&', 'p3', '=>', 'c'], ['a'], ['b'], ['p2']])
        self.assertEqual(test_query, ['d'])
        self.assertEqual(set(test_symbols), {'h', 'c', 'b', 'p3', 'f', 'p1', 'e', 'g', 'd', 'a', 'p2'})

    # mocking the file open function
    @mock.patch('builtins.open', mock.mock_open(read_data=
        """
        TELL
        (a <=> (c => ~d)) & b & (b => a); c; ~f || g;
        ASK
        d
        """
    ) )
    def test_parse_2(self):
        # Test case for the parse function with a sample input file
        test_kb, test_query, test_symbols = parse("data.txt")
        self.assertEqual(test_kb, [['(', 'a', '<=>', '(', 'c', '=>', '~', 'd', ')', ')', '&', 'b', '&', '(', 'b', '=>', 'a', ')'], ['c'], ['~', 'f', '||', 'g']])
        self.assertEqual(test_query, ['d'])
        self.assertEqual(set(test_symbols), {'a', 'b', 'c', 'd', 'f', 'g'})

    # mocking the file open function
    @mock.patch('builtins.open', mock.mock_open(read_data=
        """
        TELL
        (a <=> (c => ~d)) & b & (b => a); c; ~f || g;
        ASK
        ~d & (~g => ~f)
        """
    ) )
    def test_parse_3(self):
        # Test case for the parse function with a sample input file
        test_kb, test_query, test_symbols = parse("data.txt")
        self.assertEqual(test_kb, [['(', 'a', '<=>', '(', 'c', '=>', '~', 'd', ')', ')', '&', 'b', '&', '(', 'b', '=>', 'a', ')'], ['c'], ['~', 'f', '||', 'g']])
        self.assertEqual(test_query, ['~', 'd', '&', '(', '~', 'g', '=>', '~', 'f', ')'])
        self.assertEqual(set(test_symbols), {'a', 'b', 'c', 'd', 'f', 'g'})

if __name__ == "__main__":
    unittest.main()
