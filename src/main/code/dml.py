# import devconfig
import os
import sys
# from src.main.logs import file_logs
sys.path.insert(1, os.path.dirname(os.path.dirname(__file__)) + '\\' + 'logs')
import file_logs


class StudentDetails:
    def __init__(self, db, cursor):
        self.logger = file_logs.logs_handler("dml_log","dml_log")
        self.db = db
        self.cursor = cursor
        # print(self.cursor)

    def total_marks_obtained(self, student_name, class_no):
        self.cursor.execute(
            "select distinct (maths+biology+chemistry+english+physics+computer) as sum, "
            "((maths+biology+chemistry+english+physics+computer)/600)*100 as percentage "
            "from student s join marks m on s.id=m.id "
            "join class c on c.class_id=m.class_id "
            "where s.name='{}' and c.class='{}';".format(student_name, class_no))

        marks = self.cursor.fetchall()
        for mark in marks:
            print("Marks obtained out of 600 : ", mark[0])
            print("Percentage of marks obtained : ", mark[1])
        self.logger.info("Sum and Percentage of the student {} is found".format(student_name))

        self.cursor.execute(
            "select * from "
            "(select distinct name, "
            "dense_rank() over(partition by m.class_id "
            "order by maths+biology+chemistry+english+physics+computer desc) as std_rank, "
            "c.class from student s join marks m on s.id=m.id "
            "join class c on c.class_id=m.class_id) as tab "
            "where name = '{}' and class = '{}'".format(student_name, class_no))

        ranks = self.cursor.fetchall()
        for rank in ranks:
            print("Rank obtained is : ", rank[1])
            self.logger.info("Rank of the student {} from class {} and rank {} is found".format(student_name, class_no, rank[1]))
