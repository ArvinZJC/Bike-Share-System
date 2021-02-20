import sqlite3
import time

import numpy as np

from bss.temp.bike import Bike  # TODO
from bss.temp.companys_pocket import CentralBank  # TODO
from bss.conf import attrs
from bss.temp.customer.customer import Customer  # TODO
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
	bike_ids : a list of bikes found
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

	bikes = c.fetchall()
	conn.close()
	return bikes


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


def calculate_charge(ride_time) -> float:
	'''
	Calculate the charge of a ride.

	Parameters
	----------
	ride_time : the time for calculating the fee

	Returns
	-------
	amount : the amount of money for the ride
	'''

	return round(float(ride_time) / 60, 2) * 0.5


def drop_bike(customer: Customer, rented_bike: Bike):
	'''
	Do something after the customer selects dropping a bike.

	Parameters
	----------
	customer : a `Customer` object representing a customer
	rented_bike : a `Bike` object representing the bike dropped

	Returns
	-------
	customer : a `Customer` object
	rented_bike : a `Bike` object
	transaction_date : the date of a transaction
	'''

	customer.is_using_bike(False)
	extra_time = rented_bike.get_extra_time()
	amount = customer.charge(extra_time)
	duration = time.strftime('%H:%M:%S', time.gmtime(extra_time))
	transaction_date = time.strftime('%b %d %Y %H:%M:%S', time.gmtime(time.time()))
	conn = sqlite3.connect(db.get_db_path())
	c = conn.cursor()
	c.execute("INSERT INTO movement(bike_id,user_id,distance,duration,startTime) VALUES({},{},{},'{}','{}')".format(rented_bike.get_id(), customer.get_id(), rented_bike.get_distance(), duration, transaction_date))
	conn.commit()
	conn.close()
	rented_bike.set_is_being_used()
	CentralBank().track_changes(amount, transaction_date)
	return customer, rented_bike, transaction_date


def report_break(bike: Bike, report_time: str) -> None:
	'''
	Set the defective status to a bike usually when a bike needs overhauling.

	Parameters
	----------
	bike : a defective bike
	report_time : time that a bike is reported defective
	'''

	if not bike.is_defective():
		bike.set_defective(bike.get_location(), attrs.BIKE_DAMAGE_MAX)

	conn = sqlite3.connect(db.get_db_path())
	c = conn.cursor()
	c.execute("INSERT INTO bike_status(id,time_of_event,defective_start,defective_end) VALUES({},'{}',{},{})".format(bike.get_id(), report_time, bike.get_defective(), attrs.BIKE_DAMAGE_MAX))
	conn.commit()
	conn.close()