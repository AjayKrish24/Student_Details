import os
import devconfig
import datetime
import sys

environment = str(sys.argv[0])




class CreateInsert:

    def __init__(self, logger):
        self.logger = logger
        self.db = devconfig.connect_db()
        self.logger.info("Database Connection Established")
        self.cursor = self.db.cursor()
        # self.logger.info("Database Connection Established")

    # method to check the tables is present or not and empty or not
    def check_table(self, name):
        """
            Parameter : name of file
            Return : True
        """

        self.cursor.execute("use datamodel")
        self.db.commit()
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
                    if data_len != 0:
                        self.cursor.execute("truncate table {}".format(name))
                        self.db.commit()
                        self.insert_table(name)  # insert_table method is invoked for inserting the data's
                    else:
                        self.insert_table(name)  # insert_table method is invoked for inserting the data's
            if flag == 0:
                self.create_table(name)  # create_table method is invoked for inserting the data's

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
            file_open = open(ddl_path + '\\' + '{}.txt'.format(name))
            lines = file_open.read().split(';')
            create = lines[0].strip()
            self.cursor.execute(create)
            self.db.commit()
            self.logger.info("Table {} is created ".format(name))
            print("Table created")
            self.cursor.execute("alter table {} add column {} timestamp".format(name, 'updated_time'))
            self.db.commit()
            self.logger.info("Added column timestamp in {}".format(name))
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
        # print(col_names)
        nested_list = [list(x) for x in col_names]
        # print(nested_list)
        flat_list = [item for sublist in nested_list for item in sublist]
        # print(flat_list)

        try:
            file = open(ddl_path + '\\' + '{}.csv'.format(name))
            value = file.read().splitlines()
            for val in value:
                val_list = val.split(",")
                val_list.append(datetime.datetime.now())
                keys = (",".join(flat_list))
                joiner = (",".join(["%s" for x in range(len(val_list))]))
                self.cursor.execute("insert into {} ({}) values({})".format(name, keys, joiner), val_list)
            self.db.commit()
            self.logger.info("Data's are inserted into table {}".format(name))
            print("Insert done")
            self.cursor.execute('select * from {}'.format(name))
            result_set = self.cursor.fetchall()
            return result_set

        except FileNotFoundError as e:
            print(e)
            self.logger.exception("File not found")

        except Exception as e:
            print(e)
            self.logger.exception("Exception occurred!!!!!")

    def connection_close(self):
        """
            Parameter : None
            Return : None
        """

        try:
            self.db.close()
            self.logger.info("Database connection closed")

        except Exception as e:
            print(e)
            self.logger.exception("Exception occurred!!!!!")
