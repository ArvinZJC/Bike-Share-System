import sys
from manager import *
def manager_pilot(user):
	while True:
		choice = user.menu_options()
		if choice == 7:
			sys.exit()
		user.viz(choice)
