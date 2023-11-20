operators = ['~', '||', '&', '=>', '<=>']

def transform_to_cnf(sentence : list[str]):

    print("===================================")
    sentence = add_parentheses_around_operator(sentence, "&")
    print("1. add_parentheses_around_operator(sentence, '&')")
    print(sentence)
    sentence = add_parentheses_around_operator(sentence, "||")
    print("2. add_parentheses_around_operator(sentence, '||')")
    print(sentence)
    sentence = simplify_parentheses(sentence)
    print("3. simplify_parentheses(sentence)")
    print(sentence)
    sentence = bidirectional_elemination(sentence)
    print("4. bidirectional_elemination(sentence)")
    print(sentence)
    sentence = implication_elemination(sentence)
    print("5. implication_elemination(sentence)")
    print(sentence)
    sentence = double_negation_elimination(sentence)
    print("6. double_negation_elimination(sentence)")
    print(sentence)
    sentence = simplify_parentheses(sentence)
    print("7. simplify_parentheses(sentence)")
    print(sentence)
    sentence = de_morgan_law(sentence)
    print("8. de_morgan_law(sentence)")
    print(sentence)
    sentence = simplify_parentheses(sentence)
    print("9. simplify_parentheses(sentence)")
    print(sentence)
    sentence = combine_negation(sentence)
    print("10. combine_negation(sentence)")
    print(sentence)
    sentence = simplify_parentheses(sentence)
    print("11. simplify_parentheses(sentence)")
    print(sentence)
    sentence = distribute(sentence)
    print("12. distribute(sentence)")
    print(sentence)

    # split to list of clauses
    sentence = "".join(sentence)
    sentence = sentence.replace('(', '').replace(')', '')
    print("13. split to list of clauses")
    print(sentence)
    sentence = sentence.split('&')
    print("14. split to list of clauses")
    print(sentence)
    sentence = [i.split('||') for i in sentence]
    print("15. split to list of clauses")
    print(sentence)

    return sentence

def de_morgan_law(sentence):
    index = 0
    while index < len(sentence):
        if (sentence[index] == '~') and (sentence[index + 1] == '('):

            temp_sentence = []

            following_begin, following_end = get_following_operand(sentence, index)

            temp_sentence = sentence[:index] + ['(']
            if get_main_operator(sentence[following_begin + 1: following_end]) == '&':
                changed_operator = "||"
            elif get_main_operator(sentence[following_begin + 1: following_end]) == '||':          
                changed_operator = "&"

            sub_index = -1
            sub_sentence = sentence[following_begin + 1: following_end]
            while sub_index < len(sub_sentence):
                operand_begin, operand_end = get_following_operand(sub_sentence, sub_index)
                temp_sentence += ['~'] + sub_sentence[operand_begin: operand_end + 1] + [changed_operator]
                sub_index = operand_end + 1

            sentence = temp_sentence[:-1] + [')'] + sentence[following_end + 1:]
            sentence = double_negation_elimination(sentence)

        index += 1
    return sentence

def distribute(sentence):
    index = 0
    while index < len(sentence):

        if sentence[index] == '||':
            previous_begin, previous_end = get_previous_operand(sentence, index)
            following_begin, following_end = get_following_operand(sentence, index)
            temp_sentence = []

            if sentence[index + 1] == '(':
                sub_index = -1
                sub_sentence = sentence[following_begin + 1: following_end]
                
                while sub_index < len(sub_sentence):
                    operand_begin, operand_end = get_following_operand(sub_sentence, sub_index)
                    temp_sentence += ['('] + sentence[previous_begin: previous_end + 1] + ['||'] + sub_sentence[operand_begin: operand_end + 1] + [')', '&']
                    sub_index = operand_end + 1
                
                sentence = sentence[:previous_begin] + ['('] + temp_sentence[:-1] + [')'] + sentence[following_end + 1:]
                sentence = simplify_parentheses(sentence)
                
                index = previous_begin

            elif sentence[index - 1] == ')':
                sub_index = -1
                sub_sentence = sentence[previous_begin + 1: previous_end]
                
                while sub_index < len(sub_sentence):
                    operand_begin, operand_end = get_following_operand(sub_sentence, sub_index)
                    temp_sentence += ['('] + sub_sentence[operand_begin: operand_end + 1] + ['||'] + sentence[following_begin: following_end + 1] + [')', '&']
                    sub_index = operand_end + 1
                
                sentence = sentence[:previous_begin] + ['('] + temp_sentence[:-1] + [')'] + sentence[following_end + 1:]
                sentence = simplify_parentheses(sentence)
                
                index = previous_begin
        
        index += 1
    
    return sentence

def bidirectional_elemination(sentence):
    while '<=>' in sentence:
        index = sentence.index('<=>')
        previous_begin, previous_end = get_previous_operand(sentence, index)
        following_begin, following_end = get_following_operand(sentence, index)
        sentence = sentence[:previous_begin] +  ['(', '('] + sentence[previous_begin:previous_end + 1] + ['=>'] + sentence[following_begin:following_end + 1] + [')'] + ['&'] + ['('] + sentence[following_begin:following_end + 1] + ['=>'] + sentence[previous_begin:previous_end + 1] +[')', ')'] + sentence[following_end + 1:]
    return sentence

def implication_elemination(sentence):
    while '=>' in sentence:
        index = sentence.index('=>')
        previous_begin, previous_end = get_previous_operand(sentence, index)
        following_begin, following_end = get_following_operand(sentence, index)
        sentence = sentence[:previous_begin] +  ['(', '~'] + sentence[previous_begin:previous_end + 1] + ['||'] + sentence[following_begin:following_end + 1] + [')'] + sentence[following_end + 1:]
    return sentence    
    
