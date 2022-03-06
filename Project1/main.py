OPERATORS = ["<", "=<", "=", "!=", ">=", ">", "+", "-", "*", "/"]
OTHER = ["(", ")", ":", ";"]
KEY_WORDS = ["program", "end", "bool", "int", "while", "do", "od", "print", "false", "true", "not", "and", "or", "if", "fi", "then", "else"]
ALPHA = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
WHITESPACE = [" ", "\n"]
DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

def tokenize(buffer: list, lineNumber: int):
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
            print(f"Token is: {string} | character position: {position} | Line number: {lineNumber} | kind: {kind}")
        elif buffer[i] == "/":
            if buffer[i+1] == "/":
                i = ignoreComments(buffer, i+1)
            else:
                position = i+1
                print(f"Token is: {buffer[i]} | character position: {position} | Line number: {lineNumber} | kind: {buffer[i]}")
                i+=1
        elif buffer[i] == ":":
            if buffer[i+1] == "=":
                position = i+2
                print(f"Token is: {buffer[i]+buffer[i+1]} | character position: {position} | Line number: {lineNumber} | kind: {buffer[i]}")
                i+=1
            else:
                position = i+1
                print(f"Token is: {buffer[i]} | character position: {position} | Line number: {lineNumber} | kind: {buffer[i]}")
                i+=1
        elif buffer[i] == "<":
            pass
        elif buffer[i] == ">":
            pass
        elif buffer[i] == "!":
            pass
        elif buffer[i] == "=":
            pass
        else:
            i += 1

def readAlpha(buffer: list, curr_index: int):
    '''
    Allowed characters in an ID/Keyword are ALPHA, KEYWORKS, "_" and DIGIT
    MUST BEGIN WITH A LETTER
    '''
    if buffer[curr_index] not in ALPHA:
        raise RuntimeError("First character must be a letter")
    token = ""
    kind = ""
    charCount = curr_index
    while curr_index < len(buffer):
        token += buffer[curr_index]
        curr_index += 1
        charCount += 1
        if buffer[curr_index] in WHITESPACE:
            curr_index = ignoreWhiteSpace(buffer, curr_index)
            kind = kindOfToken(token)
            return token, curr_index, kind
        if buffer[curr_index] in OPERATORS or buffer[curr_index] in OTHER:
            kind = kindOfToken(token)
            return token, curr_index, kind
        if not buffer[curr_index] in ALPHA and not buffer[curr_index] == '_' and not buffer[curr_index] in DIGITS:
            print(f"ERROR | curr_index: {curr_index} | buffer char: {buffer[curr_index]}")
            raise RuntimeError("Invalid Token")
        

def ignoreWhiteSpace(buffer: list, curr_index: int):
    while curr_index < len(buffer) and buffer[curr_index] in WHITESPACE:
        # print(f"Ignoring {buffer[curr_index]}")
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
    with open(".\examples\euclid.txt") as file:
        try:
            for line in file.readlines():
                lineCount += 1
                lineArr = [char for char in line]
                tokenize(lineArr, lineCount)
        except:
            print(f"Invlaid token at lineNumber: {lineCount}")
if __name__ == "__main__":
    main()
