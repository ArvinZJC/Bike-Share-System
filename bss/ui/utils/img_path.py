'''
Description: an image file location helper
Version: 1.0.2.20210214
Author: Arvin Zhao
Date: 2021-02-05 14:04:27
Last Editors: Arvin Zhao
LastEditTime: 2021-02-14 14:05:23
'''

import os

from bss.conf import attrs


def get_img_path(img_filename: str) -> str:
    '''
    Get the relative path of an image based on the running location of a script file.

    Parameters
    ----------
    img_filename : the filename of the image

    Returns
    -------
    db_path : the suitable relative path of the database file
    '''

    basename = os.path.basename(os.getcwd())  # Get the basename of the script file that is run.

    if basename == attrs.UI_BASENAME:
        return os.path.join(attrs.UI_IMG_BASENAME, img_filename)
    elif basename == attrs.ROOT_BASENAME:
        return os.path.join(attrs.UI_BASENAME, attrs.UI_IMG_BASENAME, img_filename)
    else:
        return os.path.join('../..', attrs.UI_BASENAME, attrs.UI_IMG_BASENAME, img_filename)


# Test purposes only.
if __name__ == '__main__':
    print(get_img_path(attrs.APP_BANNER_FILENAME))