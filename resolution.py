from cnf_helper import transform_to_cnf

def resolution(knowledge_base : list[list[str]], query : list[str]) -> bool:
    cnf_kb = [clauses for sentence in knowledge_base for clauses in transform_to_cnf(sentence)]
    cnf_not_query = transform_to_cnf(['~', '('] + query + [')'])
    print(cnf_kb)
    print(cnf_not_query)
    clauses = cnf_kb + cnf_not_query
    print(clauses)
    new = []
    while True:
        idx1 = 0
        while idx1 < len(clauses):
            idx2 = idx1 + 1
            while idx2 < len(clauses):
                resolvents = resolve(clauses[idx1], clauses[idx2])
                if resolvents == []:
                    return True
                new.append(resolvents)
                idx2 += 1
            idx1 += 1
        # if new is the subset of clauses, return False
        
        if {tuple(x) for x in new}.issubset({tuple(x) for x in clauses}):
            return False
        clauses.extend(new)

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
