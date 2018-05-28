####
# LexWords.py
#
# SQL tokenizer
####

import re
import ply.lex as lex

# set le xto be case-insensitive
# lex.lex(reflags=re.IGNORECASE | re.VERBOSE)

class SQLLexer(object):
    # reserved words
    reserved = {
        'all': 'ALL',
        'alter': 'ALTER',
        'and': 'AND',
        'any': 'ANY',
        'as': 'AS',
        'asc': 'ASC',
        'boolean': 'BOOLEAN',
        'by': 'BY',
        'char': 'CHAR',
        'check': 'CHECK',
        'constraint': 'CONSTRAINT',
        'create': 'CREATE',
        'database': 'DATABASE',
        'delete': 'DELETE',
        'drop': 'DROP',
        'except': 'EXCEPT',
        'false': 'FALSE',
        'foreign': 'FOREIGN',
        'from': 'FROM',
        'in': 'IN',
        'insert': 'INSERT',
        'int': 'INT',
        'into': 'INTO',
        'is': 'IS',
        'key': 'KEY',
        'not': 'NOT',
        'null': 'NULL',
        'on': 'ON',
        'or': 'OR',
        'order': 'ORDER',
        'primary': 'PRIMARY',
        'set': 'SET',
        'show': 'SHOW',
        'table': 'TABLE',
        'true': 'TRUE',
        'union': 'UNION',
        'unique': 'UNIQUE',
        'update': 'UPDATE',
        'values': 'VALUES',
        'varchar': 'VARCHAR',
        'where': 'WHERE',
    }

    # List of token names.   This is always required
    tokens = [
                 'NUMBER',
                 'PLUS',
                 'MINUS',
                 'TIMES',
                 'DIVIDE',
                 'LPAREN',
                 'RPAREN',
                 'ID'
             ] + list(reserved.values())

    # Regular expression rules for simple tokens
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'

    #t_ID = r'[a-zA-Z_][a-zA-Z_0-9]*'

    # A regular expression rule with some action code
    # Note addition of self parameter since we're in a class
    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'ID')  # Check for reserved words
        return t

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Test it output
    def test(self,data):
        self.lexer.input(data)
        while True:
             tok = self.lexer.token()
             if not tok:
                 break
             print(tok)

# Build the lexer and try it out
m = SQLLexer()
m.build()           # Build the lexer
m.test("3 + 4 selecT * from")     # Test it