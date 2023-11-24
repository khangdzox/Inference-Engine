from chaining_helper import premise, conclusion

def backward_chaining_checking(knowledge_base: list[list[str]], query: str, examined_symbols = None) -> tuple[bool, set[str]]:
    """
    Checks if the query is entailed by the knowledge base using backward chaining.
    Warning: Do not use the examined_symbols parameter. It's only used for internal recursion.

    Args:
        knowledge_base (`list[list[str]]`): the list of sentences in Horn form.
        query (`str`): the query to be checked.
        examined_symbols (`list[str]`): the list of symbols that have been examined. For internal recursion only.

    Returns:
        `tuple[bool, set[str]]`: a tuple includes: `Whether the query is entailed by the knowledge base`; `The set of symbols entailed by the knowledge base`.
    """
    # avoid dangerous default value
    if examined_symbols is None:
        examined_symbols = []

    # if the query is already examined, that means there is a cycle. Return False
    if query in examined_symbols:
        return False, set()

    # if the query is in the knowledge base, return True
    if [query] in knowledge_base:
        return True, {query}

    # initialize entailed_symbols
    entailed_symbols = []

    any_true = False
    # this for loop with loop through the knowledge base to find a sentence that has the query as its conclusion
    # it will break if one of the sentences is proved to be true
    for sentence in knowledge_base:
        if conclusion(sentence) == query:

            all_true = True
            # this for loop will loop through the premise of the sentence to check if all of them are true
            # it will break if one of the premise is proved to be false
            for symbol in premise(sentence):
                truth, entailed = backward_chaining_checking(knowledge_base, symbol, examined_symbols + [query])

                # if one of the premise is false, then the sentence is false
                if truth:
                    entailed_symbols += entailed
                else:
                    all_true = False
                    break

            # if all of the premise are true, then the sentence is true
            if all_true:
                any_true = True
                break

    # if one of the sentences is true, then the query is entailed by the knowledge base
    if any_true:
        return True, set(entailed_symbols + [query])

    # if none of the sentences is true, then the query is not entailed by the knowledge base
    return False, set()
