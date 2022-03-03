
OPERATORS = ["<", "=<", "=", "!=", ">=", ">", "+", "-", "*", "/"]
OTHER = ["_", "(", ")", ":", ";"]
KEY_WORDS = ["program", "end", "bool", "int", "while", "do", "od", "print", "false", "true", "not", "and", "or", "if", "fi", "then", "else"]
alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

with open("./examples/ab.txt") as file:
    chars = [char for char in file.read()]
    print(chars)

def tokenize(buffer: list):
    tokens = []
    string = ""
    for char in buffer:
        if char in alpha:
            string += char
        elif char == " " or char == "\n":
            tokens.append(string)
            string = ""
    print(tokens)

def ignoreWhiteSpace(buffer: list):
    char = buffer[0]
    i = 1
    while ord(char) in [3, 9, 10, 11, 32]:
        buffer.pop(i)
        print("space")
        char = buffer[i]
    return buffer

def kindOfToken(token:str):
    if token in KEY_WORDS or token in OPERATORS or token in OTHER:
        return token
    if token.isdigit():
        return "NUM"
    return "ID"
        
tokenize(chars)