import sqlite3
import time
import random
from bike import *
from customer import *
from login import *
from mapping import *
from controllerCustomer import *
from controllerOperator import *

our_map = Mapping()
#state = our_map.get_state()
#print(state)

user = logging()

if isinstance(user,Customer):
	customer_pilot(user,our_map)

elif isinstance(user,OperatorWorker):
	operator_pilot(user)

	



