import re

def parse(file_name):
    # Read the file and return the data
    with open(file_name, "r", encoding="utf-8") as file:
        lines = file.readlines()
        # Remove empty lines and spaces
        lines = [x.strip() for x in lines if x.strip()]
        lines = [x.replace(" ","") for x in lines if x.strip()]

    # Initialize input Knowledge Base (input_kb) and Query lists
    input_kb = lines[1].split(";")
    input_query = lines[3]

    # Split symbols in the knowledge base and query
    output_kb = [re.split(r'(&|~|=>|\|\||<=>|\(|\))', x) for x in input_kb if x.strip()]
    output_query = re.split(r'(&|~|=>|\|\||<=>|\(|\))', input_query)

    # Extract unique symbols from both knowledge base and query
    symbols = lines[1] + lines[3]
    symbols = re.split(r'&|~|=>|\|\||<=>|\(|\)|;', symbols)
    symbols = list(set(symbols))

    return output_kb, output_query, symbols
