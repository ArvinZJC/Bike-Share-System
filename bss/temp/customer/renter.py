import sqlite3

from bss.temp.bike import Bike  # TODO
from bss.conf import attrs
from bss.data import db_path as db


def check_bikes(location_list: list, bike_code = attrs.AVAILABLE_BIKE_CODE) -> list:
	'''
	Check if there is any available/busy/defective bike in a specified location.

	Parameters
	----------
	location_list : a specified location; by default, available bikes
	bike_code : a code indicating a type of bike to check

	Returns
	-------
	bike_ids : a list of ID of bikes found
	'''

	conn = sqlite3.connect(db.get_db_path())
	c = conn.cursor()

	if bike_code == attrs.AVAILABLE_BIKE_CODE:
		c.execute(
			"SELECT id from bike where location_row=:location_row and location_col=:location_col and defective<:threshold and is_being_used=:status",
			{'location_row': location_list[0], 'location_col': location_list[1], 'threshold': attrs.DEFECTIVE_BIKE_THRESHOLD, 'status': attrs.AVAILABLE_BIKE_CODE})
	elif bike_code == attrs.BUSY_BIKE_CODE:
		c.execute(
			"SELECT id from bike where location_row=:location_row and location_col=:location_col and defective<:threshold and is_being_used=:status",
			{'location_row': location_list[0], 'location_col': location_list[1], 'threshold': attrs.DEFECTIVE_BIKE_THRESHOLD, 'status': attrs.BUSY_BIKE_CODE})
	else:
		c.execute(
			"SELECT id from bike where location_row=:location_row and location_col=:location_col and defective>=:threshold",
			{'location_row': location_list[0], 'location_col': location_list[1], 'threshold': attrs.DEFECTIVE_BIKE_THRESHOLD})

	bike_ids = c.fetchall()
	conn.close()
	return bike_ids


def renting(location_list: list):
	bike_ids = check_bikes(location_list)
	if len(bike_ids) == 0:
		return False

	answer = input("Do you want to rent a bike? ")
	if answer == "yes":
		if len(bike_ids)==1:
			conn = sqlite3.connect(db.get_db_path())
			c = conn.cursor()
			c.execute("SELECT * FROM bike where id=:Id", {'Id': bike_ids[0][0]})
			bike_details = c.fetchall()
			rented_bike = Bike(bike_ids[0][0], bike_details[0][1], [bike_details[0][2], bike_details[0][3]],bike_details[0][4])
			rented_bike.set_is_being_used()
			conn.close()

		else:
			ids = []
			for i in bike_ids:
				ids.append(i[0])
			print(ids)
			rented_id = int(input("Select one of the following: "))
			conn = sqlite3.connect(db.get_db_path())
			c = conn.cursor()
			c.execute("SELECT * FROM bike where id=:Id", {'Id': rented_id})
			bike_details = c.fetchall()
			rented_bike = Bike(rented_id, bike_details[0][1], [bike_details[0][2], bike_details[0][3]],bike_details[0][4])
			conn.close()

		return rented_bike

	else:
		return False