import configparser
import mysql.connector

db_config = configparser.ConfigParser()
db_config.read('.editorconfig')


def connect_db():
    return mysql.connector.connect(host=db_config['mysqlDB']['host'],
                                   user=db_config['mysqlDB']['user'],
                                   password=db_config['mysqlDB']['password'],
                                   db=db_config['mysqlDB']['db'])
