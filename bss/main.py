import sqlite3

from bike import *
from customer import *
from login import *
from mapping import *


our_map = Mapping()
state = our_map.get_state()

while True:
    customer_values = logging()
    if customer_values != None:
        customer = Customer(customer_values[0][0], customer_values[0][1], customer_values[0][2], customer_values[0][3],
                            [customer_values[0][4], customer_values[0][5]])
        break
    else:
        print("Fail, try again!")

direction = 'None'

while direction != '':
    our_map.print_nice()
    customer.print_nice()

    if customer.get_flag() == False:
        if direction!='unmount':
            bike_ids = customer.check_if_bike_exists(our_map)
            if bike_ids != False:
                answer = input("You want to rent a bike?")
                if answer == 'yes':
                    rented_id = customer.rent(bike_ids)
                    print("Rented bike: ",rented_id)
                    conn = sqlite3.connect('data/TEAM_PJT.db')
                    c = conn.cursor()
                    c.execute("SELECT * FROM bike where id=:Id", {'Id': rented_id})
                    bike_details = c.fetchall()
                    rented_bike = Bike(rented_id, bike_details[0][1], [bike_details[0][2], bike_details[0][3]])
                    customer.is_using_bike(True)


        direction = input("Input direction[up,down,left,right]: ")
        if direction=='':
            break
        if customer.get_flag():
            customer.move_with_bike(direction,our_map,rented_bike)
        else:
            customer.move(direction,our_map)

    else:
        direction = input("Input direction[up,down,left,right] or unmount: ")
        if direction=='':
            break
        if direction!='unmount':
            customer.move_with_bike(direction, our_map, rented_bike)
        else:
            rented_bike.set_location(rented_bike.get_location())
            customer.is_using_bike(False)


