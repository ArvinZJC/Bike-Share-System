import sqlite3


class Manager:

	def __init__(self, Id, name, password):
		self.Id = Id
		self.name = name
		self.password = password