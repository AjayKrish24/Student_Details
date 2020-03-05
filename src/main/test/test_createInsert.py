import unittest
import create_insert
import devconfig


def file_insert():
    obj = create_insert.CreateInsert()
    files = ['student', 'city', 'student_detail', 'class', 'marks']
    for file_name in files:
        ddl_path = obj.path_ddl()
        result_set = obj.check_table(file_name)
        result_file = open(ddl_path + '\\'+'{}_result.csv'.format(file_name), 'a')
        for i in result_set:
            for j in range(len(i) - 2):
                result_file.writelines(str(i[j]) + ',')
            result_file.writelines(str(i[len(i) - 2]) + '\n')
        result_file.close()


class MyTestCase(unittest.TestCase):

    def test_connection(self):
        self.assertRaises(Exception, self.assertIsNone, devconfig.connect_db)

    def file_input(self):

        obj = create_insert.CreateInsert()
        files = ['student', 'city', 'student_detail', 'class', 'marks']
        for file_name in files:
            ddl_path = obj.path_ddl()
            f1 = open(ddl_path + '\\' + '{}_result.csv'.format(file_name))
            f2 = open(ddl_path + '\\' + '{}.csv'.format(file_name))
            self.csv_data = f1.read().splitlines()
            self.sql_data = f2.read().splitlines()
            f1.close()
            f2.close()

    def test_len_comp(self):

        self.file_input()
        self.assertEqual(len(self.csv_data),len(self.sql_data))

    def test_insert_table(self):
        self.file_input()
        count = 0
        for i in range(len(self.csv_data)):
            if self.csv_data[i] == self.sql_data[i]:
                count += 1
        self.assertEqual(count, len(self.csv_data), "they are not the same")

    def test_columns(self):
        self.db = devconfig.connect_db()
        self.cursor = self.db.cursor()
        obj = create_insert.CreateInsert()
        files = ['student', 'city', 'student_detail', 'class', 'marks']
        for file_name in files:
            ddl_path = obj.path_ddl()
            file = open(ddl_path + '\\' + '{}.txt'.format(file_name))
            semicolon_splited = file.read().split(";")[0].split("(")[1].split(")")[0]
            self.cursor.execute(
                "select column_name,data_type from information_schema.columns where table_schema='datamodel' and table_name='{}'".format(file_name))
            tuples = self.cursor.fetchall()
            lists = [list(i) for i in tuples]
            listss = [" ".join(x) for x in lists]
            final_split = semicolon_splited.split(",")
            for x in final_split:
                if 'key' in x:
                    final_split.remove(x)
            count = 0
            for i in range(len(final_split)):
                if final_split[i].strip(" ") == listss[i].strip(" "):
                    count += 1
            self.assertEqual(count,len(final_split),'Columns are not same')
            file.close()


if __name__ == '__main__':
    #file_input()        ----->>> run this code by ctrl+shft+F10 for the first time and then run from the terminal by using
    #                             coverage run test_createInsert.py
    unittest.main()
