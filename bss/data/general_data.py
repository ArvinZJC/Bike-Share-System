import sqlite3

from bss.conf import attrs

db = sqlite3.connect(attrs.DB_FILENAME)
cursor = db.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS bike(
                                id INTEGER PRIMARY KEY,
                                defective INTEGER DEFAULT 0,
                                longitude INTEGER NOT NULL,
                                latitude INTEGER NOT NULL
                                )

""")

cursor.execute("""INSERT OR IGNORE into bike(id,defective, longitude, latitude)  values(10001,0,0,0)""")
cursor.execute("""INSERT OR IGNORE into bike(id,defective, longitude, latitude)  values(10002,0,0,0)""")
cursor.execute("""INSERT OR IGNORE into bike(id,defective, longitude, latitude)  values(10003,0,0,0)""")
cursor.execute("""INSERT OR IGNORE into bike(id,defective, longitude, latitude)  values(10004,0,0,0)""")
cursor.execute("""INSERT OR IGNORE into bike(id,defective, longitude, latitude)  values(10005,0,0,0)""")
cursor.execute("""INSERT OR IGNORE into bike(id,defective, longitude, latitude)  values(10006,0,0,0)""")
cursor.execute("""INSERT OR IGNORE into bike(id,defective, longitude, latitude)  values(10007,0,0,0)""")
cursor.execute("""INSERT OR IGNORE into bike(id,defective, longitude, latitude)  values(10008,0,0,0)""")
cursor.execute("""INSERT OR IGNORE into bike(id,defective, longitude, latitude)  values(10009,0,0,0)""")
cursor.execute("""INSERT OR IGNORE into bike(id,defective, longitude, latitude)  values(100010,0,0,0)""")
cursor.execute("""INSERT OR IGNORE into bike(id,defective, longitude, latitude)  values(100011,0,0,0)""")
cursor.execute("""INSERT OR IGNORE into bike(id,defective, longitude, latitude)  values(100012,0,0,0)""")
cursor.execute("""INSERT OR IGNORE into bike(id,defective, longitude, latitude)  values(100013,0,0,0)""")
cursor.execute("""INSERT OR IGNORE into bike(id,defective, longitude, latitude)  values(100014,0,0,0)""")
cursor.execute("""INSERT OR IGNORE into bike(id,defective, longitude, latitude)  values(100015,0,0,0)""")
cursor.execute("""INSERT OR IGNORE into bike(id,defective, longitude, latitude)  values(100016,0,0,0)""")
cursor.execute("""INSERT OR IGNORE into bike(id,defective, longitude, latitude)  values(100017,0,0,0)""")
cursor.execute("""INSERT OR IGNORE into bike(id,defective, longitude, latitude)  values(100018,0,0,0)""")
cursor.execute("""INSERT OR IGNORE into bike(id,defective, longitude, latitude)  values(100019,0,0,0)""")
cursor.execute("""INSERT OR IGNORE into bike(id,defective, longitude, latitude)  values(100020,0,0,0)""")




'''bike_data = ["10001, 0, 0, 0", "10002,0,0,0", "10003,0,0,0", "10004,0,0,0", "10005,0,0,0",
             "10006,0,0,0", "10007,0,0,0", "10008,0,0,0", "10009,0,0,0", "100010,0,0,0",
             "10011,0,0,0", "10012,0,0,0", "10013,0,0,0", "10014,0,0,0", "10015,0,0,0",
             "10016,0,0,0", "10017,0,0,0", "10018,0,0,0", "10019,0,0,0", "10020,0,0,0"]'''
db.commit()

cursor.execute("select * from bike")
for x in cursor.fetchall():
    print(x)


cursor.execute("""

 CREATE TABLE IF NOT EXISTS customer(
                                id INTEGER PRIMARY KEY,
                                user_name TEXT NOT NULL UNIQUE,
                                password TEXT NOT NULL,
                                wallet REAL NOT NULL,
                                longitude INTEGER NOT NULL,
                                latitude INTEGER NOT NULL
                                )

