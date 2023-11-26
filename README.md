# Assignment 2 - Inference Engine

COS30019 - Introduction to Artificial Intelligence, **Swinburne University of Technology**.\
Delivered by **Swinburne Vietnam Alliance Program**, Fall Semester, 2023.

This repository contains the code for Assignment 2 of the unit COS30019 - Introduction to Artificial Intelligence. The assignment is about implementing an inference engine for truth table checking, forward chaining, and backward chaining. All the code is written in Python 3.

### Group Members

- Khang Vo ([@khangdzox](https://github.com/khangdzox))
- Chanh Hoai Nam Nguyen ([@hnam26](https://github.com/hnam26))

<br>

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

```
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
<br>

## For Collaborators

### Preparation

Before starting to work any part of the assignment, please make sure to follow these steps:

1. Clone the repository to your local machine.

2. Create a new branch for your work. The branch name should be in the format `<your_name>/<feature_name>`. For example, `khangdzox/truth_table`.

3. Make sure to pull the latest changes from the `main` branch before starting to work on your branch.

4. After finishing your work, create a pull request to merge your branch into `main`.

### Program Structures

- `main.py`: This file is the entry point of the program. It will parse the command line arguments, read the input file, and call the appropriate functions.

- `truth_table.py`: This file contains the implementation of the truth table checking algorithm.

    - [x] `truth_table_checking(knowledge_base, query, symbols)`: This method initiates the truth table checking algorithm.

    - [x] `truth_table_enumerate_models(knowledge_base, query, symbols, model)`: This method is a recursive function that generates and enumerates all the possible models of the knowledge base.

    - [x] `is_sentence_true(sentence, model)`: This method checks if the sentence is true in the given model.

- `forward_chaining.py`: This file contains the implementation of the forward chaining algorithm.

    - [x] `forward_chaining_checking(knowledge_base, query)`: This method is a recursive function that checks if the query is entailed by the knowledge base using the forward chaining algorithm.

- `backward_chaining.py`: This file contains the implementation of the backward chaining algorithm.

    - [x] `backward_chaining_checking(knowledge_base, query, examined_symbols)`: This method is a recursive function that checks if the query is entailed by the knowledge base using the backward chaining algorithm.

- `resolution.py`: This file contains the implementation of the resolution algorithm.

    - [x] `resolution_checking(knowledge_base, query)`: This method is a function that checks if the given query is entailed by the knowledge base using the resolution algorithm.

    - [x] `resolve(clause1, clause2)`: This method is a function that resolves two clauses to a list of resolvents.

- `dpll.py`: This file contains the implementation of the DPLL algorithm.

    - [x] `dpll_checking(khowledge_base, query)`: This method is a function that checks if the given query is entailed by the knowledge base using the DPLL algorithm.

    - [x] `dpll_satisfiable(clauses, symbols, model)`: This method is a recursive function that perform the DPLL algorithm.

    - [x] `find_pure_symbol(symbols, clauses, model)`: This method finds a pure symbol in the given clauses.

    - [x] `find_unit_clause(clauses, model)`: This method finds a unit clause in the given clauses.

    - [x] `is_clause_true(clause, model)`: This method checks if the given CNF clause is true in the given model.

- `chaining_helper.py`: This file contains the helper methods for the chaining algorithm.

    - [x] `premise(sentence)`: This method returns the premise of the given sentence.

    - [x] `conclusion(sentence)`: This method returns the conclusion of the given sentence.

- `cnf_helper.py`: This file contains the helper methods for the CNF conversion.

    - [x] `transform_to_cnf(sentence)`: This method is a function that transforms a sentence to CNF.

    - [x] `add_parentheses_around_operator(sentence, operator)`: This method adds parentheses around the given operator in the given sentence.

    - [x] `simplify_parentheses(sentence)`: This method simplifies the parentheses in the given sentence.

    - [x] `bidirectional_elimination(sentence)`: This method performs the bidirectional elimination on the given sentence.

    - [x] `implies_elimination(sentence)`: This method performs the implies elimination on the given sentence.

    - [x] `double_negation_elimination(sentence)`: This method performs the double negation elimination on the given sentence.

    - [x] `combine_negation(sentence)`: This method combines the negation with the following operand in the given sentence.

    - [x] `apply_de_morgan(sentence)`: This method applies the De Morgan's law on the given sentence.

    - [x] `apply_distribute_or_over_and(sentence)`: This method distributes the OR operator over the AND operator in the given sentence.

    - [x] `get_previous_operand(sentence, index)`: This method returns the previous operand to the operator at the given index in the given sentence.

    - [x] `get_following_operand(sentence, index)`: This method returns the following operand to the operator at the given index in the given sentence.

    - [x] `get_main_operator(sentence)`: This method returns the main operator in the given sentence.

    - [x] `get_inside_parentheses(sentence, begin, end)`: This method returns the content inside the parentheses from begin index to end index in the given sentence.

- `parse.py`: This file contains utility functions that are used by the other files.

    - [x] `parse(input_file)`: This method parses the input file and returns the knowledge base, the query, and the set of propositional symbols.

- `test`: This folder contains the test cases for the program.

    - `test.py`: This file contains the test cases for the entire program.

    - `test_*.py`: These files contain the unit tests for each module of the program

### Testing

This program utilises `unittest` module for unit testing.

To test the program, run the command `python -m unittest discover test -v` from the root directory. The program will automatically run the test cases and print the results to the console.

<br>

## Resources

- [String split using RegEx](https://docs.python.org/3/library/re.html#re.split)

- [Unit Testing in Python](https://docs.python.org/3/library/unittest.html)

<br>

## Copyright

© Khang Vo and Chanh Hoai Nam Nguyen, Swinburne University of Technology, 2023.
