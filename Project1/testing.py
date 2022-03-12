from Lexeme import LexAnalyzer
lex = LexAnalyzer("examples\if.txt")

try:
    lex.next()
    while lex.kind() != "End-of-text":
        print(lex.position(), lex.kind(), lex.value())
        lex.next()
    print("End of text has been reached")
except RuntimeError as err:
    print(err)




