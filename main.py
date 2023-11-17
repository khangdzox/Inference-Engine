import sys
from parse import parse
from truth_table import truth_table_checking
from forward_chaining import forward_chaining_checking
from backward_chaining import backward_chaining_checking
# from resolution import resolution_checking
# from dpll import dpll_satisfiable

cli_usage = f"Usage: iengine <method> <input_file>\nWhere\n\t{'<method>':<12} is one of:\n\t - {'TT':<4} for  Truth Table checking\n\t - {'FC':<4} for  Forward-Chaining checking\n\t - {'BC':<4} for  Backward-Chaining checking\n\t - {'RES':<4} for  RESolution checking\n\t - {'DPLL'} for  DPLL-algorithm checking\n\n\t{'<input_file>':<12} is the path to the input file\n\nExample: iengine TT data.txt"

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
