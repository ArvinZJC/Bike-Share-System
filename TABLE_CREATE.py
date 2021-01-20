import sqlite3

def connection_check(db_name):
    #Checking for connection and create a database file named "TEAM_PJT.db" if not exists.
    conn = None
    try:
        conn = sqlite3.connect(db_name)
        return conn
    except sqlite3.Error as er:
        print(er)
    return conn

def create_table(conn, sqldb_table):
    try:
        c = conn.cursor()
        c.execute(sqldb_table)
    except sqlite3.Error as er:
        print(er)

def main():
    db_name = 'TEAM_PJT.db' #version update

    bike_table = """CREATE TABLE IF NOT EXISTS bike(
                                 id INTEGER PRIMARY KEY,
                                 defective INTEGER DEFAULT 0
                                 );"""
    customer_table = """ CREATE TABLE IF NOT EXISTS customer(
                                id INTEGER PRIMARY KEY,
                                bike_id INTEGER,
                                wallet REAL NOT NULL,
                                location TEXT NOT NULL,
                                FOREIGN KEY(bike_id) REFERENCES bike(id)
                                );"""
    bike_where_table = """CREATE TABLE IF NOT EXISTS bike_usage(
                                id INTEGER,
                                time TEXT,
                                defective INTEGER,
                                location TEXT NOT NULL,
                                FOREIGN KEY(id) REFERENCES bike(id),
                                FOREIGN KEY(defective) REFERENCES bike(defective)
                                );"""
    conn = connection_check(db_name) #checking connection to database

    if conn is not None:
        create_table(conn, customer_table)
        create_table(conn, bike_table)
        create_table(conn, bike_where_table)
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
'''
