import os
import unittest
import csv
import create_insert
import devconfig


class MyTestCase(unittest.TestCase):
    def test_connection(self):
        # self.assertIsNone(devconfig.connect_db())
        self.assertRaises(Exception, self.assertIsNone, devconfig.connect_db)
        # self.assertEqual(self.assertIsNone(devconfig.connect_db()),None)

    def file_input(self):
        obj = create_insert.CreateInsert()
        files = ['student', 'city', 'student_detail', 'class', 'marks']
        for file_name in files:
            ddl_path = obj.path_ddl()
            result_set = obj.check_table(file_name)
            result_file = open(ddl_path + '\{}_result.csv'.format(file_name), 'a')
            for i in result_set:
                for j in range(len(i) - 2):
                    result_file.writelines(str(i[j]) + ',')
                result_file.writelines(str(i[len(i) - 2]) + '\n')
            f1 = open(ddl_path + '\\' + '{}_result.csv'.format(file_name))
            f2 = open(ddl_path + '\\' + '{}.csv'.format(file_name))
            self.csv_data = f1.read().splitlines()
            self.sql_data = f2.read().splitlines()

    def test_len_comp(self):
        self.file_input()
        self.assertEqual(len(self.csv_data), len(self.sql_data))

    def test_insert_table(self):
        self.file_input()
        count = 0
        for i in range(len(self.csv_data)):
            if self.csv_data[i] == self.sql_data[i]:
                count += 1

        self.assertEqual(count, len(self.csv_data), "they are not the same")
        # cnt = 0
        # count = 0
        # csv_data = []
        # sql_data = []
        # for i in data:
        #     print(type(i))
        #     csv_data.append(tuple(i))
        #

        # if len(sql_data) == len(csv_data):
        #     for i in range(len(csv_data)):
        #         if len(sql_data[i]) == len(csv_data[i]):
        #             count = len(sql_data[i]) * len(csv_data)
        #             for k in range(len(sql_data[i])):
        #                 if str(sql_data[i][k]) == str(csv_data[i][k]):
        #                     cnt = cnt+1
        # self.assertEqual(cnt, count, 'Tested : {}'.format(file_name))


if __name__ == '__main__':
    unittest.main()
