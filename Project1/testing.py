from main import *

# Test Cases for kind of token
tokens = [("program","program"), ("Program", "ID"), ("3400", "NUM"), ("0", "NUM"), (";", ";"), ("myProgram", "ID")]
for test, correct in tokens:
    print(f"Testing: {test}. Correct: {correct}. Valid? {correct == kindOfToken(test)}")

simplePrograms = [
    "program test: \n" +
    "   int a := b"
]

next()

