import sqlite3

import numpy as np

from bss.conf import attrs
from bss.temp.customer.customer import Customer  # TODO
from bss.data import db_path as db


class Mapping:
	'''
	The class for defining the mapping array.
	'''

	def __init__(self, customer = None) -> None:
		'''
		The constructor of the class for defining the mapping array.

		Parameters
		----------
		customer : the customer represented in the mapping array
		'''

		self.__map_array = np.full((attrs.MAP_LENGTH, attrs.MAP_LENGTH), attrs.EMPTY_CELL_CODE)
		self.__customer = customer
		self.__refresh()

	def __refresh(self) -> None:
		'''
		Refresh the mapping array.
		'''

		new_map_array = np.full((attrs.MAP_LENGTH, attrs.MAP_LENGTH), attrs.EMPTY_CELL_CODE)
		conn = sqlite3.connect(db.get_db_path())
		c = conn.cursor()

		# Keep the query order to ensure any display priority.
		# Set the defective code to the specified map element.
		c.execute("SELECT location_row FROM bike where defective>=:threshold", {'threshold': attrs.DEFECTIVE_BIKE_THRESHOLD})
		rows = c.fetchall()
		c.execute("SELECT location_col FROM bike where defective>=:threshold", {'threshold': attrs.DEFECTIVE_BIKE_THRESHOLD})
		cols = c.fetchall()

		for i, j in zip(rows, cols):
			new_map_array[i, j] = attrs.DEFECTIVE_BIKE_CODE

		# Set the busy code to the specified map element.
		c.execute("SELECT location_row FROM bike where defective<:threshold and is_being_used=:status", {'threshold': attrs.DEFECTIVE_BIKE_THRESHOLD, 'status': attrs.BUSY_BIKE_CODE})
		rows = c.fetchall()
		c.execute("SELECT location_col FROM bike where defective<:threshold and is_being_used=:status", {'threshold': attrs.DEFECTIVE_BIKE_THRESHOLD, 'status': attrs.BUSY_BIKE_CODE})
		cols = c.fetchall()

		for i, j in zip(rows, cols):
			new_map_array[i, j] = attrs.BUSY_BIKE_CODE

		# Set the available code to the specified map element.
		c.execute("SELECT location_row FROM bike where defective<:threshold and is_being_used=:status", {'threshold': attrs.DEFECTIVE_BIKE_THRESHOLD, 'status': attrs.AVAILABLE_BIKE_CODE})
		rows = c.fetchall()
		c.execute("SELECT location_col FROM bike where defective<:threshold and is_being_used=:status", {'threshold': attrs.DEFECTIVE_BIKE_THRESHOLD, 'status': attrs.AVAILABLE_BIKE_CODE})
		cols = c.fetchall()

		for i, j in zip(rows, cols):
			new_map_array[i, j] = attrs.AVAILABLE_BIKE_CODE

		# Set the avatar code to the specified map element.
		if self.__customer is not None and isinstance(self.__customer, Customer):
			location = self.__customer.get_location()
			new_map_array[location[0], location[1]] = attrs.AVATAR_CODE

		conn.close()
		self.__map_array = new_map_array

	def get_state(self, refresh = False):
		'''
		Get the mapping array. Refresh it if required.

		Parameters
		----------
		refresh : a flag indicating if the mapping array should be refreshed

		Returns
		-------
		map_array : the mapping array
		'''

		if refresh:
			self.__refresh()

		return self.__map_array

	def get_square_val(self, location):
		return self.__map_array[location[0], location[1]]

	def set_state(self, location, value) -> bool:
		'''
		Set a specified code to the specified element of the mapping array.

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