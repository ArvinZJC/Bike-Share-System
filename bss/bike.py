import sqlite3

class Bike:

    def __init__(self, Id, defective, location):
        self.Id = Id
        self.location = location
        self.defective = defective

    def print_nice(self):
    	print("Bike Id: ",self.Id),
    	print("%% defective: ",self.defective)

    def print_details(self):
        print("Bike Id: ",self.Id),
        print("%% defective: ",self.defective),
        print("Location: ",self.location)

    def get_defective(self):
    	return self.defective

    def is_defective(self):
    	return self.defective>0.9

    def set_defective(self):
        if self.defective >=0.9:
        	self.defective = 0
        else:
        	self.defective = 1

    def get_location(self):
        return self.location

    def set_location(self, location,operator=1):
        self.location = location
        self.defective+=0.05

        conn = sqlite3.connect('data/TEAM_PJT.db')
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