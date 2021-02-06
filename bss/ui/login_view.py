'''
Description: the definition of a login view
Version: 1.1.1.20210206
Author: Arvin Zhao
Date: 2021-01-24 15:03:00
Last Editors: Arvin Zhao
LastEditTime: 2021-02-06 18:23:21
'''

from PIL import Image, ImageTk
from tkinter import font, messagebox, StringVar, Tk, Toplevel, ttk
from tkinter.constants import E, LEFT, RIGHT, W, X

from bss.conf import attrs
from bss.login_temp import logging  # TODO
from bss.ui.conf import attrs as ui_attrs, styles
from bss.ui.home_view import HomeView
from bss.ui.img_path import get_img_path
from bss.ui.signup_view import SignupView
from bss.ui.tooltip import Tooltip


class LoginView:
    '''
    The class for creating a login view.
    '''

    def __init__(self, parent) -> None:
        '''
        The constructor of the class for creating a login view.

        Parameters
        ----------
        parent : the parent window for the login view to display
        '''

        self.__parent = parent
        self.__signup_window = None  # Initialise the sign-up window here to avoid opening duplicated windows.
        screen_width = self.__parent.winfo_screenwidth()
        screen_height = self.__parent.winfo_screenheight()
        parent_width = 300
        parent_height = 430
        column_num = 2

        self.__parent.geometry('%dx%d+%d+%d' % (parent_width, parent_height, (screen_width - parent_width) / 2, (screen_height - parent_height) / 2))  # Centre the parent window.
        self.__parent.title('Log in')
        self.__parent.iconbitmap(get_img_path(attrs.APP_ICON_FILENAME))
        self.__parent.resizable(False, False)

        font_dict = styles.apply_style()

        # The link font.
        font_link = font.Font(family = ui_attrs.FONT_FAMILY, size = ui_attrs.CONTENT_FONT_SIZE)
        font_link.config(underline = True)

        # New row: the logo image label.
        row_count = 0  # Make it convenient to index the row of the grid.
        image_banner = Image.open(get_img_path(attrs.APP_BANNER_FILENAME))
        image_banner = image_banner.resize((parent_width, ui_attrs.BANNER_WIDTH), Image.ANTIALIAS)
        self.__photo_image_banner = ImageTk.PhotoImage(image_banner)  # Keep a reference in self to prevent GC.
        ttk.Label(self.__parent, image = self.__photo_image_banner).grid(columnspan = column_num, row = row_count)

        # New row: the role label.
        row_count += 1
        ttk.Label(self.__parent, style = styles.CONTENT_LABEL, text = 'Role:').grid(columnspan = column_num, padx = ui_attrs.PADDING_X, pady = ui_attrs.PADDING_Y, row = row_count, sticky = W)

        # New row: the role combobox.
        row_count += 1
        self.__combobox_role = ttk.Combobox(self.__parent, font = font_dict['content_font'], state = 'readonly', values = attrs.ROLE_LIST)
        self.__combobox_role.grid(columnspan = column_num, padx = ui_attrs.PADDING_X, row = row_count, sticky = (E, W))
        self.__combobox_role.bind('<<ComboboxSelected>>', self.__select_role)

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
        frame_password = ttk.Frame(self.__parent)
        frame_password.grid(columnspan = column_num, padx = ui_attrs.PADDING_X, row = row_count, sticky = (E, W))

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
        row_count += 1
        ttk.Label(self.__parent, style = styles.PLACEHOLDER_LABEL).grid(columnspan = 2, row = row_count)

        # New row: the login button.
        row_count += 1
        button_login = ttk.Button(self.__parent, command = self.__log_in, text = 'Log in')
        button_login.grid(columnspan = column_num, padx = ui_attrs.PADDING_X, pady = ui_attrs.PADDING_Y, row = row_count, sticky = (E, W))

        # New row: the label for questioning sign-up status.
        row_count += 1
        column_count = 0  # Make it convenient to index the column of the grid.
        ttk.Label(self.__parent, style = styles.CONTENT_LABEL, text = 'New here?').grid(column = column_count, row = row_count, sticky = E)

        # Same row, new column: the sign-up label.
        column_count += 1
        self.__label_signup = ttk.Label(self.__parent, font = font_link, style = styles.LINK_LABEL, text = 'Sign up now.')
        self.__label_signup.grid(column = column_count, row = row_count, sticky = W)
        self.__label_signup.bind('<Button-1>', self.__press_label_signup)
        self.__label_signup.bind('<ButtonRelease-1>', self.__goto_signup)
        self.__tooltip_signup = Tooltip(self.__label_signup, None)
        self.__is_over_label_signup = False  # A flag indicating if the mouse is over the sign-up label.

        # Initial the status of the role combobox.
        self.__combobox_role.current(0)
        self.__select_role(None)

    # noinspection PyUnusedLocal
    def __select_role(self, event) -> None:
        '''
        Select the role to log in.

        Parameters
        ----------
        event : the event bound to the widget calling this function
        '''

        if self.__combobox_role.get() == attrs.CUSTOMER:
            self.__label_signup['state'] = '!disabled'
            self.__tooltip_signup.set_text()
            self.__label_signup.bind('<Enter>', self.__enter_label_signup)
            self.__label_signup.bind('<Leave>', self.__leave_label_signup)
        else:
            self.__label_signup['state'] = 'disabled'
            self.__tooltip_signup.set_text('You can only sign up as a customer.')

        self.__entry_username.focus()

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

    def __log_in(self) -> None:
        '''
        Log in the user with the selected role when the specified button is clicked.
        '''

        self.__variable_username.set(self.__variable_username.get().strip())
        user = logging(self.__combobox_role.get(), self.__variable_username.get(), self.__variable_password.get())

        if user is None:
            messagebox.showerror(attrs.APP_NAME, 'Wrong username or password. Please try again!')
        else:
            self.__parent.destroy()
            self.__parent = None

            # TODO: create different views for various roles?
            home_window = Tk()
            HomeView(home_window)
            home_window.mainloop()

    # noinspection PyUnusedLocal
    def __enter_label_signup(self, event) -> None:
        '''
        Execute actions when the mouse enters the specified label.

        Parameters
        ----------
        event : the event bound to the widget calling this function
        '''

        self.__is_over_label_signup = True

        if str(self.__label_signup['state']) != 'disabled':
            self.__label_signup['state'] = 'active'

    # noinspection PyUnusedLocal
    def __leave_label_signup(self, event) -> None:
        '''
        Execute actions when the mouse leaves the specified label.

        Parameters
        ----------
        event : the event bound to the widget calling this function
        '''

        self.__is_over_label_signup = False

        if str(self.__label_signup['state']) != 'disabled':
            self.__label_signup['state'] = '!active'

    # noinspection PyUnusedLocal
    def __press_label_signup(self, event) -> None:
        '''
        Focus the sign-up label to look like it is pressed.

        Parameters
        ----------
        event : the event bound to the widget calling this function
        '''

        if str(self.__label_signup['state']) != 'disabled':
            self.__label_signup.focus()

    # noinspection PyUnusedLocal
    def __goto_signup(self, event) -> None:
        '''
        Go to the sign-up view.

        Parameters
        ----------
        event : the event bound to the widget calling this function
        '''

        if str(self.__label_signup['state']) != 'disabled':
            self.__parent.focus()

            if self.__is_over_label_signup:
                if self.__signup_window is None:
                    self.__signup_window = Toplevel(self.__parent)
                    self.__signup_window.protocol('WM_DELETE_WINDOW', self.__reset_signup_window)
                    SignupView(self.__signup_window, attrs.CUSTOMER, 'Sign up')
                else:
                    self.__signup_window.focus()

    def __reset_signup_window(self) -> None:
        '''
        Reset the sign-up window.
        '''

        self.__signup_window.destroy()
        self.__signup_window = None


# Test purposes only.
if __name__ == '__main__':
    login_window = Tk()
    LoginView(login_window)
    login_window.mainloop()