import sys
from parse import parse
from truth_table import truth_table_checking
from forward_chaining import forward_chaining_checking
from backward_chaining import backward_chaining_checking
# from dpll import dpll_satisfiable

cli_usage = f"Usage: iengine <method> <input_file>\nWhere\n\t{'<method>':<11} is one of [TT, FC, BC, DPLL]\n\t{'<input_file>':<11} is the path to the input file\n\nExample: iengine TT data.txt"

# Get command line arguments
try:
    method, input_file = sys.argv[1], sys.argv[2]
except IndexError:
    print("Error: Not enough argument\n\n" + cli_usage)
    sys.exit()

knowledge_base, query, symbols = parse(input_file)

match method.lower():
    case "tt":
        result, details = truth_table_checking(knowledge_base, query, symbols)
    case "fc":
        result, details = forward_chaining_checking(knowledge_base, query[0])
        details = ", ".join(details)
    case "bc":
        result, details = backward_chaining_checking(knowledge_base, query[0])
        details = ", ".join(details)
    # case "dpll":
    #     result, details = dpll_satisfiable(knowledge_base)
    case _:
        print("Error: Invalid method \"" + method + "\"\n\n" + cli_usage)
        sys.exit()

print(f"YES: {details}" if result else "NO")
