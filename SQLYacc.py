####
# SQLLexer.py
#
# SQL yacc file
####

import ply.yacc as yacc
from SQLLexer import SQLLexer
from ExprNode import *
from Functions import OperationQueue

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

operations = OperationQueue()

def p_expression_set(p):
    """expression_set : expression_set expression_sql
        |               expression_sql
    """
    p[0] = p[1]

def p_expression(p):
    """expression_sql : expression_create_database
        |               expression_show_database
        |               expression_use_database
        |               expression_exit
        |               expression_comments
        |               expression_show_tables
        |               expression_create_table
        |               expression_drop_table
        |               expression_insert_table
        |               expression_select_table
        |               expression_update_table
        |               expression_delete_from_table
    """
    p[0] = p[1]

def p_show_dbs(p):
    """expression_show_database : SHOW DATABASES ';'"""
    operation = SingleOp("sql_show_databases", None)
    operations.put(operation)
    p[0] = p[1]

def p_create_db(p):
    """expression_create_database : CREATE DATABASE ID ';'"""
    operation = SingleOp("sql_create_database", p[3])
    operations.put(operation)

def p_use_db(p):
    """expression_use_database : USE ID ';'"""
    operation = SingleOp("sql_use_database", p[2])
    operations.put(operation)

def p_drop_db(p):
    """expression_create_database : DROP DATABASE ID ';'"""
    operation = SingleOp("sql_drop_database", p[3])
    operations.put(operation)

def p_exit_system(p):
    """expression_exit : EXIT
        |                EXIT ';'
    """
    p[0] = p[1]
    print("Bye.")
    exit(0)

def p_show_tables(p):
    """expression_show_tables : SHOW TABLES ';' """
    operation = SingleOp("sql_show_tables", None)
    operations.put(operation)
    p[0] = p[1]

def p_create_table(p):
    """expression_create_table : CREATE TABLE ID '(' table_fields_definition ')' ';'"""
    name = p[3]
    fields = p[5]
    operation = BinaryOp("sql_create_table", name, fields)
    operations.put(operation)

def p_insert_table(p):
    """expression_insert_table : INSERT INTO ID '(' names ')' VALUES '(' given_values ')' ';'
        |                        INSERT INTO ID VALUES '(' given_values ')' ';'
    """
    table_name = p[3]
    if p[4] == '(':
        column_names = p[5]
        given_values = p[9]
    else:
        column_names = None
        given_values = p[6]
    operation = BinaryOp("sql_insert_table", table_name, [column_names, given_values])
    operations.put(operation)

def p_select_table(p):
    """expression_select_table : SELECT '*' FROM names ';'
        |                        SELECT names FROM names ';'
        |                        SELECT '*' FROM names WHERE expression_logic ';'
        |                        SELECT names FROM names WHERE expression_logic ';'
    """
    l = len(p)
    table = None
    condition = None
    if l == 6:
        table = [p[4], p[2]]
        condition = True
    elif l == 8:
        table = [p[4], p[2]]
        condition = p[6]
    operation = BinaryOp("sql_select_table", table, condition)
    operations.put(operation)

def p_update_table(p):
    """expression_update_table : UPDATE ID SET column_values ';'
        |                        UPDATE ID SET column_values WHERE expression_logic ';'
    """
    l = len(p)
    column_values = p[4]
    table = p[2]
    condition = None
    if l == 6:
        condition = True
    elif l == 8:
        condition = p[6]
    operation = BinaryOp("sql_update_table", [table, column_values], condition)
    operations.put(operation)

def p_column_values(p):
    """column_values : column_values ',' column_value
        |              column_value
    """
    res = []
    if len(p) == 2:
        res.append(p[1])
    elif len(p) == 4:
        for i in p[1]:
            res.append(i)
        res.append(p[3])
    p[0] = res

def p_column_value(p):
    """column_value : ID '=' NUMBER
        |             ID '=' STRING
    """
    p[0] = [p[1], p[3]]

