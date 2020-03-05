import create_insert
import os
import sys
import dml
import devconfig
# from src.main.log_files import file_logs
sys.path.insert(1, os.path.dirname(os.path.dirname(__file__)) + '\\' + 'logs')
import file_logs


def main():
    loggers, db, cursor = connection()
    creation(loggers, db, cursor)
    operation(loggers, db, cursor)
    close(loggers, db)


def connection():
    loggers = file_logs.logs_handler("connection_log", __name__)
    db, host, user, password = devconfig.connect_db(sys.argv[1])
    cursor = db.cursor()
    loggers.info("Database Connection Established {}@{} with password {}".format(user, host,
                                                                                 '*'*len(password)))
    return loggers, db, cursor


def creation(loggers, db, cursor):
    files = ['student', 'city', 'class_detail', 'student_detail', 'class', 'marks']
    log_files = ['student_log', 'class_details', 'city_log', 'student_detail_log', 'class_log', 'marks_log']
    loggers.info("Object Created")
    for i in range(len(files)):
        loggers = file_logs.logs_handler(log_files[i], files[i])
        obj = create_insert.CreateInsert(loggers, db, cursor)
        obj.check_table(files[i])


def operation(loggers, db, cursor):
    dml_obj = dml.StudentDetails(db, cursor)
    loggers.info("Instance created for Dml operation")
    student_name = input("Enter the student name:")
    class_no = input("Enter the class (10th/11th/12th):")
    dml_obj.total_marks_obtained(student_name, class_no)


def close(loggers, db):
    try:
        db.close()
        loggers.info("Program ended And connection closed")
    except Exception as e:
        loggers.exception("Cant close the connection")


if __name__ == '__main__':
    main()
