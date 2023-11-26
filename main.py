import sys
import time
from parse import parse
from truth_table import truth_table_checking
from forward_chaining import forward_chaining_checking
from backward_chaining import backward_chaining_checking
from resolution import resolution_checking
from dpll import dpll_checking

cli_usage = f"Usage: iengine <method> <input_file> [time]\nWhere:\n\t<method> The method to perform. Is one of:\n\t - {'TT':<4} for  Truth Table checking\n\t - {'FC':<4} for  Forward-Chaining checking\n\t - {'BC':<4} for  Backward-Chaining checking\n\t - {'RES':<4} for  RESolution checking\n\t - {'DPLL'} for  DPLL-algorithm checking\n\n\t{'<input_file>':<12} The path to the input file\n\n\t{'[time]':<12} Optional flag. To measure the processing time of the engine\n\nExample: iengine TT data.txt time"

# Get command line arguments
try:
    method, input_file = sys.argv[1], sys.argv[2]
    is_timing = "time" in sys.argv[3:]
except IndexError:
    print("Error: Not enough argument\n\n" + cli_usage)
    sys.exit()

try:
    knowledge_base, query, symbols = parse(input_file)
except FileNotFoundError:
    print("Error: File \"" + input_file + "\" not found\n\n" + cli_usage)
    sys.exit()

match method.lower():
    case "tt":
        start = time.perf_counter_ns()
        result, details = truth_table_checking(knowledge_base, query, symbols)
        end = time.perf_counter_ns()
    case "fc":
        start = time.perf_counter_ns()
        result, details = forward_chaining_checking(knowledge_base, query[0])
        end = time.perf_counter_ns()
        details = ", ".join(details)
    case "bc":
        start = time.perf_counter_ns()
        result, details = backward_chaining_checking(knowledge_base, query[0])
        end = time.perf_counter_ns()
        details = ", ".join(details)
    case "dpll":
        start = time.perf_counter_ns()
        result = dpll_checking(knowledge_base, query, symbols)
        end = time.perf_counter_ns()
        details = ""
    case "res":
        start = time.perf_counter_ns()
        result = resolution_checking(knowledge_base, query)
        end = time.perf_counter_ns()
        details = ""
    case _:
        print("Error: Invalid method \"" + method + "\"\n\n" + cli_usage)
        sys.exit()

print((f"YES: {details}" if details else "YES") if result else "NO")
if is_timing:
    print(f"Time: {(end - start) / 1000}ms")
