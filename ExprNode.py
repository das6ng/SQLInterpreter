###
# ExprNode.py
#
# Grammar tree node types
###


class ExprNode(object):
    op_type = None

    def __init__(self, op_type):
        self.op_type = op_type

class BinaryOp(ExprNode):
    types = [
        "arith_+",
        "arith_-",
        "arith_*",
        "arith_/",
        "logic_and",
        "logic_or",
        "compare_>",
        "compare_<",
        "compare_=",
        "compare_!=",

        "sql_create_table",
        "sql_insert_table",
        "sql_select_table",
        "sql_update_table",
        "sql_delete_from_table",
    ]

    def __init__(self, op_type, op1, op2):
        if op_type not in self.types:
            raise Exception("<BinaryOperation>wrong operation type '%s'!" % op_type)
        super().__init__(op_type)
        self.op1 = op1
        self.op2 = op2

    def __str__(self):
        return "(%s,%s,%s)" % (self.op_type, str(self.op1), str(self.op2))

class SingleOp(ExprNode):
    types = [
        "variable",
        "arith_minus",
        "logic_not",

        "sql_show_databases",
        "sql_create_database",
        "sql_use_database",
        "sql_drop_database",

        "sql_show_tables",
        "sql_drop_table",
             ]

    def __init__(self, op_type, op):
        if op_type not in self.types:
            raise Exception("<SingleOperation>wrong operation type '%s'!" % op_type)
        super().__init__(op_type)
        self.op = op

    def __str__(self):
        return "(%s,%s)" % (self.op_type, str(self.op))