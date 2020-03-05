import logging
import os


def logs_handler(log_name, table_name):
    logger = logging.getLogger(table_name)
    file_handler = logging.FileHandler(os.path.dirname(__file__) + r"\\" + log_name)
    formatter = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    return logger
