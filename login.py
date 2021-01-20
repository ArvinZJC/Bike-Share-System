import sqlite3
from Customer import *
def logging():
	conn = sqlite3.connect('TEAM_PJT.db')
	c = conn.cursor()

	name = input("Input your username: ")
	password = input("Input your password: ")

	c.execute("SELECT name FROM customer WHERE name=:name",{'name':name.lower().capitalize()})
	
	if c.fetchone()!=None:
		c.execute("SELECT password FROM customer WHERE name=:name",{'name':name.lower().capitalize()})

		if c.fetchall()[0][0]==password:
			c.execute("SELECT * FROM customer WHERE name=:name",{'name':name.lower().capitalize()})
			customer_values = c.fetchall()
		else:
			customer_values= None

	else:
		customer_values = None

	conn.close()

	return customer_values
