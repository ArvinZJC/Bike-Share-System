import sqlite3
from bike import *

class OperatorWorker:

	def __init__(self, Id, name, password):
		self.Id = Id
		self.name = name
		self.password = password

	def track_bikes(self):
		conn = sqlite3.connect('data/TEAM_PJT.db')
		c = conn.cursor()
		c.execute("SELECT * FROM bike")

		bikes = c.fetchall()

		for i in bikes:
			Bike(i[0],i[1],[i[2],i[3]]).print_details()

		conn.close()

		return bikes

	def repair_bikes(self):
		conn = sqlite3.connect('data/TEAM_PJT.db')
		c = conn.cursor()
		c.execute("SELECT * FROM bike where defective>=0.9")

		bikes = c.fetchall()

		for i in bikes:
			to_repair = Bike(i[0],i[1],[i[2],i[3]])
			to_repair.set_defective()
			c.execute("UPDATE bike set defective=:defective where id=:Id",{'defective':to_repair.get_defective(),'Id':to_repair.get_id()})
			conn.commit()

		conn.close()

	def move_bikes(self):
		conn = sqlite3.connect('data/TEAM_PJT.db')
		c = conn.cursor()
		c.execute("SELECT id,location_row,location_col FROM bike")

		bikes = c.fetchall()

		ids = []
		locs = []

		for i in bikes:
			ids.append(i[0])
			locs.append([i[1],i[2]])
			print(i[0],'\t',i[1],",",i[2])

		while True:
			try:
				to_move = int(input("Choose a bike (by id) to move: "))
				if to_move not in ids:
					raise SystemError
				break
			except:
				print('Invalid. Try again. Choose from: \n',ids)

		while True:
			try:
				location_row,location_col = [int(x) for x in input("Give row & col to move the bike: ").split()]
				if (location_row>19 or location_row<0) and (location_col<0 or location_row>19):
					raise SystemError
				break
			except:
				print('Invalid location. Try again.')

		conn = sqlite3.connect('data/TEAM_PJT.db')
		c = conn.cursor()
		c.execute("UPDATE bike set location_row =:location_row, location_col=:location_col where id=:Id",
				  {'location_row': location_row, 'location_col': location_col, 'Id': to_move})
		conn.commit()
		conn.close()




	