'''
Description: a database file location helper
Version: 1.0.4.20210222
Author: Arvin Zhao
Date: 2021-02-04 12:58:54
Last Editors: Arvin Zhao
LastEditTime: 2021-02-22 13:23:33
'''

import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

from bss.conf import attrs


def get_db_path() -> str:
    '''
    Get the relative path of the database file based on the running location of a script file.

    Returns
    -------
    db_path : the suitable relative path of the database file
    '''

    basename = os.path.basename(os.getcwd())  # Get the basename of the script file that is run.

    if basename == attrs.DATA_BASENAME:
        return attrs.DB_FILENAME
    elif basename == attrs.ROOT_BASENAME:
        return os.path.join(attrs.DATA_BASENAME, attrs.DB_FILENAME)
    elif attrs.PROJECT_BASENAME in basename:
        return os.path.join(attrs.ROOT_BASENAME, attrs.DATA_BASENAME, attrs.DB_FILENAME)
    else:
        return os.path.join('..', attrs.DATA_BASENAME, attrs.DB_FILENAME)


# Test purposes only.
if __name__ == '__main__':
    print(get_db_path())