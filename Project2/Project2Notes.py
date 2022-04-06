'''
main program:
    next() # start up the L.A. and call the next function
    Program() # program handles the subtree for the non-terminal symbol Program
    Print("Successful parsing")

def Program():
    match('Program') # the first thing expected to see is 'Program'
    match(Identifier)
    match(':')
    Body()
    match('end')

def match(symbol): # Match the curr_symbol to the symbol
    if curr_symbol == symbol: 
        next() # get the next token
    else: # an error occurred
        ERROR # Should tell us the position and the nature of the error
        # At POSITION, curr_symbol seen when expected symbol

def Body():
    if curr_symbol in ('bool', 'int'):
        Declarations()
    Statements()

def Declarations():
    Declaration()
    while curr_symbol in ('bool', 'int'):
        Declaration()

def Declaration()
    Assert(curr_symbol in ('bool', 'int'))
    next()
    match(Identifier)
    match(';')

def Statements():
    Statement()
    while curr_symbol == ';':
        next()
        Statement()

def Statement():
    if curr_symbol is Identifier: # the kind of curr_symbol is ID
        AssignmentStatment()
    elif curr is 'if':
        ConditionalStatement()
    elif curr is 'while':
        IterativeStatement()
    elif curr is 'print':
        PrintStatement()
    else:
        Expected([Id, if, while, print]) # Used when more than one terminal was expected

def Expected(SetSymbols):
    if curr_symbol is not in SetSymbols:
        ERROR -> At POSITION Curr_symbol is seen. Expected SetSymbols

def AssignmentStatement():
    match(Identifier)
    match(':=')
    Expression()

def ConditionalStatement():
    match('if')
    Expression()
    match('then')
    Body()
    if curr_symbol == "else":
        next()
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
    if curr_symbol in ("<", "=<", "=", "!=", ">=", ">"):
        next()
        SimpleExpression()

def SimpleExpression():
    Term()
    while curr_symbol in ('+', '-', 'or'):
        next()
        Term()

def Term():
    Factor()
    while curr_symbol in ('*', '/', 'and'):
        next()
        Factor()

def Factor():
    if curr_symbol in ('-', 'not'):
        next()
    if curr_symbol in ('true', 'false', 'NUM'):
        Literal()
    elif curr_symbol is ID:
        next()
    elif curr_symbol == '(':
        next()
        Expression()
        match(')')
    else:
        Expected(('true', 'false', 'NUM', ID, '('))

def Literal():
    assert( curr_symbol in ('true', 'false', NUM))
    if curr_symbol is NUM:
        next()
    else:
        BooleanLiteral()

def BooleanLiteral():
    assert( curr_symbol in ('true', 'false'))
    next()

EXTRA CREDIT: PRODUCE ABSTRACT SYNTAX TREE (20 points)
def term():
    tree := factor()
    while curr_symbol in ('*', '/', 'and'):
        op := curr_symbol
        next()
        tree2 := factor()
        tree := node(op, tree, tree2)
    return tree;
'''

''' Example program
Program Euclid:
    int a;
    int b;
    int c;
    a := 2;
    print(a)
end
'''