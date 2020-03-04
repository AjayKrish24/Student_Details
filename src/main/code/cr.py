import os
import csv
import devconfig
import logging

logging.basicConfig(filename="student.log",
                    filemode='a',
                    format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s",
                    level=logging.INFO)

class CreateInsert:

    def __init__(self):
        self.db = devconfig.connect_db()
        logging.info("Database Connection Established")
        self.cursor = self.db.cursor()

    # method to check the tables is present or not and empty or not
    def check_table(self, name):
        """
                Parameter : name of file
                Return : True
        """
        self.cursor.execute("use datamodel")
        self.db.commit()
        self.cursor.execute("show tables")
        logging.info("Tables are fetched from database")
        table = self.cursor.fetchall()
        flag = 0
        try:
            for tables in table:
                if name in tables:
                    flag = 1
                    self.cursor.execute("select * from {}".format(name))
                    data = self.cursor.fetchall()
                    length = len(data)
                    if length != 0:
                        self.cursor.execute("truncate table {}".format(name))
                        self.db.commit()
                        self.insert_table(name)
                    else:
                        self.insert_table(name)
            if flag == 0:
                self.create_table(name)
        except Exception as e:
            print(e)
            logging.exception("Exception occured!!!!!")

    # static method to fetch the ddl path
    @staticmethod
    def path_ddl():
        try:
            ddl_folder = os.path.dirname(os.path.dirname(__file__))
            ddl_path = os.path.join(ddl_folder, "{}".format("ddl"))
            logging.info("Path of the ddl folder is fetched")
            return ddl_path
        except Exception as e:
            print(e)
            logging.exception("Exception occured!!!!!")

    # function to create table
    def create_table(self, name):
        """
                Parameter : name of file
                Return : True
        """
        try:
            ddl_path = self.path_ddl()
            file_open = open(os.path.join(ddl_path, "{}.txt".format(name)))
            lines = file_open.read().split(';')
            self.cursor.execute(lines[0])
            self.db.commit()
            logging.info("Table {} is created ".format(name))
            print("Table created")
            self.insert_table(name)
        except FileNotFoundError as e:
            print('File Not Found', e)

    # function to insert values into table
    def insert_table(self, name):
        """
                Parameter : name of file
                Return : True if inserted successfully
        """
        ddl_path = self.path_ddl()                             # function call to fetch ddl dir path
        self.cursor.execute("select column_name from information_schema.columns where table_schema='datamodel' and "
                            "table_name='{}'".format(name))
        col_names = self.cursor.fetchall()
        nested_list = [list(x) for x in col_names]
        flat_list = [item for sublist in nested_list for item in sublist]
        try:
            file = open(os.path.join(ddl_path, '{}.csv'.format(name)))
            value = file.read().splitlines()
            for val in value:
                val_list = val.split(",")
                zipped = zip(flat_list, val_list)
                dicted = dict(zipped)
                values = ([x for x in dicted.values()])
                keys = (",".join([x for x in dicted.keys()]))
                joiner = (",".join(["%s" for x in range(len(val_list))]))
                self.cursor.execute("insert into {} ({}) values({})".format(name, keys, joiner), values)
            self.db.commit()
            logging.info("Datas are inserted into table {}".format(name))
            print("Insert done")
            self.cursor.execute('select * from {}'.format(name))
            resultset = self.cursor.fetchall()
            return resultset
        except FileNotFoundError as e:
            print(e)
            logging.exception("File not found")

        except Exception as e:
            print(e)
            logging.exception("Exception occured!!!!!")

    def connection_close(self):
        try:
            self.db.close()
            logging.info("Database connection closed" )
        except Exception as e:
            print(e)
            logging.exception("Exception occured!!!!!")


if __name__ == "__main__":
    files = ['student', 'city', 'student_detail', 'class', 'marks']
    obj = CreateInsert()
    for file_name in files:
        obj.check_table(file_name)
    obj.connection_close()
