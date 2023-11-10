# Assignment 2 - Inference Engine

COS30019 - Introduction to Artificial Intelligence, **Swinburne University of Technology**.\
Delivered by **Swinburne Vietnam Alliance Program**, Fall Semester, 2023.

This repository contains the code for Assignment 2 of the unit COS30019 - Introduction to Artificial Intelligence. The assignment is about implementing an inference engine for truth table checking, forward chaining, and backward chaining. All the code is written in Python 3.

### Group Members

- Khang Vo ([@khangdzox](https://github.com/khangdzox))
- Chanh Hoai Nam Nguyen ([@hnam26](https://github.com/hnam26))

## Running the Program

### System Requirements

- OS: Windows 10 and above
- Runtime: Python 3.10 and above

### Input File Format

The problems are stores in simple text file in the following format:

```
TELL
<knowledge_base>

ASK
<query>
```

where:

- `<knowledge_base>` is a list of Horn clauses separated by semicolons.
- `<query>` is a propositional symbol.

For example:

```
TELL
p2 => p3; p3 => p1; c => e; b&e => f; f&g => h; p1=>d; p1&p3 => c; a; b; p2;

ASK
d
```

### Command Line Operation

To run the program, navigate to the root directory of the repository and run the following command:

```console
iengine <method> <input_file>
```

where:

- `<method>` is the inference method to use. It can be either `TT` (truth table checking), `FC` (forward chaining), or `BC` (backward chaining).
- `<input_file>` is the path to the input file.

### Output Format

Standard output is an answer of the form YES or NO, depending on whether the ASK(ed) query q follows from the TELL(ed) knowledge base KB.

When the method is TT and the answer is YES, it should be followed by a colon (:) and the number of models of KB. When the method is FC or BC and the answer is YES, it should be followed by a colon (:) and the list of propositional symbols entailed from KB that has been
found during the execution of the specified algorithm.

Example 1: Running `iengine` with method `TT`

```
YES: 3
```

Example 2: Running `iengine` with method `FC`

```
YES: a, b, p2, p3, p1, d
```

## Collaborators

This section contains information for collaborators of this repository.

### Files (placeholder)

- `main.py`: This file contains the main program logic.
- `truth_table.py`: This file contains the implementation of the truth table checking algorithm.
- `forward_chaining.py`: This file contains the implementation of the forward chaining algorithm.
- `backward_chaining.py`: This file contains the implementation of the backward chaining algorithm.

### Methods (placeholder)

- `generate_truth_table()`: This function generates a truth table for a given set of propositional symbols and a logical expression.
- `forward_chaining()`: This function implements the forward chaining algorithm for a given knowledge base and a query.
- `backward_chaining()`: This function implements the backward chaining algorithm for a given knowledge base and a query.

### Testing

To test the program, simply run the `main.py` file using Python 3. The program will automatically run the test cases and print the results to the console.

## Resources

This section contains resources used for this assignment.

### Acknowledgements (placeholder)

- [Truth Table Generator](https://web.stanford.edu/class/cs103/tools/truth-table-tool/)

### References (placeholder)

- [Truth Table Generator](https://web.stanford.edu/class/cs103/tools/truth-table-tool/)

## Copyright

© Khang Vo and Chanh Hoai Nam Nguyen, Swinburne University of Technology, 2023.
