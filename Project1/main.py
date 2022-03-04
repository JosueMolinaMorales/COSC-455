OPERATORS = ["<", "=<", "=", "!=", ">=", ">", "+", "-", "*", "/"]
OTHER = ["(", ")", ":", ";"]
KEY_WORDS = ["program", "end", "bool", "int", "while", "do", "od", "print", "false", "true", "not", "and", "or", "if", "fi", "then", "else"]
ALPHA = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
WHITESPACE = [" ", "\n"]

def tokenize(buffer: list):
    tokens = []
    string = ""
    i = 0
    while i < len(buffer):
        if buffer[i] in WHITESPACE:
            i = ignoreWhiteSpace(buffer, i)
            continue
        if buffer[i] in ALPHA:
            string, i = readAlpha(buffer, i)

def readAlpha(buffer: list, curr_index: int):
    '''
    Allowed characters in an ID/Keyword are ALPHA, KEYWORKS, "_" and DIGIT
    MUST BEGIN WITH A LETTER
    '''
    if buffer[curr_index] not in ALPHA:
        raise RuntimeError("First character must be a letter")
    token = ""
    value = ""
    charCount = curr_index
    while curr_index < len(buffer):
        token += buffer[curr_index]
        curr_index += 1
        if buffer[curr_index] in WHITESPACE:
            curr_index = ignoreWhiteSpace(buffer, curr_index)
            return token, curr_index
        if buffer[curr_index] in OPERATORS:
            return token, curr_index
        if buffer[curr_index] != "_":
            return "ERROR"
        

def ignoreWhiteSpace(buffer: list, curr_index: int):
    while curr_index < len(buffer):
        if buffer[curr_index] in WHITESPACE:
            curr_index += 1
    return curr_index

def kindOfToken(token:str):
    if token in KEY_WORDS or token in OPERATORS or token in OTHER:
        return token
    if token.isdigit():
        return "NUM"
    return "ID"

def main():
    lineCount = 0
    with open("./examples/if.txt") as file:
        for line in file.readlines():
            lineCount += 1
            lineArr = [char for char in line]
            tokenize(lineArr)

if __name__ == "__main__":
    main()