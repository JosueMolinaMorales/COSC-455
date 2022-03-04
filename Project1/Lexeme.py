OPERATORS = ["<", "=<", "=", "!=", ">=", ">", "+", "-", "*", "/"]
OTHER = ["_", "(", ")", ":", ";"]
KEY_WORDS = ["program", "end", "bool", "int", "while", "do", "od", "print", "false", "true", "not", "and", "or", "if", "fi", "then", "else"]
ALPHA = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

class Lexeme:
    def __init__(self):
        self.token = ""
        self.kind = ""
        self.value = ""
        self.position = 0

    def getKind(self):
        if len(self.token) == 0:
            raise RuntimeError("Token must have a value")
        
        if self.token in KEY_WORDS or self.token in OPERATORS or self.token in OTHER:
            return self.__delattr__token
        if self.token.isdigit():
            return "NUM"
        return "ID"