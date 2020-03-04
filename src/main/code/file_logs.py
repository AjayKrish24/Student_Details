import logging


# logging.basicConfig(filename="student.log",
#                     filemode='a',
#                     format="%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s",
#                     level=logging.INFO)

# logger = logging.getLogger("StudentDetails")
def logs_handler():

    logger = logging.getLogger("StudentDetails")
    file_handler = logging.FileHandler(r"C:\Users\ajay.krishnamurthi\PycharmProjects\DataModel\src\main\log_file"
                                       r"\student.log")
    formatter = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    return logger
