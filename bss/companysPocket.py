import sqlite3

from bss.conf import attrs


class CentralBank:

	def __init__(self):
		self.__db_path = 'data/' + attrs.DB_FILENAME
		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		c.execute("SELECT account From companyMoney")
		self.money = c.fetchall()
		self.money = self.money[0][0]

		conn.close()

	def get_money(self):
		return self.money

	def track_changes(self,sumOfMoney,time):
		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		c.execute("INSERT INTO transactions (sumOfMoney,timeOfEvent) VALUES({},'{}')".format(sumOfMoney,time))
		conn.commit()
		conn.close()
		self.change(sumOfMoney)
		

	def change(self,sumOfMoney):
		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		self.money+= sumOfMoney
		c.execute("UPDATE companyMoney set account=:sumOfMoney",{'sumOfMoney':self.money})
		conn.commit()
		conn.close()

	def pay_operator(self,operator,money,time):
		skill = operator.get_skill_level()
		self.track_changes(-money,time)
		operator.set_balance(money)



