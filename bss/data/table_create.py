import sqlite3
from conf import attrs
def connection_check(db_name):
	# Checking for connection and create a database file named "TEAM_PJT.db" if not exists.
	conn = None
	try:
		conn = sqlite3.connect(db_name)
		return conn
	except sqlite3.Error as er:
		print('1,',er)
	return conn


def create_table(conn, sqldb_table):
	try:
		c = conn.cursor()
		c.execute(sqldb_table)
		print('ok')
	except sqlite3.Error:
		print(sqldb_table)


def main():

	db_name = attrs.DB_FILENAME  # version update

	bike_table = """CREATE TABLE IF NOT EXISTS bike(
								id INTEGER PRIMARY KEY,
								defective REAL DEFAULT 0,
								location_row INTEGER NOT NULL,
								location_col INTEGER NOT NULL,
								is_being_used INTEGER NOT NULL
								);"""
								
	customer_table = """ CREATE TABLE IF NOT EXISTS customer(
								id INTEGER PRIMARY KEY,
								name TEXT NOT NULL UNIQUE,
								password TEXT NOT NULL,
								wallet REAL NOT NULL,
								location_row INTEGER NOT NULL,
								location_col INTEGER NOT NULL,
								is_online INTEGER NOT NULL
								);"""
								
	bike_status_table = """CREATE TABLE IF NOT EXISTS bike_status(
								id INTEGER,
								time_of_event TEXT,
								defective_start REAL,
								defective_end REAL,
								FOREIGN KEY(id) REFERENCES bike(id)
								);"""
								
	manager_table = """CREATE TABLE IF NOT EXISTS manager(
								id INTEGER PRIMARY KEY,
								name TEXT NOT NULL UNIQUE,
								password TEXT NOT NULL,
								is_online INTEGER NOT NULL
								);"""  
	
	operator_table = """CREATE TABLE IF NOT EXISTS operator(
								id INTEGER PRIMARY KEY,
								name TEXT NOT NULL UNIQUE,
								password TEXT NOT NULL,
								account REAL NOT NULL,
								skill_level INTEGER NOT NULL,
								is_online INTEGER NOT NULL
								);"""
								
	movement_table = """CREATE TABLE IF NOT EXISTS movement(
								movement_id INTEGER PRIMARY KEY AUTOINCREMENT,
								bike_id INTEGER NOT NULL,
								user_id INTEGER NOT NULL,
								distance REAL,
								duration TEXT,
								endTime TEXT,
								FOREIGN KEY(bike_id) REFERENCES bike(id),
								FOREIGN KEY(user_id) REFERENCES customer(id)
								);"""                            

	transactions = """CREATE TABLE IF NOT EXISTS transactions(
								sumOfMoney REAL,
								timeOfEvent TEXT
								);"""

	company_table = """CREATE TABLE IF NOT EXISTS companyMoney(
								account REAL
								);"""

	conn = connection_check(db_name) #checking connection to database

	if conn is not None:
		create_table(conn, customer_table)
		create_table(conn, bike_table)
		create_table(conn, bike_status_table)
		create_table(conn, manager_table)
		create_table(conn, operator_table)
		create_table(conn, movement_table)
		create_table(conn,company_table)
		create_table(conn,transactions)
		conn.close()
	else:
		print("ERROR. Unable to create database connection.")

if __name__ == '__main__':
	main()

'''
reference:
https://www.sqlitetutorial.net/sqlite-python/create-tables/
https://www.sqlite.org/datatype3.html#:~:text=SQLite%20does%20not%20have%20a,)%20and%201%20(true).
A First Course in Database Systems(Third Edition) by Jeffrey D. Ullman
TIME data_type in sqlite: https://www.sqlite.org/lang_datefunc.html
'''
