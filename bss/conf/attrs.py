'''
Description: an attribute sheet to make it convenient to manage code attributes
Version: 1.0.8.20210219
Author: Arvin Zhao
Date: 2021-02-01 17:00:57
Last Editors: Arvin Zhao
LastEditTime: 2021-02-19 17:01:54
'''

# Login status.
ALREADY_ONLINE = -1
OFFLINE = 0
ONLINE = 1

# Filenames.
APP_BANNER_FILENAME = 'banner.png'
APP_ICON_FILENAME = 'icon.ico'
AVAILABLE_BIKE_FILENAME = 'available_bike.png'
BIKE_WITH_RIDER_FILENAME = 'bike_with_rider.png'
BUSY_BIKE_FILENAME = 'busy_bike.png'
CLOSED_EYE_FILENAME = 'closed_eye.png'
CUSTOMER_AVATAR_FILENAME = 'customer.png'
DB_FILENAME = 'TEAM_PJT.db'
DEFECTIVE_BIKE_FILENAME = 'defective_bike.png'
HINT_FILENAME = 'hint.png'
MANAGER_AVATAR_FILENAME = 'manager.png'
OPERATOR_AVATAR_FILENAME = 'operator.png'
OPENING_EYE_FILENAME = 'opening_eye.png'

# Operation status.
ERROR = -1
FAIL = 0
PASS = 1

# Map attributes.
AVAILABLE_BIKE_CODE = 0  # 2nd
AVATAR_CODE = 2  # 4th
BIKE_WITH_RIDER_CODE = 3  # 5th
BUSY_BIKE_CODE = 1  # 3rd
DEFECTIVE_BIKE_CODE = -1  # 1st
EMPTY_CELL_CODE = 5  # 6th
MAP_LENGTH = 20

# Project configuration.
APP_NAME = 'BikeSims'
CUSTOMER = 'Customer'
DATA_BASENAME = 'data'
DEFECTIVE_BIKE_THRESHOLD = 0.9
MANAGER = 'Manager'
OPERATOR = 'Operator'
PASSWORD_LENGTH_MAX = 18
PASSWORD_LENGTH_MIN = 6
ROLE_LIST = [CUSTOMER, MANAGER, OPERATOR]
ROOT_BASENAME = 'bss'
UI_BASENAME = 'ui'
UI_IMG_BASENAME = 'img'
USERNAME_LENGTH_MAX = 10
USERNAME_LENGTH_MIN = 1