import os
import datetime


class CreateInsert:

    def __init__(self, logger, db, cursor):
        self.logger = logger
        self.db = db
        self.cursor = cursor

    # method to check the tables is present or not and empty or not
    def check_table(self, name):
        """
            Parameter : name of file
            Return : True
        """

        # self.cursor.execute("use datamodel")
        # self.db.commit()
        self.cursor.execute("show tables")
        self.logger.info("Tables are fetched from database")
        table = self.cursor.fetchall()
        flag = 0
        try:
            for tables in table:
                if name in tables:
                    flag = 1
                    self.cursor.execute("select * from {}".format(name))
                    data = self.cursor.fetchall()
                    data_len = len(data)
                    if data_len == 0:
                        self.insert_table(name)  # insert_table method is invoked for inserting the data's
                    else:
                        print("table  " + name + " already exists with data")
            if flag == 0:
                self.create_table(name)  # create_table method is invoked for inserting the data's
            self.cursor.execute('select * from {}'.format(name))
            result_set = self.cursor.fetchall()
            return result_set
        except Exception as e:
            print(e)
            self.logger.exception("Exception occured!!!!!")

    # Method to fetch the ddl path
    def path_ddl(self):
        try:
            ddl_folder = os.path.dirname(os.path.dirname(__file__))
            ddl_path = ddl_folder + "\\" + '{}'.format("ddl")
            self.logger.info("Path of the ddl folder is fetched : {}".format(ddl_path))
            return ddl_path

        except Exception as e:
            print(e)
            self.logger.exception("Exception occured!!!!!")

    # Method to create table
    def create_table(self, name):
        """
            Parameter : name of file
            Return : nothing
        """

        ddl_path = self.path_ddl()
        try:
            file_open = open(ddl_path + '\\' + '{}.sql'.format(name))
            lines = file_open.read().split(';')
            create = lines[0].strip()
            self.cursor.execute(create)
            self.db.commit()
            self.logger.info("Table {} is created ".format(name))
            print("Table {} created".format(name))
            self.insert_table(name)  # insert_table method is invoked for inserting the data's

        except FileNotFoundError as e:
            print('File Not Found', e)
            self.logger.exception("File not found")

    # Method to insert values into table
    def insert_table(self, name):
        """
            Parameter : name of file
            Return : records of the table
        """

        ddl_path = self.path_ddl()  # function call to fetch ddl dir path
        self.cursor.execute("select column_name from information_schema.columns where table_schema='datamodel' and "
                            "table_name='{}' order by ordinal_position".format(name))
        col_names = self.cursor.fetchall()
        nested_list = [list(x) for x in col_names]
        flat_list = [item for sublist in nested_list for item in sublist]

        try:
            file = open(ddl_path + '\\' + '{}.csv'.format(name))
            value = file.read().splitlines()
            for val in value:
                val_list = val.split(",")
                val_list.append(datetime.datetime.now())
                keys = (",".join(flat_list))
                joiner = (",".join(["%s" for x in range(len(val_list))]))
                # print(name)
                # print(keys)
                # print(joiner)
                # print(val_list)
                self.cursor.execute("insert into {} ({}) values({})".format(name, keys, joiner), val_list)
            self.db.commit()
            self.logger.info("Data's are inserted into table {}".format(name))
            print("Insert done")


        except FileNotFoundError as e:
            print(e)
            self.logger.exception("File not found")

        except Exception as e:
            print(e)
            self.logger.exception("Exception occurred!!!!!")
