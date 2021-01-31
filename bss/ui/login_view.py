'''
Description: the definition of a login view
Version: 1.0.6.20210131
Author: Arvin Zhao
Date: 2021-01-24 15:03:00
Last Editors: Arvin Zhao
LastEditTime: 2021-01-31 18:23:21
'''

from tkinter import font, StringVar, Tk, Toplevel, ttk
from tkinter.constants import E, W

from bss.ui.conf import attrs, styles
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
        parent_height = 500
        column_num = 2

        self.__parent.geometry('%dx%d+%d+%d' % (parent_width, parent_height, (screen_width - parent_width) / 2, (screen_height - parent_height) / 2))  # Centre the __parent window.
        self.__parent.title('Log in')
        self.__parent.iconbitmap(attrs.APP_ICON_PATH)

        # Enable auto-resizing controls with the grid geometry manager.
        for index in range(column_num):
            self.__parent.columnconfigure(index, weight = 1)

        font_dict = styles.apply_style()

        # The link font.
        font_link = font.Font(family = attrs.FONT_FAMILY, size = attrs.CONTENT_FONT_SIZE)
        font_link.config(underline = True)

        # TODO: New row: the logo image label.
        row_count = 0  # Make it convenient to index the row of the grid.
        ttk.Label(self.__parent, text = '(logo image placeholder)').grid(columnspan = column_num, row = row_count)

        # New row: the role label.
        row_count += 1
        ttk.Label(self.__parent, style = styles.CONTENT_LABEL, text = 'Role:').grid(columnspan = column_num, padx = attrs.PADDING_X, pady = attrs.PADDING_Y, row = row_count, sticky = W)

        # New row: the role combobox.
        row_count += 1
        self.__role_list = ['Customer', 'Manager', 'Operator']
        self.__variable_role = StringVar()
        self.__combobox_role = ttk.Combobox(self.__parent, font = font_dict['content_font'], state = 'readonly', textvariable = self.__variable_role, values = self.__role_list)
        self.__combobox_role.grid(columnspan = column_num, padx = attrs.PADDING_X, row = row_count, sticky = (E, W))
        self.__combobox_role.bind('<<ComboboxSelected>>', self.__select_role)

        # New row: the username label.
        row_count += 1
        ttk.Label(self.__parent, style = styles.CONTENT_LABEL, text = 'Username:').grid(columnspan = column_num, padx = attrs.PADDING_X, pady = attrs.PADDING_Y, row = row_count, sticky = W)

        # New row: the username entry.
        row_count += 1
        self.__variable_username = StringVar()
        self.__entry_username = ttk.Entry(self.__parent, font = font_dict['content_font'], textvariable = self.__variable_username)
        self.__entry_username.grid(columnspan = column_num, padx = attrs.PADDING_X, row = row_count, sticky = (E, W))
        self.__entry_username.focus()

        # New row: the password label.
        row_count += 1
        ttk.Label(self.__parent, style = styles.CONTENT_LABEL, text = 'Password:').grid(columnspan = column_num, padx = attrs.PADDING_X, pady = attrs.PADDING_Y, row = row_count, sticky = W)

        # New row: the password entry.
        row_count += 1
        self.__variable_password = StringVar()
        self.__entry_password = ttk.Entry(self.__parent, font = font_dict['content_font'], show = '*', textvariable = self.__variable_password)
        self.__entry_password.grid(columnspan = column_num, padx = attrs.PADDING_X, row = row_count, sticky = (E, W))

        # New row: placeholder.
        row_count += 1
        ttk.Label(self.__parent, style = styles.PLACEHOLDER_LABEL).grid(columnspan = 2, row = row_count)

        # New row: the login button.
        row_count += 1
        self.__button_login = ttk.Button(self.__parent, command = self.__log_in, text = 'Log in')
        self.__button_login.grid(columnspan = column_num, padx = attrs.PADDING_X, pady = attrs.PADDING_Y, row = row_count, sticky = (E, W))

        # New row: the label for questioning sign-up status.
        row_count += 1
        column_count = 0  # Make it convenient to index the column of the grid.
        ttk.Label(self.__parent, style = styles.CONTENT_LABEL, text = 'New here?').grid(column = column_count, row = row_count, sticky = E)

        # Same row, new column: the sign-up label.
        column_count += 1
        self.__label_signup = ttk.Label(self.__parent, font = font_link, style = styles.LINK_LABEL, text = 'Sign up now.')
        self.__label_signup.grid(column = column_count, row = row_count, sticky = W)
        self.__label_signup.bind('<Button-1>', self.__goto_signup)
        self.__tooltip_signup = Tooltip(self.__label_signup, None)

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

        if self.__combobox_role.get() == self.__role_list[0]:
            self.__label_signup['state'] = '!disabled'
            self.__tooltip_signup.set_text()
            self.__label_signup.bind('<Enter>', self.__enter_label_signup)
            self.__label_signup.bind('<Leave>', self.__leave_label_signup)
        else:
            self.__label_signup['state'] = 'disabled'
            self.__tooltip_signup.set_text('You can only sign up as a customer.')

        self.__entry_username.focus()

    def __log_in(self) -> None:
        '''
        Log the user with the selected role in when the specified button is clicked.
        '''

        pass

    # noinspection PyUnusedLocal
    def __enter_label_signup(self, event) -> None:
        '''
        Execute actions when the mouse enters the specified label.

        Parameters
        ----------
        event : the event bound to the widget calling this function
        '''

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

        if str(self.__label_signup['state']) != 'disabled':
            self.__label_signup['state'] = '!active'

    # noinspection PyUnusedLocal
    def __goto_signup(self, event) -> None:
        '''
        Go to the sign-up view.

        Parameters
        ----------
        event : the event bound to the widget calling this function
        '''

        if str(self.__label_signup['state']) != 'disabled':
            self.__label_signup.focus()
            self.__entry_username.focus()

            if self.__signup_window is None:
                self.__signup_window = Toplevel(self.__parent)
                self.__signup_window.protocol('WM_DELETE_WINDOW', self.__reset_signup_window)
                SignupView(self.__signup_window)
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