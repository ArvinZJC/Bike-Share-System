import sqlite3


def connection_check(db_name):
    # Checking for connection and create a database file named "TEAM_PJT.data" if not exists.
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
    db_name = 'TEAM_PJT.db'

    bike_table = """CREATE TABLE IF NOT EXISTS bike(
                                    id INTEGER PRIMARY KEY,
                                    defective INTEGER DEFAULT 0,
                                    longitude INTEGER NOT NULL,
                                    latitude INTEGER NOT NULL,
                                    );"""
    customer_table = """ CREATE TABLE IF NOT EXISTS customer(
                                    id INTEGER PRIMARY KEY,
                                    bike_id INTEGER,
                                    wallet REAL NOT NULL,
                                    longitude INTEGER NOT NULL,
                                    latitude INTEGER NOT NULL,
                                    FOREIGN KEY(bike_id) REFERENCES bike(id)
                                    );"""
    bike_status_table = """CREATE TABLE IF NOT EXISTS bike_status(
                                    id INTEGER,
                                    time TEXT,
                                    defective INTEGER,
                                    FOREIGN KEY(id) REFERENCES bike(id),
                                    FOREIGN KEY(defective) REFERENCES bike(defective)
                                    );"""

    conn = connection_check(db_name)  # checking connection to database

    if conn is not None:
        create_table(conn, customer_table)
        create_table(conn, bike_table)
        create_table(conn, bike_status_table)
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
