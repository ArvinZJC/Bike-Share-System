from customer import *
from bike import *
import sqlite3


def check_available_bikes(map,customer):
	location = customer.get_location()
	conn = sqlite3.connect('data/' + attrs.DB_FILENAME)
	c = conn.cursor()
	c.execute("SELECT id from bike where location_row=:location_row and location_col=:location_col and defective<0.9 and is_being_used=0",
				{'location_row': location[0], 'location_col': location[1]})

	bike_ids = c.fetchall()
	conn.close()
	return bike_ids

def renting(map,customer):
	bike_ids = check_available_bikes(map,customer)
	if len(bike_ids)==0:
		return False

	answer = input("Do you want to rent a bike? ")
	if answer == "yes":
		if len(bike_ids)==1:
			conn = sqlite3.connect('data/' + attrs.DB_FILENAME)
			c = conn.cursor()
			c.execute("SELECT * FROM bike where id=:Id", {'Id': bike_ids[0][0]})
			bike_details = c.fetchall()
			rented_bike = Bike(bike_ids[0][0], bike_details[0][1], [bike_details[0][2], bike_details[0][3]],bike_details[0][4],bike_details[0][5])
			rented_bike.set_is_being_used()
			conn.close()

		else:
			ids = []
			for i in bike_ids:
				ids.append(i[0])
			print(ids)
			rented_id = int(input("Select one of the following: "))
			conn = sqlite3.connect('data/' + attrs.DB_FILENAME)
			c = conn.cursor()
			c.execute("SELECT * FROM bike where id=:Id", {'Id': rented_id})
			bike_details = c.fetchall()
			rented_bike = Bike(rented_id, bike_details[0][1], [bike_details[0][2], bike_details[0][3]],bike_details[0][4],bike_details[0][5])
			conn.close()

		return rented_bike

	else:
		return False





