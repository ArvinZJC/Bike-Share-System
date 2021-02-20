import sqlite3
import random

from bss.conf import attrs
from bss.data import db_path as db


class Bike:
	'''
	The class for defining a bike.
	'''

	def __init__(self, bike_id, defective, location, is_being_used) -> None:
		'''
		The constructor of the class for defining a bike.

		Parameters
		----------
		bike_id : the ID of a bike
		defective : a value representing the bike status
		location : a specified location
		is_being_used : a flag indicating if a bike is available
		'''

		self.__Id = bike_id
		self.__location = location
		self.__defective = defective
		self.__db_path = db.get_db_path()
		self.__is_being_used = is_being_used
		self.__distance = 0
		self.__extra_time = 0

	def print_nice(self):
		print("Bike Id: ",self.__Id),
		print("%% defective: ",self.__defective)

	def print_details(self):
		print("Bike Id: ",self.__Id),
		print("%% defective: ",self.__defective),
		print("Location: ",self.__location)

	def get_defective(self):
		return self.__defective

	def is_defective(self):
		return self.__defective>0.9

	def set_defective(self):
		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		if self.__defective==1:
			self.__defective = 0
			c.execute("UPDATE bike set defective=0 where id=:Id",{'Id':self.get_id()})
		
		else:
			self.__defective = 1
			c.execute("UPDATE bike set defective=1 where id=:Id",{'Id':self.get_id()})

		conn.commit()
		conn.close()

	def get_is_being_used(self):
		return self.__is_being_used
		
	def set_is_being_used(self) -> None:
		'''
		Set the using status of a bike.
		'''

		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		self.__is_being_used = attrs.AVAILABLE_BIKE_CODE if self.__is_being_used == attrs.BUSY_BIKE_CODE else attrs.BUSY_BIKE_CODE
		self.__distance = 0
		self.__extra_time = 0
		c.execute("UPDATE bike set is_being_used=:status where id=:Id", {'status': self.__is_being_used, 'Id': self.__Id})
		conn.commit()
		conn.close()

	def get_distance(self) -> int:
		'''
		Distance getter.

		Returns
		-------
		distance : the riding distance
		'''

		return self.__distance

	def add_distance(self) -> None:
		'''
		Add 1 to the riding distance.
		'''

		self.__distance += 1

	def get_extra_time(self) -> float:
		'''
		Extra time getter.

		Returns
		-------
		extra_time : the extra time
		'''

		return self.__extra_time

	def add_extra_time(self) -> None:
		'''
		Add a random value to the extra time.
		'''

		self.__extra_time += random.randint(3, 5) * random.randint(50, 60) * max(0.5, (1 - self.get_defective()))

	def get_location(self):
		return self.__location

	def set_location(self, location,operator=1):
		self.__location = location
		self.__defective+=round(random.uniform(0.01,0.05),2)
		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		c.execute("UPDATE bike set location_row =:location_row, location_col=:location_col,defective=:value where id=:Id",
				  {'location_row': location[0], 'location_col': location[1],'value':self.__defective, 'Id': self.__Id})
		conn.commit()
		conn.close()

	def get_id(self):
		return self.__Id

	def move(self, direction, map):
		location = self.get_location()

		og_val = map.get_square_val(location)
		if direction == 'up':
			if location[0]>0:
				map.set_state(location, og_val - 1)
				location[0] -= 1
				self.set_location(location)
				map.set_state(location, map.get_square_val(location) + 1)

		elif direction == 'down':
			if location[0]<19:
				map.set_state(location, og_val - 1)
				location[0] += 1
				self.set_location(location)
				map.set_state(location, map.get_square_val(location) + 1)

		elif direction == 'left':
			if location[1]>0:
				map.set_state(location, og_val - 1)
				location[1] -= 1
				self.set_location(location)
				map.set_state(location, map.get_square_val(location) + 1)

		else:
			if location[1]<19:
				map.set_state(location, og_val - 1)
				location[1] += 1
				self.set_location(location)
				map.set_state(location, map.get_square_val(location) + 1)