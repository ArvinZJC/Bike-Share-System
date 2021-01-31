'''
Description: the definition of a sign-up view
Version: 1.0.1.20210131
Author: Arvin Zhao
Date: 2021-01-30 18:31:28
Last Editors: Arvin Zhao
LastEditTime: 2021-01-31 18:31:39
'''

from tkinter import StringVar, ttk, Tk
from tkinter.constants import E, W

from bss.ui.conf import attrs, styles


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
        __parent_width = 300
        __parent_height = 500
        column_num = 2

        self.__parent.geometry('%dx%d+%d+%d' % (__parent_width, __parent_height, (screen_width - __parent_width) / 2, (screen_height - __parent_height) / 2))  # Centre the __parent window.
        self.__parent.title('Sign up')
        self.__parent.iconbitmap()  # TODO: add the path of the ICO image.

        # Enable auto-resizing controls with the grid geometry manager.
        for index in range(column_num):
            self.__parent.columnconfigure(index, weight = 1)

        font_dict = styles.apply_style()

        # TODO: New row: the logo image label.
        row_count = 0  # Make it convenient to index the row of the grid.
        ttk.Label(self.__parent, text = '(logo image placeholder)').grid(columnspan = column_num, row = row_count)

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

        # New row: the password confirmation label.
        row_count += 1
        ttk.Label(self.__parent, style=styles.CONTENT_LABEL, text='Confirm password:').grid(columnspan = column_num, padx = attrs.PADDING_X, pady = attrs.PADDING_Y, row = row_count, sticky = W)

        # New row: the password confirmation entry.
        row_count += 1
        self.__variable_confirm_password = StringVar()
        self.__entry_confirm_password = ttk.Entry(self.__parent, font = font_dict['content_font'], show = '*', textvariable = self.__variable_confirm_password)
        self.__entry_confirm_password.grid(columnspan = column_num, padx = attrs.PADDING_X, row = row_count, sticky = (E, W))

        # New row: placeholder.
        row_count += 1
        ttk.Label(self.__parent, style = styles.PLACEHOLDER_LABEL).grid(columnspan = 2, row = row_count)

        # New row: the sign-up button.
        row_count += 1
        self.__button_signup = ttk.Button(self.__parent, command = self.__sign_up, text = 'Sign up')
        self.__button_signup.grid(columnspan = column_num, padx = attrs.PADDING_X, pady = attrs.PADDING_Y, row = row_count, sticky = (E, W))

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