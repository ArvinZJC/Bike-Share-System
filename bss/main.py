import sqlite3
import time
import random
from bike import *
from customer import *
from login import *
from mapping import *
from bss.customer.controllerCustomer import *
from bss.operator.controllerOperator import *
from bss.manager.controllerManager import *

our_map = Mapping()
#state = our_map.get_state()
#print(state)

user = logging()

if isinstance(user,Customer):
	customer_pilot(user,our_map)

elif isinstance(user,OperatorWorker):
	operator_pilot(user)

elif isinstance(user,Manager):
	manager_pilot(user)

	



