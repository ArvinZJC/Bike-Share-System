import random
from bike import *
from login import *
from mapping import *
from operator import *
from companysPocket import *
import time
import os

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
			conn = sqlite3.connect(os.getcwd()+'\\data\\' + attrs.DB_FILENAME)
			c = conn.cursor()
			c.execute("UPDATE operator SET is_online = 0 where id =:val",{'val':operatorWorker.get_id()})
			conn.commit()
			conn.close()
			break
		elif menu_choice==1:
			operatorWorker.track_bikes()
		elif menu_choice==2:
			lst = operatorWorker.repair_bikes()
			print(lst)
			money = lst[0]
			time = lst[1]
			centralPocket.pay_operator(operatorWorker,money,time)
		else:
			operatorWorker.move_bikes()

		operatorWorker.print_nice()

