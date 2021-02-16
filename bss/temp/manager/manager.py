import sqlite3

from bss.data.db_path import get_db_path


class Manager:

    def __init__(self, Id, name, password):
        self.Id = Id
        self.name = name
        self.password = password
        self.riding = False
        self.__db_path = get_db_path()