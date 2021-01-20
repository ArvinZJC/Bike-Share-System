import sys
import numpy as np
import sqlite3

class Mapping():

	def __init__(self):
		self.map_array = np.zeros((20,20))
		conn = sqlite3.connect('TEAM_PJT.db')
		c = conn.cursor()

		c.execute("SELECT location_row FROM bike")
		rows = c.fetchall()
		c.execute("SELECT location_col FROM bike")
		cols = c.fetchall()
		for i,j in zip(rows,cols):
			self.map_array[i,j]+=1

		c.execute("SELECT location_row FROM customer")
		rows = c.fetchall()
		c.execute("SELECT location_col FROM customer")
		cols = c.fetchall()
		for i,j in zip(rows,cols):
			self.map_array[i,j]+=100

		conn.close()


	def get_state(self):
		return self.map_array

	def get_square_val(self,location):
		return self.map_array[location[0],location[1]]

	def set_state(self,location,value):
		map_array = self.get_state()
		try:
			map_array[location[0],location[1]]= value
		except Exception as e:
			sys.Exit(sys.exc_info()[0])

		self.map_array = map_array

	def print_nice(self):
		for i in range(20):
			for j in range(20):
				print(self.get_square_val([i,j]),end="\t"),
			print("\n")








