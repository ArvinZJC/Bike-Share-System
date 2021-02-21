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

	def get_defective(self) -> float:
		'''
		Defective level getter.

		Returns
		-------
		defective : a defective level of a bike
		'''

		return self.__defective

	def is_defective(self) -> bool:
		'''
		Check if a bike is defective or needs overhauling.

		Returns
		-------
		is_defective : `True` if a bike is defective; otherwise, `False`
		'''

		return self.__defective >= attrs.DEFECTIVE_BIKE_THRESHOLD

	def set_defective(self, location: list, defective: float) -> None:
		'''
		Defective level setter.

		Parameters
		----------
		location : the location of a bike
		defective : a defective level of a bike
		'''

		if attrs.BIKE_DAMAGE_MIN <= defective <= attrs.BIKE_DAMAGE_MAX:
			self.__defective = defective
			conn = sqlite3.connect(self.__db_path)
			c = conn.cursor()
			c.execute(
				"UPDATE bike set location_row =:location_row, location_col=:location_col, defective=:value where id=:Id",
				{'location_row': location[0], 'location_col': location[1], 'value': self.__defective, 'Id': self.__Id})
			conn.commit()
			conn.close()

	def get_is_being_used(self):  # TODO
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

	def get_location(self) -> list:
		'''
		Location getter.

		Returns
		-------
		location : a specified location
		'''

		return self.__location

	def set_location(self, location, is_operator = False) -> None:
		'''
		Move a bike to a location.

		Parameters
		----------
		location : a specified location
		is_operator : a flag indicating if a bike is moved by an operator
		'''

		self.__location = location

		if not is_operator:
			self.__defective += round(random.uniform(0.01, 0.05), 2)
			self.__defective = attrs.BIKE_DAMAGE_MAX if self.__defective > attrs.BIKE_DAMAGE_MAX else self.__defective

		self.set_defective(location, self.__defective)

	def get_id(self) -> int:
		'''
		Get the ID of a bike.

		Returns
		-------
		Id : the ID of a bike
		'''

		return self.__Id