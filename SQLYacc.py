####
# SQLLexer.py
#
# SQL yacc file
####

import ply.yacc as yacc

from SQLLexer import SQLLexer
lexer = SQLLexer()
lexer.build()
tokens = lexer.tokens

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('left', '=', 'NOTEQUALS'),
    ('left', '>', '<'),
    ('left', '+', '-'),
    ('left', '*', '/'),
    ('right', '-'),
)

# logical expression
def p_expression_logic(p):
    '''expression_logic : expression_logic AND expression_logic
        |                 expression_logic OR  expression_logic
    '''
    # print("Logical expression")
    if str.lower(p[2]) == 'and':
        if str.lower(p[1]) == 'true' and str.lower(p[3]) == 'true':
            p[0] = 'true'
        else:
            p[0] = 'false'
    else:
        if str.lower(p[1]) == 'true' or str.lower(p[3]) == 'true':
            p[0] = 'true'
        else:
            p[0] = 'false'

def p_expression_logic_group(p):
    '''expression_logic : '(' expression_logic ')' '''
    p[0] = p[2]

def p_expression_logic_not(p):
    'expression_logic : NOT expression_logic'
    if str.lower(p[2]) == 'true':
        p[0] = 'false'
    else:
        p[0] = 'false'

def p_expression_logic_member(p):
    '''expression_logic : TRUE
        |                 FALSE
        |                 expression_comp
    '''
    p[0] = p[1]


# Comparision expression
def p_expression_compare(p):
    '''expression_comp : expression_comp '>' expression_comp
        |                expression_comp '<' expression_comp
        |                expression_comp '=' expression_comp
        |                expression_comp NOTEQUALS expression_comp
    '''
    # print("Comparison expression")
    if p[2] == '>':
        if p[1] > p[3]:
            p[0] = 'true'
        else:
            p[0] = 'false'
    elif p[2] == '<':
        if p[1] < p[3]:
            p[0] = 'true'
        else:
            p[0] = 'false'
    elif p[2] == '=':
        if p[1] == p[3]:
            p[0] = 'true'
        else:
            p[0] = 'false'

def p_expression_compare_group(p):
    '''expression_comp : '(' expression_comp ')' '''
    p[0] = p[2]

def p_expression_compare_member(p):
    '''expression_comp : expression_arith
        |                ID
    '''
    p[0] = p[1]


# arithmetic expression
def p_expression_arith(p):
    '''expression_arith : expression_arith '+' expression_arith
        |           expression_arith '-' expression_arith
        |           expression_arith '*' expression_arith
        |           expression_arith '/' expression_arith
    '''
    # print("Arithmetic expression")
    op = p[2]
    if op == '+':
        p[0] = p[1] + p[3]
    elif op == '-':
        p[0] = p[1] - p[3]
    elif op == '*':
        p[0] = p[1] * p[3]
    elif op == '/':
        p[0] = p[1] / p[3]

def p_expression_arith_group(p):
    '''expression_arith : '(' expression_arith ')' '''
    p[0] = p[2]

def p_expression_arith_member(p):
    ''' expression_arith : NUMBER
        |                  ID
    '''
    p[0] = p[1]

def p_expression_arith_minus(p):
    '''expression_arith : '-' expression_arith'''
    p[0] = -p[2]

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = input('> ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)