""")

cursor.execute("""INSERT OR IGNORE into customer(id,user_name, password, wallet, longitude, latitude)
values(20001, 'Tony', 'Tony', 0.00, 0, 0)""")
cursor.execute("""INSERT OR IGNORE into customer(id,user_name, password, wallet, longitude, latitude)  
values(20002, 'Jack', 'Jack', 0.00, 0, 0)""")
cursor.execute("""INSERT OR IGNORE into customer(id,user_name, password, wallet, longitude, latitude)  
values(20003, 'Lucy', 'Lucy', 0.00, 0, 0)""")
cursor.execute("""INSERT OR IGNORE into customer(id,user_name, password, wallet, longitude, latitude)  
values(20004, 'James', 'James', 0.00, 0, 0)""")
cursor.execute("""INSERT OR IGNORE into customer(id,user_name, password, wallet, longitude, latitude)  
values(20005, 'Martin', 'Martin', 0.00, 0, 0)""")
cursor.execute("""INSERT OR IGNORE into customer(id,user_name, password, wallet, longitude, latitude)  
values(20006, 'Diana', 'Diana', 0.00, 0, 0)""")
cursor.execute("""INSERT OR IGNORE into customer(id,user_name, password, wallet, longitude, latitude)  
values(20007, 'Judy', 'Judy', 0.00, 0, 0)""")
cursor.execute("""INSERT OR IGNORE into customer(id,user_name, password, wallet, longitude, latitude)  
values(20008, 'Louis', 'Louis', 0.00, 0, 0)""")
cursor.execute("""INSERT OR IGNORE into customer(id,user_name, password, wallet, longitude, latitude)  
values(20009, 'Lisa', 'Lisa', 0.00, 0, 0)""")
cursor.execute("""INSERT OR IGNORE into customer(id,user_name, password, wallet, longitude, latitude)  
values(20010, 'Peter', 'Peter', 0.00, 0, 0)""")
cursor.execute("""INSERT OR IGNORE into customer(id,user_name, password, wallet, longitude, latitude)  
values(20011, 'Mary', 'Mary', 0.00, 0, 0)""")
cursor.execute("""INSERT OR IGNORE into customer(id,user_name, password, wallet, longitude, latitude)  
values(20012, 'Joy', 'Joy', 0.00, 0, 0)""")
cursor.execute("""INSERT OR IGNORE into customer(id,user_name, password, wallet, longitude, latitude)  
values(20013, 'Vivian', 'Vivian', 0.00, 0, 0)""")
cursor.execute("""INSERT OR IGNORE into customer(id,user_name, password, wallet, longitude, latitude)  
values(20014, 'Mark', 'Mark', 0.00, 0, 0)""")
cursor.execute("""INSERT OR IGNORE into customer(id,user_name, password, wallet, longitude, latitude)  
values(20015, 'Kate', 'Kate', 0.00, 0, 0)""")
cursor.execute("""INSERT OR IGNORE into customer(id,user_name, password, wallet, longitude, latitude)  
values(20016, 'Poul', 'Poul', 0.00, 0, 0)""")
cursor.execute("""INSERT OR IGNORE into customer(id,user_name, password, wallet, longitude, latitude)  
values(20017, 'Allen', 'Allen', 0.00, 0, 0)""")
cursor.execute("""INSERT OR IGNORE into customer(id,user_name, password, wallet, longitude, latitude)  
values(20018, 'Fiona', 'Fiona', 0.00, 0, 0)""")
cursor.execute("""INSERT OR IGNORE into customer(id,user_name, password, wallet, longitude, latitude)  
values(20019, 'May', 'May', 0.00, 0, 0)""")
cursor.execute("""INSERT OR IGNORE into customer(id,user_name, password, wallet, longitude, latitude)  
values(20020, 'Julie', 'Julie', 0.00, 0, 0)""")

db.commit()

cursor.execute("select * from customer")
for x in cursor.fetchall():
    print(x)










cursor.execute("""

CREATE TABLE IF NOT EXISTS bike_status(
                                id INTEGER,
                                time TEXT,
                                defective INTEGER,
                                FOREIGN KEY(id) REFERENCES bike(id)
                                )

