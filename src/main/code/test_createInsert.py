import unittest
import csv
import create_insert


class MyTestCase(unittest.TestCase):
    def test_insert_table(self):
        obj = create_insert.CreateInsert()
        files = ['student', 'city', 'student_detail', 'class', 'marks']
        for file_name in files:
            f = open(os.path.join(CreateInsert.path_ddl,'{}.csv'.format(file_name)))
            data = csv.reader(f)
            cnt = 0
            count = 0
            csv_data = []
            sql_data = []
            for i in data:
                csv_data.append(tuple(i))
            for i in obj.insert_table(file_name):
                sql_data.append(i)
            if len(sql_data) == len(csv_data):
                for i in range(len(csv_data)):
                    if len(sql_data[i]) == len(csv_data[i]):
                        count = len(sql_data[i]) * len(csv_data)
                        for k in range(len(sql_data[i])):
                            if str(sql_data[i][k]) == str(csv_data[i][k]):
                                cnt = cnt+1
            self.assertEqual(cnt, count, 'Tested : {}'.format(file_name))


if __name__ == '__main__':
    unittest.main()

