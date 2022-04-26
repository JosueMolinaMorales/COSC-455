#! /usr/bin/env python3
from ast import Assert
from LexAnalyzer import Tokenizer
import os

file = ""
lex: Tokenizer

def main():
    global lex, file
    file = input("Enter the file name >>>> ")
    if not os.path.exists(file):
        print(f"ERROR {file} does not exist")
    
    print(f"File being parsed is: {file}")
    lex = Tokenizer(file)
    try:
        lex.next()
        Program({'End-of-text'})
        print(f"Sucessfully parsed {file}\n")
    except Exception as e:
        print(e)
        
def genErr(symbol) -> str:
    errLine = lex.curr_line
    errPos = lex.position()[1]-1 # get the position of the error
    err = f"{file} >>> PARSING ERROR: At Position {lex.position()}. {lex.value()} was seen. Expected {symbol}\n" + \
            f"{errLine}" + \
                " "*errPos+"^"
    return err

def Expected(setSymbols):
    if lex.kind() not in setSymbols:
        raise RuntimeError(genErr(setSymbols))

def match(symbol: str):
    if lex.kind() == symbol:
        lex.next()
    else:
        raise RuntimeError(genErr(symbol))

def Program(follow:set):
    match('program')
    match('ID')
    match(':')
    Body({'end'})
    match('end')
    Expected(follow)

def Body(follow:set):
    if lex.kind() in ('bool', 'int'):
        Declarations({'ID', 'if', 'while', 'print'})
    Statements(follow)
    Expected(follow)

def Declarations(follow:set):
    Declaration(follow.union({'bool', 'int'}))
    while lex.kind() in ('bool', 'int'):
        Declaration(follow.union({'bool', 'int'}))
    Expected(follow)

def Declaration(follow:set):
    Assert(lex.kind() in ('bool', 'int'))
    lex.next()
    match('ID')
    match(';')
    Expected(follow)

def Statements(follow:set):
    Statement(follow.union({';'}))
    while lex.kind() == ';':
        lex.next()
        Statement(follow.union({';'}))
    Expected(follow)

def Statement(follow:set):
    if lex.kind() == 'ID': # the kind of curr_symbol is ID
        AssignmentStatement(follow)
    elif lex.kind() == 'if':
        ConditionalStatement(follow)
    elif lex.kind() == 'while':
        IterativeStatement(follow)
    elif lex.kind() == 'print':
        PrintStatement(follow)
    else:
        Expected({'ID', 'if', 'while', 'print'})

def AssignmentStatement(follow:set):
    match("ID")
    match(':=')
    Expression(follow)
    Expected(follow)

def ConditionalStatement(follow:set):
    match('if')
    Expression({ 'then' })
    match('then')
    Body({ 'fi', 'else' })
    if lex.kind() == "else":
        lex.next()
        Body({ 'fi' })
    match('fi')
    Expected(follow)

def IterativeStatement(follow:set):
    match('while')
    Expression({ 'do' })
    match('do')
    Body({ 'od' })
    match('od')
    Expected(follow)

def PrintStatement(follow:set):
    match('print')
    Expression(follow)
    Expected(follow)

def Expression(follow:set):
    SimpleExpression(follow.union({ '<', '=<', '=', '!=', '>=', '>' }))
    if lex.kind() in ("<", "=<", "=", "!=", ">=", ">"):
        lex.next()
        Expected({ '-', 'not', 'NUM', 'ID', "(", 'true','false' }) # Follow of RelationalOperator
        SimpleExpression(follow)
    Expected(follow)

def SimpleExpression(follow:set):
    Term(follow.union({ '+', '-', 'or' }))
    while lex.kind() in ('+', '-', 'or'):
        lex.next()
        Term(follow.union({ '+', '-', 'or' }))
    Expected(follow)

def Term(follow:set):
    Factor(follow.union({ '*', '/', 'and' }))
    while lex.kind() in ('*', '/', 'and'):
        lex.next()
        Factor(follow.union({ '*', '/', 'and' }))
    Expected(follow)

def Factor(follow:set):
    if lex.kind() in ('-', 'not'):
        lex.next()
    if lex.kind() in ('true', 'false', 'NUM'):
        Literal(follow)
    elif lex.kind() == 'ID':
        lex.next()
    elif lex.kind() == '(':
        lex.next()
        Expression({ ')' })
        match(')')
    else:
        Expected({'true', 'false', 'NUM', 'ID', '('})

def Literal(follow:set):
    assert( lex.kind() in ('true', 'false', 'NUM'))
    if lex.kind() == 'NUM':
        lex.next()
    else:
        BooleanLiteral(follow)
    Expected(follow)

def BooleanLiteral(follow:set):
    assert( lex.kind() in ('true', 'false'))
    lex.next()
    Expected(follow)


if __name__ == "__main__":
    main()