'''
Description: the definition of a sign-up view
Version: 1.0.0.20210130
Author: Arvin Zhao
Date: 2021-01-30 18:31:28
Last Editors: Arvin Zhao
LastEditTime: 2021-01-30 18:31:39
'''

from tkinter import font, StringVar, ttk, Tk
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
        parent : the parent window for the sign-up view to display
        '''

        self.parent = parent
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        parent_width = 300
        parent_height = 500
        column_num = 2

        self.parent.geometry('%dx%d+%d+%d' % (parent_width, parent_height, (screen_width - parent_width) / 2, (screen_height - parent_height) / 2))  # Centre the parent window.
        self.parent.title('Sign up')
        self.parent.iconbitmap()  # TODO: add the path of the ICO image.

        # Enable auto-resizing controls with the grid geometry manager.
        for index in range(column_num):
            self.parent.columnconfigure(index, weight = 1)

        font_dict = styles.apply_style()

        # The link font.
        font_link = font.Font(family = attrs.FONT_FAMILY, size = attrs.CONTENT_FONT_SIZE)
        font_link.config(underline = True)

        # TODO: New row: the logo image label.
        row_count = 0  # Make it convenient to index the row of the grid.
        ttk.Label(self.parent, text = '(logo image placeholder)').grid(columnspan = column_num, row = row_count)

        # New row: the username label.
        row_count += 1
        ttk.Label(self.parent, style = styles.CONTENT_LABEL, text = 'Username:').grid(columnspan = column_num, padx = attrs.PADDING_X, pady = attrs.PADDING_Y, row = row_count, sticky = W)

        # New row: the username entry.
        row_count += 1
        self.variable_username = StringVar()
        self.entry_username = ttk.Entry(self.parent, font = font_dict['content_font'], textvariable = self.variable_username)
        self.entry_username.grid(columnspan = column_num, padx = attrs.PADDING_X, row = row_count, sticky = (E, W))
        self.entry_username.focus()

        # New row: the password label.
        row_count += 1
        ttk.Label(self.parent, style = styles.CONTENT_LABEL, text = 'Password:').grid(columnspan = column_num, padx = attrs.PADDING_X, pady = attrs.PADDING_Y, row = row_count, sticky = W)

        # New row: the password entry.
        row_count += 1
        self.variable_password = StringVar()
        self.entry_password = ttk.Entry(self.parent, font = font_dict['content_font'], show = '*', textvariable = self.variable_password)
        self.entry_password.grid(columnspan = column_num, padx = attrs.PADDING_X, row = row_count, sticky = (E, W))

        # New row: the password confirmation label.
        row_count += 1
        ttk.Label(self.parent, style=styles.CONTENT_LABEL, text='Confirm password:').grid(columnspan = column_num, padx = attrs.PADDING_X, pady = attrs.PADDING_Y, row = row_count, sticky = W)

        # New row: the password confirmation entry.
        row_count += 1
        self.variable_confirm_password = StringVar()
        self.entry_confirm_password = ttk.Entry(self.parent, font = font_dict['content_font'], show = '*', textvariable = self.variable_confirm_password)
        self.entry_confirm_password.grid(columnspan = column_num, padx = attrs.PADDING_X, row = row_count, sticky = (E, W))

        # New row: placeholder.
        row_count += 1
        ttk.Label(self.parent, style = styles.PLACEHOLDER_LABEL).grid(columnspan = 2, row = row_count)

        # New row: the sign-up button.
        row_count += 1
        self.button_signup = ttk.Button(self.parent, command = self.__sign_up, text = 'Sign up')
        self.button_signup.grid(columnspan = column_num, padx = attrs.PADDING_X, pady = attrs.PADDING_Y, row = row_count, sticky = (E, W))

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