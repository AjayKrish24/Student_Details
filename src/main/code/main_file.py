import create_insert_01
import file_logs
import dml
# import devconfig


+ env + '.properties'

def main():
    loggers = file_logs.logs_handler()
    dataset_creation(loggers)
    data_operation(loggers)
    loggers.info("Program ended")


def dataset_creation(loggers):
    files = ['student', 'city', 'student_detail', 'class', 'marks']
    obj = create_insert_01.CreateInsert(loggers)
    loggers.info("Object Created")
    for file_name in files:
        obj.check_table(file_name)
    obj.connection_close()
    return True


def data_operation(loggers):
    dml_obj = dml.StudentDetails(loggers)
    student_name = input("Enter the student name:")
    class_no = input("Enter the class (10th/11th/12th):")
    dml_obj.total_marks_obtained(student_name, class_no)
    return True


# def db_connect():
#     db = devconfig.connect_db()
#     cursor = db.cursor()
#     return cursor


if __name__ == '__main__':
    main()
