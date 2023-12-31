operators = ['~', '||', '&', '=>', '<=>']

def transform_to_cnf(sentence : list[str]) -> list[list[str]]:
    """
    Transform a general propositional logic sentence into Conjunctive Normal Form (CNF).\\
    A CNF sentence is a list of clauses, which are connected by conjuction,\\
    where a clause is a list of literals, which are connected by disjuction.

    Args:
        sentence (`list[str]`): The propositional logic sentence.

    Returns:
        `list[list[str]]`: The transformed sentence in CNF.
    """

    # add parentheses around the operators to ensure the order of operations
    sentence = add_parentheses_around_operator(sentence, "&")
    sentence = add_parentheses_around_operator(sentence, "||")

    # remove unnecessary parentheses
    sentence = simplify_parentheses(sentence)

    # eliminate operators other than '~', '||', '&' from the sentence
    sentence = bidirectional_elemination(sentence)
    sentence = implication_elemination(sentence)
    sentence = double_negation_elimination(sentence)

    # remove unnecessary parentheses created during elimination to prevent unwanted behavior when applying De Morgan's law
    sentence = simplify_parentheses(sentence)

    # apply De Morgan's law to move negation inside the parentheses
    sentence = apply_de_morgan(sentence)

    # remove unnecessary parentheses created during the application of De Morgan's law
    sentence = simplify_parentheses(sentence)

    # combine the negation operator with the operand following it
    sentence = combine_negation(sentence)

    # apply the law of distributivity of disjunction over conjunction to the sentence
    sentence = apply_distributivity_or_over_and(sentence)

    # split to list of clauses
    result = "".join(sentence).replace('(', '').replace(')', '').split('&')

    # split each clause to list of symbols
    result = [i.split('||') for i in result]

    return result

def add_parentheses_around_operator(sentence: list[str], operator: str) -> list[str]:
    """
    Add parentheses to isolate the operands connected by the operator in the sentence.

    Args:
        sentence (`list[str]`): The sentence to add parentheses to.
        operator (`str`): The operator to isolate.

    Returns:
        `list[str]`: The sentence with parentheses added.
    """
    idx = 0
    # iterate through the sentence
    while idx < len(sentence):

        # if the current character is the operator
        if sentence[idx] == operator:

            # find the operands preceding the operator until the beginning of the sentence or a different operator
            before = idx
            while True:
                begin, end = get_previous_operand(sentence, before)
                before = begin - 1
                if before < 0 or sentence[before] != operator:
                    break

            # find the operands following the operator until the end of the sentence or a different operator
            after = idx
            while True:
                begin, end = get_following_operand(sentence, after)
                after = end + 1
                if after >= len(sentence) or sentence[after] != operator:
                    break

            # if the operands are already enclosed in parentheses, then skip
            if sentence[before] == "(" and sentence[after] == ")":
                idx = after
                continue

            # add parentheses around the operands
            # format: ... ( operands ) ...
            sentence = sentence[:before+1] + ["("] + sentence[before+1:after] + [")"] + sentence[after:]

            # skip to the end of the parentheses
            idx = after + 2

        # if the current character is not the operator, then skip
        else:
            idx += 1

    return sentence

