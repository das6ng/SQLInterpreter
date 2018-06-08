####
# functions.py
#
# functions
###

import os
from prettytable import PrettyTable


class Functions(object):
    def __init__(self):
        os.chdir("./DBMS")
        #print("$ cwd "+os.getcwd())
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
    def del_line(name, del_line):
        del_line += '\n'
        with open(name, mode='r', encoding="UTF-8") as old_file:
            with open(name+".tmp", mode='w', encoding="UTF-8") as new_file:
                line = old_file.readline()
                while len(line) > 0:
                    if line == del_line:
                        #print("@del: %s" % line)
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
            raise SQLException("database '%s' doesn't exist!" % name)

    def create_database(self, name):
        if not self.db_exists(name):
            os.mkdir(name)
            open(name+"/table.info", mode="w", encoding="UTF-8").close()
            self.dbinfo.write(name+"\n")
            self.dbinfo.flush()
            print("Successfully created database '%s'!" % name)
        else:
            raise SQLException("database '%s' already exists!" % name)

    def drop_database(self, name):
        if self.db_exists(name):
            self.rm_dir(name)
            self.dbinfo.close()
            self.del_line(self.dbms_file, name)
            self.dbinfo = open(self.dbms_file, mode='r+', encoding='UTF-8')
            print("Successfully dropped database '%s'!" % name)
        else:
            raise SQLException("database '%s' doesn't exist!" % name)

    def show_databases(self):
        self.dbinfo.seek(0, 0)
        dbs = self.dbinfo.readlines()
        x = PrettyTable(["database"])
        for i in range(len(dbs)):
            x.add_row([dbs[i][:-1]])
        print(x)
        print("Query OK! %d row(s) matched." % len(dbs))

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

    def create_table(self, name, fields):
        if self.currentdb is None:
            raise SQLException("No database selected!")
        if not self.table_exists(name):
            info = "%s" % name
            for item in fields:
                info += "|"+item[0]+' '+item[1]
                if len(item) == 3:
                    info += ' '+str(item[2])
            print("info: "+info)
            info += '\n'
            with open(self.currentdb+"/"+self.table_file, 'r+', encoding="UTF-8") as table_info:
                table_info.seek(0, 2)
                table_info.write(info)
            path = self.currentdb+"/"+name+".txt"
            open(path, mode="w", encoding="UTF-8").close()
        else:
            raise SQLException("table '%s' already exists!" % name)


class SQLException(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


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