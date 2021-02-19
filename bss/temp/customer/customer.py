import sqlite3

from bss.data import db_path as db


class Customer:
	'''
	The class for defining a customer and his/her actions.
	'''

	def __init__(self, user_id, name, password, balance, location) -> None:
		'''
		The constructor of the class for defining a customer and his/her actions.

		Parameters
		----------
		user_id, name, password, balance, location : properties of a customer
		'''

		self.__Id = user_id
		self.__name = name
		self.__password = password
		self.__balance = balance
		self.__location = location
		self.__riding = False
		self.__db_path = db.get_db_path()

	def get_id(self):
		return self.__Id

	def get_name(self) -> str:
		'''
		Name getter.

		Returns
		-------
		name : customer's name
		'''

		return self.__name

	def charge(self, time):
		amount = round(float(time) / 60, 2) * 0.5
		self.__balance -= amount
		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		c.execute("UPDATE customer SET wallet =:new_amount where id=:__Id", {'new_amount': self.__balance, 'Id': self.__Id})
		conn.commit()
		conn.close()
		return amount

	def update_balance(self, amount):
		self.__balance += amount
		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		c.execute("UPDATE customer SET wallet =:new_amount where id=:Id", {'new_amount': self.__balance, 'Id': self.__Id})
		conn.commit()
		conn.close()

	def get_balance(self) -> float:
		'''
		Balance getter.

		Returns
		-------
		balance : customer's balance
		'''

		return self.__balance

	def get_location(self) -> list:
		'''
		Location getter.

		Returns
		-------
		location : a list containing location info
		'''

		return self.__location

	def set_location(self, location):
		self.__location = location
		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		c.execute("UPDATE customer set location_row =:location_row, location_col=:location_col where id=:Id", {'location_row': self.__location[0], 'location_col': self.__location[1], 'Id': self.__Id})
		conn.commit()
		conn.close()

	def move_with_bike(self, direction, mapping, bike):
		print("% to defect: ", bike.get_defective())
		if not bike.is_defective():
			if direction == 'unmount':
				self.is_using_bike(False)

			else:
				bike.move(direction, mapping)
				self.move(direction, mapping)
		else:
			print("This bike broke down. Forced to unmount.")
			direction=='unmount'
			self.is_using_bike(False)

	def is_using_bike(self, flag):
		self.__riding = flag

	def get_flag(self):
		while self.get_balance() < 0:
			print("You can't rent a bike while your balance is negative. Please update your balance."),
			amount = int(input("How much you want to transfer to your account? "))
			self.update_balance(amount)
		return self.__riding