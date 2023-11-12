class parse:
    def __init__(self, fileName) -> None:
        self.fileName = fileName
        self.lines = self.read_file()
        self.KB = []
        self.query = []
        self.parse()
        print(self.KB)
        print(self.query)

    def read_file(self):
        # Read the file and return the data
        with open(self.fileName, "r", encoding="utf-8") as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]
            return lines
        
    def parse(self):
        # the first line of the file is the word TELL
        # add the next line to the KB until read the word ASK
        # add the next line to the query
        # return the KB and the query
        KB = []
        if self.lines[0] == "TELL":
            for i in range(1, len(self.lines)):
                if self.lines[i] == "ASK":
                    self.query.append(self.lines[i+1])
                    break
                else:
                    KB = (self.lines[i].split(";"))
                    # remove the space in the KB
                    # Remove empty string
                    KB = [x.strip() for x in KB if x.strip()]
        self.KB = KB
        # split by " " for each element in the KB
        for i in range(len(self.KB)):
            self.KB[i] = self.KB[i].split(" ")
            
        return self.KB, self.query
        
if __name__ == "__main__":
    fileName = "data.txt"
    kb = parse(fileName)

