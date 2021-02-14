import sqlite3
from bike import *
import time

class OperatorWorker:

	def __init__(self, Id, name, password,balance,skill_level):
		self.Id = Id
		self.name = name
		self.password = password
		self.balance = balance
		self.skill_level = skill_level
		self.__db_path = 'data/' + attrs.DB_FILENAME

	def print_nice(self):
		print("Name: ",self.name),
		print("Id: ",self.Id),
		print("Skill Level: ",self.skill_level)
		print("Balance: ",self.balance)

	def get_skill_level(self):
		return self.skill_level

	def get_id(self):
		return self.Id

	def track_bikes(self):
		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		c.execute("SELECT * FROM bike")

		bikes = c.fetchall()

		for i in bikes:
			Bike(i[0],i[1],[i[2],i[3]],i[4]).print_details()

		conn.close()

		return bikes

	def repair_bikes(self):
		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		c.execute("SELECT * FROM bike where defective=1")

		bikes = c.fetchall()
		print("Choose which bike to fix from the following: ")
		bike_ids = []
		for i in bikes:
			bike_ids.append(i[0])
			
		print(bike_ids)
		while True:
			to_fix = int(input("\n"))
			if to_fix in bike_ids:
				break
			else:
				print("Invalid id for bike.Try again.")

		c.execute("SELECT * FROM bike where id=:Id",{'Id':to_fix})
		i = c.fetchone()
		to_repair = Bike(i[0],i[1],[i[2],i[3]],i[4])
		c.execute("SELECT defective_start,time_of_event from bike_status where id=:Id",{'Id':to_repair.get_id()})
		rows = c.fetchall()
		how_broken = rows[0][0]
		timeBegin = rows[0][1]
		conn.commit()
		print("Fixing.....")
		timeToFix = (60/self.skill_level)*how_broken
		time.sleep(timeToFix)
		timeToFix = timeToFix*10*self.skill_level
		conn.close()
		to_repair.set_defective()
		timeOfFix = time.strftime("%b %d %Y %H:%M:%S",time.gmtime(time.time()))

		if (time.time()+timeToFix)<time.mktime(time.strptime(timeBegin,"%b %d %Y %H:%M:%S")):
			timeOfFix = time.strftime("%b %d %Y %H:%M:%S",time.gmtime(time.mktime(time.strptime(timeBegin,"%b %d %Y %H:%M:%S"))+timeToFix))

		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()

		c.execute("INSERT INTO bike_status (id,time_of_event,defective_start,defective_end) VALUES ({},'{}',{},{})".format(to_repair.get_id(),
																										timeOfFix,1,0))
		conn.commit()
		conn.close()
		return [timeToFix/20,timeOfFix]

	def move_bikes(self):
		conn = sqlite3.connect(self.__db_path)
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
				if (location_row>19 or location_row<0) or (location_col<0 or location_row>19):
					raise SystemError
				break
			except:
				print('Invalid location. Try again.')

		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		c.execute("UPDATE bike set location_row =:location_row, location_col=:location_col where id=:Id",
				  {'location_row': location_row, 'location_col': location_col, 'Id': to_move})
		conn.commit()
		conn.close()


	def set_balance(self,money):
		self.balance += money
		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		c.execute("UPDATE operator set account=:sum where id=:Id",{'sum':self.balance,'Id':self.Id})
		conn.commit()
		conn.close()




	