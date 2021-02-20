import random
import sqlite3

from bss.conf import attrs
from bss.data import db_path as db


def logging(role: str, name: str, password: str):
    '''
    Backend code of the login process.

    Parameters
    ----------
    role : the user role
    name : the username
    password : the password

    Returns
    -------
    user : a `Customer` or `OperatorWorker` or `Manager` object or `None` or a status code indicating the user has already logged in somewhere else.
    '''

    # Put module references here to attempt to avoid a circular import.
    from bss.temp.customer.customer import Customer  # TODO
    from bss.temp.manager.manager import Manager  # TODO
    from bss.temp.operator.operator import OperatorWorker  # TODO

    conn = sqlite3.connect(db.get_db_path())
    c = conn.cursor()
    
    user = None

    if role == attrs.CUSTOMER:
        c.execute('SELECT * FROM customer WHERE name=:name and password=:password', {'name': name, 'password': password})
        values = c.fetchall()

        if len(values) > 0:
            if values[0][6] == attrs.OFFLINE:
                user = Customer(values[0][0], values[0][1], values[0][2], values[0][3], [values[0][4], values[0][5]])
                c.execute('UPDATE customer SET is_online =:status where id =:val', {'status': attrs.ONLINE, 'val': values[0][0]})
            else:
                return attrs.ALREADY_ONLINE
    elif role == attrs.OPERATOR:
        c.execute('SELECT * From operator Where name=:name and password=:password', {'name': name, 'password': password})
        values = c.fetchall()

        if len(values) > 0:
            if values[0][5] == attrs.OFFLINE:
                user = OperatorWorker(values[0][0], values[0][1], values[0][2], values[0][3], values[0][4])
                c.execute('UPDATE operator SET is_online =:status where id =:val', {'status': attrs.ONLINE, 'val': values[0][0]})
            else:
                return attrs.ALREADY_ONLINE
    elif role == attrs.MANAGER:
        c.execute('SELECT * From manager Where name=:name and password=:password', {'name': name, 'password': password})
        values = c.fetchall()

        if len(values) > 0:
            if values[0][3] == attrs.OFFLINE:
                user = Manager(values[0][0], values[0][1], values[0][2])
                c.execute('UPDATE manager SET is_online =:status where id =:val', {'status': attrs.ONLINE, 'val': values[0][0]})
            else:
                return attrs.ALREADY_ONLINE

    conn.commit()
    conn.close()

    return user


def log_out(user) -> None:
    '''
    Backend code of the log-out process.

    Parameters
    ----------
    user : a `Customer` or `OperatorWorker` or `Manager` object
    '''

    # Put module references here to attempt to avoid a circular import.
    from bss.temp.customer.customer import Customer  # TODO
    from bss.temp.manager.manager import Manager  # TODO
    from bss.temp.operator.operator import OperatorWorker  # TODO

    conn = sqlite3.connect(db.get_db_path())
    c = conn.cursor()

    if isinstance(user, Customer):
        c.execute('UPDATE customer SET is_online =:status where id =:val', {'status': attrs.OFFLINE, 'val': user.get_id()})
    elif isinstance(user, OperatorWorker):
        c.execute('UPDATE operator SET is_online =:status where id =:val', {'status': attrs.OFFLINE, 'val': user.get_id()})
    elif isinstance(user, Manager):
        c.execute('UPDATE manager SET is_online =:status where id =:val', {'status': attrs.OFFLINE, 'val': user.get_id()})

    conn.commit()
    conn.close()


def register_customer(name: str, password: str) -> int:
    '''
    Backend code of the customer's sign-up process.

    Parameters
    ----------
    name : the username
    password : the password

    Returns
    -------
    status_code : a sign-up status code
    '''

    import re

    username_pattern = r'^[a-zA-Z\d]{' + str(attrs.USERNAME_LENGTH_MIN) + ',' + str(attrs.USERNAME_LENGTH_MAX) + '}$'  # Alphanumeric characters.
    password_pattern = r'^(?!\d+$)(?![a-zA-Z]+$)[a-zA-Z\d]{' + str(attrs.PASSWORD_LENGTH_MIN) + ',' + str(attrs.PASSWORD_LENGTH_MAX) + '}$'  # Letters and digits.

    if re.match(username_pattern, name) is None or re.match(password_pattern, password) is None:
        return attrs.FAIL  # Invalid username or password.
    else:
        conn = sqlite3.connect(db.get_db_path())
        c = conn.cursor()
        row = random.randint(0, attrs.MAP_LENGTH - 1)
        col = random.randint(0, attrs.MAP_LENGTH - 1)
        sql = "select max(id) from customer"
        c.execute(sql)
        cid = c.fetchall()[0][0] + 1

        try:
            c.execute("INSERT INTO customer(id,name,password,wallet,location_row,location_col,is_online) VALUES({},'{}','{}',{},{},{},{})".format(cid, name, password, 0.0, row, col, attrs.OFFLINE))
            conn.commit()
            conn.close()
            return attrs.PASS  # Sign up a user successfully.
        except sqlite3.IntegrityError:
            return attrs.ERROR  # The username already exists.


# Test purposes only.
if __name__ == '__main__':
    print(logging(attrs.CUSTOMER, 'jichen ', '12345') is None)  # Expect: True
    print(logging(attrs.MANAGER, '???????', 'hello_world') is None)  # Expect: True
    print(register_customer('ji_chen', 'hello12345'))  # Expect: 0
    print(register_customer('jichen', '123456'))  # Expect: 0
    print(register_customer('jichen', 'hello_world'))  # Expect: 0
    print(register_customer('jichen', 'helloworld'))  # Expect: 0
    print(register_customer('jichen', 'hello12345'))  # Expect: -1