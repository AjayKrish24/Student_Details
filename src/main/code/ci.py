import os
import csv
import devconfig


# db = mysql.connector.connect(host="localhost", user="root", passwd="root", db="datamodel")
# db = devconfig.connect_db()
# cursor = db.cursor()


class CreateInsert:

    def __init__(self):
        self.db = devconfig.connect_db()
        self.cursor = self.db.cursor()

    def check_table(self, name):
        self.cursor.execute("use datamodel")
        self.db.commit()
        self.cursor.execute("show tables")
        table = self.cursor.fetchall()
        print(table)
        for tables in table:
            if name in tables:
                # print(tables)
                self.cursor.execute("drop table {}".format(name))
                self.db.commit()
                # self.cursor.execute("select * from {}".format(name))
                # data = self.cursor.fetchone()
                # # print(data)
                # if data:
                #     print(data)
                #     self.cursor.execute("truncate {}".format(name))
                #     self.db.commit()
                #     self.insert_table(name)
                # else:
                #     self.insert_table(name)
        self.create_table(name)

    @staticmethod
    def path_ddl():
        ddl_folder = os.path.dirname(os.path.dirname(__file__))
        # print(ddl_folder)
        ddl_path = os.path.join(ddl_folder, "{}".format("ddl"))
        # print(ddl_path)
        return ddl_path

    def create_table(self, name):
        ddl_path = self.path_ddl()
        file_open = open(os.path.join(ddl_path, "{}.txt".format(name)))
        lines = file_open.read().split(';')
        self.cursor.execute(lines[0])
        self.db.commit()
        print("Table created")
        self.insert_table(name)
        # return True

    def insert_table(self, name):
        ddl_path = self.path_ddl()
        # column_name = "select column_name from information_schema.columns where table_schema='datamodel' and table_name='{}'".format(name)
        self.cursor.execute("select column_name from information_schema.columns where table_schema='datamodel' and "
                            "table_name='{}'".format(name))
        len_ins = self.cursor.fetchall()
        ins_len = len(len_ins)
        file_csv = open(os.path.join(ddl_path, '{}.csv'.format(name)))
        data = csv.reader(file_csv)
        for datas in data:
            # print(datas)
            # sq = "insert into {} values ({})".format(name, ','.join(['%s' for num in range(ins_len)]))
            # print(sq)
            self.cursor.execute("insert into {} values ({})".format(name, ','.join(['%s' for num in range(ins_len)])),
                                datas)
            self.db.commit()
            print("Insert done")


if __name__ == "__main__":
    file_name = input("Enter a file name : ")
    obj = CreateInsert()
    obj.check_table(file_name)
    # check_table(file_name)
    # insert_table(file_name



import os
import mysql.connector
import csv

db = mysql.connector.connect(host="localhost", user="root", passwd="root", db="datamodel")
cursor=db.cursor()

# def check_table(file_name):
#     cursor.execute("use datamodel")
#     db.commit()
#     cursor.execute("show tables")
#     table = cursor.fetchall()
#     # print(table)
#     for tables in table:
#         if file_name in tables:
#             # print(tables)
#             cursor.execute("drop table {}" .format(file_name))
#             db.commit()
#     create_table(file_name)
#
# def path_ddl():
#     ddl_folder = os.path.dirname(os.path.dirname(__file__))
#     # print(ddl_folder)
#     ddl_path = os.path.join(ddl_folder, "{}".format("ddl"))
#     # print(ddl_path)
#     return ddl_path
#
# def create_table(file_name):
#     ddl_path = path_ddl()
#     file_open = open(os.path.join(ddl_path, "{}.txt".format(file_name)))
#     lines = file_open.read().split(';')
#     cursor.execute(lines[0])
#     insert_table(file_name, lines[1])
#     return True

def insert_table(file_name):
    # ddl_path = path_ddl()
    cursor.execute("select column_name from information_schema.columns where table_name='{}'".format(file_name))
    print(cursor.fetchall())



    # file_csv = open(os.path.join(ddl_path, '{}.csv'.format(file_name)))
    # data = csv.reader(file_csv)
    # for datas in data:
    #     # print(datas)
    #     cursor.execute(lines, datas)
    #     db.commit()


if __name__ == "__main__":
    file_name = input("Enter a file name : ")
    # check_table(file_name)
    insert_table(file_name)

# cursor.execute("select column_name from information_schema.columns where table_name='{}'".format(inp))
# print(cursor.fetchall())