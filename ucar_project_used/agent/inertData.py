from ignore import db2 as db
import pymysql
import string
import random


def connect():
    try:
        database = pymysql.connect(host=db.host, port=db.port, user=db.user,
                                   passwd=db.pwd, db=db.db, charset=db.charset)
        return database
    except Exception as e:
        print(e)
        exit()


def insert_data():
    try:
        db = connect()
        cursor = db.cursor()
        for i in range(22, 30):
            sql = "insert into agent_withdraw (aid,amount,real_amount,tax,amount_type,grant_status,created_at) " \
                  "VALUE (%d,%d,%d,%d,%d,%d,now())" % (i, 500 + i, 500 + i, 200 + i, 2, 1)
            print(sql)
            cursor.execute(sql)
        db.commit()
    except Exception as e:
        print(e)


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


insert_data()