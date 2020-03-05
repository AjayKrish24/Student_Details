import configparser
import sys
import mysql.connector

db_config = configparser.ConfigParser()
db_config.read('.editorconfig')

# print(db_config.sections())
# env = input("Enter the environment : ")
# host = db_config.get(env, 'host')
# user = db_config.get(env, 'user')
# password = db_config.get(env, 'password')
# db = db_config.get(env, 'db')


# env = sys.argv[0]
# host = db_config.get(env, sys.argv[1])
# user = db_config.get(env, sys.argv[2])
# password = db_config.get(env, sys.argv[3])
# db = db_config.get(env, sys.argv[4])


def connect_db(env):
    # env = input("Enter the environment : ")
    host = db_config.get(env, 'host')
    user = db_config.get(env, 'user')
    password = db_config.get(env, 'password')
    db = db_config.get(env, 'db')
    return mysql.connector.connect(host=host, user=user, password=password, db=db), host, user, password
