import configparser
import mysql.connector

db_config = configparser.ConfigParser()
db_config.read('.editorconfig')

print(db_config.sections())
env = input("Enter the environment : ")
host = db_config.get('{}'.format(env), 'host')
user = db_config.get('{}'.format(env), 'user')
password = db_config.get('{}'.format(env), 'password')
db = db_config.get('{}'.format(env), 'db')
# print(host)


def connect_db():
    return mysql.connector.connect(host=host, user=user, password=password, db=db)


# return mysql.connector.connect(host=db_config['mysqlDB']['host'],
#                                    user=db_config['mysqlDB']['user'],
#                                    password=db_config['mysqlDB']['password'],
#                                    db=db_config['mysqlDB']['db'])
