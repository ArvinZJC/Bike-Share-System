import sqlite3


db_name = 'TEAM_PJT.db'

try:
	conn = sqlite3.connect(db_name)
except sqlite3.Error as er:
	print(er)

c = conn.cursor()



c.execute("INSERT INTO customer (name,password,wallet,location_row,location_col) VALUES('{}','{}',{},{},{})".format("Tony","1234",132.5,10,11))
c.execute("INSERT INTO customer (name,password,wallet,location_row,location_col) VALUES('{}','{}',{},{},{})".format("Jichen","12345",232.5,0,1))
c.execute("INSERT INTO customer (name,password,wallet,location_row,location_col) VALUES('{}','{}',{},{},{})".format("Shihao","123456",172.5,8,3))
c.execute("INSERT INTO customer (name,password,wallet,location_row,location_col) VALUES('{}','{}',{},{},{})".format("Yuan","1234567",188.6,4,12))


c.execute("INSERT INTO bike (defective,location_row,location_col) VALUES({},{},{})".format(0,11,15))
c.execute("INSERT INTO bike (defective,location_row,location_col) VALUES({},{},{})".format(0,12,16))
c.execute("INSERT INTO bike (defective,location_row,location_col) VALUES({},{},{})".format(0,13,10))
c.execute("INSERT INTO bike (defective,location_row,location_col) VALUES({},{},{})".format(0,7,5))
c.execute("INSERT INTO bike (defective,location_row,location_col) VALUES({},{},{})".format(0,4,17))
c.execute("INSERT INTO bike (defective,location_row,location_col) VALUES({},{},{})".format(0,10,19))
c.execute("INSERT INTO bike (defective,location_row,location_col) VALUES({},{},{})".format(0,19,18))
c.execute("INSERT INTO bike (defective,location_row,location_col) VALUES({},{},{})".format(0,17,16))
c.execute("INSERT INTO bike (defective,location_row,location_col) VALUES({},{},{})".format(0,14,12))
c.execute("INSERT INTO bike (defective,location_row,location_col) VALUES({},{},{})".format(0,1,6))




conn.commit()

c.execute("SELECT * FROM customer")
rows=c.fetchall()
for i in rows:
	print(i)



c.execute("SELECT * FROM bike")
rows=c.fetchall()
for i in rows:
	print(i)

conn.close()