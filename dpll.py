from cnf_helper import transform_to_cnf

def dpll_checking(knowledge_base: list[list[str]], query: list[str], symbols: list[str]) -> bool:
    """
    Check if the query is entailed by the knowledge base, using DPLL algorithm.

    This method check for entailment by contradiction:\\
        If `KB |= query`, then `~KB || query` is true in all models, then `KB & ~query` will be unsatisfiable.

    Args:
        knowledge_base (`list[list[str]]`): The knowledge base.
        query (`list[str]`): The query.
        symbols (`list[str]`): The symbols in the knowledge base and query.

    Returns:
        `bool`: Whether the knowledge base entails the query.
    """

    # transform knowledge base and query to CNF
    cnf_kb = [clauses for sentence in knowledge_base for clauses in transform_to_cnf(sentence)]
    cnf_not_query = transform_to_cnf(['~', '('] + query + [')'])

    # return whether the sentence "KB & ~query" is unsatisfiable
    return not dpll_satisfiable(cnf_kb + cnf_not_query, symbols, {})

def dpll_satisfiable(clauses: list[list[str]], symbols: list[str], model: dict[str, bool]) -> bool:
    """
    Checking satisfiability of a sentence using DPLL algorithm.

    Args:
        clauses (`list[list[str]]`): The clauses of the sentence.
        symbols (`list[str]`): The symbols in the sentence.
        model (`dict[str, bool]`): The model for the sentence.

    Returns:
        `bool`: Whether the sentence is satisfiable.
    """

    # if all clauses are known to be true, return True
    if all( is_clause_true(clause, model) is True for clause in clauses ):
        return True

    # if any clause is known to be false, return False
    if any( is_clause_true(clause, model) is False for clause in clauses ):
        return False

    # determine the value of a pure symbol if there is any
    P, value = find_pure_symbol(symbols, clauses, model)
    if P is not None:
        return dpll_satisfiable(clauses, [symbol for symbol in symbols if symbol != P], {**model, P: value})

    # determine the value of a unit clause if there is any
    P, value = find_unit_clause(clauses, model)
    if P is not None:
        return dpll_satisfiable(clauses, [symbol for symbol in symbols if symbol != P], {**model, P: value})

    # if no pure symbol or unit clause is found, choose a symbol and try both value
    P = symbols[0]
    rest = symbols[1:]
    return dpll_satisfiable(clauses, rest, {**model, P: True}) or \
           dpll_satisfiable(clauses, rest, {**model, P: False})

def find_pure_symbol(symbols: list[str], clauses: list[list[str]], model: dict[str, bool]) -> tuple[str | None, bool]:
    """
    Find a pure symbol in the sentence and determine its value so that the sentence is true.

    Args:
        symbols (`list[str]`): A list of symbols.
        clauses (`list[list[str]]`): The sentence in CNF.
        model (`dict[str, bool]`): The model for the sentence.

    Returns:
        `tuple[str | None, bool]`: A tuple includes: `A pure symbol or None if not found`; `The symbol's value`.
    """

    # eliminate clause that is already true
    clauses = [clause for clause in clauses if not is_clause_true(clause, model)]

    # flatten the list of clauses to a list of literals in the sentence
    flatten_clauses = [literal for clause in clauses for literal in clause]

    for symbol in symbols:
        # skip symbol with already known value
        if symbol in model:
            continue

        # if symbol is pure, return it and its value
        if symbol in flatten_clauses and '~' + symbol not in flatten_clauses:
            return symbol, True
        if '~' + symbol in flatten_clauses and symbol not in flatten_clauses:
            return symbol, False

    # no pure symbol found
    return None, False

def find_unit_clause(clauses: list[list[str]], model: dict[str, bool]) -> tuple[str | None, bool]:
    """
    Find a unit clause in the sentence.

    Args:
        clauses (`list[list[str]]`): The sentence in CNF.
        model (`dict[str, bool]`): The model for the sentence.

    Returns:
        `tuple[str | None, bool]`: A tuple includes: `A unit clause or None if not found`; `The symbol's value`.
    """

    # eliminate clause that is already true
    clauses = [clause for clause in clauses if not is_clause_true(clause, model)]

    # return the first single-symbol clause in the sentence if there is any
    if single_symbol_clauses := [clause for clause in clauses if len(clause) == 1]:
        first_symbol = single_symbol_clauses[0][0]
        return first_symbol.removeprefix('~'), not first_symbol.startswith('~')

    # iterate through all clauses to find a clause that has only one non-false symbol
    for clause in clauses:

        # find all symbols known to be false in clause
        false_symbols_in_clause = [
            symbol.removeprefix('~') for symbol in clause
            if symbol.removeprefix('~') in model and model[symbol.removeprefix('~')] is symbol.startswith('~')
        ]

        # find all symbols in clause
        all_symbols_in_clause = [symbol.removeprefix('~') for symbol in clause]

        # find the difference between all symbols and false symbols, which is the symbols without known value
        difference_symbols = list(set(all_symbols_in_clause) - set(false_symbols_in_clause))

        # if there is only one symbol without known value, return it and its value
        if len(difference_symbols) == 1:
            return difference_symbols[0].removeprefix('~'), not difference_symbols[0].startswith('~')

    # no unit clause found
    return None, False

def is_clause_true(clause: list[str], model: dict[str, bool]) -> bool | None:
    """
    Checking whether a CNF clause is true in model.

    Args:
        clause (`list[str]`): a CNF clause.
        model (`dict[str, bool]`): The model for the sentence.

    Returns:
        `bool | None`: Whether the CNF clause is true or None if the truthfulness of clause cannot be determined.
    """
    # return True if any symbol in model is true in clause
    if any(
        ('~' if not value else '') + symbol in clause
        for symbol, value in model.items()
    ):
        return True

    # no true symbol in clause
    # return None if any symbol in clause is not in model
    if any(
        symbol.removeprefix('~') not in model
        for symbol in clause
    ):
        return None

    # no non-value symbol in clause
    # only false symbols remain in clause
    return False
