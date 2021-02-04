import sqlite3
from customer import *
from operators import *
from manager import *
import random
import time


def hello():
    while True:
        try:
            typeOfUser = int(input(
                "Hello. Would you like to enter as :\n1) Customer\n2) Operator\n3)Manager\n4)Sign in\nChoose a number appropriately.\n"))
            if typeOfUser in [1, 2, 3,4]:
                return typeOfUser
        except:
            print("Invalid input please try again")


def logging():
    conn = sqlite3.connect('data/' + attrs.DB_FILENAME)
    c = conn.cursor()

    typeOfUser = hello()

    user = None

    while (user == None and typeOfUser in [1, 2, 3]):
        name = input("Input your username: ")
        password = input("Input your password: ")
        if typeOfUser == 1:
            c.execute("SELECT * FROM customer WHERE name=:name and password=:password",
                      {'name': name, 'password': password})
            values = c.fetchall()
            if len(values) == 0:
                print("Your username or password is wrong,please try again.")
            else:
                user = Customer(values[0][0], values[0][1], values[0][2], values[0][3],
                                [values[0][4], values[0][5]])

        elif typeOfUser == 2:
            c.execute("SELECT * From operator Where name=:name and password=:password",
                      {'name': name, 'password': password})
            values = c.fetchall()
            if len(values) == 0:
                print("Your username or password is wrong,please try again.")
            else:
                user = OperatorWorker(values[0][0], values[0][1], values[0][2], values[0][3], values[0][4])

        elif typeOfUser == 3:
            c.execute("SELECT * From manager Where name=:name and password=:password",
                      {'name': name, 'password': password})
            values = c.fetchall()
            if len(values) == 0:
                print("Your username or password is wrong,please try again.")
            else:
                user = Manager(values[0][0], values[0][1], values[0][2])

    if typeOfUser == 4:
        flag = True
        while flag:
            username = input("please enter your username to register:")
            try:
                    password0 = int(input("Please enter your password:"))
            except:
                print("Invalid input please try again")
                continue
            try:
                password1 = int(input("Please confirm the password you entered:"))
                flag = False
            except:
                print("Invalid input please try again")
                continue
            if password0 != password1:
                print("The two passwords you typed do not match!")
                flag = True
                continue
            elif len(username) == 0:
                print("The username cannot be empty!")
                flag = True
                continue
            else:
                conn = sqlite3.connect('data/' + attrs.DB_FILENAME)
                c = conn.cursor()
                balance = int(input('Please enter the money you want to recharge:'))
                row = random.randint(0, 19)
                col = random.randint(0, 19)
                sql = "select max(id) from customer"
                c.execute(sql)
                id = c.fetchall()[0][0] + 1
                try:
                    c.execute(
                        "INSERT INTO customer (id,name,password,wallet,location_row,location_col) VALUES({},'{}','{}',{},{},{})".format(
                            id, username, password1, balance, row, col))
                    conn.commit()
                    print(" You have registered successfully!\n Wait a second, the system will log you in automatically")
                    time.sleep(5)
                    c.execute("SELECT * FROM customer WHERE name=:username and password=:password0",
                                {'username': username, 'password0': password0})
                    values = c.fetchall()
                    user = Customer(values[0][0], values[0][1], values[0][2], values[0][3],
                                    [values[0][4], values[0][5]])

                except sqlite3.IntegrityError:
                    print("registration fails,the account already exists")

    conn.close()
    return user


# def register():
#     flag = True
#     while flag:
#         username = input("please enter your username to register:")
#         try:
#             password0 = int(input("Please enter your password:"))
#         except:
#             print("Invalid input please try again")
#             continue
#         try:
#             password1 = int(input("Please confirm the password you entered:"))
#             flag = False
#         except:
#             print("Invalid input please try again")
#             continue
#         if password0 != password1:
#             print("The two passwords you typed do not match!")
#             flag = True
#             continue
#         elif len(username) == 0:
#             print("The username cannot be empty!")
#             flag = True
#             continue
#         else:
#             conn = sqlite3.connect('data/' + attrs.DB_FILENAME)
#             c = conn.cursor()
#
#             balance = int(input('Please enter the money you want to recharge:'))
#             row = random.randint(0,19)
#             col = random.randint(0,19)
#             sql = "select max(id) from customer"
#             c.execute(sql)
#             id = c.fetchall()[0][0]+1
#             try:
#                 c.execute(
#                     "INSERT INTO customer (id,name,password,wallet,location_row,location_col) VALUES({},'{}','{}',{},{},{})".format(
#                         id, username, password1, balance, row, col))
#                 conn.commit()
#                 conn.close()
#                 print(" You have registered successfully!")
#             except sqlite3.IntegrityError:
#                 print("registration fails,the account already exists")