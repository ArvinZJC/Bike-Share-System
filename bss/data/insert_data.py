import sqlite3
db_name = 'TEAM_PJT.db'

try:
	conn = sqlite3.connect(db_name)
except sqlite3.Error as er:
	print(er)

c = conn.cursor()



c.execute("INSERT INTO customer (id,name,password,wallet,location_row,location_col) VALUES({},'{}','{}',{},{},{})".format(1,"Tony","1234",132.5,10,11))
c.execute("INSERT INTO customer (id,name,password,wallet,location_row,location_col) VALUES({},'{}','{}',{},{},{})".format(2,"Jichen","12345",232.5,0,1))
c.execute("INSERT INTO customer (id,name,password,wallet,location_row,location_col) VALUES({},'{}','{}',{},{},{})".format(3,"Shihao","123456",172.5,8,3))
c.execute("INSERT INTO customer (id,name,password,wallet,location_row,location_col) VALUES({},'{}','{}',{},{},{})".format(4,"Yuan","1234567",188.6,4,12))


c.execute("INSERT INTO bike (id,defective,location_row,location_col) VALUES({},{},{},{})".format(1,0,11,15))
c.execute("INSERT INTO bike (id,defective,location_row,location_col) VALUES({},{},{},{})".format(2,0,12,16))
c.execute("INSERT INTO bike (id,defective,location_row,location_col) VALUES({},{},{},{})".format(3,0,13,10))
c.execute("INSERT INTO bike (id,defective,location_row,location_col) VALUES({},{},{},{})".format(4,0,7,5))
c.execute("INSERT INTO bike (id,defective,location_row,location_col) VALUES({},{},{},{})".format(5,0,4,17))
c.execute("INSERT INTO bike (id,defective,location_row,location_col) VALUES({},{},{},{})".format(6,0,10,19))
c.execute("INSERT INTO bike (id,defective,location_row,location_col) VALUES({},{},{},{})".format(7,0,19,18))
c.execute("INSERT INTO bike (id,defective,location_row,location_col) VALUES({},{},{},{})".format(8,0,17,16))
c.execute("INSERT INTO bike (id,defective,location_row,location_col) VALUES({},{},{},{})".format(9,0,14,12))
c.execute("INSERT INTO bike (id,defective,location_row,location_col) VALUES({},{},{},{})".format(10,0,1,6))


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