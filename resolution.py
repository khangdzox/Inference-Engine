from cnf_helper import transform_to_cnf

def resolution_checking(knowledge_base : list[list[str]], query : list[str]) -> bool:
    """
    Check if the query is entailed by the knowledge base, using resolution algorithm.

    This method check for entailment by contradiction:

    If `KB |= query`, then `~KB || query` is true in all models, then `KB & ~query` will be unsatisfiable.

    Args:
        knowledge_base (`list[list[str]]`): The knowledge base.
        query (`list[str]`): The query to be checked.

    Returns:
        `bool`: Whether the query is entailed by the knowledge base.
    """
    # transform knowledge base and query to CNF
    cnf_kb = [clauses for sentence in knowledge_base for clauses in transform_to_cnf(sentence)]
    cnf_not_query = transform_to_cnf(['~', '('] + query + [')'])

    # clause: KB & ~query
    clauses = cnf_kb + cnf_not_query

    # empty list for resolved clauses
    new: list[list[str]] = []

    while True:

        # for each pair of clauses, resolve them
        for i in range(len(clauses) - 1):
            for j in range(i + 1, len(clauses)):

                resolvent = resolve(clauses[i], clauses[j])

                # if two clauses resolve to an empty clause, it means the sentence "KB & ~query" is unsatisfiable
                # therefore, the query is entailed by the knowledge base. Return True
                if resolvent == []:
                    return True

                # if resolvent is not in new, add it to new
                if resolvent not in new and resolvent is not None:
                    new.append(resolvent)

        # if new is the subset of clauses, return False
        if all(clause in clauses for clause in new):
            return False

        # add new to clauses
        for clause in new:
            if clause not in clauses:
                clauses.append(clause)

def resolve(clause_1: list[str], clause_2: list[str]) -> list[str] | None:
    """
    Resolve two clauses using the resolution rule.

    This method will remove all complementary literals between the two clause and only produce one new clause.

    Args:
        clause_1 (`list[str]`): The first clause.
        clause_2 (`list[str]`): The second clause.

    Returns:
        `list[str] | None`: The resolvent or None if two clauses cannot be resolved.
    """
    # negate all literals in clause 1
    not_clause_1_set = {literal[1:] if literal[0] == '~' else '~' + literal for literal in clause_1}

    # turn clause 2 into a set of literals
    clause_2_set = set(clause_2)

    # find the overlap between not_clause_1_set and clause_2_set
    # which is the complementary literals between the two clauses
    overlap = not_clause_1_set & clause_2_set

    # if there is no overlap, or there are more than one overlap, return None
    if not overlap or len(overlap) != 1:
        return None

    # remove the overlap from both sets
    clause_2_set -= overlap
    not_clause_1_set -= overlap

    # negate all literals in not_clause_1_set to get the original literals
    clause_1_set = {literal[1:] if literal[0] == '~' else '~' + literal for literal in not_clause_1_set}

    # return the union of two clause sets as a list
    return list(clause_1_set | clause_2_set)
