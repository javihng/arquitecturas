
import pymysql


def conn_myslq():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='1234',
                           db='movies')
