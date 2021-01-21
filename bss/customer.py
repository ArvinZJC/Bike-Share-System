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

    def update_balance(self, amount):
        self.balance += amount

    def get_location(self):
        return self.location

    def set_location(self, location):
        self.location = location
        conn = sqlite3.connect('data/TEAM_PJT.db')
        c = conn.cursor()
        c.execute("UPDATE customer set location_row =:location_row, location_col=:location_col where name=:name",
                  {'location_row': location[0], 'location_col': location[1], 'name': self.name})
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
            map.set_state(location, og_val - 100)
            temp = location[0]
            if temp >= 1:
                location[0] -= 1
                self.set_location(location)
                map.set_state(location, map.get_square_val(location) + 1)

        elif direction == 'down':
            map.set_state(location, og_val - 100)
            temp = location[0]
            if temp <= 18:
                location[0] += 1
                self.set_location(location)
                map.set_state(location, map.get_square_val(location) + 100)

        elif direction == 'left':
            map.set_state(location, og_val - 100)
            temp = location[1]
            if temp >= 1:
                location[1] -= 1
                self.set_location(location)
                map.set_state(location, map.get_square_val(location) + 100)

        else:
            map.set_state(location, og_val - 100)
            temp = location[1]
            if temp <= 18:
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