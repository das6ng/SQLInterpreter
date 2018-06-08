####
# Functions.py
#
# functions
###

import os
from prettytable import PrettyTable
from queue import Queue
from ExprNode import *


class Functions(object):
    """
    using_tables:   ["table name", ...]
    table_cache:    [[["column name", ...], [column], ...], ...]
    current_column: [[["column name", ...], [column]], ...]
    """
    using_tables = []
    table_cache = []
    current_column = [[], []]

    def __init__(self):
        os.chdir("./DBMS")
        # print("$ cwd "+os.getcwd())
        self.dbms_file = "db.info"
        self.table_file = "table.info"
        self.dbinfo = open(self.dbms_file, mode='r+', encoding='UTF-8')
        self.currentdb = None

    def __del__(self):
        self.dbinfo.close()

    def db_exists(self, name):
        self.dbinfo.seek(0, 0)
        for line in self.dbinfo.readlines():
            if line == name+'\n':
                return True
        return False

    @staticmethod
    def del_database(name, del_line):
        del_line += '\n'
        with open(name, mode='r', encoding="UTF-8") as old_file:
            with open(name+".tmp", mode='w', encoding="UTF-8") as new_file:
                line = old_file.readline()
                while len(line) > 0:
                    if line == del_line:
                        # print("@del: %s" % line)
                        pass
                    else:
                        new_file.write(line)
                    line = old_file.readline()
        os.remove(name)
        os.rename(name+'.tmp', name)

    @staticmethod
    def del_table(name, del_line):
        with open(name, mode='r', encoding="UTF-8") as old_file:
            with open(name+".tmp", mode='w', encoding="UTF-8") as new_file:
                line = old_file.readline()
                while len(line) > 0:
                    if line.split('|')[0] == del_line:
                        # print("@del: %s" % line)
                        pass
                    else:
                        new_file.write(line)
                    line = old_file.readline()
        os.remove(name)
        os.rename(name+'.tmp', name)

    @staticmethod
    def rm_dir(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.removedirs(path)

    def use_database(self, name):
        if self.db_exists(name):
            self.currentdb = name
            print("Database changed to '%s'." % name)
        else:
            raise SQLException("SQLError: database '%s' doesn't exist!" % name)

    def create_database(self, name):
        if not self.db_exists(name):
            os.mkdir(name)
            open(name+"/table.info", mode="w", encoding="UTF-8").close()
            self.dbinfo.write(name+"\n")
            self.dbinfo.flush()
            print("Successfully created database '%s'!" % name)
        else:
            raise SQLException("SQLError: database '%s' already exists!" % name)

    def drop_database(self, name):
        if self.db_exists(name):
            self.rm_dir(name)
            self.dbinfo.close()
            self.del_database(self.dbms_file, name)
            self.dbinfo = open(self.dbms_file, mode='r+', encoding='UTF-8')
            print("Successfully dropped database '%s'!" % name)
        else:
            raise SQLException("SQLError: database '%s' doesn't exist!" % name)

    def show_databases(self):
        self.dbinfo.seek(0, 0)
        databases = self.dbinfo.readlines()
        x = PrettyTable(["database"])
        for i in range(len(databases)):
            x.add_row([databases[i][:-1]])
        print(x)
        print("Query OK! %d row(s) matched." % len(databases))

    def table_exists(self, name):
        if self.currentdb is not None:
            with open(self.currentdb+"/"+self.table_file, encoding="UTF-8") as table_info:
                line = table_info.readline()
                while len(line) > 0:
                    slices = line.split('|')
                    # print(slices)
                    if name == slices[0]:
                        return True
                    line = table_info.readline()
                return False

    def show_tables(self):
        if self.currentdb is None:
            raise SQLException("SQLError: No database selected!")
        with open(self.currentdb+"/"+self.table_file, 'r', encoding="UTF-8") as table_info:
            tables = table_info.readlines()
            x = PrettyTable(["table"])
            for i in range(len(tables)):
                x.add_row([tables[i].split('|')[0]])
            print(x)
            print("Query OK! %d row(s) matched." % len(tables))

    def del_table_cache(self):
        self.using_tables = []
        self.table_cache = []
        self.current_column = [[], []]

    def create_table(self, name, fields):
        if self.currentdb is None:
            raise SQLException("SQLError: No database selected!")
        if not self.table_exists(name):
            info = "%s" % name
            for item in fields:
                info += "|"+item[0]+' '+item[1]
                if len(item) == 3:
                    info += ' '+str(item[2])
            # print("info: "+info)
            info += '\n'
            with open(self.currentdb+"/"+self.table_file, 'r+', encoding="UTF-8") as table_info:
                table_info.seek(0, 2)
                table_info.write(info)
            path = self.currentdb+"/"+name+".txt"
            open(path, mode="w", encoding="UTF-8").close()
        else:
            raise SQLException("SQLError: table '%s' already exists!" % name)

    def get_column_info(self, table_name):
        if self.currentdb is None:
            raise SQLException("SQLError: No database selected!")
        column_names = []
        column_types = []
        with open(self.currentdb + "/" + self.table_file, 'r', encoding="UTF-8") as table_info:
            for line in table_info.readlines():
                line = line[:-1]
                if line.split('|')[0] == table_name:
                    column_types = line.split('|')[1:]
        for c in column_types:
            column_names.append(c.split()[0])
        return column_names, column_types

    def insert_table(self, table_name, param):
        """
        :param table_name: table name
        :param param: [["column names"], ["values"]]
        :return:
        """
        if self.currentdb is None:
            raise SQLException("SQLError: No database selected!")
        if not self.table_exists(table_name):
            raise SQLException("SQLError: table '%s' doesn't exist!" % table_name)
        column_names = param[0]
        column_values = param[1]
        all_columns = []
        with open(self.currentdb + "/" + self.table_file, 'r+', encoding="UTF-8") as table_info:
            lines = table_info.readlines()
            for line in lines:
                line = line[:-1]
                if line.split('|')[0] == table_name:
                    all_columns = line.split('|')[1:]
        all_column_names = []
        for i in all_columns:
            all_column_names.append(i.split()[0])
        if column_names is None:
            if len(all_columns) != len(column_values):
                raise SQLException("SQLError: wrong count of values!")
            info = column_values
        else:
            for i in column_names:
                if i not in all_column_names:
                    raise SQLException("SQLError: no column named '%s'!" % i)
            info = []
            for i in range(len(all_column_names)):
                if all_column_names[i] in column_names:
                    info.insert(i, column_values[column_names.index(all_column_names[i])])
                else:
                    info.append('')
        # print("info: %s" % str(info))
        with open(self.currentdb + "/" + table_name + '.txt', 'r+', encoding="UTF-8") as table_file:
            table_file.seek(0, 2)
            info_str = ''
            for i in info:
                info_str += str(i)+'|'
            table_file.write(info_str + '\n')
            print("Query OK! 1 row affected.")

    def drop_table(self, name):
        if self.currentdb is None:
            raise SQLException("SQLError: No database selected!")
        if self.table_exists(name):
            os.remove(self.currentdb+"/"+name+'.txt')
            self.del_table(self.currentdb+"/"+self.table_file, name)
            print("Successfully dropped table '%s'!" % name)
        else:
            raise SQLException("SQLError: table '%s' doesn't exist!" % name)

    def cache_tables(self):
        if self.using_tables is None or self.currentdb is None:
            return
        for table in self.using_tables:
            column_names, column_types = self.get_column_info(table)
            table_content = []
            with open(self.currentdb + "/" + table + '.txt', 'r', encoding="UTF-8") as table_file:
                for line in table_file.readlines():
                    table_content.append(line.split('|')[:-1])
            self.table_cache.append([column_names, table_content])

    @staticmethod
    def product(a, b):
        res = []
        for i in a:
            for j in b:
                res.append(i+j)
        return res

    def select_table(self, table, condition):
        """
        :param table: [["table names"], ["column names"]]
        :param condition: Expression tree
        :return:
        """
        if self.currentdb is None:
            raise SQLException("SQLError: No database selected!")
        for t in table[0]:
            if not self.table_exists(t):
                raise SQLException("SQLError: table '%s' doesn't exist!" % t)
        self.using_tables = table[0]
        self.cache_tables()
        select_columns = table[1]
        # print("tables: %s columns: %s" % (str(self.using_tables), str(select_columns)))
        # print("condition expression: %s" % str(condition))
        pxx = self.table_cache[0][1]
        all_column_names = self.table_cache[0][0]
        result_set = []
        for each_table_cache in self.table_cache[1:]:
            if len(each_table_cache[1]) > 0:
                pxx = self.product(pxx, each_table_cache[1])
                # print(" pxx: %s" % str(pxx))
                all_column_names.extend(each_table_cache[0])
        self.current_column[0] = all_column_names
        for each in pxx:
            self.current_column[1] = each
            # print("  current_column: %s" % str(self.current_column), end=' ')
            flag = self.compute(condition)
            # print("   condition:%s=%s" % (str(condition), str(flag)))
            if flag:
                result_set.append(self.current_column[1])
        self.del_table_cache()
        # print("all_column_names: %s, result_set: %s" % (str(all_column_names), str(result_set)))
        if select_columns != '*':
            for column in all_column_names:
                if column not in select_columns:
                    index = all_column_names.index(column)
                    for i in range(len(result_set)):
                        result_set[i].pop(index)
                    all_column_names.pop(index)
        x = PrettyTable(all_column_names)
        for i in result_set:
            x.add_row(i)
        print(x)
        print("Query OK! %d row(s) matched." % len(result_set))

    def update_table(self, table, condition):
        """
        :param table: ["table name", [[column, value], ...]]
        :param condition: Expression tree
        :return:
        """
        table_name = table[0]
        column_values = table[1]
        if self.currentdb is None:
            raise SQLException("SQLError: No database selected!")
        if not self.table_exists(table_name):
            raise SQLException("SQLError: table '%s' doesn't exist!" % table_name)
        # print("table_name: %s  column_values: %s" % (str(table_name), str(column_values)))
        # print("condition expression: %s" % str(condition))
        file_path = self.currentdb + '/' + table_name + '.txt'
        column_names, column_types = self.get_column_info(table_name)
        self.current_column[0] = column_names
        count = 0
        with open(file_path, mode='r', encoding='UTF-8') as old_file:
            with open(file_path + '.tmp', mode='w', encoding='UTF-8') as new_file:
                line = old_file.readline()
                while len(line) > 0:
                    self.current_column[1] = line.split('|')[:-1]
                    if not self.compute(condition):
                        new_file.write(line)
                    else:
                        for column_value in column_values:
                            index = self.current_column[0].index(column_value[0])
                            self.current_column[1][index] = column_value[1]
                        new_line = ''
                        for i in self.current_column[1]:
                            new_line += str(i)+'|'
                        new_file.write(new_line+'\n')
                        count += 1
                    line = old_file.readline()
        os.remove(file_path)
        os.rename(file_path + '.tmp', file_path)
        print("Query OK! %d row(s) affected." % count)

    def delete_from_table(self, table, condition):
        if self.currentdb is None:
            raise SQLException("SQLError: No database selected!")
        if not self.table_exists(table):
            raise SQLException("SQLError: table '%s' doesn't exist!" % table)
        # print("table_name: %s" % (str(table)))
        # print("condition expression: %s" % str(condition))
        file_path = self.currentdb+'/'+table+'.txt'
        column_names, column_types = self.get_column_info(table)
        self.current_column[0] = column_names
        count = 0
        with open(file_path, mode='r', encoding='UTF-8') as old_file:
            with open(file_path+'.tmp', mode='w', encoding='UTF-8') as new_file:
                line = old_file.readline()
                while len(line) > 0:
                    self.current_column[1] = line.split('|')[:-1]
                    if not self.compute(condition):
                        new_file.write(line)
                    else:
                        count += 1
                    line = old_file.readline()
        os.remove(file_path)
        os.rename(file_path+'.tmp', file_path)
        print("Query OK! %d row(s) affected." % count)

    def get_column_value(self, column_name):
        column_names = self.current_column[0]
        pos = column_names.index(column_name)
        res = self.current_column[1][pos]
        # print("  value of '%s' is %s." % (str(column_name), str(res)))
        return res

    def compute(self, tree):
        res = None
        if isinstance(tree, SingleOp):
            if not isinstance(tree.op, ExprNode):
                op = tree.op
            else:
                op = self.compute(tree.op)

            if tree.op_type == "arith_minus":
                res = - int(op)
            elif tree.op_type == "logic_not":
                res = not bool(op)
            elif tree.op_type == "variable":
                res = self.get_column_value(tree.op)
        elif isinstance(tree, BinaryOp):
            if not isinstance(tree.op1, ExprNode):
                op1 = tree.op1
            else:
                op1 = self.compute(tree.op1)
            if not isinstance(tree.op2, ExprNode):
                op2 = tree.op2
            else:
                op2 = self.compute(tree.op2)
            try:
                if tree.op_type == "arith_+":
                    res = int(op1) + int(op2)
                elif tree.op_type == "arith_-":
                    res = int(op1) - int(op2)
                elif tree.op_type == "arith_*":
                    res = int(op1) * int(op2)
                elif tree.op_type == "arith_/":
                    res = int(op1) / int(op2)
                elif tree.op_type == "logic_and":
                    res = bool(op1) and bool(op2)
                elif tree.op_type == "logic_or":
                    res = bool(op1) or bool(op2)
                elif tree.op_type == "compare_>":
                    res = (int(op1) > int(op2))
                elif tree.op_type == "compare_<":
                    res = (int(op1) < int(op2))
                elif tree.op_type == "compare_=":
                    res = (str(op1) == str(op2))
                elif tree.op_type == "compare_!=":
                    res = (str(op1) != str(op2))
            except Exception as e:
                print(e)
                res = False
        else:
            res = tree
        return res

class SQLException(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class OperationQueue(Queue):
    Fun = Functions()

    def __init__(self):
        super().__init__()

    def exec_queue(self):
        while not self.empty():
            item = self.get()
            try:
                if item.op_type == "sql_use_database":
                    self.Fun.use_database(item.op)
                elif item.op_type == "sql_show_databases":
                    self.Fun.show_databases()
                elif item.op_type == "sql_create_database":
                    self.Fun.create_database(item.op)
                elif item.op_type == "sql_drop_database":
                    self.Fun.drop_database(item.op)
                elif item.op_type == "sql_show_tables":
                    self.Fun.show_tables()
                elif item.op_type == "sql_create_table":
                    self.Fun.create_table(item.op1, item.op2)
                elif item.op_type == "sql_insert_table":
                    self.Fun.insert_table(item.op1, item.op2)
                elif item.op_type == "sql_select_table":
                    self.Fun.select_table(item.op1, item.op2)
                elif item.op_type == "sql_update_table":
                    self.Fun.update_table(item.op1, item.op2)
                elif item.op_type == "sql_delete_from_table":
                    self.Fun.delete_from_table(item.op1, item.op2)
                elif item.op_type == "sql_drop_table":
                    self.Fun.drop_table(item.op)
            except Exception as e:
                print(e)


if __name__ == "__main__":
    Fun = Functions()
    Fun.use_database("test")

    dbs = ["aa", "bb", "cc", "dd", "ee"]
    for db in dbs:
        if not Fun.db_exists(db):
            Fun.create_database(db)
    Fun.show_databases()
    for db in dbs:
        if Fun.db_exists(db):
            Fun.drop_database(db)
            pass