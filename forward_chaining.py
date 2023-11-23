from chaining_helper import premise, conclusion

def forward_chaining_checking(knowledge_base: list[list[str]], query: str) -> tuple[bool, set[str]]:
    """
    This function implements the forward chaining algorithm for the given knowledge base and query.

    Args:
        knowledge_base (`list[list[str]]`): The knowledge base.
        query (`str`): The query to be checked.

    Returns:
        `tuple[bool, set[str]]`: A tuple includes: `Whether the query is entailed by the knowledge base`; `The set of symbols entailed by the knowledge base`.
    """
    # count: a table, where count[c] is initially the number of symbols in clause c's premise
    # inferred: a list containing inferred symbols
    # queue: a queue of symbols, initially symbols known to be true in KB
    count = {tuple(c): len(premise(c)) for c in knowledge_base if len(c) != 1}
    infered = []
    queue =  [c[0]for c in knowledge_base if len(c) == 1]

    # while queue is not empty
    while queue:

        # pop a symbol p from queue
        p = queue.pop(0)

        # if p is the query, return True
        if p == query:
            return True, set(infered + [p])

        # if p is not inferred yet
        if p not in infered:

            # add p to inferred
            infered.append(p)

            # for each clause c in KB where p is in c's premise and c is not a unit clause
            for c in knowledge_base:
                if p in premise(c) and len(c) != 1:

                    # decrement the count of c's premise
                    count[tuple(c)] -= 1

                    # if count of c is 0, add c's conclusion to queue
                    if count[tuple(c)] == 0:
                        queue.append(conclusion(c))

    # if queue is empty, return False
    return False, set()
