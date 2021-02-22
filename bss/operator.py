import sqlite3
import time

from bss.bike import Bike
from bss.companys_pocket import CentralBank
from bss.conf import attrs
from bss.data import db_path as db


class OperatorWorker:
	'''
	The class for defining an operator.
	'''

	def __init__(self, operator_id, name, password, balance, skill_level) -> None:
		'''
		The constructor of the class for defining an operator.

		Parameters
		----------
		operator_id : the ID of an operator
		name : an operator's name
		password : an operator's password
		balance : an operator's balance
		skill_level : an operator's skill level
		'''

		self.__Id = operator_id
		self.__name = name
		self.__password = password
		self.__balance = balance
		self.__skill_level = skill_level
		self.__location = [0, 0]  # An operator's location is not recorded in the database. We assume that they are at the origin.
		self.__riding = False
		self.__db_path = db.get_db_path()

	def get_id(self) -> int:
		'''
		ID getter.

		Returns
		-------
		operator_id : the ID of an operator
		'''

		return self.__Id

	def get_name(self) -> str:
		'''
		Name getter.

		Returns
		-------
		name : an operator's name
		'''

		return self.__name

	def get_balance(self) -> float:
		'''
		Balance getter.

		Returns
		-------
		balance : an operator's balance
		'''

		return self.__balance

	def get_location(self) -> list:
		'''
		Location getter.

		Returns
		-------
		location : an operator's location
		'''

		return self.__location

	def set_location(self, location: list) -> None:
		'''
		Location setter.

		Parameters
		----------
		location : a specified location
		'''

		self.__location = location

	def get_skill_level(self) -> int:
		'''
		Skill level getter.

		Returns
		-------
		skill_level : an operator's skill level
		'''

		return self.__skill_level

	def is_using_bike(self, flag) -> None:
		'''
		Set a value to the flag indicating if an operator is moving a bike.

		Parameters
		----------
		flag : a value indicating if an operator is moving a bike
		'''

		self.__riding = flag

	def get_flag(self) -> bool:
		'''
		Riding status flag getter.

		Returns
		-------
		riding : `True` if an operator is moving a bike; otherwise, `False`
		'''

		return self.__riding

	def repair_bikes(self, bike_id: int):
		'''
		Overhaul a bike.

		Parameters
		----------
		bike_id : the ID of a bike to overhaul

		Returns
		-------
		to_repair : a `Bike` object
		time_begin : a time string indicating the begin time
		how_broken : a defective value
		time_to_fix : a floating point value representing how long to overhaul a bike
		'''

		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		c.execute("SELECT * FROM bike where id=:Id", {'Id': bike_id})
		i = c.fetchone()
		to_repair = Bike(i[0], i[1], [i[2], i[3]], i[4])
		c.execute("SELECT defective_start,time_of_event from bike_status where id=:Id", {'Id': bike_id})
		rows = c.fetchall()
		how_broken = rows[0][0]
		time_begin = rows[0][1]
		conn.commit()
		time_to_fix = 60 * self.__skill_level * how_broken
		conn.close()
		return to_repair, time_begin, how_broken, time_to_fix

	def record_repair(self, to_repair: Bike, time_begin: str, how_broken: float, time_to_fix: float):
		'''
		Record a repair.

		Parameters
		----------
		to_repair : a `Bike` object representing the bike to overhaul
		time_begin : a time string indicating the begin time
		how_broken : a defective value
		time_to_fix : a floating point value representing how long to overhaul a bike

		Returns
		-------
		bonus : bonus received by an operator
		time_of_fix : a time string indicating the end time
		'''

		if to_repair.get_is_being_used() == attrs.BUSY_BIKE_CODE:
			to_repair.set_is_being_used()

		to_repair.set_defective(to_repair.get_location(), attrs.BIKE_DAMAGE_MIN)
		time_of_fix = time.strftime('%b %d %Y %H:%M:%S', time.gmtime(time.time()))

		if (time.time() + time_to_fix) < time.mktime(time.strptime(time_begin, '%b %d %Y %H:%M:%S')):
			time_of_fix = time.strftime('%b %d %Y %H:%M:%S', time.gmtime(time.mktime(time.strptime(time_begin, '%b %d %Y %H:%M:%S')) + time_to_fix))

		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		c.execute("INSERT INTO bike_status(id,time_of_event,defective_start,defective_end) VALUES({},'{}',{},{})".format(to_repair.get_id(), time_of_fix, how_broken, attrs.BIKE_DAMAGE_MIN))
		conn.commit()
		conn.close()
		money = time_to_fix / 20
		CentralBank().track_changes(-money, time_of_fix)
		self.set_balance(money)

	def move_bikes(self, bike_id: int) -> None:
		'''
		Drop a bike after moving.

		Parameters
		----------
		bike_id : the ID of a bike
		'''

		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		c.execute(
			"UPDATE bike set location_row =:location_row, location_col=:location_col, is_being_used=:status where id=:Id",
			{'location_row': self.__location[0], 'location_col': self.__location[1], 'status': attrs.AVAILABLE_BIKE_CODE, 'Id': bike_id})
		conn.commit()
		conn.close()

	def set_balance(self, money) -> None:
		'''
		Add bonus to the wallet of an operator.

		Parameters
		----------
		money : the amount of bonus
		'''

		self.__balance += money
		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		c.execute("UPDATE operator set account=:sum where id=:Id", {'sum': self.__balance, 'Id': self.__Id})
		conn.commit()
		conn.close()