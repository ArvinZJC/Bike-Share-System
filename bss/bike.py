import sqlite3


class Bike:

    def __init__(self, defective, Id, location):
        self.Id = Id
        self.location = location
        self.defective = defective

    # map.set_state(location,1)

    def is_defective(self):
        return self.defective

    def set_defective(self):
        self.defective = not self.defective
        return self.defective

    def get_location(self):
        return self.location

    def set_location(self, location):
        self.location = location
        conn = sqlite3.connect('data/TEAM_PJT.db')
        c = conn.cursor()
        c.execute("UPDATE bike set location_row =:location_row, location_col=:location_col where id=:Id",
                  {'location_row': location[0], 'location_col': location[1], 'Id': self.Id})
        conn.commit()
        conn.close()

    def get_id(self):
        return self.Id

    def move(self, direction, map):
        location = self.get_location()
        og_val = map.get_square_val(location)
        if direction == 'up':
            map.set_state(location, og_val - 1)
            location[0] -= 1
            self.set_location(location)
            map.set_state(location, map.get_square_val(location) + 1)

        elif direction == 'down':
            map.set_state(location, og_val - 1)
            location[0] += 1
            self.set_location(location)
            map.set_state(location, map.get_square_val(location) + 1)

        elif direction == 'left':
            map.set_state(location, og_val - 1)
            location[1] -= 1
            self.set_location(location)
            map.set_state(location, map.get_square_val(location) + 1)

        else:
            map.set_state(location, og_val - 1)
            location[1] += 1
            self.set_location(location)
            map.set_state(location, map.get_square_val(location) + 1)
