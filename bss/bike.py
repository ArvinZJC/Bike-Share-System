import sqlite3
import random

from conf import attrs


class Bike:

	def __init__(self, Id, defective, location,mileage,is_being_used):
		self.Id = Id
		self.location = location
		self.defective = defective
		self.mileage = mileage
		self.__db_path = 'data/' + attrs.DB_FILENAME
		self.is_being_used = is_being_used

	def print_nice(self):
		print("Bike Id: ",self.Id),
		print("%% defective: ",self.defective)
		

	def print_details(self):
		print("Bike Id: ",self.Id),
		print("%% defective: ",self.defective),
		print("Mileage: ",self.mileage)
		print("Location: ",self.location)

	def get_defective(self):
		return self.defective

	def is_defective(self):
		return self.defective>0.9

	def set_defective(self):
		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		if self.defective==1:
			self.defective = 0
			self.mileage = 0
			c.execute("UPDATE bike set mileage=0,defective=0 where id=:Id",{'Id':self.get_id()})
		
		else:
			self.defective = 1
			c.execute("UPDATE bike set defective=1 where id=:Id",{'Id':self.get_id()})

		conn.commit()
		conn.close()

	def get_is_being_used(self):
		return self.is_being_used
		
		
	def set_is_being_used(self):
		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		if self.is_being_used==1:
			self.is_being_used=0
			c.execute("UPDATE bike set is_being_used=0 where id=:Id",{'Id':self.get_id()})
		
		else:
			self.is_being_used = 1
			c.execute("UPDATE bike set is_being_used=1 where id=:Id",{'Id':self.get_id()})

		conn.commit()
		conn.close()




	def get_location(self):
		return self.location

	def get_mileage(self):
		return self.mileage

	def set_mileage(self,val):
		self.mileage += val
		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		c.execute("UPDATE bike set mileage=:val where id=:Id",{'Id':self.get_id(),'val':val})
		conn.commit()
		conn.close()


	def set_location(self, location,operator=1):
		self.location = location
		self.defective+=round(random.uniform(0.01,0.05),2)
		conn = sqlite3.connect(self.__db_path)
		c = conn.cursor()
		c.execute("UPDATE bike set location_row =:location_row, location_col=:location_col,defective=:value where id=:Id",
				  {'location_row': location[0], 'location_col': location[1],'value':self.defective, 'Id': self.Id})
		conn.commit()
		conn.close()

	def get_id(self):
		return self.Id

	def move(self, direction, map):
		location = self.get_location()

		og_val = map.get_square_val(location)
		if direction == 'up':
			if location[0]>0:
				map.set_state(location, og_val - 1)
				location[0] -= 1
				self.set_location(location)
				map.set_state(location, map.get_square_val(location) + 1)

		elif direction == 'down':
			if location[0]<19:
				map.set_state(location, og_val - 1)
				location[0] += 1
				self.set_location(location)
				map.set_state(location, map.get_square_val(location) + 1)

		elif direction == 'left':
			if location[1]>0:
				map.set_state(location, og_val - 1)
				location[1] -= 1
				self.set_location(location)
				map.set_state(location, map.get_square_val(location) + 1)

		else:
			if location[1]<19:
				map.set_state(location, og_val - 1)
				location[1] += 1
				self.set_location(location)
				map.set_state(location, map.get_square_val(location) + 1)