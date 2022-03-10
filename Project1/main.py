OPERATORS = ["<", "=<", "=", "!=", ">=", ">", "+", "-", "*", "/"]
OTHER = ["(", ")", ":", ";", "//", ":="]
KEY_WORDS = ["program", "end", "bool", "int", "while", "do", "od", "print", "false", "true", "not", "and", "or", "if", "fi", "then", "else"]
ALPHA = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
WHITESPACE = [" ", "\n"]
DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

def next(buffer: list, lineNumber: int):
    string = ""
    position = 1
    i = 0
    while i < len(buffer):
        if buffer[i] in WHITESPACE:
            i = ignoreWhiteSpace(buffer, i)
            continue
        elif buffer[i] in ALPHA:
            position = i+1
            string, i, kind = readAlpha(buffer, i)
        elif buffer[i] in OPERATORS or buffer[i] in OTHER or checkExclamationPoint(buffer, i):
            position = i+1
            string, i, kind = readOp(buffer, i)
        elif buffer[i] in DIGITS:
            position = i+1
            string, i, kind = readDigits(buffer, i)
        else:
            raise RuntimeError(f"ERROR: Invalid token at Line: {lineNumber}, Position: {position}, Character: {buffer[i]}")
        print(f"Line: {lineNumber}, Char: {position}, Kind: {kind}, {string}")

def checkExclamationPoint(buffer: list, curr_index: int):
    return buffer[curr_index] == "!" and curr_index+1 < len(buffer) and buffer[curr_index+1] == "="

def readDigits(buffer: list, curr_index: int):
    token = buffer[curr_index]
    curr_index += 1
    while curr_index < len(buffer) and buffer[curr_index] in DIGITS:
        token += buffer[curr_index]
        curr_index += 1
    return int(token), curr_index, kindOfToken(token)
    

def readOp(buffer: list, curr_index: int):
    token = buffer[curr_index]

    if not (curr_index+1 < len(buffer)):
        return token, curr_index+1, kindOfToken(buffer[curr_index])

    if token == "/" and buffer[curr_index+1] == "/": # Comments
        token += "/"
        curr_index = ignoreComments(buffer, curr_index+1)
        return token, curr_index, kindOfToken(token)
    elif token == ":" and buffer[curr_index+1] == "=": # assignment op 
        token += "="
        curr_index += 1
    elif token == ">" and buffer[curr_index+1] == "=": # Greater than or equal to
        token += ">="
        curr_index += 1

    return token, curr_index+1, kindOfToken(token)

        
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
    while curr_index < len(buffer) and buffer[curr_index] != "\n":
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
    with open("./examples/nonsense.txt") as file:
        try:
            for line in file.readlines():
                lineCount += 1
                lineArr = [char for char in line]
                next(lineArr, lineCount)
        except RuntimeError as err:
            print(err)
if __name__ == "__main__":
    main()
