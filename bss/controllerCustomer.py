import sqlite3
import time
import random
from bike import *
from customer import *
from login import *
from mapping import *
from renter import *
import random
from companysPocket import *
from closestBike import *
from reportBreakDown import *


def customer_pilot(customer,our_map):
	state = our_map.get_state()
	direction = 'None'
	centralPocket = CentralBank()

	while direction != '':
		our_map.print_nice()
		customer.print_nice()

		if customer.get_flag() == False:
			if direction!='unmount':
				get_closest_bike(customer)
				rented_bike = renting(our_map,customer)
				if rented_bike!=False:
					conn = sqlite3.connect('data/TEAM_PJT.db')
					c = conn.cursor()
					c.execute("SELECT movement_id FROM movement")
					try:
						movement_id = max(c.fetchall())
						movement_id = movement_id[0]+1
					except:
						movement_id = 0
					distance,extra_time = 0,0
					timeOfStart = time.time()
					customer.is_using_bike(True)
					conn.close()
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
				rented_bike.set_mileage(distance)
				dateOfTransaction = time.strftime("%b %d %Y %H:%M:%S",time.gmtime(extra_time+timeOfStart))
				conn = sqlite3.connect('data/TEAM_PJT.db')
				c = conn.cursor()
				c.execute("INSERT INTO movement (movement_id,bike_id,user_id,distance,duration,startTime) VALUES ({},{},{},{},'{}','{}')".format(movement_id,rented_bike.get_id(),
											customer.Id,distance,duration,dateOfTransaction))
				conn.commit()
				conn.close()
				centralPocket.track_changes(amount,dateOfTransaction)
				reportBreak(rented_bike,dateOfTransaction)

			else:
				og_loc = customer.get_location().copy()
				check = customer.move_with_bike(direction, our_map, rented_bike)
				
				if customer.get_location()!=og_loc:
					distance +=1
					extra_time += random.randint(3,5)*random.randint(50,60)* max(0.5,(1-rented_bike.get_defective()))
