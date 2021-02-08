import sqlite3
import time

from bss.data.db_path import get_db_path


def reportBreak(bike,time):
	answer = ''
	if bike.get_defective()<0.9:
		answer = input("Did the bike work fine?")
	if answer == 'no' or bike.get_defective()>=0.9:
		conn = sqlite3.connect(get_db_path())
		c = conn.cursor()
		c.execute("INSERT INTO bike_status (id,time_of_event,defective_start,defective_end) VALUES ({},'{}',{},{})".format(bike.get_id(),
																										time,bike.get_defective(),1))

		conn.commit()
		conn.close()
		bike.set_defective()