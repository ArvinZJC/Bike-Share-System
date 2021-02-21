import sqlite3

import numpy as np

from bss.conf import attrs
from bss.temp.customer.customer import Customer  # TODO
from bss.data import db_path as db


class Mapping:
	'''
	The class for defining the map array.
	'''

	def __init__(self, user) -> None:
		'''
		The constructor of the class for defining the map array.

		Parameters
		----------
		user : a `Customer` or `OperatorWorker` object
		'''

		self.__user = user
		self.__map_array = self.download()

	def download(self):
		'''
		Retrieve the data source to create a map array.

		Returns
		-------
		map_array : a new map array
		'''

		map_array = np.full((attrs.MAP_LENGTH, attrs.MAP_LENGTH), attrs.EMPTY_CELL_CODE)
		conn = sqlite3.connect(db.get_db_path())
		c = conn.cursor()

		# Available bikes have more priority than defective bikes for a customer.
		if isinstance(self.__user, Customer):
			# Set the defective bike code to the specified map element.
			c.execute('SELECT location_row FROM bike where defective>=:threshold', {'threshold': attrs.DEFECTIVE_BIKE_THRESHOLD})
			rows = c.fetchall()
			c.execute('SELECT location_col FROM bike where defective>=:threshold', {'threshold': attrs.DEFECTIVE_BIKE_THRESHOLD})
			cols = c.fetchall()

			for i, j in zip(rows, cols):
				map_array[i, j] = attrs.DEFECTIVE_BIKE_CODE

			# Set the available bike code to the specified map element.
			c.execute('SELECT location_row FROM bike where defective<:threshold and is_being_used=:status', {'threshold': attrs.DEFECTIVE_BIKE_THRESHOLD, 'status': attrs.AVAILABLE_BIKE_CODE})
			rows = c.fetchall()
			c.execute('SELECT location_col FROM bike where defective<:threshold and is_being_used=:status', {'threshold': attrs.DEFECTIVE_BIKE_THRESHOLD, 'status': attrs.AVAILABLE_BIKE_CODE})
			cols = c.fetchall()

			for i, j in zip(rows, cols):
				map_array[i, j] = attrs.AVAILABLE_BIKE_CODE
		else:
			# Set the available bike code to the specified map element.
			c.execute('SELECT location_row FROM bike where defective<:threshold and is_being_used=:status', {'threshold': attrs.DEFECTIVE_BIKE_THRESHOLD, 'status': attrs.AVAILABLE_BIKE_CODE})
			rows = c.fetchall()
			c.execute('SELECT location_col FROM bike where defective<:threshold and is_being_used=:status', {'threshold': attrs.DEFECTIVE_BIKE_THRESHOLD, 'status': attrs.AVAILABLE_BIKE_CODE})
			cols = c.fetchall()

			for i, j in zip(rows, cols):
				map_array[i, j] = attrs.AVAILABLE_BIKE_CODE

			# Set the defective bike code to the specified map element.
			c.execute('SELECT location_row FROM bike where defective>=:threshold', {'threshold': attrs.DEFECTIVE_BIKE_THRESHOLD})
			rows = c.fetchall()
			c.execute('SELECT location_col FROM bike where defective>=:threshold', {'threshold': attrs.DEFECTIVE_BIKE_THRESHOLD})
			cols = c.fetchall()

			for i, j in zip(rows, cols):
				map_array[i, j] = attrs.DEFECTIVE_BIKE_CODE

		# Set the avatar code to the specified map element.
		location = self.__user.get_location()
		map_array[location[0], location[1]] = attrs.AVATAR_CODE

		conn.close()
		return map_array

	def get_state(self):
		'''
		Map array getter.

		Returns
		-------
		map_array : a map array
		'''

		return self.__map_array

	def set_map_array(self, map_array) -> None:
		'''
		Map array setter.
		Parameters
		----------
		map_array : a map array
		'''

		self.__map_array = map_array

	def set_state(self, location, value) -> bool:
		'''
		Set a specified code to the specified element of the map array.

		Parameters
		----------
		location : the location of the specified element
		value : a specified code

		Returns
		-------
		succeed : `True` if the change is applied; otherwise, `False`
		'''

		if 0 <= location[0] < attrs.MAP_LENGTH and 0 <= location[1] < attrs.MAP_LENGTH:
			self.__map_array[location[0], location[1]] = value
			return True
		else:
			return False