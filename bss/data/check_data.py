import sqlite3

db_name = 'TEAM_PJT.db'
conn = sqlite3.connect(db_name)
c = conn.cursor()

c.execute("SELECT * FROM customer")
rows=c.fetchall()
for i in rows:
	print(i)

print('========================')

c.execute("SELECT * FROM bike")
rows=c.fetchall()
for i in rows:
	print(i)

print('========================')

c.execute("SELECT * FROM bike_status")
rows=c.fetchall()
for i in rows:
	print(i)

print('========================')

c.execute("SELECT * FROM operator")
rows=c.fetchall()
for i in rows:
	print(i)

print('========================')

c.execute("SELECT * FROM manager")
rows=c.fetchall()
for i in rows:
	print(i)

print('========================')

c.execute("SELECT * FROM movement")
rows=c.fetchall()
for i in rows:
	print(i)

print('========================')

c.execute("SELECT * FROM transactions")
rows=c.fetchall()
for i in rows:
	print(i)

print('========================')

c.execute("SELECT * FROM companyMoney")
rows=c.fetchall()
for i in rows:
	print(i)

print('========================')
