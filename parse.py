def parse(file_name):
    # Read the file and return the data
    with open(file_name, "r", encoding="utf-8") as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]

    # Initialize input Knowledge Base (input_kb) and Query lists
    input_kb = []
    query = []

    # Check if the first line is "TELL"
    if lines[0] == "TELL":
        # Iterate through the lines starting from the second line
        for i in range(1, len(lines)):
            # Check if the current line is "ASK"
            if lines[i] == "ASK":
                # Append the next line to the query list and break the loop
                query.append(lines[i+1])
                break
            else:
                # Split the current line by semicolon, remove spaces, and add to input_kb
                input_kb = (lines[i].split(";"))
                input_kb = [x.strip() for x in input_kb if x.strip()]

    # Split each element in input_kb by space
    for i in range(len(input_kb)):
        input_kb[i] = input_kb[i].split(" ")

    # Process input_kb: if there is '&' in the first element, split it and add the symbol
    processed_kb = []
    for sublist in input_kb:
        if '&' in sublist[0]:
            elements = sublist[0].split('&')
            processed_kb.append([elements[0]] + ['&'] + [elements[1]] + ['=>'] + sublist[2:])
        else:
            processed_kb.append(sublist)

    return processed_kb, query
