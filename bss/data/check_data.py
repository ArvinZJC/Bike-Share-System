import sqlite3

db_name = 'TEAM_PJT.db'
conn = sqlite3.connect(db_name)
c = conn.cursor()


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