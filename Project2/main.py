#! /usr/bin/env python3
from ast import Assert
from LexAnalyzer import Tokenizer
from AbstractSyntaxTree import AST, Node
import os

DATA_TYPES = ['bool', 'int']
RELATIONAL_OP = ["<", "=<", "=", "!=", ">=", ">"]
ADDITIVE_OP = ["+", "-", "or"]
MULTIPLATIVE_OP = ['*', '/', 'and']
UNARY_OP = ['-', 'not']
BOOLEAN_LITERALS = ['false', 'true']

FILE = "./examples/ab.txt"
lex = Tokenizer(FILE)

def main():
    global lex
    # try:
    #     lex.next()
    #     Program()
    #     print(f"Sucessfully parsed {FILE}")
    # except Exception as e:
        # print(e)
    for file in os.listdir("./examples"):
        print(f"File being parsed is: {file}")
        lex = Tokenizer("./examples/"+file)
        try:
            lex.next()
            AST = Program()
            print(f"Sucessfully parsed {file}\n")
        except Exception as e:
            print(e)
        

def match(symbol: str):
    if lex.kind() != symbol:
        raise RuntimeError(f"ERROR: At Position {lex.position()}. {lex.kind()} was seen, expected {symbol}")

    value = lex.kind() if lex.kind() != 'ID' else lex.value()
    lex.next()
    return Node(value=value)
    

def Program():
    match('program')
    match('ID')
    match(':')
    Body()
    match('end')

def Body():
    if lex.kind() in DATA_TYPES:
        Declarations()
    Statements()

def Declarations():
    Declaration()
    while lex.kind() in DATA_TYPES:
        Declaration()

def Declaration():
    Assert(lex.kind() in DATA_TYPES)
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
        raise RuntimeError(f"ERROR: At Position {lex.position()}. {lex.value()} was seen. Expected {setSymbols}")

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
    if lex.kind() in RELATIONAL_OP:
        lex.next()
        SimpleExpression()

def SimpleExpression():
    Term()
    while lex.kind() in ADDITIVE_OP:
        lex.next()
        Term()

def Term():
    tree = Factor()
    while lex.kind() in MULTIPLATIVE_OP:
        op = lex.kind()
        lex.next()
        subTree = Factor()
        tree.addChildren()

def Factor() -> Node:
    '''
    
    '''
    if lex.kind() in UNARY_OP:
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
    assert( lex.kind() in BOOLEAN_LITERALS)
    lex.next()


if __name__ == "__main__":
    main()