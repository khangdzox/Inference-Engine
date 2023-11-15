from chaining_helper import premise, conclusion

def forward_chaining_checking(knowledge_base, query):
    """
    This function implements the forward chaining algorithm for the given knowledge base and query.
    :param knowledge_base: The knowledge base in the form of a dictionary
    :param query: The query to be checked
    :return: True if the query is entailed by the knowledge base, False otherwise
    """
    # count: a table, where count[c] is initially the number of symbols in clause c's premise
    # inferred: a table, where inferred[s] is initially false for all symbols
    # queue: a queue of symbols, initially symbols known to be true in KB
    count = {tuple(c): len(premise(c)) for c in knowledge_base if len(c) != 1}
    infered = []
    queue =  [c[0]for c in knowledge_base if len(c) == 1]
    while queue:
        p = queue.pop(0)
        if p == query:
            return True, set(infered + [p])
        if p not in infered:
            infered.append(p)
            for c in knowledge_base:
                if p in premise(c) and len(c) != 1:
                    count[tuple(c)] -= 1
                    if count[tuple(c)] == 0:
                        queue.append(conclusion(c))
    return False, set()
