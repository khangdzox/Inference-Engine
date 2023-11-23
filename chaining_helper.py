
def premise(sentence: list[str]) -> list[str]:
    """
    Return a list of symbol in the sentence's premise

    Args:
        sentence (`list[str]`): the sentence in Horn form

    Returns:
        `list[str]`: the list of symbol
    """
    result = []
    for symbol in sentence:
        if symbol == "&":
            continue
        if symbol == "=>":
            break
        result.append(symbol)
    return result

def conclusion(sentence: list[str]) -> str:
    """
    Return the symbol in the sentence's conclusion

    Args:
        sentence (`list[str]`): the sentence in Horn form

    Returns:
        `str`: the symbol
    """
    return sentence[-1]
