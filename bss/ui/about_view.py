from tkinter import ttk
from tkinter.constants import CENTER, E, S, W
import time
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

from PIL import Image, ImageTk

from bss.conf import attrs
from bss.ui.conf import attrs as ui_attrs, styles
from bss.ui.utils import img_path as img


class AboutView:
    '''
    The class for creating an about-app view.
    '''

    def __init__(self, parent, role: str) -> None:
        '''
        The constructor of the class for creating an about-app view.
        All roles can have access to this view.

        Parameters
        ----------
        parent : the parent window for the about-app view to display
        role : a user role string representation
        '''

        screen_width = parent.winfo_screenwidth()
        screen_height = parent.winfo_screenheight()
        parent_width = 550
        column_num = 2

        if role == attrs.CUSTOMER:
            parent_height = 450
        elif role == attrs.OPERATOR:
            parent_height = 500
        else:
            parent_height = 350

        parent.geometry('%dx%d+%d+%d' % (parent_width, parent_height, (screen_width - parent_width) / 2, (screen_height - parent_height) / 2))  # Centre the parent window.
        parent.title('About ' + attrs.APP_NAME)
        parent.iconbitmap(img.get_img_path(attrs.APP_ICON_FILENAME))
        parent.resizable(False, False)
        styles.apply_style()

        # New row: the logo image label.
        row_index = 0  # Make it convenient to index the row of the grid.
        label_banner = ttk.Label(parent)
        label_banner.grid(columnspan = column_num, row = row_index)
        image_banner = Image.open(img.get_img_path(attrs.APP_BANNER_FILENAME))
        image_banner = image_banner.resize((ui_attrs.BANNER_WIDTH, ui_attrs.BANNER_HEIGHT), Image.ANTIALIAS)
        label_banner.image = ImageTk.PhotoImage(image_banner)
        label_banner['image'] = label_banner.image  # Keep a reference to prevent GC.
        parent.rowconfigure(row_index, weight = 1)

        # New row: the description label.
        row_index += 1
        description = attrs.APP_NAME + ' is a bike-sharing system demonstrated a general bike rental process. It is built by Antonios Evmorfopoulos, Jiamin Ji, Jichen Zhao, Nan Chen, Shihao Chen, Xiaoran Kang, and Yuan Gao as an outcome of the team project.'
        self.__label_description = ttk.Label(parent, justify = CENTER, style = styles.PRIMARY_LABEL, text = description, wraplength = parent_width - ui_attrs.PADDING_X * 2)
        self.__label_description.grid(columnspan = column_num, padx = ui_attrs.PADDING_X, pady = ui_attrs.PADDING_Y, row = row_index)
        parent.rowconfigure(row_index, weight = 0)

        if role != attrs.MANAGER:
            # New row: the available bike image label.
            row_index += 1
            column_count = 0  # Make it convenient to index the column of the grid.
            image_available_bike = Image.open(img.get_img_path(attrs.AVAILABLE_BIKE_FILENAME)).resize((ui_attrs.MAP_CELL_LENGTH, ui_attrs.MAP_CELL_LENGTH), Image.ANTIALIAS)
            label_available_bike_image = ttk.Label(parent)
            label_available_bike_image.grid(column = column_count, row = row_index, sticky = E)
            label_available_bike_image.image = ImageTk.PhotoImage(image_available_bike)
            label_available_bike_image['image'] = label_available_bike_image.image
            parent.rowconfigure(row_index, weight = 0)

            # Same row, new column: the available bike description label.
            column_count += 1
            ttk.Label(parent, style = styles.CONTENT_LABEL, text = ' represents one or more available bikes.').grid(column = column_count, row = row_index, sticky = W)

            # New row: the defective bike image label.
            row_index += 1
            column_count = 0
            image_defective_bike = Image.open(img.get_img_path(attrs.DEFECTIVE_BIKE_FILENAME)).resize((ui_attrs.MAP_CELL_LENGTH, ui_attrs.MAP_CELL_LENGTH), Image.ANTIALIAS)
            label_defective_bike_image = ttk.Label(parent)
            label_defective_bike_image.grid(column = column_count, row = row_index, sticky = E)
            label_defective_bike_image.image = ImageTk.PhotoImage(image_defective_bike)
            label_defective_bike_image['image'] = label_defective_bike_image.image
            parent.rowconfigure(row_index, weight = 0)

            # Same row, new column: the defective bike description label.
            column_count += 1
            ttk.Label(parent, style = styles.CONTENT_LABEL, text = ' represents one or more defective bikes.').grid(column = column_count, row = row_index, sticky = W)

            # New row: the busy bike explanation label.
            row_index += 1
            busy_bike_explanation = 'To protect privacy, busy bikes are not visualised on a map.'

            if role == attrs.OPERATOR:
                busy_bike_explanation += ' However, as an operator, you can view their locations in a bike tracking report.'

            ttk.Label(parent, justify = CENTER, style = styles.CONTENT_LABEL, text = busy_bike_explanation, wraplength = parent_width - ui_attrs.PADDING_X * 2).grid(columnspan = column_num, padx = ui_attrs.PADDING_X, pady = ui_attrs.PADDING_Y, row = row_index)
            parent.rowconfigure(row_index, weight = 0)

        # New row: the frame for the version and copyright area.
        row_index += 1
        frame_version_copyright = ttk.Frame(parent)
        frame_version_copyright.grid(columnspan = column_num, padx = ui_attrs.PADDING_X, pady = ui_attrs.PADDING_Y, row = row_index, sticky = S)
        parent.rowconfigure(row_index, weight = 1)

        # New row: the version label.
        ttk.Label(frame_version_copyright, style = styles.EXPLANATION_LABEL, text = 'Version: ' + attrs.APP_VERSION).pack()

        # New row: the copyright label.
        ttk.Label(frame_version_copyright, style = styles.EXPLANATION_LABEL, text = 'Copyright © ' + time.strftime('%Y', time.localtime()) + ' Lab 1_2d').pack()

        # New row: placeholder.
        ttk.Label(frame_version_copyright, style = styles.PLACEHOLDER_LABEL).pack()


# Test purposes only.
if __name__ == '__main__':
    from tkinter import Tk

    about_window = Tk()
    AboutView(about_window, attrs.CUSTOMER)
    # AboutView(about_window, attrs.OPERATOR)
    # AboutView(about_window, attrs.MANAGER)
    about_window.mainloop()