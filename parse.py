import re
import unittest

def parse(file_name):
    # Read the file and return the data
    with open(file_name, "r", encoding="utf-8") as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]

    # Initialize input Knowledge Base (input_kb) and Query lists
    input_kb = []
    input_query = []

    # Check if the first line is "TELL"
    if lines[0] == "TELL":
        # Iterate through the lines starting from the second line
        for i in range(1, len(lines)):
            # Check if the current line is "ASK"
            if lines[i] == "ASK":
                # Append the next line to the query list and break the loop
                input_query.append(lines[i+1])
                break
            else:
                # Split the current line by semicolon, remove spaces
                input_kb = (lines[i].split(";"))
                input_kb = [x.strip() for x in input_kb if x.strip()]
                input_kb = [x.replace(" ","") for x in input_kb if x.strip()]
                
    # Split symbols in the knowledge base and query
    output_kb = split_symbols(input_kb)
    output_query = split_symbols(input_query)

    return output_kb, output_query

def split_symbols(arr):
    output_arr = []
    for element in arr:
        # Split the current element by symbols (logical operators and parentheses)
        new_string = re.split(r'(&|~|=>|\|\||<=>|\(|\))', element)
        # Remove empty strings and spaces
        new_string = [x.strip() for x in new_string if x.strip()]
        output_arr.append(new_string)
    
    return output_arr


# Unit Tests
import unittest

class TestParse(unittest.TestCase):
    
    def test_split_symbols(self):
        # Test case with logical operators and spaces
        test_arr = ["A & B", "C => D", "~E", "F"]
        expected_arr = [["A", "&", "B"], ["C", "=>", "D"], ["~", "E"], ["F"]]
        self.assertEqual(split_symbols(test_arr), expected_arr)

        # Test case with various logical operators and extra spaces
        test_arr = ["A& B", "C  => D", "~E", "F", "G||H", "I   <=> J", " ( K& L)"]
        expected_arr = [["A", "&", "B"], ["C", "=>", "D"], ["~", "E"], ["F"], ["G", "||", "H"], ["I", "<=>", "J"], ["(", "K", "&", "L", ")"]]
        self.assertEqual(split_symbols(test_arr), expected_arr)
            
    def test_parse(self):
        # Test case for the parse function with a sample input file
        test_kb, test_query = parse("data.txt")
        expected_kb = [['p2', '=>', 'p3'], ['p3', '=>', 'p1'], ['c', '=>', 'e'], ['b', '&', 'e', '=>', 'f'], ['f', '&', 'g', '=>', 'h'], ['p1S', '=>', 'd'], ['p1', '&', 'p3', '=>', 'c'], ['a'], ['b'], ['p2']]
        expected_query = [['d']]
        self.assertEqual(test_kb, expected_kb)
        self.assertEqual(test_query, expected_query)

if __name__ == "__main__":
    unittest.main()