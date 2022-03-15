OPERATORS = ["<", "=<", "=", "!=", ">=", ">", "+", "-", "*", "/"]
OTHER = ["(", ")", ":", ";", ":="]
KEY_WORDS = ["program", "end", "bool", "int", "while", "do", "od", "print", "false", "true", "not", "and", "or", "if", "fi", "then", "else"]
ALPHA = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
WHITESPACE = [" ", "\n"]
DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

class LexAnalyzer:
    def __init__(self, fileName: str):
        self.token = "" # Store the token
        self.kindToken = "" # Store the kind of token
        self.lineCount = 0 # Store the line count of file
        self.positionToken = 0 # Character count of the token
        self.file = open(fileName) # Creates the file object for the object
        self.buffer = self.__getBuffer__() # Generates the buffer
        self.curr_index = 0 # Sets the current index to 0
    
    def kind(self):
        '''
        Returns the kind of the token
        '''
        return self.kindToken

    def value(self):
        '''
        Returns the value of the token
        '''
        return self.token

    def position(self):
        '''
        Returns the position of the token
        (LineCount, CharacterCount)
        '''
        return (self.lineCount, self.positionToken)
        
    def next(self):
        '''
        Gets the next token in the buffer
        '''
        self.__reset__() # Reset token and kind

        # Check to see if there is whitespace or a comment
        self.curr_index = ignoreWhiteSpace(self.buffer, self.curr_index)
        self.curr_index = ignoreComments(self.buffer, self.curr_index)
        
        # Check to see if the buffer is at the end
        self.__checkBuffer__()

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

    def __checkBuffer__(self):
        '''
        Ensures that the buffer can still be read
        If the index is >= than the buffer length, get the next line in the buffer
        Ignore all leading whitespace (if any)
        '''
        if self.curr_index >= len(self.buffer):
            self.buffer = self.__getBuffer__()
            self.curr_index = ignoreWhiteSpace(self.buffer, self.curr_index)
        

    def __getBuffer__(self):
        '''
        Reads the next line in the text file and creates a buffer for the object to read
        '''
        line = self.file.readline()
        if line == "": # readline() returns '' when the EOF has been reached
            self.kindToken = "End-of-text"
        
        self.curr_index = 0
        self.positionToken = self.curr_index+1

        self.lineCount += 1
        lineArr = [char for char in line] # Generate buffer

        return lineArr

    def __reset__(self):
        '''
        Resets the token and kind of token to prepare for the next "Next()" call
        '''
        self.token = ""
        self.kindToken = ""
    
    
def isComment(buffer: list, curr_index: int):
    ''' Checks to see if the first / seen is followed by another / to make a comment'''
    return curr_index < len(buffer) and buffer[curr_index] == "/" and curr_index+1 < len(buffer) and buffer[curr_index+1] == "/"

def checkExclamationPoint(buffer: list, curr_index: int):
    ''' Check For Exclamation point or for != '''
    return buffer[curr_index] == "!" and curr_index+1 < len(buffer) and buffer[curr_index+1] == "="

def readDigits(buffer: list, curr_index: int):
    '''
    Read Digits
    '''
    token = buffer[curr_index]
    curr_index += 1
    while curr_index < len(buffer) and buffer[curr_index] in DIGITS:
        token += buffer[curr_index]
        curr_index += 1
    return token, curr_index, kindOfToken(token)
    

def readOp(buffer: list, curr_index: int):
    '''
    Read operators
    '''
    # store the first token (That has already been checked to be an operator)
    token = buffer[curr_index]
    curr_index += 1

    # return if the end of the line buffer has been reached
    if curr_index >= len(buffer):
        return token, curr_index, kindOfToken(token)

    if token == ":" and buffer[curr_index] == "=": # assignment op 
        token += "="
    elif token == ">" and buffer[curr_index] == "=": # Greater than or equal to
        token += "="
    elif token == "=" and buffer[curr_index] == "<": # Less than or equal to 
        token += "<"
    elif token == "!" and buffer[curr_index] == "=": # Not equal to
        token += "="

    # If the token is a single character, move the index up 1
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
    '''
    Ignores whitespace
    '''
    while curr_index < len(buffer) and buffer[curr_index] in WHITESPACE:
        curr_index += 1
    return curr_index

def ignoreComments(buffer: list, curr_index: int):
    '''
    Checks to see if the character at curr_index and curr_index+1 are '//' if so, ignore the rest of the line
    '''
    if isComment(buffer, curr_index):
        return len(buffer)
    else:
        return curr_index


def kindOfToken(token:str):
    '''
    Returns the token kind
    '''
    if token in KEY_WORDS or token in OPERATORS or token in OTHER:
        return token
    if token.isdigit():
        return "NUM"
    return "ID"

