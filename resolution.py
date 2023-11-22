from cnf_helper import transform_to_cnf

def resolution(knowledge_base : list[list[str]], query : list[str]) -> bool:
    cnf_kb = [clauses for sentence in knowledge_base for clauses in transform_to_cnf(sentence)]
    cnf_not_query = transform_to_cnf(['~', '('] + query + [')'])

    # clause: KB & ~query
    clauses = cnf_kb + cnf_not_query

    new: list[list[str]] = []

    while True:
        for i in range(len(clauses) - 1):

            for j in range(i + 1, len(clauses)):

                resolvent = resolve(clauses[i], clauses[j])

                if not resolvent:
                    return True

                if resolvent not in new:
                    new.append(resolvent)

        # if new is the subset of clauses, return False
        if all(clause in clauses for clause in new):
            return False

        # add new to clauses
        for clause in new:
            if clause not in clauses:
                clauses.append(clause)

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
