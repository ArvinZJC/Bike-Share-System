import sqlite3


class Customer:

    def __init__(self, Id, name, password, balance, location):
        self.Id = Id
        self.name = name
        self.password = password
        self.balance = balance
        self.location = location
        self.riding = False

    # map.set_state(location,100)

    def print_nice(self):
        print("ID: ", self.Id),
        print(" Name: ", self.name),
        print(" Balance: ", self.balance)
        print(" Location: ", self.location)

    def charge(self, amount):
        if amount > self.balance:
            print("Balance not enough to pay! Invalid transaction.")
            return
        self.balance -= amount
        c = conn.cursor()
        c.execute("Update customer set wallet =:new_amount",{'new_amount':self.balance})
        conn.commit()
        conn.close()

    def update_balance(self, amount):
        self.balance += amount
        conn = sqlite3.connect('data/TEAM_PJT.db')
        c = conn.cursor()
        c.execute("Update customer set wallet =:new_amount",{'new_amount':self.balance})
        conn.commit()
        conn.close()

    def get_location(self):
        return self.location

    def set_location(self, location):
        self.location = location
        conn = sqlite3.connect('data/TEAM_PJT.db')
        c = conn.cursor()
        c.execute("UPDATE customer set location_row =:location_row, location_col=:location_col where id=:Id",
                  {'location_row': location[0], 'location_col': location[1], 'Id': self.Id})
        
        conn.commit()
        conn.close()

    def check_if_bike_exists(self, map):
        location = self.get_location()
        val = map.get_square_val(location)
        if val % 100 == 0:
            return False
        else:
            conn = sqlite3.connect('data/TEAM_PJT.db')
            c = conn.cursor()
            c.execute(
                "SELECT id from bike where location_row=:location_row and location_col=:location_col and defective=:defective",
                {'location_row': location[0], 'location_col': location[1], 'defective': 0})
            bikes_ids = c.fetchall()
            conn.close()
            return bikes_ids

    def is_bike_defective(self, bike):
        return bike.is_defective()

    def rent(self, bike_list):
        if len(bike_list) == 0:
            return False
        elif len(bike_list) == 1:
            return bike_list[0][0]
        else:
            print(bike_list)
            Id = input("Which bike you want to rent? ")
            return Id

    def move(self, direction, map):
        location = self.get_location()
        og_val = map.get_square_val(location)

        if direction == 'up':
            if location[0] >= 0:
                map.set_state(location, og_val - 100)
                location[0] -= 1
                self.set_location(location)
                map.set_state(location, map.get_square_val(location) + 100)

        elif direction == 'down':
            if location[0] <= 19:
                map.set_state(location, og_val - 100)
                location[0] += 1
                self.set_location(location)
                map.set_state(location, map.get_square_val(location) + 100)

        elif direction == 'left':
            if location[1] >= 0:
                map.set_state(location, og_val - 100)
                location[1] -= 1
                self.set_location(location)
                map.set_state(location, map.get_square_val(location) + 100)

        else:
            if location[1] <= 19:
                map.set_state(location, og_val - 100)
                location[1] += 1
                self.set_location(location)
                map.set_state(location, map.get_square_val(location) + 100)

    def move_with_bike(self, direction, map, bike):
        if direction == 'unmount':
            self.is_using_bike(False)

        else:
            bike.move(direction, map)
            self.move(direction, map)

    def is_using_bike(self, flag):
        self.riding = flag

    def get_flag(self):
        return self.riding
