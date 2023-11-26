import re

def parse(file_name: str) -> tuple[list[list[str]], list[str], list[str]]:
    """
    Parse the input file and return the knowledge base and query.

    Args:
        file_name (`str`): The name of the input file.

    Returns:
        `tuple[list[list[str]], list[str], list[str]]`: A tuple includes: `The knowledge base`; `The query`; `The symbols in the knowledge base and query`.
    """

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

    # Remove empty strings from the list
    symbols = list(set(filter(None, symbols)))
    output_kb = [[x for x in y if x] for y in output_kb]
    output_query = [x for x in output_query if x]

    return output_kb, output_query, symbols
