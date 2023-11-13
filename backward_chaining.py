from chaining_helper import premise, conclusion

def backward_chaining_checking(knowledge_base: list[list[str]], query: str, examined_symbols = None) -> bool:
    """
    Checks if the query is entailed by the knowledge base using backward chaining.

    Args:
        knowledge_base (list[list[str]]): the list of sentences in Horn form
        query (str): the query to be checked

    Returns:
        bool: True if the query is entailed by the knowledge base, False otherwise
    """
    # avoid dangerous default value
    if examined_symbols is None:
        examined_symbols = []

    # if the query is already examined, that means there is a cycle. Return False
    if query in examined_symbols:
        return False

    # if the query is in the knowledge base, return True
    if [query] in knowledge_base:
        return True

    # will return true if any sentence that concludes the query is proved to be true
    return any(

        # will return true if all symbol in the sentence's premise are proved to be true
        all(
            backward_chaining_checking(knowledge_base, symbol, examined_symbols + [query]) for symbol in premise(sentence)
        ) for sentence in knowledge_base if conclusion(sentence) == query
    )
