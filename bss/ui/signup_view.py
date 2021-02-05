'''
Description: the definition of a sign-up view
Version: 1.0.3.20210205
Author: Arvin Zhao
Date: 2021-01-30 18:31:28
Last Editors: Arvin Zhao
LastEditTime: 2021-02-05 18:31:39
'''

from PIL import Image, ImageTk
from tkinter import StringVar, ttk, Tk
from tkinter.constants import E, LEFT, RIGHT, W, X

from bss.conf import attrs
from bss.ui.conf import attrs as ui_attrs, styles
from bss.ui.img_path import get_img_path
from bss.ui.tooltip import Tooltip


class SignupView:
    '''
    The class for creating a sign-up view.
    '''

    def __init__(self, parent) -> None:
        '''
        The constructor of the class for creating a sign-up view.

        Parameters
        ----------
        parent : the __parent window for the sign-up view to display
        '''

        self.__parent = parent
        screen_width = self.__parent.winfo_screenwidth()
        screen_height = self.__parent.winfo_screenheight()
        parent_width = 300
        parent_height = 345
        column_num = 2

        self.__parent.geometry('%dx%d+%d+%d' % (parent_width, parent_height, (screen_width - parent_width) / 2, (screen_height - parent_height) / 2))  # Centre the parent window.
        self.__parent.title('Sign up')
        self.__parent.iconbitmap(get_img_path(attrs.APP_ICON_FILENAME))
        self.__parent.resizable(False, False)

        font_dict = styles.apply_style()

        # New row: the logo image label.
        row_count = 0  # Make it convenient to index the row of the grid.
        image_banner = Image.open(get_img_path(attrs.APP_BANNER_FILENAME))
        image_banner = image_banner.resize((parent_width, ui_attrs.BANNER_WIDTH), Image.ANTIALIAS)
        self.__photo_image_banner = ImageTk.PhotoImage(image_banner)  # Keep a reference to prevent GC.
        ttk.Label(self.__parent, image = self.__photo_image_banner).grid(columnspan = column_num, row = row_count)

        # New row: the username label.
        row_count += 1
        ttk.Label(self.__parent, style = styles.CONTENT_LABEL, text = 'Username:').grid(columnspan = column_num, padx = ui_attrs.PADDING_X, pady = ui_attrs.PADDING_Y, row = row_count, sticky = W)

        # New row: the username entry.
        row_count += 1
        self.__variable_username = StringVar()
        self.__entry_username = ttk.Entry(self.__parent, font = font_dict['content_font'], textvariable = self.__variable_username)
        self.__entry_username.grid(columnspan = column_num, padx = ui_attrs.PADDING_X, row = row_count, sticky = (E, W))
        self.__entry_username.focus()

        # New row: the password label.
        row_count += 1
        ttk.Label(self.__parent, style = styles.CONTENT_LABEL, text = 'Password:').grid(columnspan = column_num, padx = ui_attrs.PADDING_X, pady = ui_attrs.PADDING_Y, row = row_count, sticky = W)

        # New row: a frame for the password area.
        row_count += 1
        self.__frame_password_area = ttk.Frame(self.__parent)
        self.__frame_password_area.grid(columnspan = column_num, padx = ui_attrs.PADDING_X, row = row_count, sticky = (E, W))

        # Same row in the frame: the password entry.
        self.__variable_password = StringVar()
        self.__entry_password = ttk.Entry(self.__frame_password_area, font = font_dict['content_font'], show = '*', textvariable = self.__variable_password)
        self.__entry_password.pack(expand = True, fill = X, side = LEFT)

        # Same row in the frame: the button with an eye image for controlling the visibility of password
        image_opening_eye = Image.open(get_img_path(attrs.OPENING_EYE_FILENAME))
        image_opening_eye = image_opening_eye.resize((ui_attrs.PRIMARY_FONT_SIZE, ui_attrs.PRIMARY_FONT_SIZE), Image.ANTIALIAS)
        self.__photo_image_opening_eye = ImageTk.PhotoImage(image_opening_eye)
        image_closed_eye = Image.open(get_img_path(attrs.CLOSED_EYE_FILENAME))
        image_closed_eye = image_closed_eye.resize((ui_attrs.PRIMARY_FONT_SIZE, ui_attrs.PRIMARY_FONT_SIZE), Image.ANTIALIAS)
        self.__photo_image_closed_eye = ImageTk.PhotoImage(image_closed_eye)
        self.__button_password_eye = ttk.Button(self.__frame_password_area, command = self.__set_password_visibility, image = self.__photo_image_closed_eye, style = styles.SQUARE_BUTTON)
        self.__button_password_eye.pack(side = RIGHT)
        self.__text_show_password = 'Click to show the password.'
        self.__text_hide_password = 'Click to hide the password.'
        self.__tooltip_password_eye = Tooltip(self.__button_password_eye, self.__text_show_password)

        # New row: placeholder.
        row_count += 1
        ttk.Label(self.__parent, style = styles.PLACEHOLDER_LABEL).grid(columnspan = 2, row = row_count)

        # New row: the sign-up button.
        row_count += 1
        self.__button_signup = ttk.Button(self.__parent, command = self.__sign_up, text = 'Sign up')
        self.__button_signup.grid(columnspan = column_num, padx = ui_attrs.PADDING_X, pady = ui_attrs.PADDING_Y, row = row_count, sticky = (E, W))

    def __set_password_visibility(self) -> None:
        '''
        Show or hide the password when the specified button is clicked.
        '''

        if self.__entry_password['show'] == '*':
            self.__entry_password['show'] = ''
            self.__button_password_eye['image'] = self.__photo_image_opening_eye
            self.__tooltip_password_eye.set_text(self.__text_hide_password)
        else:
            self.__entry_password['show'] = '*'
            self.__button_password_eye['image'] = self.__photo_image_closed_eye
            self.__tooltip_password_eye.set_text(self.__text_show_password)

    def __sign_up(self) -> None:
        '''
        Sign a customer up when the specified button is clicked.
        '''

        pass


# Test purposes only.
if __name__ == '__main__':
    signup_window = Tk()
    SignupView(signup_window)
    signup_window.mainloop()