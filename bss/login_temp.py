import random
import sqlite3

from bss.conf import attrs
from bss.customer import Customer
from bss.data.db_path import get_db_path
from bss.manager import Manager
from bss.operators_temp import OperatorWorker  # TODO


def logging(role: str, name: str, password: str):
    conn = sqlite3.connect(get_db_path())
    c = conn.cursor()

    user = None

    if role == attrs.CUSTOMER:
        c.execute("SELECT * FROM customer WHERE name=:name and password=:password",
                  {'name': name, 'password': password})
        values = c.fetchall()
        if len(values) > 0:
            user = Customer(values[0][0], values[0][1], values[0][2], values[0][3],
                            [values[0][4], values[0][5]])

    elif role == attrs.OPERATOR:
        c.execute("SELECT * From operator Where name=:name and password=:password",
                  {'name': name, 'password': password})
        values = c.fetchall()
        if len(values) > 0:
            user = OperatorWorker(values[0][0], values[0][1], values[0][2], values[0][3], values[0][4])

    elif role == attrs.MANAGER:
        c.execute("SELECT * From manager Where name=:name and password=:password",
                  {'name': name, 'password': password})
        values = c.fetchall()
        if len(values) > 0:
            user = Manager(values[0][0], values[0][1], values[0][2])

    conn.close()

    return user


def register():
    username = input("please enter your username to register:")
    password0 = int(input("Please enter your password:"))
    password1 = int(input("Please confirm the password you entered:"))
    if password0 != password1:
        print("The two passwords you typed do not match!")
    elif len(username) == 0 or password1 == 0:
        print("The username and password cannot be empty!")
    else:
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()

        balance = int(input('Please enter the money you want to recharge:'))
        row = random.randint(0,19)
        col = random.randint(0,19)
        sql = "select max(id) from customer"
        c.execute(sql)
        id = c.fetchall()[0][0]+1
        try:
            c.execute(
                "INSERT INTO customer (id,name,password,wallet,location_row,location_col) VALUES({},'{}','{}',{},{},{})".format(
                    id, username, password1, balance, row, col))
            conn.commit()
            conn.close()
            print(" You have registered successfully!")
        except sqlite3.IntegrityError:
            print("registration fails,the account already exists")
