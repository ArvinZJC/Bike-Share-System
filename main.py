from Map import *
from Bike import *
from Customer import *
from login import *


our_map = Mapping()

state = our_map.get_state()

our_map.print_nice()

while True:
	customer_values = logging()
	if customer_values!=None:
		customer = Customer(customer_values[0][0],customer_values[0][1],customer_values[0][2],customer_values[0][3],
								[customer_values[0][4],customer_values[0][5]])
		break
	else:
		print("Fail, try again!")


customer.print_nice()
direction = input("Input direction [up,down,left,right]:")
while direction!='':
	if customer.get_flag()==False:
		customer.move(direction,our_map)
		our_map.print_nice()
		customer.print_nice()
		bike_ids=customer.check_if_bike_exists(our_map)
		if bike_ids!=False:
			answer = input("You want to rent a bike?")
			if answer == 'yes':
				rented_id = customer.rent(bike_ids)
				print(rented_id)
				conn = sqlite3.connect('TEAM_PJT.db')
				c = conn.cursor()
				c.execute("SELECT * FROM bike where id=:Id",{'Id':rented_id})
				bike_details = c.fetchall()
				rented_bike = Bike(rented_id,bike_details[0][1],[bike_details[0][2],bike_details[0][3]])
				customer.is_using_bike(True)
		
		direction = input("Input direction[up,down,left,right]: ")

	else:
		customer.move_with_bike(direction,our_map,rented_bike)
		our_map.print_nice()
		customer.print_nice()

		direction = input("Input direction[up,down,left,right] or unmount: ")





	
