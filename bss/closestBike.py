import sqlite3
import numpy as np

from bss.data.db_path import get_db_path


def get_closest_bike(customer):
	location = customer.get_location().copy()
	conn = sqlite3.connect(get_db_path())
	c = conn.cursor()
	c.execute("SELECT location_row,location_col FROM bike where defective<1 and is_being_used=0")
	distance = np.inf
	for i,j in c.fetchall():
		temp_distance = abs(i-location[0]) + abs(j-location[1])
		if temp_distance < distance :
			distance = temp_distance
			row = i
			col = j

	s = ''
	if col>location[1]:
		s = 'You have to go '+str(col - location[1])+' to the right.'
	elif col < location[1]:
		s = 'You have to go '+str(location[1] - col)+' to the left.'

	if row < location[0]:
		s += 'You have to go '+str(location[0]-row)+' up.'
	elif row > location[0]:
		s += 'You have to go '+str(row - location[0])+ ' down.'

	print(s)