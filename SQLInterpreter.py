######
# file: SQLInterpreter.py
#
# Main program
##

from SQLYacc import parser, operations

if __name__ == "__main__":
    # Build the parser

    info = '''
+-----------------------+
|  Welcome to DashSQL!  |
|         ^_^           |
|  <dashengyeah@github> |
|  @Author: Dash Wong   |
|            2018/06/08 |
+-----------------------+
    '''
    print(info)
    info = '(None)> '
    while True:
        try:
            s = input(info)
        except EOFError:
            break
        if not s:
            continue
        parser.parse(s)
        operations.exec_queue()
        info = "(%s)> " % str(operations.Fun.currentdb)
