#! /usr/bin/env python3
from LexAnalyzer import Tokenizer

FILE = "./examples/ab.txt"
lex = Tokenizer(FILE)

def main():
    global FILE, lex
    try:
        lex.next()
        Program()
        print(f"Curr_token: {lex.value()}")
        print("Hello world")
    except Exception as e:
        print(e)

def match(symbol: str):
    global lex
    if lex.kind() == symbol:
        lex.next()
    else:
        raise RuntimeError(f"ERROR: At Position {lex.position()}. Expected {symbol}, Saw {lex.kind()}")

def Program():
    match('program')
    match('ID')
    match(':')
    Body()
    match('end')

def Body():
    pass


if __name__ == "__main__":
    main()