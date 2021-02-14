'''
Description: the definition of a sign-up view
Version: 1.1.7.20210214
Author: Arvin Zhao
Date: 2021-01-30 18:31:28
Last Editors: Arvin Zhao
LastEditTime: 2021-02-14 18:31:39
'''

from tkinter import messagebox, StringVar, ttk, Tk
from tkinter.constants import E, LEFT, RIGHT, W, X

from PIL import Image, ImageTk

from bss.conf import attrs
from bss.temp.login import register_customer
from bss.ui.conf import attrs as ui_attrs, styles
from bss.ui.img_path import get_img_path
from bss.ui.tooltip import Tooltip


class SignupView:
    '''
    The class for creating a sign-up view.
    '''

    def __init__(self, parent, role: str, signup_text: str) -> None:
        '''
        The constructor of the class for creating a sign-up view.
        This view is role-specific. All roles can have access to it.

        Parameters
        ----------
        parent : the parent window for the sign-up view to display
        role : the user role
        signup_text : the parent window's title and the text on the sign-up button
        '''

        self.__parent = parent
        self.__role = role
        screen_width = self.__parent.winfo_screenwidth()
        screen_height = self.__parent.winfo_screenheight()
        parent_width = 300
        parent_height = 330
        column_num = 2

        self.__parent.geometry('%dx%d+%d+%d' % (parent_width, parent_height, (screen_width - parent_width) / 2, (screen_height - parent_height) / 2))  # Centre the parent window.
        self.__parent.title(signup_text)
        self.__parent.iconbitmap(get_img_path(attrs.APP_ICON_FILENAME))
        self.__parent.minsize(parent_width, parent_height)
        self.__parent.maxsize(parent_width * 2, parent_height * 2)

        for index in range(column_num):
            self.__parent.columnconfigure(index, weight = 1)

        font_dict = styles.apply_style()

        # New row: the logo image label.
        row_index = 0  # Make it convenient to index the row of the grid.
        label_banner = ttk.Label(self.__parent)
        label_banner.grid(columnspan=column_num, row=row_index)
        image_banner = Image.open(get_img_path(attrs.APP_BANNER_FILENAME))
        image_banner = image_banner.resize((parent_width, ui_attrs.BANNER_HEIGHT), Image.ANTIALIAS)
        label_banner.image = ImageTk.PhotoImage(image_banner)
        label_banner['image'] = label_banner.image  # Keep a reference to prevent GC.
        self.__parent.rowconfigure(row_index, weight = 1)

        # New row: a frame for the username label area.
        row_index += 1
        frame_username_label = ttk.Frame(self.__parent)
        frame_username_label.grid(columnspan = column_num, padx = ui_attrs.PADDING_X, row = row_index, sticky = (E, W))
        ttk.Label(frame_username_label, style = styles.CONTENT_LABEL, text = 'Username:').pack(fill = X, side = LEFT)  # Same row in the frame: the username label.
        self.__parent.rowconfigure(row_index, weight = 0)

        # Same row in the frame: the username hint label.
        image_hint = Image.open(get_img_path(attrs.HINT_FILENAME))
        image_hint = image_hint.resize((ui_attrs.PRIMARY_FONT_SIZE, ui_attrs.PRIMARY_FONT_SIZE), Image.ANTIALIAS)
        self.__photo_image_hint = ImageTk.PhotoImage(image_hint)  # Keep a reference in self to prevent GC.
        label_username_hint = ttk.Label(frame_username_label, image = self.__photo_image_hint, style = styles.CONTENT_LABEL)
        label_username_hint.pack(fill = X, side = LEFT)
        Tooltip(label_username_hint, 'Please enter at most 10 alphanumeric characters.')

        # New row: the username entry.
        row_index += 1
        self.__variable_username = StringVar()
        entry_username = ttk.Entry(self.__parent, font = font_dict['content_font'], textvariable = self.__variable_username)
        entry_username.grid(columnspan = column_num, padx = ui_attrs.PADDING_X, row = row_index, sticky = (E, W))
        entry_username.focus()
        self.__parent.rowconfigure(row_index, weight = 0)

        # New row: a frame for the password label area.
        row_index += 1
        frame_password_label = ttk.Frame(self.__parent)
        frame_password_label.grid(columnspan = column_num, padx = ui_attrs.PADDING_X, row = row_index, sticky = (E, W))
        self.__parent.rowconfigure(row_index, weight = 0)

        ttk.Label(frame_password_label, style = styles.CONTENT_LABEL, text = 'Password:').pack(fill = X, side = LEFT)  # Same row in the frame: the password label.

        # Same row in the frame: the password hint label.
        label_password_hint = ttk.Label(frame_password_label, image = self.__photo_image_hint, style = styles.CONTENT_LABEL)
        label_password_hint.pack(fill = X, side = LEFT)
        Tooltip(label_password_hint, 'Please enter 6 - 18 alphanumeric characters, including both letters and digits. ')

        # New row: a frame for the password area.
        row_index += 1
        frame_password = ttk.Frame(self.__parent)
        frame_password.grid(columnspan = column_num, padx = ui_attrs.PADDING_X, row = row_index, sticky = (E, W))
        self.__parent.rowconfigure(row_index, weight = 0)

        # Same row in the frame: the password entry.
        self.__variable_password = StringVar()
        self.__entry_password = ttk.Entry(frame_password, font = font_dict['content_font'], show = '*', textvariable = self.__variable_password)
        self.__entry_password.pack(expand = True, fill = X, side = LEFT)

        # Same row in the frame: the button with an eye image for controlling the visibility of password
        image_opening_eye = Image.open(get_img_path(attrs.OPENING_EYE_FILENAME))
        image_opening_eye = image_opening_eye.resize((ui_attrs.PRIMARY_FONT_SIZE, ui_attrs.PRIMARY_FONT_SIZE), Image.ANTIALIAS)
        self.__photo_image_opening_eye = ImageTk.PhotoImage(image_opening_eye)  # Keep a reference in self to prevent GC.
        image_closed_eye = Image.open(get_img_path(attrs.CLOSED_EYE_FILENAME))
        image_closed_eye = image_closed_eye.resize((ui_attrs.PRIMARY_FONT_SIZE, ui_attrs.PRIMARY_FONT_SIZE), Image.ANTIALIAS)
        self.__photo_image_closed_eye = ImageTk.PhotoImage(image_closed_eye)  # Keep a reference in self to prevent GC.
        self.__button_password_eye = ttk.Button(frame_password, command = self.__set_password_visibility, image = self.__photo_image_closed_eye, style = styles.IMG_BUTTON)
        self.__button_password_eye.pack(side = RIGHT)
        self.__text_show_password = 'Click to show the password.'
        self.__text_hide_password = 'Click to hide the password.'
        self.__tooltip_password_eye = Tooltip(self.__button_password_eye, self.__text_show_password)

        # New row: placeholder.
        row_index += 1
        ttk.Label(self.__parent, style = styles.PLACEHOLDER_LABEL).grid(columnspan = 2, row = row_index)
        self.__parent.rowconfigure(row_index, weight = 0)

        # New row: the sign-up button.
        row_index += 1
        button_signup = ttk.Button(self.__parent, command = lambda: self.__sign_up(None), text = signup_text)
        button_signup.grid(columnspan = column_num, padx = ui_attrs.PADDING_X, pady = ui_attrs.PADDING_Y, row = row_index, sticky = (E, W))
        self.__parent.rowconfigure(row_index, weight = 0)

        # New row: placeholder.
        row_index += 1
        ttk.Label(self.__parent, style = styles.PLACEHOLDER_LABEL).grid(columnspan = 2, row = row_index)
        self.__parent.rowconfigure(row_index, weight = 1)

        # Bind events.
        entry_username.bind('<Return>', self.__sign_up)
        self.__entry_password.bind('<Return>', self.__sign_up)
        button_signup.bind('<Return>', self.__sign_up)

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

    # noinspection PyUnusedLocal
    def __sign_up(self, event) -> None:
        '''
        Sign up a user when the specified button is clicked.

        Parameters
        ----------
        event : the event bound to the widget calling this function
        '''

        if self.__role == attrs.CUSTOMER:
            username = self.__variable_username.get()
            status_code = register_customer(username, self.__variable_password.get())

            if status_code == attrs.PASS:
                messagebox.showinfo(attrs.APP_NAME, 'Congratulations! ' + attrs.CUSTOMER + ' "' + username + '" has been registered successfully.')
                self.__parent.destroy()
                self.__parent = None
            elif status_code == attrs.FAIL:
                if messagebox.showerror(attrs.APP_NAME, 'Invalid username or password. Please see the hints by hovering over the question mark icon.') == messagebox.OK:
                    self.__parent.focus()
            else:
                if messagebox.showerror(attrs.APP_NAME, 'The username already exists.') == messagebox.OK:
                    self.__parent.focus()
        else:
            pass  # TODO: manager/operator


# Test purposes only.
if __name__ == '__main__':
    signup_window = Tk()
    SignupView(signup_window, attrs.CUSTOMER, 'Sign up')
    signup_window.mainloop()