""")


cursor.execute("""INSERT OR IGNORE into bike_status(id,time, defective)
values(10001, '2021-1-24 21:53:29',0)""")
cursor.execute("""INSERT OR IGNORE into bike_status(id,time, defective)
values(10002, '2021-1-24 21:53:29',0)""")
cursor.execute("""INSERT OR IGNORE into bike_status(id,time, defective)
values(10003, '2021-1-24 21:53:29',0)""")
cursor.execute("""INSERT OR IGNORE into bike_status(id,time, defective)
values(10004, '2021-1-24 21:53:29',0)""")
cursor.execute("""INSERT OR IGNORE into bike_status(id,time, defective)
values(10005, '2021-1-24 21:53:29',0)""")
cursor.execute("""INSERT OR IGNORE into bike_status(id,time, defective)
values(10006, '2021-1-24 21:53:29',0)""")
cursor.execute("""INSERT OR IGNORE into bike_status(id,time, defective)
values(10007, '2021-1-24 21:53:29',0)""")
cursor.execute("""INSERT OR IGNORE into bike_status(id,time, defective)
values(10008, '2021-1-24 21:53:29',0)""")
cursor.execute("""INSERT OR IGNORE into bike_status(id,time, defective)
values(10009, '2021-1-24 21:53:29',0)""")
cursor.execute("""INSERT OR IGNORE into bike_status(id,time, defective)
values(10010, '2021-1-24 21:53:29',0)""")
cursor.execute("""INSERT OR IGNORE into bike_status(id,time, defective)
values(10011, '2021-1-24 21:53:29',0)""")
cursor.execute("""INSERT OR IGNORE into bike_status(id,time, defective)
values(10012, '2021-1-24 21:53:29',0)""")
cursor.execute("""INSERT OR IGNORE into bike_status(id,time, defective)
values(10013, '2021-1-24 21:53:29',0)""")
cursor.execute("""INSERT OR IGNORE into bike_status(id,time, defective)
values(10014, '2021-1-24 21:53:29',0)""")
cursor.execute("""INSERT OR IGNORE into bike_status(id,time, defective)
values(10015, '2021-1-24 21:53:29',0)""")
cursor.execute("""INSERT OR IGNORE into bike_status(id,time, defective)
values(10016, '2021-1-24 21:53:29',0)""")
cursor.execute("""INSERT OR IGNORE into bike_status(id,time, defective)
values(10017, '2021-1-24 21:53:29',0)""")
cursor.execute("""INSERT OR IGNORE into bike_status(id,time, defective)
values(10018, '2021-1-24 21:53:29',0)""")
cursor.execute("""INSERT OR IGNORE into bike_status(id,time, defective)
values(10019, '2021-1-24 21:53:29',0)""")
cursor.execute("""INSERT OR IGNORE into bike_status(id,time, defective)
values(10020, '2021-1-24 21:53:29',0)""")

cursor.execute("select * from bike_status")
for x in cursor.fetchall():
    print(x)



cursor.execute("""

CREATE TABLE IF NOT EXISTS manager(
                                id INTEGER PRIMARY KEY,
                                user_name TEXT NOT NULL UNIQUE,
                                password TEXT NOT NULL
                                )

""")


cursor.execute("""INSERT OR IGNORE into manager(id,user_name, password)
values(30001, 'Tony', 'Tony')""")
cursor.execute("""INSERT OR IGNORE into manager(id,user_name, password)
values(30002, 'Jack', 'Jack')""")
cursor.execute("""INSERT OR IGNORE into manager(id,user_name, password)
values(30003, 'Lucy', 'Lucy')""")
cursor.execute("""INSERT OR IGNORE into manager(id,user_name, password)
values(30004, 'James', 'James')""")
cursor.execute("""INSERT OR IGNORE into manager(id,user_name, password)
values(30005, 'Martin', 'Martin')""")
cursor.execute("""INSERT OR IGNORE into manager(id,user_name, password)
values(30006, 'Diana', 'Diana')""")
cursor.execute("""INSERT OR IGNORE into manager(id,user_name, password)
values(30007, 'Judy', 'Judy')""")
cursor.execute("""INSERT OR IGNORE into manager(id,user_name, password) 
values(30008, 'Louis', 'Louis')""")
cursor.execute("""INSERT OR IGNORE into manager(id,user_name, password)
values(30009, 'Lisa', 'Lisa')""")
cursor.execute("""INSERT OR IGNORE into manager(id,user_name, password)
values(30010, 'Peter', 'Peter')""")
cursor.execute("""INSERT OR IGNORE into manager(id,user_name, password)
values(30011, 'Mary', 'Mary')""")
cursor.execute("""INSERT OR IGNORE into manager(id,user_name, password)
values(30012, 'Joy', 'Joy')""")
cursor.execute("""INSERT OR IGNORE into manager(id,user_name, password)
values(30013, 'Vivian', 'Vivian')""")
cursor.execute("""INSERT OR IGNORE into manager(id,user_name, password)
values(30014, 'Mark', 'Mark')""")
cursor.execute("""INSERT OR IGNORE into manager(id,user_name, password)
values(30015, 'Kate', 'Kate')""")
cursor.execute("""INSERT OR IGNORE into manager(id,user_name, password)
values(30016, 'Poul', 'Poul')""")
cursor.execute("""INSERT OR IGNORE into manager(id,user_name, password)
values(30017, 'Allen', 'Allen')""")
cursor.execute("""INSERT OR IGNORE into manager(id,user_name, password)
values(30018, 'Fiona', 'Fiona')""")
cursor.execute("""INSERT OR IGNORE into manager(id,user_name, password)
values(30019, 'May', 'May')""")
cursor.execute("""INSERT OR IGNORE into manager(id,user_name, password)
values(30020, 'Julie', 'Julie')""")



cursor.execute("select * from manager")
for x in cursor.fetchall():
    print(x)






cursor.execute("""

CREATE TABLE IF NOT EXISTS operator(
                                id INTEGER PRIMARY KEY,
                                user_name TEXT NOT NULL UNIQUE,
                                password TEXT NOT NULL
                                )

