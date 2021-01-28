import sqlite3
from customer import *
from operators import *
from manager import *

def hello():
    while True:
        try:
            typeOfUser = int(input("Hello. Would you like to enter as :\n1) Customer\n2) Operator\n3)Manager\nChoose a number appropriately.\n"))
            if typeOfUser in [1,2,3]:
                return typeOfUser
        except:
            print("Invalid input please try again")



def logging():
    conn = sqlite3.connect('data/TEAM_PJT.db')
    c = conn.cursor()

    typeOfUser = hello()

    name = input("Input your username: ")
    password = input("Input your password: ")

    if typeOfUser == 1:
        c.execute("SELECT * FROM customer WHERE name=:name and password=:password", {'name': name,'password':password})
        values = c.fetchall()
        user = Customer(values[0][0], values[0][1], values[0][2], values[0][3],
                            [values[0][4], values[0][5]])

    elif typeOfUser == 2:
        c.execute("SELECT * From operator Where name=:name and password=:password", {'name': name,'password':password})
        values = c.fetchall()
        user = OperatorWorker(values[0][0],values[0][1],values[0][2],values[0][3],values[0][4])

    elif typeOfUser == 3:
        c.execute("SELECT * From manager Where name=:name and password=:password", {'name': name,'password':password})
        values = c.fetchall()
        user = Manager(values[0][0],values[0][1],values[0][2])

    conn.close()

    return user
