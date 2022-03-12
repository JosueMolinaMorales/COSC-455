OPERATORS = ["<", "=<", "=", "!=", ">=", ">", "+", "-", "*", "/"]
OTHER = ["(", ")", ":", ";", ":="]
KEY_WORDS = ["program", "end", "bool", "int", "while", "do", "od", "print", "false", "true", "not", "and", "or", "if", "fi", "then", "else"]
ALPHA = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
WHITESPACE = [" ", "\n"]
DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

class LexAnalyzer:
    def __init__(self, fileName: str):
        self.token = ""
        self.kindToken = ""
        self.lineCount = 0
        self.positionToken = 0
        self.file = open(fileName)
        self.buffer = self.__getBuffer()
        self.curr_index = 0

    def __reset(self):
        self.token = ""
        self.kindToken = ""
    
    def value(self):
        return self.token

    def position(self):
        return self.positionToken
        
    def next(self):
        self.__reset() # Reset token and kind

        # Check to see if there is whitespace or a comment
        self.curr_index = ignoreWhiteSpace(self.buffer, self.curr_index)
        self.curr_index = ignoreComments(self.buffer, self.curr_index)
        
        # Check to see if the buffer is at the end
        self.__checkBuffer()

        if len(self.buffer) == 0: # End of Text has been reached
            return self.kindToken
            
        if self.buffer[self.curr_index] in ALPHA:
            self.positionToken = self.curr_index+1
            self.token, self.curr_index, self.kindToken = readAlpha(self.buffer, self.curr_index)
        elif self.buffer[self.curr_index] in OPERATORS or self.buffer[self.curr_index] in OTHER or checkExclamationPoint(self.buffer, self.curr_index):
            self.positionToken = self.curr_index+1
            self.token, self.curr_index, self.kindToken = readOp(self.buffer, self.curr_index)
        elif self.buffer[self.curr_index] in DIGITS:
            self.positionToken = self.curr_index+1
            self.token, self.curr_index, self.kindToken = readDigits(self.buffer, self.curr_index)
        else:
            raise RuntimeError(f"ERROR: Invalid token at Line: {self.lineCount}, Position: {self.positionToken}, Character: {self.buffer[self.curr_index]}")

        #print(f"Line: {self.lineCount}, Char: {self.positionToken}, Kind: {self.kindToken}, {self.token}")
        return self.token

    def __checkBuffer(self):
        if self.curr_index >= len(self.buffer):
            self.buffer = self.__getBuffer()
            self.curr_index = ignoreWhiteSpace(self.buffer, self.curr_index)
        

    def __getBuffer(self):
        line = self.file.readline()
        if line == "":
            self.kindToken = "End-of-text"
        self.curr_index = 0
        self.positionToken = self.curr_index+1
        self.lineCount += 1
        lineArr = [char for char in line]
        return lineArr
    
    def kind(self):
        return self.kindToken
    
def isComment(buffer: list, curr_index: int):
    return curr_index < len(buffer) and buffer[curr_index] == "/" and curr_index+1 < len(buffer) and buffer[curr_index+1] == "/"

def checkExclamationPoint(buffer: list, curr_index: int):
    return buffer[curr_index] == "!" and curr_index+1 < len(buffer) and buffer[curr_index+1] == "="

def readDigits(buffer: list, curr_index: int):
    token = buffer[curr_index]
    curr_index += 1
    while curr_index < len(buffer) and buffer[curr_index] in DIGITS:
        token += buffer[curr_index]
        curr_index += 1
    return token, curr_index, kindOfToken(token)
    

def readOp(buffer: list, curr_index: int):
    token = buffer[curr_index]
    curr_index += 1
    if not (curr_index < len(buffer)):
        return token, curr_index, kindOfToken(token)

    if token == ":" and buffer[curr_index] == "=": # assignment op 
        token += "="
    elif token == ">" and buffer[curr_index] == "=": # Greater than or equal to
        token += "="
    elif token == "=" and buffer[curr_index] == "<": # Less than or equal to 
        token += "<"
    elif token == "!" and buffer[curr_index] == "=": # Not equal to
        token += "="

    if len(token) > 1:
        return token, curr_index+1, kindOfToken(token)
    
    return token, curr_index, kindOfToken(token)

        
def readAlpha(buffer: list, curr_index: int):
    '''
    Allowed characters in an ID/Keyword are ALPHA, KEYWORKS, "_" and DIGIT
    MUST BEGIN WITH A LETTER
    '''
    if buffer[curr_index] not in ALPHA:
        raise RuntimeError("First character must be a letter")
    token = ""
    while curr_index < len(buffer) and buffer[curr_index] in ALPHA or buffer[curr_index] in DIGITS or buffer[curr_index] == "_" :
        token += buffer[curr_index]
        curr_index += 1
    return token, curr_index, kindOfToken(token)

def ignoreWhiteSpace(buffer: list, curr_index: int):
    while curr_index < len(buffer) and buffer[curr_index] in WHITESPACE:
        curr_index += 1
    return curr_index

def ignoreComments(buffer: list, curr_index: int):
    if isComment(buffer, curr_index):
        return len(buffer)
    else:
        return curr_index


def kindOfToken(token:str):
    if token in KEY_WORDS or token in OPERATORS or token in OTHER:
        return token
    if token.isdigit():
        return "NUM"
    return "ID"