""")

cursor.execute("""INSERT OR IGNORE into operator(id,user_name, password)
values(40001, 'Tom', 'Tom')""")
cursor.execute("""INSERT OR IGNORE into operator(id,user_name, password)
values(40002, 'Tom', 'Tom')""")
cursor.execute("""INSERT OR IGNORE into operator(id,user_name, password)
values(40003, 'Bob', 'Bob')""")
cursor.execute("""INSERT OR IGNORE into operator(id,user_name, password)
values(40004, 'John', 'John')""")
cursor.execute("""INSERT OR IGNORE into operator(id,user_name, password)
values(40005, 'May', 'May')""")
cursor.execute("""INSERT OR IGNORE into operator(id,user_name, password)
values(40006, 'Helen', 'Helen')""")
cursor.execute("""INSERT OR IGNORE into operator(id,user_name, password)
values(40007, 'Jan', 'Jan')""")
cursor.execute("""INSERT OR IGNORE into operator(id,user_name, password)
values(40008, 'Charles', 'Charles')""")
cursor.execute("""INSERT OR IGNORE into operator(id,user_name, password)
values(40009, 'Linda', 'Linda')""")
cursor.execute("""INSERT OR IGNORE into operator(id,user_name, password)
values(40010, 'Lee', 'Lee')""")


cursor.execute("select * from operator")
for x in cursor.fetchall():
    print(x)



cursor.execute("""

CREATE TABLE IF NOT EXISTS movement(
                                bike_id INTEGER NOT NULL,
                                usr_id INTEGER NOT NULL,
                                distance REAL,
                                time INTEGER,
                                FOREIGN KEY(bike_id) REFERENCES bike(id),
                                FOREIGN KEY(usr_id) REFERENCES customer(id)
                                )

""")

cursor.execute("""INSERT OR IGNORE into movement(bike_id,usr_id, distance, time)
values(10001, 20001, 0.00, 0)""")
cursor.execute("""INSERT OR IGNORE into movement(bike_id,usr_id, distance, time)
values(10002, 20002, 0.00, 0)""")
cursor.execute("""INSERT OR IGNORE into movement(bike_id,usr_id, distance, time)
values(10003, 20003, 0.00, 0)""")
cursor.execute("""INSERT OR IGNORE into movement(bike_id,usr_id, distance, time)
values(10004, 20004, 0.00, 0)""")
cursor.execute("""INSERT OR IGNORE into movement(bike_id,usr_id, distance, time)
values(10005, 20005, 0.00, 0)""")
cursor.execute("""INSERT OR IGNORE into movement(bike_id,usr_id, distance, time)
values(10006, 20006, 0.00, 0)""")
cursor.execute("""INSERT OR IGNORE into movement(bike_id,usr_id, distance, time)
values(10007, 20007, 0.00, 0)""")
cursor.execute("""INSERT OR IGNORE into movement(bike_id,usr_id, distance, time)
values(10008, 20008, 0.00, 0)""")
cursor.execute("""INSERT OR IGNORE into movement(bike_id,usr_id, distance, time)
values(10009, 20009, 0.00, 0)""")
cursor.execute("""INSERT OR IGNORE into movement(bike_id,usr_id, distance, time)
values(10010, 20010, 0.00, 0)""")
cursor.execute("""INSERT OR IGNORE into movement(bike_id,usr_id, distance, time)
values(10011, 20011, 0.00, 0)""")
cursor.execute("""INSERT OR IGNORE into movement(bike_id,usr_id, distance, time)
values(10012, 20012, 0.00, 0)""")
cursor.execute("""INSERT OR IGNORE into movement(bike_id,usr_id, distance, time)
values(10013, 20013, 0.00, 0)""")
cursor.execute("""INSERT OR IGNORE into movement(bike_id,usr_id, distance, time)
values(10014, 20014, 0.00, 0)""")
cursor.execute("""INSERT OR IGNORE into movement(bike_id,usr_id, distance, time)
values(10015, 20015, 0.00, 0)""")
cursor.execute("""INSERT OR IGNORE into movement(bike_id,usr_id, distance, time)
values(10016, 20016, 0.00, 0)""")
cursor.execute("""INSERT OR IGNORE into movement(bike_id,usr_id, distance, time)
values(10017, 20017, 0.00, 0)""")
cursor.execute("""INSERT OR IGNORE into movement(bike_id,usr_id, distance, time)
values(10018, 20018, 0.00, 0)""")
cursor.execute("""INSERT OR IGNORE into movement(bike_id,usr_id, distance, time)
values(10019, 20019, 0.00, 0)""")
cursor.execute("""INSERT OR IGNORE into movement(bike_id,usr_id, distance, time)
values(10020, 20020, 0.00, 0)""")

cursor.execute("select * from movement")
for x in cursor.fetchall():
    print(x)


cursor.close()
db.close()