def simplify_parentheses(sentence: list[str]) -> list[str]:
    """
    Simplify the parentheses in the sentence.\\
    Remove the parantheses if the sub-sentence inside the parentheses has the same main operator as the sentence.\\
    If the sentence does not contain any parentheses, then the sentence has been simplified.

    Args:
        sentence (`list[str]`): The sentence to simplify.

    Returns:
        `list[str]`: The simplified sentence.
    """
    # if the sentence does not contain any parentheses, then the sentence has been simplified
    if "(" not in sentence:
        return sentence

    # get the main operator of the sentence
    main_operator = get_main_operator(sentence)

    # if the sentence has no operator, then the sentence is enclosed in parentheses
    if main_operator == "":
        # if the sentence starts with a '~', then it is in the form of ~ ( sub-sentence )
        if sentence[0] == "~":
            sub_begin, sub_end = get_inside_parentheses(sentence, 0, len(sentence) - 1)

            # if the sub-sentence has only one operand, remove the parentheses
            # then return the form of ~ operand
            if get_main_operator(sentence[sub_begin:sub_end+1]) == "":
                return ['~'] + simplify_parentheses(sentence[sub_begin:sub_end+1])

            # else, keep the parentheses
            # return the form of ~ ( sub-sentence )
            return ['~', '('] + simplify_parentheses(sentence[sub_begin:sub_end+1]) + [')']

        # else, the sentence is in the form of ( sub-sentence )
        # remove the parentheses
        return simplify_parentheses(sentence[1:-1])

    # else, the sentence is in the form of operand operator operand ...
    # where operand can be a single character or a sub-sentence enclosed in parentheses

    idx = -1
    # iterate through the sentence
    while idx < len(sentence):

        # find the operand following the operator at the current index
        begin, end = get_following_operand(sentence, idx)

        # if the operand is longer than 2 elements, then the operand is enclosed in parentheses
        if end - begin > 1:

            # simplify the sub-sentence inside the parentheses and replace the sub-sentence with the simplified version
            sub_begin, sub_end = get_inside_parentheses(sentence, begin, end)
            sentence[sub_begin:sub_end+1] = (simplified := simplify_parentheses(sentence[sub_begin:sub_end+1]))

            # update the end index of the operand
            end = sub_begin + len(simplified)
            sub_end = end - 1

            # if the sub-sentence has the same main operator as the sentence and the operand not start with "~", then remove the parentheses
            sub_operator = get_main_operator(sentence[sub_begin:sub_end+1])
            if sub_operator in (main_operator, "") and sentence[begin] != "~":
                sentence = sentence[:begin] + sentence[sub_begin:sub_end+1] + sentence[end+1:]
                idx = end - 1

            # else, skip to the end of the parentheses
            else:
                idx = end + 1
        else:
            idx = end + 1

    return sentence

def bidirectional_elemination(sentence: list[str]) -> list[str]:
    """
    Eliminate the bidirectional operator from the sentence.

    Args:
        sentence (`list[str]`): The sentence to eliminate the bidirectional operator from.

    Returns:
        `list[str]`: The sentence with the bidirectional operator eliminated.
    """
    # while the sentence contains the bidirectional operator
    while '<=>' in sentence:

        # get the index of the bidirectional operator
        index = sentence.index('<=>')

        # get the operands preceding and following the bidirectional operator
        previous_begin, previous_end = get_previous_operand(sentence, index)
        following_begin, following_end = get_following_operand(sentence, index)

        # replace the bidirectional operator with the implication operator
        # format: ... ( ( previous_operand => following_operand ) & ( following_operand => previous_operand ) ) ...
        sentence = sentence[:previous_begin] +  ['(', '('] + sentence[previous_begin:previous_end + 1] + ['=>'] + sentence[following_begin:following_end + 1] + [')'] + ['&'] + ['('] + sentence[following_begin:following_end + 1] + ['=>'] + sentence[previous_begin:previous_end + 1] +[')', ')'] + sentence[following_end + 1:]

    return sentence

def implication_elemination(sentence: list[str]) -> list[str]:
    """
    Eliminate the implication operator from the sentence.

    Args:
        sentence (`list[str]`): The sentence to eliminate the implication operator from.

    Returns:
        `list[str]`: The sentence with the implication operator eliminated.
    """
    # while the sentence contains the implication operator
    while '=>' in sentence:

        # get the index of the implication operator
        index = sentence.index('=>')

        # get the operands preceding and following the implication operator
        previous_begin, previous_end = get_previous_operand(sentence, index)
        following_begin, following_end = get_following_operand(sentence, index)

        # replace the implication operator with the disjunction operator
        # format: ... ( ~ previous_operand || following_operand ) ...
        sentence = sentence[:previous_begin] +  ['(', '~'] + sentence[previous_begin:previous_end + 1] + ['||'] + sentence[following_begin:following_end + 1] + [')'] + sentence[following_end + 1:]

    return sentence