def p_delete_from_table(p):
    """expression_delete_from_table : DELETE FROM ID ';'
        |                             DELETE FROM ID WHERE expression_logic ';'
    """
    l = len(p)
    table = p[3]
    condition = None
    if l == 5:
        condition = True
    elif l == 7:
        condition = p[5]
    operation = BinaryOp("sql_delete_from_table", table, condition)
    operations.put(operation)

def p_names_table(p):
    """names : names ',' ID
        |      ID
    """
    res = []
    if len(p) == 2:
        res.append(p[1])
    elif len(p) == 4:
        for i in p[1]:
            res.append(i)
        res.append(p[3])
    p[0] = res

def p_given_values_table(p):
    """given_values : given_values ',' given_value
        |             given_value
    """
    res = []
    if len(p) == 2:
        res.append(p[1])
    elif len(p) == 4:
        for i in p[1]:
            res.append(i)
        res.append(p[3])
    p[0] = res

def p_given_value_table(p):
    """given_value : NUMBER
        |            STRING
    """
    p[0] = p[1]

def p_drop_table(p):
    """expression_drop_table : DROP TABLE ID ';'"""
    operation = SingleOp("sql_drop_table", p[3])
    operations.put(operation)

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

def p_comments(p):
    """expression_comments : COMMENT"""

# logical expression
def p_expression_logic(p):
    """expression_logic : expression_logic AND expression_logic
        |                 expression_logic OR  expression_logic
    """
    # print("Logical expression")
    if str.lower(p[2]) == 'and':
        p[0] = BinaryOp("logic_and", p[1], p[3])
    else:
        p[0] = BinaryOp("logic_or", p[1], p[3])

def p_expression_logic_group(p):
    """expression_logic : '(' expression_logic ')' """
    p[0] = p[2]

def p_expression_logic_not(p):
    """expression_logic : NOT expression_logic"""
    p[0] = SingleOp("logic_not", p[2])

def p_expression_logic_member(p):
    """expression_logic : BOOLEAN
        |                 expression_comp
    """
    p[0] = p[1]

# Comparision expression
def p_expression_compare(p):
    """expression_comp : expression_comp_member '>' expression_comp_member
        |                expression_comp_member '<' expression_comp_member
        |                expression_comp_member '=' expression_comp_member
        |                expression_comp_member NOTEQUALS expression_comp_member
    """
    # print("Comparison expression")
    if p[2] == '>':
        p[0] = BinaryOp("compare_>", p[1], p[3])
    elif p[2] == '<':
        p[0] = BinaryOp("compare_<", p[1], p[3])
    elif p[2] == '=':
        p[0] = BinaryOp("compare_=", p[1], p[3])
    else:
        p[0] = BinaryOp("compare_!=", p[1], p[3])

def p_expression_compare_member(p):
    """expression_comp_member : expression_arith
        |                       variable
        |                       STRING
    """
    p[0] = p[1]

# arithmetic expression
def p_expression_arith(p):
    """expression_arith : expression_arith '+' expression_arith
        |                 expression_arith '-' expression_arith
        |                 expression_arith '*' expression_arith
        |                 expression_arith '/' expression_arith
    """
    # print("Arithmetic expression")
    op = p[2]
    if op == '+':
        p[0] = BinaryOp("arith_+", p[1], p[3])
    elif op == '-':
        p[0] = BinaryOp("arith_-", p[1], p[3])
    elif op == '*':
        p[0] = BinaryOp("arith_*", p[1], p[3])
    elif op == '/':
        p[0] = BinaryOp("arith_/", p[1], p[3])

def p_expression_arith_group(p):
    """expression_arith : '(' expression_arith ')' """
    p[0] = p[2]

def p_expression_arith_member(p):
    """ expression_arith : NUMBER
        |                  variable
    """
    p[0] = p[1]

def p_expression_arith_minus(p):
    """expression_arith : '-' expression_arith"""
    p[0] = SingleOp("arith_minus", p[2])

def p_variable(p):
    """variable : ID"""
    p[0] = SingleOp("variable", p[1])

# Error rule for syntax errors
def p_error(p):
    print("SQLError: Syntax error!")


parser = yacc.yacc()
