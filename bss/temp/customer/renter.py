import sqlite3

import numpy as np

from bss.temp.bike import Bike  # TODO
from bss.conf import attrs
from bss.data import db_path as db


def check_bikes(location: list, bike_code = attrs.AVAILABLE_BIKE_CODE) -> list:
	'''
	Check if there is any available/busy/defective bike in a specified location.

	Parameters
	----------
	location : a specified location; by default, available bikes
	bike_code : a code indicating a type of bike to check

	Returns
	-------
	bike_ids : a list of ID of bikes found
	'''

	conn = sqlite3.connect(db.get_db_path())
	c = conn.cursor()

	if bike_code == attrs.AVAILABLE_BIKE_CODE:
		c.execute(
			'SELECT id from bike where location_row=:location_row and location_col=:location_col and defective<:threshold and is_being_used=:status',
			{'location_row': location[0], 'location_col': location[1], 'threshold': attrs.DEFECTIVE_BIKE_THRESHOLD, 'status': attrs.AVAILABLE_BIKE_CODE})
	elif bike_code == attrs.BUSY_BIKE_CODE:  # TODO: consider removing this part if it is not used by operators or managers
		c.execute(
			'SELECT id from bike where location_row=:location_row and location_col=:location_col and defective<:threshold and is_being_used=:status',
			{'location_row': location[0], 'location_col': location[1], 'threshold': attrs.DEFECTIVE_BIKE_THRESHOLD, 'status': attrs.BUSY_BIKE_CODE})
	else:
		c.execute(
			'SELECT id from bike where location_row=:location_row and location_col=:location_col and defective>=:threshold',
			{'location_row': location[0], 'location_col': location[1], 'threshold': attrs.DEFECTIVE_BIKE_THRESHOLD})

	bike_ids = c.fetchall()
	conn.close()
	return bike_ids


def get_closest_bike(location):
	'''
	Get the ID(s) of available bikes at a specified location or a guide to get to the closest available bikes.

	Parameters
	----------
	location : a specified location

	Returns
	-------
	bike_ids / s : a list of ID(s) of available bikes at a specified location, or a guide to get to the closest available bikes
	'''

	conn = sqlite3.connect(db.get_db_path())
	c = conn.cursor()
	c.execute('SELECT location_row,location_col FROM bike where defective<:threshold and is_being_used=:status', {'threshold': attrs.DEFECTIVE_BIKE_THRESHOLD, 'status': attrs.AVAILABLE_BIKE_CODE})
	distance = np.inf
	row = -1
	col = -1

	for i, j in c.fetchall():
		temp_distance = abs(i - location[0]) + abs(j - location[1])

		if temp_distance < distance:
			distance = temp_distance
			row = i
			col = j

	if row == location[0] and col == location[1]:
		return check_bikes(location)
	else:
		s = 'Oops! No available bike here. You are suggested to:\n'

		if row < location[0]:
			s += 'Go ' + str(location[0] - row) + ' UP. '
		else:
			s += 'Go ' + str(row - location[0]) + ' DOWN. '

		if col < location[1]:
			s += 'Go ' + str(location[1] - col) + ' LEFT.'
		else:
			s += 'Go ' + str(col - location[1]) + ' RIGHT.'

		return s


def renting(bike_id: int, location: list):
	'''
	Attempt to pick up a specified bike at a specified location.

	Parameters
	----------
	bike_id : the ID of a bike
	location : a specified location

	Returns
	-------
	rented_bike : a `Bike` object or `None`
	'''

	conn = sqlite3.connect(db.get_db_path())
	c = conn.cursor()
	c.execute("SELECT * FROM bike where id=:Id", {'Id': bike_id})
	bike_details = c.fetchall()
	rented_bike = None

	# A simplified way to recheck if the bike is still available here.
	if bike_details[0][2] == location[0] and bike_details[0][3] == location[1] and bike_details[0][4] == attrs.AVAILABLE_BIKE_CODE:
		rented_bike = Bike(bike_id, bike_details[0][1], [bike_details[0][2], bike_details[0][3]], bike_details[0][4])
		rented_bike.set_is_being_used()
		conn.close()

	return rented_bike