def double_negation_elimination(sentence: list[str]) -> list[str]:
    """
    Eliminate the double negation operator from the sentence.

    Args:
        sentence (`list[str]`): The sentence to eliminate the double negation operator from.

    Returns:
        `list[str]`: The sentence with the double negation operator eliminated.
    """
    index = 0
    # iterate through the sentence
    while index < len(sentence):

        # if the current character is a '~' and followed by a '~', then remove the double negation
        if sentence[index] == '~' and sentence[index + 1] == '~':
            sentence = sentence[:index] + sentence[index + 2:]
        index += 1

    return sentence

def combine_negation(sentence: list[str]) -> list[str]:
    """
    Combine the negation operator with the operand following it.

    Args:
        sentence (`list[str]`): The sentence to combine.

    Returns:
        `list[str]`: The combined sentence.
    """
    # while the sentence contains the negation operator
    while '~' in sentence:

        # get the index of the negation operator
        index = sentence.index('~')

        # combine the negation operator with the character following it
        # format: ... ~character ...
        sentence = sentence[:index] + ['~' + sentence[index + 1]] + sentence[index + 2:]

    return sentence

def apply_de_morgan(sentence: list[str]) -> list[str]:
    """
    Apply De Morgan's law to the sentence to move negation inside the parentheses.

    Only works with simplified sentence.

    Args:
        sentence (`list[str]`): The sentence to apply De Morgan's law to.

    Raises:
        `ValueError`: If the sentence contains an unwanted operator.

    Returns:
        `list[str]`: The sentence with De Morgan's law applied.
    """

    index = 0
    # iterate through the sentence
    while index < len(sentence):

        # if the current character is a '~' and followed by a '(', then apply De Morgan's law
        if (sentence[index] == '~') and (sentence[index + 1] == '('):

            temp_sentence = []

            # get the parentheses enclosing the operand after the '~'
            parenthesis_begin, parenthesis_end = get_following_operand(sentence, index)

            # get the sub-sentence inside the parentheses
            sub_sentence = sentence[parenthesis_begin + 1: parenthesis_end]

            # determine the operator after the De Morgan's law is applied
            if get_main_operator(sub_sentence) == '&':
                operator_after_demorgan = "||"
            elif get_main_operator(sub_sentence) == '||':
                operator_after_demorgan = "&"

            # if the operator inside parentheses is not all '&' or not all '||', then the sentence is invalid
            else:
                raise ValueError("Invalid sentence: unwanted operator")

            sub_index = -1
            # iterate through the operands in the sub-sentence
            while sub_index < len(sub_sentence):
                operand_begin, operand_end = get_following_operand(sub_sentence, sub_index)

                # apply De Morgan's law to the operand and add it to the new sentence
                # format: ~ operand operator_after_demorgan
                temp_sentence += ['~'] + sub_sentence[operand_begin: operand_end + 1] + [operator_after_demorgan]

                # update the index to the next operator
                sub_index = operand_end + 1

            # replace the sub-sentence with the new sentence
            # old: ... ~ ( sub-sentence ) ...
            # new: ... ( new sub-sentence ) ...
            sentence = sentence[:index] + ['('] + temp_sentence[:-1] + [')'] + sentence[parenthesis_end + 1:]

            # eliminate double negation created during the application of De Morgan's law
            sentence = double_negation_elimination(sentence)

        # if the current character is not a '~' and followed by a '(', then skip
        index += 1

    # return the sentence
    return sentence

