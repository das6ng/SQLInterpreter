####
# SQLLexer.py
#
# SQL tokenizer
####

import re
import ply.lex as lex


class SQLLexer(object):
    # reserved words
    reserved = {
        # data types
        'char': 'CHAR',
        'int': 'INT',
        'varchar': 'VARCHAR',

        # values
        'all': 'ALL',
        'any': 'ANY',
        'null': 'NULL',

        # case operators
        'where': 'WHERE',
        'and': 'AND',
        'or': 'OR',
        'not': 'NOT',
        'is': 'IS',
        'in': 'IN',

        # other key words
        'as': 'AS',
        'asc': 'ASC',
        'by': 'BY',
        'check': 'CHECK',
        'constraint': 'CONSTRAINT',
        'create': 'CREATE',
        'database': 'DATABASE',
        'databases': 'DATABASES',
        'delete': 'DELETE',
        'drop': 'DROP',
        'exit': 'EXIT',
        'foreign': 'FOREIGN',
        'from': 'FROM',
        'insert': 'INSERT',
        'into': 'INTO',
        'key': 'KEY',
        'order': 'ORDER',
        'primary': 'PRIMARY',
        'set': 'SET',
        'select': 'SELECT',
        'show': 'SHOW',
        'table': 'TABLE',
        'tables': 'TABLES',
        'union': 'UNION',
        'unique': 'UNIQUE',
        'update': 'UPDATE',
        'use': 'USE',
        'values': 'VALUES',
    }

    # List of token names.   This is always required
    tokens = [
                 'NOTEQUALS',
                 'NUMBER',
                 'BOOLEAN',
                 'ID',
                 'STRING',
             ] + list(reserved.values())

    # Literals.  Should be placed in module given to lex()
    # literals = ['+', '-', '*', '/', '>', '<', '=', '(', ')', ',', ';']
    literals = '+-*/<>()=,;'

    # Regular expression rules for simple tokens
    t_NOTEQUALS = '!='
    t_STRING = r'\'(.*?)\'|"(.*?)"'

    # A regular expression rule with some action code
    # Note addition of self parameter since we're in a class
    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t


    def t_BOOLEAN(self, t):
        r'[tT][rR][uU][eE]|[fF][aA][lL][sS][eE]'
        if 'true' == str.lower(t.value):
            t.value = True
        elif 'false' == str.lower(t.value):
            t.value = False
        return t

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(str.lower(t.value), 'ID')  # Check for reserved words
        return t

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore = ' \t'
    t_ignore_COMMENT = r'//.*'

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self, **kwargs):
        # set lex to be case-insensitive
        self.lexer = lex.lex(module=self, reflags=int(re.IGNORECASE | re.VERBOSE), **kwargs)

    # Test it output
    def test(self, data):
        self.lexer.input(data)
        while True:
             tok = self.lexer.token()
             if not tok:
                 break
             print(tok)

if __name__ == "__main__":
    data = '''
    3 + 4
    selEct e,d fRom hello
    where 1=2 anD 255<3;
    'nihao'
    "jdsa d aow pap hfp"
    //comments
    '''
    data = '''
//测试CREATE DATABASE SHOW DATABASES DROP DATABASE USE DATABASE
CREATE DATABASE XJGL;
CREATE DATABASE JUST_FOR_TEST;
CREATE DATABASE JUST_FOR_TEST;
SHOW DATABASES;
DROP DATABASE JUST_FOR_TEST;
SHOW DATABASES;
USE XJGL;

//测试CREATE TABLE SHOW TABLES DROP TABLE
CREATE TABLE STUDENT(SNAME CHAR(20),SAGE INT,SSEX INT);CREATE TABLE COURSE(CNAME CHAR(20),CID INT);
CREATE TABLE CS(SNAME CHAR(20),CID INT);
CREATE TABLE TEST_TABLE(COL1 CHAR(22),COL2 INT,COL3 CHAR(22);
CREATE TABLE TEST_TABLE(COL1 CHAR(22),COL2 INT,COL3 CHAR(22);
SHOW TABLES;
DROP TABLE TEST_TABLE;
SHOW TABLES;

//测试INSERT INTO VALUES
INSERT INTO STUDENT(SNAME,SAGE,SSEX) VALUES ('ZHANGSAN',22,1);
INSERT INTO STUDENT VALUES ('LISI',23,0);
INSERT INTO STUDENT(SNAME,SAGE) VALUES ('WANGWU',21);
INSERT INTO STUDENT VALUES ('ZHAOLIU',22,1);
INSERT INTO STUDENT VALUES ('XIAOBAI',23,0);
INSERT INTO STUDENT VALUES ('XIAOHEI',19,0);
INSERT INTO COURSE(CNAME,CID) VALUES ('DB',1);
INSERT INTO COURSE (CNAME,CID) VALUES('COMPILER',2);
insert into course (CNAME,CID) VALUES('C',3);

//测试单表查询
SELECT SNAME,SAGE,SSEX FROM STUDENT;
SELECT SNAME,SAGE FROM STUDENT;
SELECT * FROM STUDENT;
SELECT SNAME,SAGE FROM STUDENT WHERE SAGE=21;
SELECT SNAME,SAGE FROM STUDENT WHERE (((SAGE=21)));
SELECT SNAME,SAGE FROM STUDENT WHERE (SAGE>21) AND (SSEX=0);
SELECT SNAME,SAGE FROM STUDENT WHERE (SAGE>21) OR (SSEX=0);
SELECT * FROM STUDENT WHERE SSEX!=1;

// 测试多表查询
SELECT * FROM STUDENT;SELECT * FROM COURSE;
select * from student,course;
SELECT * FROM STUDENT,COURSE WHERE (SSEX=0) AND (CID=1);

//测试DELETE语句
SELECT * FROM STUDENT;
DELETE FROM STUDENT WHERE (SAGE>21) AND (SSEX=0);
SELECT * FROM STUDENT;

//测试UPDATE
SELECT * FROM STUDENT;
UPDATE STUDENT SET SAGE=21 WHERE SSEX=1;
SELECT * FROM STUDENT;
UPDATE STUDENT SET SAGE=27,SSEX=1 WHERE SNAME='ZHANGSAN';
SELECT * FROM STUDENT;
    '''
    data = 'true and false sasas exit Quit'
    #data = '1+2 true'

    # Build the lexer and try it out
    m = SQLLexer()
    m.build()        # Build the lexer
    m.test(data)     # Test it