import sqlite3
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

import db_path as db


conn = sqlite3.connect(db.get_db_path())
c = conn.cursor()

print("Customer table")
print("========================")

c.execute("SELECT * FROM customer")
rows=c.fetchall()
for i in rows:
	print(i)

print('========================')

print("Bike status table")
print("========================")

c.execute("SELECT * FROM bike_status")
rows=c.fetchall()
for i in rows:
	print(i)

print('========================')

print("Movements Table")

c.execute("SELECT * FROM movement")
rows=c.fetchall()
for i in rows:
	print(i)

print('========================')

print("Transactions table")

c.execute("SELECT * FROM transactions")
rows=c.fetchall()
for i in rows:
	print(i)

print('========================')

print("Company Money Table")

c.execute("SELECT * FROM companyMoney")
rows=c.fetchall()
for i in rows:
	print(i)

print('========================')