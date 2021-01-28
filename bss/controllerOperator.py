import random
from bike import *
from customer import *
from login import *
from mapping import *
from renter import *
from operators import *
from companysPocket import *
import time

def operator_pilot(operatorWorker):
	centralPocket = CentralBank()

	while True:
		try:
			menu_choice = int(input("Choose one of the available options.\n1) Track the location of bikes in the city\n2) Repair the defective bikes\n3) Move a bike somewhere else\n4) quit\n"))
		except:
			menu_choice=0
		if menu_choice not in [1,2,3,4]:
			continue

		if menu_choice==4:
			break
		elif menu_choice==1:
			operatorWorker.track_bikes()
		elif menu_choice==2:
			centralPocket.pay_operator(operatorWorker,operatorWorker.repair_bikes(),time.strftime("%H:%M:%S",time.gmtime(time.time())))
		else:
			operatorWorker.move_bikes()

		operatorWorker.print_nice()

