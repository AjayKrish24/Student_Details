import devconfig

class StudentDetails:
    def __init__(self, logger):
        self.logger = logger
        self.db = devconfig.connect_db()
        self.cursor = self.db.cursor()
        # print(self.cursor)

    def total_marks_obtained(self, student_name, class_no):
        self.cursor.execute("select distinct maths+biology+chemistry+english+physics+computer as sum ,((maths+biology+chemistry+english+physics+computer)/600)*100 as percentage from student s join marks m on s.student_id=m.student_id join class c on c.class_id=m.class_id where s.student_name='{0}' and c.class='{1}'".format(student_name, class_no))

        marks = self.cursor.fetchall()
        for mark in marks:
            print("Marks obtained out of 600:", mark[0])
            print("Percentage of marks obtained:", mark[1])

        self.cursor.execute("select * from (select distinct student_name,dense_rank() over(partition by m.class_id order by maths+biology+chemistry+english+physics+computer desc)r ,c.class from student s join marks m on s.student_id=m.student_id join class c on c.class_id=m.class_id) as tab where s.student_name ='{}' and c.class = '{}'".format(student_name, class_no))

        ranks = self.cursor.fetchall()
        for rank in ranks:
            print("rank obtained is", rank[1])
