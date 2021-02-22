import sqlite3
from bss.conf import attrs
db_name = attrs.DB_FILENAME 

try:
	conn = sqlite3.connect(db_name)
except sqlite3.Error as er:
	print(er)

c = conn.cursor()

c.execute("INSERT INTO companyMoney (account) VALUES({})".format(1000))

c.execute("INSERT INTO customer (id,name,password,wallet,location_row,location_col,is_online) VALUES({},'{}','{}',{},{},{},{})".format(1,"tony","1234",132.5,10,11,0))
c.execute("INSERT INTO customer (id,name,password,wallet,location_row,location_col,is_online) VALUES({},'{}','{}',{},{},{},{})".format(2,"jichen","12345",232.5,0,1,0))
c.execute("INSERT INTO customer (id,name,password,wallet,location_row,location_col,is_online) VALUES({},'{}','{}',{},{},{},{})".format(3,"shihao","123456",172.5,8,3,0))
c.execute("INSERT INTO customer (id,name,password,wallet,location_row,location_col,is_online) VALUES({},'{}','{}',{},{},{},{})".format(4,"yuan","1234567",188.6,4,12,0))


c.execute("INSERT INTO operator (id,name,password,account,skill_level,is_online) VALUES({},'{}','{}',{},{},{})".format(1,"jiamin","1234",0,4,0))
c.execute("INSERT INTO operator (id,name,password,account,skill_level,is_online) VALUES({},'{}','{}',{},{},{})".format(2,"nan","12345",0,3,0))

c.execute("INSERT INTO manager (id,name,password,is_online) VALUES({},'{}','{}',{})".format(1,"xiaoran","1234",0))



c.execute("INSERT INTO bike (id,defective,location_row,location_col,is_being_used) VALUES({},{},{},{},{})".format(1,0,11,15,0))
c.execute("INSERT INTO bike (id,defective,location_row,location_col,is_being_used) VALUES({},{},{},{},{})".format(2,0,12,16,0))
c.execute("INSERT INTO bike (id,defective,location_row,location_col,is_being_used) VALUES({},{},{},{},{})".format(3,0,13,10,0))
c.execute("INSERT INTO bike (id,defective,location_row,location_col,is_being_used) VALUES({},{},{},{},{})".format(4,0,7,5,0))
c.execute("INSERT INTO bike (id,defective,location_row,location_col,is_being_used) VALUES({},{},{},{},{})".format(5,0,4,17,0))
c.execute("INSERT INTO bike (id,defective,location_row,location_col,is_being_used) VALUES({},{},{},{},{})".format(6,0,10,19,0))
c.execute("INSERT INTO bike (id,defective,location_row,location_col,is_being_used) VALUES({},{},{},{},{})".format(7,0,19,18,0))
c.execute("INSERT INTO bike (id,defective,location_row,location_col,is_being_used) VALUES({},{},{},{},{})".format(8,0,17,16,0))
c.execute("INSERT INTO bike (id,defective,location_row,location_col,is_being_used) VALUES({},{},{},{},{})".format(9,0,14,12,0))
c.execute("INSERT INTO bike (id,defective,location_row,location_col,is_being_used) VALUES({},{},{},{},{})".format(10,0,1,6,0))


conn.commit()

conn.close()