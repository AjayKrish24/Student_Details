import os
import csv
import devconfig



class CreateInsert:

    def __init__(self):
        self.db = devconfig.connect_db()
        self.cursor = self.db.cursor()

    def check_table(self, name):
        self.cursor.execute("show docker")
        self.cursor.execute("show tables")
        table = self.cursor.fetchall()
        for tables in table:
            if name in tables:
                self.cursor.execute("select * from {}".format(name))
                data = self.cursor.fetchall()
                length=len(data)
                if length != 0:
                    self.cursor.execute("truncate table {}".format(name))
                    self.db.commit()
                    self.insert_table(name)
                else:
                    self.insert_table(name)
        self.create_table(name)

    @staticmethod
    def path_ddl():
        ddl_folder = os.path.dirname(os.path.dirname(__file__))
        ddl_path = os.path.join(ddl_folder, "{}".format("ddl"))
        return ddl_path

    def create_table(self, name):
        ddl_path = self.path_ddl()
        file_open = open(os.path.join(ddl_path, "{}.txt".format(name)))
        lines = file_open.read().split(';')
        self.cursor.execute(lines[0])
        self.db.commit()
        self.insert_table(name)

    def insert_table(self, name):
        ddl_path = self.path_ddl()
        self.cursor.execute("select column_name from information_schema.columns where table_name = '{}' and table_schema='docker' order by ordinal_position".format(name))
        col_names = self.cursor.fetchall ()
        nested_list = [list (x) for x in col_names]
        flat_list = [item for sublist in nested_list for item in sublist]
        file = open(os.path.join(ddl_path, '{}.csv'.format(name)))
        value = file.read ().splitlines ()
        for val in value :
            val_list = val.split (",")
            zipped = zip (flat_list, val_list)
            dicted = dict (zipped)
            values = ([x for x in dicted.values ()])
            keys = (",".join ([x for x in dicted.keys ()]))
            joiner = (",".join (["%s" for x in range (len (val_list))]))
            self.cursor.execute ("insert into {} ({}) values({})".format (name, keys, joiner), values)
        self.db.commit()


if __name__ == "__main__":
    file_name = input("Enter a file name : ")
    obj = CreateInsert()
    obj.check_table(file_name)