def double_negation_elimination(sentence):
    index = 0
    while index < len(sentence):
        if sentence[index] == '~' and sentence[index + 1] == '~':
            sentence = sentence[:index] + sentence[index + 2:]
        index += 1
    return sentence

def combine_negation(sentence):
    while '~' in sentence:
        index = sentence.index('~')
        sentence = sentence[:index] + ['~' + sentence[index + 1]] + sentence[index + 2:]
    return sentence

##############################################################################################################

def get_previous_operand(sentence: list[str], index: int) -> tuple[int, int]:
    """
    Get the index of the operand preceding the operator at the given index.

    Args:
        sentence (list[str]): The sentence to check.
        index (int): The index of the operator.

    Raises:
        ValueError: If the sentence is invalid.

    Returns:
        tuple[int, int]: The begin and end index of the operand preceding the operator.
    """
    # if the previous character is not a ')', then the operand is a single character
    if sentence[index - 1] != ')':
        return index - 1, index - 1

    parenthesis_stack = []
    # iterate backwards from the operator
    for i in range(index - 1, -1, -1):
        if sentence[i] == ')':
            parenthesis_stack.append(i)
        elif sentence[i] == '(':
            if len(parenthesis_stack) > 0:
                parenthesis_stack.pop()

        # if the parenthesis stack is empty, then the whole operand has been found
        if len(parenthesis_stack) == 0:
            begin = i
            return begin, index - 1

    # if the parenthesis stack is not empty, then the sentence is invalid
    raise ValueError("Invalid sentence")

def get_following_operand(sentence: list[str], index: int) -> tuple[int, int]:
    """
    Get the index of the operand following the operator at the given index.

    Args:
        sentence (list[str]): The sentence to check.
        index (int): The index of the operator.

    Raises:
        ValueError: If the sentence is invalid.

    Returns:
        tuple[int, int]: The begin and end index of the operand following the operator.
    """
    if sentence[index + 1] == '~':
        _, end_after_not = get_following_operand(sentence, index + 1)
        return index + 1, end_after_not

    # if the next character is not a '(', then the operand is a single character
    if sentence[index + 1] != '(':
        return index + 1, index + 1

    parenthesis_stack = []
    # iterate forwards from the operator
    for i in range(index + 1, len(sentence)):
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
    raise ValueError("Invalid sentence")

def add_parentheses_around_operator(sentence: list[str], operator: str) -> list[str]:
    """
    Add parentheses to isolate the operands connected by the operator in the sentence.

    Args:
        sentence (list[str]): The sentence to add parentheses to.
        operator (str): The operator to isolate.

    Returns:
        list[str]: The sentence with parentheses added.
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
            sentence = sentence[:before+1] + ["("] + sentence[before+1:after] + [")"] + sentence[after:]

            # skip to the end of the parentheses
            idx = after + 2

        # if the current character is not the operator, then skip
        else:
            idx += 1

    return sentence

def simplify_parentheses(sentence: list[str]) -> list[str]:
    """
    Simplify the parentheses in the sentence.

    Remove the parantheses if the sub-sentence inside the parentheses has the same main operator as the sentence.

    If the sentence does not contain any parentheses, then the sentence has been simplified.

    Args:
        sentence (list[str]): The sentence to simplify.

    Returns:
        list[str]: The simplified sentence.
    """
    # if the sentence does not contain any parentheses, then the sentence has been simplified
    if "(" not in sentence:
        return sentence

    # get the main operator of the sentence
    main_operator = get_main_operator(sentence)

    # if the sentence has no operator, then the sentence is enclosed in parentheses
    if main_operator == "":
        return simplify_parentheses(sentence[1:-1])

    idx = -1
    # iterate through the sentence
    while idx < len(sentence):

        # find the operands following the operator at the current index
        begin, end = get_following_operand(sentence, idx)

        # if the operands are enclosed in parentheses
        if sentence[begin] == "(" and sentence[end] == ")":

            # simplify the sub-sentence inside the parentheses and replace the sub-sentence with the simplified version
            sentence[begin+1:end] = (simplified := simplify_parentheses(sentence[begin+1:end]))
            end = begin + len(simplified) + 1

            # if the sub-sentence has the same main operator as the sentence, or the sub-sentence is a single operand, then remove the parentheses
            sub_operator = get_main_operator(sentence[begin+1:end])
            if sub_operator == main_operator or sub_operator == "":
                sentence = sentence[:begin] + sentence[begin+1:end] + sentence[end+1:]
                idx = end - 1

            # else, skip to the end of the parentheses
            else:
                idx = end + 1
        else:
            idx = end + 1

    return sentence

def get_main_operator(sentence: list[str]) -> str | None:
    """
    Get the main operator that connects the operands in the sentence.

    Return "" if the sentence is a single operand (no operator).

    Return None if the sentence has more than one operator connecting the operands (more than one operator).

    Return the operator if the sentence has only one operator connecting the operands (exactly one operator).

    Args:
        sentence (list[str]): The sentence to check.

    Returns:
        str | None: The main operator that connects the operands in the sentence.
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

sentence = ['(', '(', '~', '(', '(', '~', 'c', '||', '~', 'd', ')', ')', '||', 'a', ')', ')']
sentence = simplify_parentheses(sentence)
print(sentence)
