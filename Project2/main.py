#! /usr/bin/env python3
from ast import Assert
from LexAnalyzer import Tokenizer

FILE = "./examples/euclid.txt"
lex = Tokenizer(FILE)

def main():
    try:
        lex.next()
        Program()
        print(f"Sucessfully parsed {FILE}")
    except Exception as e:
        print(e)

def match(symbol: str):
    print("In match(), lex.kind() is: " + lex.kind() + " and symbol is: " + symbol)
    if lex.kind() == symbol:
        lex.next()
    else:
        value = lex.value() if lex.value != "" else lex.kind()
        raise RuntimeError(f"ERROR: At Position {lex.position()}. Expected {symbol}, Saw {value}")

def Program():
    match('program')
    match('ID')
    match(':')
    Body()
    match('end')

def Body():
    if lex.kind() in ('bool', 'int'):
        Declarations()
    Statements()

def Declarations():
    Declaration()
    while lex.kind() in ('bool', 'int'):
        Declaration()

def Declaration():
    Assert(lex.kind() in ('bool', 'int'))
    lex.next()
    match('ID')
    match(';')

def Statements():
    Statement()
    while lex.kind() == ';':
        lex.next()
        Statement()

def Statement():
    if lex.kind() == 'ID': # the kind of curr_symbol is ID
        AssignmentStatement()
    elif lex.kind() == 'if':
        ConditionalStatement()
    elif lex.kind() == 'while':
        IterativeStatement()
    elif lex.kind() == 'print':
        PrintStatement()
    else:
        Expected(['ID', 'if', 'while', 'print'])

def Expected(setSymbols):
    if lex.kind() not in setSymbols:
        raise RuntimeError(f"ERROR: At Position {lex.position}. {lex.value()} was seen. Expected {setSymbols}")

def AssignmentStatement():
    match("ID")
    match(':=')
    Expression()

def ConditionalStatement():
    match('if')
    Expression()
    match('then')
    Body()
    if lex.kind() == "else":
        lex.next()
        Body()
    match('fi')

def IterativeStatement():
    match('while')
    Expression()
    match('do')
    Body()
    match('od')

def PrintStatement():
    match('print')
    Expression()

def Expression():
    SimpleExpression()
    if lex.kind() in ("<", "=<", "=", "!=", ">=", ">"):
        lex.next()
        SimpleExpression()

def SimpleExpression():
    Term()
    while lex.kind() in ('+', '-', 'or'):
        lex.next()
        Term()

def Term():
    Factor()
    while lex.kind() in ('*', '/', 'and'):
        lex.next()
        Factor()

def Factor():
    if lex.kind() in ('-', 'not'):
        lex.next()
    if lex.kind() in ('true', 'false', 'NUM'):
        Literal()
    elif lex.kind() == 'ID':
        lex.next()
    elif lex.kind() == '(':
        lex.next()
        Expression()
        match(')')
    else:
        Expected(('true', 'false', 'NUM', 'ID', '('))

def Literal():
    assert( lex.kind() in ('true', 'false', 'NUM'))
    if lex.kind() == 'NUM':
        lex.next()
    else:
        BooleanLiteral()

def BooleanLiteral():
    assert( lex.kind() in ('true', 'false'))
    lex.next()


if __name__ == "__main__":
    main()