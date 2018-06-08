###
# ExprNode.py
#
# Grammar tree node types
###


class ExprNode(object):
    pass


class BinOp(ExprNode):
    def __init__(self, type, op1, op2):
        self.type = type
        self.op1 = op1
        self.op2 = op2
