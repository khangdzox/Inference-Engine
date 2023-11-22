from cnf_helper import transform_to_cnf

def resolution(knowledge_base, query):
    clauses = transform_to_cnf(knowledge_base) + transform_to_cnf(['~' + query])
    new = []
    while True:
        for [clause1, clause2] in clauses:
            resolvents = resolve(clause1, clause2)
            if [] in resolvents:
                return True
            new += resolvents
        if new in clauses:
            return False
        clauses += new

def resolve(clause_1: list[str], clause_2: list[str]) -> list[str]:
    """
    Resolve two clauses.

    Args:
        clause_1 (list[str]): The first clause.
        clause_2 (list[str]): The second clause.

    Returns:
        list[str]: The resolvents.
    """
    # negate all literal in clause 1
    not_clause_1_set = {literal[1:] if literal[0] == '~' else '~' + literal for literal in clause_1}

    # turn clause 2 into a set of literal
    clause_2_set = set(clause_2)

    # find the overlap between not_clause_1_set and clause_2_set
    overlap = not_clause_1_set & clause_2_set

    # remove the overlap from both sets
    clause_2_set -= overlap
    not_clause_1_set -= overlap

    # negate all literal in not_clause_1_set
    clause_1_set = {literal[1:] if literal[0] == '~' else '~' + literal for literal in not_clause_1_set}

    # return the list of union of two clauses
    return list(clause_1_set | clause_2_set)
