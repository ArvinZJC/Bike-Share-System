import sqlite3

from bss.data import db_path as db


class Manager:

    def __init__(self, Id, name, password):
        self.Id = Id
        self.name = name
        self.password = password
        self.riding = False
        self.__db_path = db.get_db_path()