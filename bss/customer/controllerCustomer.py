import sqlite3
import time
import random
from bike import *
from customers.customer import *
from login import *
from mapping import *
from customers.renter import *
import random
from companysPocket import *
from customers.closestBike import *
from customers.reportBreakDown import *
import os

from bss.customer.reportBreakDown import reportBreak


def customer_pilot(customer,our_map):
	state = our_map.get_state()
	direction = 'None'
	centralPocket = CentralBank()
	db_path = os.getcwd()+'\\data\\' + attrs.DB_FILENAME

	while direction != '':
		our_map.print_nice()
		customer.print_nice()

		if customer.get_flag() == False:
			if direction!='unmount':
				get_closest_bike(customer)
				rented_bike = renting(our_map,customer)
				if rented_bike!=False:
					distance,extra_time = 0,0
					timeOfStart = time.time()
					customer.is_using_bike(True)
					if customer.get_balance()<40:
						answer = input("Your funds are low. Do you want to update your balance? ")
						if answer == 'yes':
							amount = int(input("How much you want to transfer to your account? "))
							customer.update_balance(amount)

			while True:
				direction = input("Input direction[up,down,left,right]: ")
				if direction not in ['up','down','right','left','']:
					print("Invalid.Try again.")
				else:
					break

			if direction == '':
				break
			elif customer.get_flag()==True:
				customer.move_with_bike(direction,our_map,rented_bike)
			else:
				customer.move(direction,our_map)

		else:
			rented_bike.print_nice()
			while True:
				
				if rented_bike.is_defective()==False:
					direction = input("Input direction[up,down,left,right] or unmount: ")
				else:
					direction = 'unmount'
					print("The bike broke down.Force to unmount.")

				if direction not in ['up','down','right','left','unmount']:
					print("Invalid.Try again.")
				elif direction == '':
					print("First unmount to log out.")
				else:
					break

			if direction == 'unmount':
				customer.is_using_bike(False)
				amount = customer.charge(extra_time)
				duration = time.strftime("%H:%M:%S",time.gmtime(extra_time))
				dateOfTransaction = time.strftime("%b %d %Y %H:%M:%S",time.gmtime(time.time()))
				conn = sqlite3.connect(db_path)
				c = conn.cursor()
				c.execute("INSERT INTO movement (bike_id,user_id,distance,duration,startTime) VALUES ({},{},{},'{}','{}')".format(rented_bike.get_id(),
											customer.Id,distance,duration,dateOfTransaction))
				conn.commit()
				conn.close()
				rented_bike.set_is_being_used()
				our_map.get_state()
				centralPocket.track_changes(amount,dateOfTransaction)
				reportBreak(rented_bike,dateOfTransaction)

			else:
				og_loc = customer.get_location().copy()
				check = customer.move_with_bike(direction, our_map, rented_bike)
				
				if customer.get_location()!=og_loc:
					distance +=1
					extra_time += random.randint(3,5)*random.randint(50,60)* max(0.5,(1-rented_bike.get_defective()))

	conn = sqlite3.connect('data/' + attrs.DB_FILENAME)
	c = conn.cursor()
	c.execute("UPDATE customer SET is_online = 0 where id =:val",{'val':customer.get_id()})
	conn.commit()
	conn.close()
