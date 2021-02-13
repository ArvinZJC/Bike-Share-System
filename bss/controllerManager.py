import sys
from manager import *
def manager_pilot(user):
	while True:
		choice = user.menu_options()
		if choice == 7:
			conn = sqlite3.connect('data/' + attrs.DB_FILENAME)
			c = conn.cursor()
			c.execute("UPDATE manager SET is_online = 0 where id =:val",{'val':user.get_id()})
			conn.commit()
			conn.close()
		user.viz(choice)
