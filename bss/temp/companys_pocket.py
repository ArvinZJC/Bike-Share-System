import sqlite3

from bss.data import db_path as db


class CentralBank:
	'''
	The class for defining a central bank of the system.
	'''

	def __init__(self) -> None:
		'''
		The constructor of the class for defining a central bank of the system.
		'''

		self.__db_path = db.get_db_path()
		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		c.execute('SELECT account FROM companyMoney')
		self.money = c.fetchall()
		self.money = self.money[0][0]
		conn.close()

	def get_money(self):
		return self.money

	def track_changes(self, amount, time) -> None:
		'''
		Track changes in the bank.

		Parameters
		----------
		amount : the amount of a transaction
		time : the time of a transaction
		'''

		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		c.execute("INSERT INTO transactions(sumOfMoney,timeOfEvent) VALUES({},'{}')".format(amount, time))
		conn.commit()
		conn.close()
		self.change(amount)

	def change(self, amount) -> None:
		'''
		Update the money in the system.

		Parameters
		----------
		amount : the amount of money to update
		'''

		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		self.money += amount
		c.execute('UPDATE companyMoney set account=:amount', {'amount': self.money})
		conn.commit()
		conn.close()

	def pay_operator(self,operator,money,time):
		skill = operator.get_skill_level()
		self.track_changes(-money,time)
		operator.set_balance(money)