def apply_distributivity_or_over_and(sentence: list[str]) -> list[str]:
    """
    Apply the law of distributivity of disjunction over conjunction to the sentence.

    Args:
        sentence (`list[str]`): The sentence to apply the law of distributivity to.

    Returns:
        `list[str]`: The sentence with the law of distributivity applied.
    """

    index = 0
    # iterate through the sentence
    while index < len(sentence):

        # if found ||, then check if one of the operands is enclosed in parentheses
        if sentence[index] == '||':
            previous_begin, previous_end = get_previous_operand(sentence, index)
            following_begin, following_end = get_following_operand(sentence, index)
            temp_sentence = []

            # if || followed by a parentheses, then distribute the parentheses over the other operand
            if sentence[index + 1] == '(':
                sub_index = -1
                sub_sentence = sentence[following_begin + 1: following_end]

                # iterate through the operands in the sub-sentence
                while sub_index < len(sub_sentence):
                    operand_begin, operand_end = get_following_operand(sub_sentence, sub_index)

                    # add the distributed operand to the new sentence
                    # format: ( previous_operand || operand ) &
                    temp_sentence += ['('] + sentence[previous_begin: previous_end + 1] + ['||'] + sub_sentence[operand_begin: operand_end + 1] + [')', '&']

                    # update the index to the next operator in the sub-sentence
                    sub_index = operand_end + 1

                # replace both operands with the new sentence
                # old: ... previous_operand || ( sub-sentence ) ...
                # new: ... ( new sub-sentence ) ...
                sentence = sentence[:previous_begin] + ['('] + temp_sentence[:-1] + [')'] + sentence[following_end + 1:]

                # remove the unnecessary parentheses created during the distribution
                sentence = simplify_parentheses(sentence)

                # jump back to the beginning of the new sub-sentence
                index = previous_begin

            # if || preceded by a parentheses, then distribute the parentheses over the other operand
            elif sentence[index - 1] == ')':
                sub_index = -1
                sub_sentence = sentence[previous_begin + 1: previous_end]

                # iterate through the operands in the sub-sentence
                while sub_index < len(sub_sentence):
                    operand_begin, operand_end = get_following_operand(sub_sentence, sub_index)

                    # add the distributed operand to the new sentence
                    # format: ( operand || following_operand ) &
                    temp_sentence += ['('] + sub_sentence[operand_begin: operand_end + 1] + ['||'] + sentence[following_begin: following_end + 1] + [')', '&']

                    # update the index to the next operator in the sub-sentence
                    sub_index = operand_end + 1

                # replace both operands with the new sentence
                # old: ... ( sub-sentence ) || following_operand ...
                # new: ... ( new sub-sentence ) ...
                sentence = sentence[:previous_begin] + ['('] + temp_sentence[:-1] + [')'] + sentence[following_end + 1:]

                # remove the unnecessary parentheses created during the distribution
                sentence = simplify_parentheses(sentence)

                # jump back to the beginning of the new sub-sentence
                index = previous_begin

        # move to the next operator
        index += 1

    # return the sentence
    return sentence

def get_previous_operand(sentence: list[str], index: int) -> tuple[int, int]:
    """
    Get the index of the operand preceding the operator at the given index.

    Args:
        sentence (`list[str]`): The sentence to check.
        index (`int`): The index of the operator.

    Raises:
        `ValueError`: If the sentence is invalid.

    Returns:
        `tuple[int, int]`: The begin and end index of the operand preceding the operator.
    """
    # if the previous character is not a ')', then the operand is a single character
    if sentence[index - 1] != ')':
        # if there is a '~' before the operand, then move the begin index back by 1
        if index - 2 >= 0 and sentence[index - 2] == '~':
            return index - 2, index - 1

        # else, return the index of the operand
        return index - 1, index - 1

    parenthesis_stack = []
    # iterate backwards from the operator
    for i in range(index - 1, -1, -1):

        # push and pop the parenthesis stack
        if sentence[i] == ')':
            parenthesis_stack.append(i)
        elif sentence[i] == '(':
            if len(parenthesis_stack) > 0:
                parenthesis_stack.pop()

        # if the parenthesis stack is empty, then the whole operand has been found
        if len(parenthesis_stack) == 0:
            begin = i

            # check if the operand starts with a '~'
            # if it does, then move the begin index back by 1
            if begin - 1 >= 0 and sentence[begin - 1] == '~':
                begin -= 1

            return begin, index - 1

    # if the parenthesis stack is not empty, then the sentence is invalid
    raise ValueError("Invalid sentence")

