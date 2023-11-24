from typing import Sequence

operators = ['~', '||', '&', '=>', '<=>']

def is_sentence_true(sentence: Sequence[str | bool], model: dict[str, bool]) -> bool:
    """
    Check if the sentence is true in the given model.

    Args:
        sentence (`list[str | bool]`): the propositional sentence to check.
        model (`dict[str, bool]`): the model with truth values for propositional variables.

    Returns:
        `bool`: Whether the sentence is true in the given model.
    """
    # process parentheses
    temp_sentence = []
    parentheses_stack = []

    for index, symbol in enumerate(sentence):

        # if find opening parenthese then push its index to stack
        if symbol == "(":
            parentheses_stack.append(index)

        # if find closing parenthese then pop the last opening parenthese index from stack
        elif symbol == ")":
            p_index = parentheses_stack.pop()

            # if find match parentheses then evaluate the sub-sentence and and to temp_sentence
            if len(parentheses_stack) == 0:
                temp_sentence.append(is_sentence_true(sentence[p_index+1:index], model))

        # if in parentheses, don't add value to temp_sentence,
        # because the value between parentheses will be evaluated

        # if not in any parentheses then evaluate symbol and add to temp_sentence
        elif len(parentheses_stack) == 0 and isinstance(symbol, str):
            if symbol in operators:
                temp_sentence.append(symbol)
            else:
                temp_sentence.append(model[symbol])

    sentence = temp_sentence

    # process negation
    while '~' in sentence:
        index = sentence.index('~')
        sentence = sentence[:index] + [not sentence[index+1]] + sentence[index+2:]

    # process conjunction
    while '&' in sentence:
        index = sentence.index('&')
        sentence = sentence[:index-1] + [sentence[index-1] and sentence[index+1]] + sentence[index+2:]

    # process disjunction
    while '||' in sentence:
        index = sentence.index('||')
        sentence = sentence[:index-1] + [sentence[index-1] or sentence[index+1]] + sentence[index+2:]

    # process implication
    while '=>' in sentence:
        index = sentence.index('=>')
        sentence = sentence[:index-1] + [not sentence[index-1] or sentence[index+1]] + sentence[index+2:]

    # process equivalence
    while '<=>' in sentence:
        index = sentence.index('<=>')
        sentence = sentence[:index-1] + [sentence[index-1] == sentence[index+1]] + sentence[index+2:]

    if len(sentence) != 1:
        raise ValueError("Invalid sentence")

    return bool(sentence[0])

def truth_table_checking(knowledge_base: list[list[str]], query: list[str], symbols: list[str]) -> tuple[bool, int]:
    """
    Check if the knowledge base entails the query using a truth table.

    Args:
        knowledge_base (`list[list[str]]`): the knowledge base.
        query (`list[str]`): the query to be checked.
        symbols (`list[str]`): the symbols in the knowledge base and query.

    Returns:
        `tuple[bool, int]`: a tuple includes: `Whether the knowledge base entails the query`; `The number of models checked`.
    """
    # Check if the knowledge base entails the query using a truth table
    return truth_table_enumerate_models(knowledge_base, query, symbols, {})

def truth_table_enumerate_models(knowledge_base: list[list[str]], query: list[str], symbols: list[str], model: dict[str, bool]):
    """
    Generate all possible models and check if the knowledge base entails the query.

    Args:
        knowledge_base (`list[list[str]]`): the knowledge base.
        query (`list[str]`): the query to be checked.
        symbols (`list[str]`): the symbols in the knowledge base and query.
        model (`dict[str, bool]`): the model to be checked.

    Returns:
        `tuple[bool, int]`: a tuple includes: `Whether the knowledge base entails the query`; `The number of models checked`.
    """
    # Base case: if there are no symbols left, check if the model satisfies the knowledge base and query
    if not symbols:
        if all(is_sentence_true(sentence, model) for sentence in knowledge_base):
            return is_sentence_true(query, model), 1
        else:
            return True, 0
    else:
        # Choose a symbol P and recursively evaluate with P being true and false
        P = symbols[0]
        rest = symbols[1:]

        # Recursively check with P being true and false
        true_result, true_count = truth_table_enumerate_models(knowledge_base, query, rest, {**model, P: True})
        false_result, false_count = truth_table_enumerate_models(knowledge_base, query, rest, {**model, P: False})

        return true_result and false_result, true_count + false_count
