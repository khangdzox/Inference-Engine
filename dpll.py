# from cnf_helper import transform_to_cnf

def dpll_checking(knowledge_base: list[list[str]], query: list[str], symbols: list[str]) -> bool:
    """
    Return True if the knowledge base entails the query, False otherwise.

    Args:
        knowledge_base (list[list[str]]): The knowledge base.
        query (list[str]): The query.
        symbols (list[str]): The symbols in the knowledge base and query.

    Returns:
        bool: Whether the knowledge base entails the query.
    """
    cnf_kb = [transform_to_cnf(sentence) for sentence in knowledge_base]
    cnf_not_query = transform_to_cnf(['~', '('] + query + [')'])
    return not dpll_satisfiable(cnf_kb + [cnf_not_query], symbols, {})

def dpll_satisfiable(clauses: list[list[str]], symbols: list[str], model: dict[str, bool]) -> bool:
    """
    Checking satisfiability of a sentence using DPLL algorithm.

    Args:
        clauses (list[list[str]]): The clauses of the sentence.
        symbols (list[str]): The symbols in the sentence.
        model (dict[str, bool]): The model for the sentence.

    Returns:
        bool: Whether the sentence is satisfiable.
    """
    if all( is_clause_true(clause, model) is True for clause in clauses ):
        return True

    if any( is_clause_true(clause, model) is False for clause in clauses ):
        return False

    P, value = find_pure_symbol(symbols, clauses, model)
    if P is not None:
        return dpll_satisfiable(clauses, [symbol for symbol in symbols if symbol != P], {**model, P: value})

    P, value = find_unit_clause(clauses, model)
    if P is not None:
        return dpll_satisfiable(clauses, [symbol for symbol in symbols if symbol != P], {**model, P: value})

    P = symbols[0]
    rest = symbols[1:]
    return dpll_satisfiable(clauses, rest, {**model, P: True}) or \
           dpll_satisfiable(clauses, rest, {**model, P: False})

def find_pure_symbol(symbols: list[str], clauses: list[list[str]], model: dict[str, bool]) -> tuple[str | None, bool]:
    """
    Find a pure symbol in the sentence.

    Args:
        symbols (list[str]): A list of symbols.
        clauses (list[list[str]]): The sentence in CNF.
        model (dict[str, bool]): The model for the sentence.

    Returns:
        tuple[str | None, bool]: A pure symbol and its value.
    """

    # eliminate clause that is already true
    new_clauses = []
    for clause in clauses:
        if not is_clause_true(clause, model):
            new_clauses.append(clause)
    clauses = new_clauses

    flatten_clauses = [symbol for clause in clauses for symbol in clause]

    for symbol in symbols:
        if symbol in model:
            continue
        if symbol in flatten_clauses and '~' + symbol not in flatten_clauses:
            return symbol, True
        if '~' + symbol in flatten_clauses and symbol not in flatten_clauses:
            return symbol, False

    return None, False

def find_unit_clause(clauses: list[list[str]], model: dict[str, bool]) -> tuple[str | None, bool]:
    """
    Find a unit clause in the sentence.

    Args:
        clauses (list[list[str]]): The sentence in CNF.
        model (dict[str, bool]): The model for the sentence.

    Returns:
        tuple[str | None, bool]: A unit clause and its value.
    """
    if single_symbol_clauses := [clause for clause in clauses if len(clause) == 1]:
        first_symbol = single_symbol_clauses[0][0]
        return first_symbol.removeprefix('~'), not first_symbol.startswith('~')

    for clause in clauses:
        false_symbols_in_clause = [
            symbol.removeprefix('~') for symbol in clause
            if symbol.removeprefix('~') in model and model[symbol.removeprefix('~')] is symbol.startswith('~')
        ]

        all_symbols_in_clause = [symbol.removeprefix('~') for symbol in clause]
        difference_symbols = list(set(all_symbols_in_clause) - set(false_symbols_in_clause))
        if len(difference_symbols) == 1:
            return difference_symbols[0].removeprefix('~'), not difference_symbols[0].startswith('~')

    return None, False

def is_clause_true(clause: list[str], model: dict[str, bool]) -> bool | None:
    """
    Checking whether a CNF clause is true in model.

    Args:
        clause (list[str]): a CNF clause.
        model (dict[str, bool]): The model for the sentence.

    Returns:
        bool: Whether the CNF clause is true.
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