def get_following_operand(sentence: list[str], index: int) -> tuple[int, int]:
    """
    Get the index of the operand following the operator at the given index.

    Args:
        sentence (`list[str]`): The sentence to check.
        index (`int`): The index of the operator.

    Raises:
        `ValueError`: If the sentence is invalid.

    Returns:
        `tuple[int, int]`: The begin and end index of the operand following the operator.
    """
    # check if the operand starts with a '~'
    # if it does, get the operand after the '~'
    if sentence[index + 1] == '~':
        _, end_after_not = get_following_operand(sentence, index + 1)
        return index + 1, end_after_not

    # if the operand not start with a '(', then the operand is a single character
    if sentence[index + 1] != '(':
        return index + 1, index + 1

    parenthesis_stack = []
    # iterate forwards from the operator
    for i in range(index + 1, len(sentence)):

        # push and pop the parenthesis stack
        if sentence[i] == '(':
            parenthesis_stack.append(i)
        elif sentence[i] == ')':
            if len(parenthesis_stack) > 0:
                parenthesis_stack.pop()

        # if the parenthesis stack is empty, then the whole operand has been found
        if len(parenthesis_stack) == 0:
            end = i
            return index + 1, end

    # if the parenthesis stack is not empty, then the sentence is invalid
    raise ValueError("Invalid sentence: " + " ".join(sentence))

def get_main_operator(sentence: list[str]) -> str | None:
    """
    Get the main operator that connects the operands in the sentence.

    Return `""` if the sentence is a single operand (no operator).\\
    Return `None` if the sentence has more than one operator connecting the operands (more than one operator).\\
    Return the operator if the sentence has only one operator connecting the operands (exactly one operator).

    Args:
        sentence (`list[str]`): The sentence to check.

    Returns:
        `str | None`: The main operator that connects the operands in the sentence.
    """
    operator = ""

    idx = -1
    # iterate through the sentence
    while idx < len(sentence):
        # get to the next operator after the current index
        _, end = get_following_operand(sentence, idx)
        idx = end + 1

        # if the index is out of bounds, then the sentence has no more operators
        if idx >= len(sentence):
            break

        # if the operator is not set, then set the operator
        if operator == "":
            operator = sentence[idx]

        # if the operator is already set, then check if the operator is the same as the previous operator
        # if the operator is different, then the sentence has more than one operator. return None
        elif sentence[idx] != operator:
            return None

    # return the operator
    return operator

def get_inside_parentheses(sentence: list[str], begin: int, end: int) -> tuple[int, int]:
    """
    Get the sub-sentence inside the parentheses.

    Args:
        sentence (`list[str]`): The sentence to get the sub-sentence from.
        begin (`int`): The beginning index of the parentheses.
        end (`int`): The ending index of the parentheses.

    Raises:
        `ValueError`: If the sentence is missing parentheses.
        `ValueError`: If the sub-sentence is not enclosed in parentheses.

    Returns:
        `list[str]`: The sub-sentence inside the parentheses.
    """
    # check if the sentence is enclosed in parentheses
    if get_main_operator(sentence[begin: end + 1]) != "":
        raise ValueError("Invalid range: sub-sentence should be enclosed in parentheses")

    open_parenthesis = None
    close_parenthesis = None

    # iterate through the sentence
    for index in range(begin, end + 1):

        # if found the first open parenthesis, then set the open parenthesis index
        if sentence[index] == '(' and open_parenthesis is None:
            open_parenthesis = index

        # if found the close parenthesis, then set the close parenthesis index
        elif sentence[index] == ')':
            close_parenthesis = index

    # if the open parenthesis index is None or the close parenthesis index is None, then the sentence is invalid
    if open_parenthesis is None or close_parenthesis is None:
        raise ValueError("Invalid sentence: missing parentheses")

    # return the beginning and ending index of the sub-sentence
    return open_parenthesis + 1, close_parenthesis - 1
