import sys
import sqlite3

import numpy as np

from conf import attrs


class Mapping:

	def __init__(self):
		self.map_array = np.zeros((20, 20))
		conn = sqlite3.connect('data/' + attrs.DB_FILENAME)
		c = conn.cursor()

		c.execute("SELECT location_row FROM bike where defective<0.9")
		rows = c.fetchall()
		c.execute("SELECT location_col FROM bike where defective<0.9")
		cols = c.fetchall()
		for i, j in zip(rows, cols):
			self.map_array[i, j] += 1

		c.execute("SELECT location_row FROM customer")
		rows = c.fetchall()
		c.execute("SELECT location_col FROM customer")
		cols = c.fetchall()
		for i, j in zip(rows, cols):
			self.map_array[i, j] += 100

		conn.close()

	def get_state(self):
		self.map_array = np.zeros((20, 20))
		conn = sqlite3.connect('data/' + attrs.DB_FILENAME)
		c = conn.cursor()

		c.execute("SELECT location_row FROM bike where defective<0.9")
		rows = c.fetchall()
		c.execute("SELECT location_col FROM bike where defective<0.9")
		cols = c.fetchall()
		for i, j in zip(rows, cols):
			self.map_array[i, j] += 1

		c.execute("SELECT location_row FROM customer")
		rows = c.fetchall()
		c.execute("SELECT location_col FROM customer")
		cols = c.fetchall()
		for i, j in zip(rows, cols):
			self.map_array[i, j] += 100

		conn.close()
		return self.map_array

	def get_square_val(self, location):
		return self.map_array[location[0], location[1]]

	def set_state(self, location, value):
		map_array = self.get_state()
		try:
			map_array[location[0], location[1]] = value
		except Exception as e:
			sys.exit(sys.exc_info()[0])

		self.map_array = map_array

	def print_nice(self):
		for i in range(20):
			for j in range(20):
				#print("row:", i," col: ",j),
				print(self.get_square_val([i, j]), end="\t"),
			print("\n")



