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

from functions import *
Fun = Functions()

def p_expression(p):
    """expression_sql : expression_create_database
        |               expression_show_database
        |               expression_use_database
        |               expression_exit
        |               expression_create_table
    """
    p[0] = p[1]

def p_show_dbs(p):
    """expression_show_database : SHOW DATABASES ';'"""
    try:
        Fun.show_databases()
    except SQLException as e:
        print(e)


def p_create_db(p):
    """expression_create_database : CREATE DATABASE ID ';'"""
    try:
        Fun.create_database(p[3])
    except SQLException as e:
        print(e)


def p_use_db(p):
    """expression_use_database : USE ID ';'"""
    try:
        Fun.use_database(p[2])
    except SQLException as e:
        print(e)


def p_drop_db(p):
    """expression_create_database : DROP DATABASE ID ';'"""
    try:
        Fun.drop_database(p[3])
    except SQLException as e:
        print(e)


def p_exit_system(p):
    """expression_exit : EXIT
        |                EXIT ';'
    """
    print("Bye.")
    exit(0)


def p_create_table(p):
    """expression_create_table : CREATE TABLE ID '(' table_fields_definition ')' ';'"""
    name = p[3]
    fields = p[5]
    # print("p_create_table: ", end='')
    # print(name, end='  ')
    # print(fields)
    try:
        Fun.create_table(name, fields)
    except SQLException as e:
        print(e)

def p_fields_definition(p):
    """table_fields_definition : table_fields_definition ',' table_field_definition
        |                        table_field_definition
    """
    # print("len(p): %d" % len(p))
    # print("p[1]: %s type(p[1]): %s" % (str(p[1]), str(type(p[1]))))
    if len(p) == 4:
        # print("p[3]: %s type(p[3]): %s" % (str(p[3]), str(type(p[3]))))
        p[0] = []
        for item in p[1]:
            p[0].append(item)
        p[0].append(p[3])
    else:
        p[0] = [p[1]]
    # print("p_fields_definition: " + str(p[0]))

def p_field_definition(p):
    """table_field_definition : ID CHAR '(' NUMBER ')'
        |                       ID INT
        |                       ID VARCHAR '(' NUMBER ')'
    """
    col_type = str.lower(p[2])
    if col_type in ["char", "varchar"]:
        p[0] = [p[1], col_type, p[4]]
    else:
        p[0] = [p[1], col_type]

# logical expression
def p_expression_logic(p):
    """expression_logic : expression_logic AND expression_logic
        |                 expression_logic OR  expression_logic
    """
    # print("Logical expression")
    if str.lower(p[2]) == 'and':
        p[0] = p[1] and p[3]
    else:
        p[0] = p[1] or p[3]


def p_expression_logic_group(p):
    """expression_logic : '(' expression_logic ')' """
    p[0] = p[2]


def p_expression_logic_not(p):
    """expression_logic : NOT expression_logic"""
    p[0] = not p[2]


def p_expression_logic_member(p):
    """expression_logic : BOOLEAN
        |                 expression_comp
    """
    p[0] = p[1]


# Comparision expression
def p_expression_compare(p):
    """expression_comp : expression_comp '>' expression_comp
        |                expression_comp '<' expression_comp
        |                expression_comp '=' expression_comp
        |                expression_comp NOTEQUALS expression_comp
    """
    # print("Comparison expression")
    if p[2] == '>':
        if p[1] > p[3]:
            p[0] = True
        else:
            p[0] = False
    elif p[2] == '<':
        if p[1] < p[3]:
            p[0] = True
        else:
            p[0] = False
    elif p[2] == '=':
        if p[1] == p[3]:
            p[0] = True
        else:
            p[0] = False


def p_expression_compare_group(p):
    """expression_comp : '(' expression_comp ')' """
    p[0] = p[2]


def p_expression_compare_member(p):
    """expression_comp : expression_arith
        |                ID
    """
    p[0] = p[1]


# arithmetic expression
def p_expression_arith(p):
    """expression_arith : expression_arith '+' expression_arith
        |           expression_arith '-' expression_arith
        |           expression_arith '*' expression_arith
        |           expression_arith '/' expression_arith
    """
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
    """expression_arith : '(' expression_arith ')' """
    p[0] = p[2]


def p_expression_arith_member(p):
    """ expression_arith : NUMBER
        |                  ID
    """
    p[0] = p[1]


def p_expression_arith_minus(p):
    """expression_arith : '-' expression_arith"""
    p[0] = -p[2]


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")


if __name__ == "__main__":
    # Build the parser
    parser = yacc.yacc()

    while True:
        try:
            s = input('> ')
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        # print(result)
