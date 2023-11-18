
operators = ['~', '||', '&', '=>', '<=>']

def and_or_tranformation(sentence : list[str]):

    # biconditional elemination
    while '<=>' in sentence:
        index = sentence.index('<=>')
        sentence = sentence[:index-1] + [['(', '~', sentence[index-1], '||', sentence[index+1], ')'], '&', ['(', '~', sentence[index+1], '||', sentence[index-1], ')']] + sentence[index+2:]

    # implication elemination
    while '=>' in sentence:
        index = sentence.index('=>')
        sentence = sentence[:index-1] + [['(', '~', sentence[index-1], '||', sentence[index+1], ')']] + sentence[index+2:]

    # De Morgan's Law
    if '~' in sentence:
        if sentence[sentence.index('~') + 1] == '(':
            sentence = de_morgan(sentence[sentence.index('~') + 1:])

    # Distributivity of & over ||
    if '||' in sentence:
        if sentence[sentence.index('||') + 1] == '(':
            sentence = distribute(sentence[sentence.index('||') - 1:])

    return sentence

def de_morgan(sentence):
    # Implement De Morgan's Law
    if '&' in sentence:
        conjunction_index = sentence.index('&')

        # Initialize the new sentence
        new_sentence = sentence[:conjunction_index]
        new_sentence.insert(1, '~')


        for i in range(conjunction_index + 1, len(sentence), 2):
            new_sentence += ['||', '~', sentence[i]]
    else:
        conjunction_index = sentence.index('||')

        # Initialize the new sentence
        new_sentence = sentence[:conjunction_index]
        new_sentence.insert(1, '~')


        for i in range(conjunction_index + 1, len(sentence), 2):
            new_sentence += ['&', '~', sentence[i]]

    new_sentence.append(')')
    return new_sentence

def distribute(sentence):
# def distribute_or_over_and(sentence):
    # Find the index of the OR operator '||'
    or_index = sentence.index('||') if '||' in sentence else -1

    # If OR operator is not found, return the original sentence
    if or_index == -1:
        return sentence

    # Find the index of the AND operator '&'
    and_index = sentence.index('&', or_index)

    # Extract operands before and after the AND operator
    operand_before = sentence[:or_index]
    print(operand_before)
    operand_after = sentence[and_index + 1::2]
    # remove all the '&' operator in operand_after
    
    # Extract the AND operands
    and_operands = sentence[or_index + 2:and_index]
    
    # Distribute '||' over '&'
    distributed_sentence = ['('] + operand_before + ['||', and_operands[0], ')']

    while operand_after:
        operand = operand_after.pop(0)
        distributed_sentence += ['&', '(', operand_before[0], '||',  operand, ')']


    return distributed_sentence
