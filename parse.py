def parse(file_name):

    # Read the file and return the data
    with open(file_name, "r", encoding="utf-8") as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]

    KB = []
    query = []
    if lines[0] == "TELL":
        for i in range(1, len(lines)):
            if lines[i] == "ASK":
                query.append(lines[i+1])
                break
            else:
                KB = (lines[i].split(";"))
                # remove the space in the KB
                # Remove empty string
                KB = [x.strip() for x in KB if x.strip()]
    # split by " " for each element in the KB
    for i in range(len(KB)):
        KB[i] = KB[i].split(" ")
        
    return KB, query
