import sqlite3

from bss import rental
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

	def get_id(self) -> int:
		'''
		ID getter.

		Returns
		-------
		user_id : the ID of a customer
		'''

		return self.__Id

	def get_name(self) -> str:
		'''
		Name getter.

		Returns
		-------
		name : customer's name
		'''

		return self.__name

	def charge(self, time) -> float:
		'''
		Charge for the ride.

		Parameters
		----------
		time : the time for calculating the fee

		Returns
		-------
		amount : the amount of money for the ride
		'''

		amount = rental.calculate_charge(time)
		self.__balance -= amount
		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		c.execute('UPDATE customer SET wallet =:new_amount where id=:Id', {'new_amount': self.__balance, 'Id': self.__Id})
		conn.commit()
		conn.close()
		return amount

	def update_balance(self, amount) -> None:
		'''
		Add the customer's balance.

		Parameters
		----------
		amount : the amount to add
		'''

		self.__balance += amount
		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		c.execute('UPDATE customer SET wallet =:new_amount where id=:Id', {'new_amount': self.__balance, 'Id': self.__Id})
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

	def set_location(self, location) -> None:
		'''
		Set the location of a customer.

		Parameters
		----------
		location : a specified location
		'''

		self.__location = location
		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		c.execute('UPDATE customer set location_row =:location_row, location_col=:location_col where id=:Id', {'location_row': self.__location[0], 'location_col': self.__location[1], 'Id': self.__Id})
		conn.commit()
		conn.close()

	def is_using_bike(self, flag) -> None:
		'''
		Set a value to the flag indicating if a customer is riding a bike.

		Parameters
		----------
		flag : a value indicating if a customer is riding a bike
		'''

		self.__riding = flag

	def get_flag(self) -> bool:
		'''
		Riding status flag getter.

		Returns
		-------
		riding : `True` if a customer is riding a bike; otherwise, `False`
		'''

		return self.__riding