import sqlite3

from conf import attrs


class Customer:

	def __init__(self, Id, name, password, balance, location):
		self.Id = Id
		self.name = name
		self.password = password
		self.balance = balance
		self.location = location
		self.riding = False
		self.__db_path = 'data/' + attrs.DB_FILENAME

	# map.set_state(location,100)
	def get_id(self):
		return self.Id

	def print_nice(self):
		print("ID: ", self.Id),
		print(" Name: ", self.name),
		print(" Balance: ", self.balance)
		print(" Location: ", self.location)

	def charge(self, time):
		amount = round(float(time)/60,2)*0.5
		self.balance -= amount
		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		c.execute("UPDATE customer SET wallet =:new_amount where id=:Id",{'new_amount':self.balance,'Id':self.Id})
		conn.commit()
		conn.close()
		return amount

	def update_balance(self, amount):
		self.balance += amount
		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		c.execute("UPDATE customer SET wallet =:new_amount where id=:Id",{'new_amount':self.balance,'Id':self.Id})
		conn.commit()
		conn.close()

	def get_balance(self):
		return self.balance

	def get_location(self):
		return self.location

	def set_location(self, location):
		self.location = location
		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		c.execute("UPDATE customer set location_row =:location_row, location_col=:location_col where id=:Id",
				  {'location_row': location[0], 'location_col': location[1], 'Id': self.Id})
		
		conn.commit()
		conn.close()

	def move(self, direction, map):
		location = self.get_location()
		og_val = map.get_square_val(location)

		if direction == 'up':
			if location[0] > 0:
				map.set_state(location, og_val - 100)
				location[0] -= 1
				self.set_location(location)
				map.set_state(location, map.get_square_val(location) + 100)

		elif direction == 'down':
			if location[0] < 19:
				map.set_state(location, og_val - 100)
				location[0] += 1
				self.set_location(location)
				map.set_state(location, map.get_square_val(location) + 100)

		elif direction == 'left':
			if location[1] > 0:
				map.set_state(location, og_val - 100)
				location[1] -= 1
				self.set_location(location)
				map.set_state(location, map.get_square_val(location) + 100)

		else:
			if location[1] < 19:
				map.set_state(location, og_val - 100)
				location[1] += 1
				self.set_location(location)
				map.set_state(location, map.get_square_val(location) + 100)

	def move_with_bike(self, direction, map, bike):
		print("% to defect: ",bike.get_defective())
		if bike.is_defective()==False:
			if direction == 'unmount':
				self.is_using_bike(False)

			else:
				bike.move(direction, map)
				self.move(direction, map)
		else:
			print("This bike broke down. Forced to unmount.")
			direction=='unmount'
			self.is_using_bike(False)

	def is_using_bike(self, flag):
		self.riding = flag

	def get_flag(self):
		while self.get_balance()<0:
			print("You can't rent a bike while your balance is negative. Please update your balance."),
			amount = int(input("How much you want to transfer to your account? "))
			self.update_balance(amount)
		return self.riding
