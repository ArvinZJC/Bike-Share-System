'''
Description: the definition of a login view
Version: 1.0.0.20210124
Author: Arvin Zhao
Date: 2021-01-24 15:03:00
Last Editors: Arvin Zhao
LastEditTime: 2021-01-24 18:23:21
'''

from tkinter import BooleanVar, Button, Checkbutton, Entry, font, Label, StringVar, Tk
from tkinter.constants import E, W


class LoginView:
    '''
    The class for creating a login view.
    '''

    def __init__(self, parent: Tk) -> None:
        '''
        The constructor of the class for creating a login view.

        Parameters
        ----------
        parent : the parent window for the login view to display
        '''

        self.parent = parent
        font_content = font.Font(self.parent, size = 12)  # TODO: consider conf file
        font_placeholder = font.Font(self.parent, size = 5)

        # Enable auto-resizing controls with the grid geometry manager.
        self.parent.columnconfigure(0, weight = 1)
        self.parent.columnconfigure(1, weight = 1)

        self.parent.geometry('300x500')
        self.parent.title('Lab1_2d')  # TODO: change the title

        Label(self.parent, text = '(TODO: image placeholder)').grid(columnspan = 2, row = 0)  # TODO: image

        Label(self.parent, font = font_placeholder).grid(columnspan = 2, row = 1)  # Placeholder.
        Label(self.parent, font = font_content, text = 'Username:').grid(columnspan = 2, padx = 15, pady = 5, row = 2, sticky = W)  # The username label.

        # The username entry.
        variable_username = StringVar()
        entry_username = Entry(self.parent, font = font_content, textvariable = variable_username)
        entry_username.grid(columnspan = 2, padx = 15, row = 3, sticky = (E, W))

        Label(self.parent, font = font_placeholder).grid(columnspan = 2, row = 4)  # Placeholder.
        Label(self.parent, font = font_content, text = 'Password:').grid(columnspan = 2, padx = 15, pady = 5, row = 5, sticky = W)  # The password label.

        # The password entry.
        variable_password = StringVar()
        entry_password = Entry(self.parent, font = font_content, show = '*', textvariable = variable_password)
        entry_password.grid(columnspan = 2, padx = 15, row = 6, sticky = (E, W))

        Label(self.parent, font = font_placeholder).grid(columnspan = 2, row = 7)  # Placeholder.

        # The check button for remembering me.
        variable_remember_me = BooleanVar(value = False)
        checkbutton_remember_me = Checkbutton(self.parent, font = font_content, text = 'Remember me', variable = variable_remember_me)
        checkbutton_remember_me.grid(columnspan = 2, padx = 15, pady = 5, row = 8, sticky = W)

        # The login button.
        button_login = Button(self.parent, background = '#0081FF', command = self.log_in, font = font_content, foreground = 'white', text = 'Log in')
        button_login.grid(columnspan = 2, padx = 15, row = 9, sticky = (E, W))

        Label(self.parent, font = font_content, text = 'New here?').grid(row = 10, pady = 5, sticky = E)  # The label for questioning sign-up status.

        # The sign-up label.
        font_sign_up = font_content.copy()
        font_sign_up.config(underline = True)
        label_sign_up = Label(self.parent, font = font_sign_up, foreground = '#0081FF', text = 'Sign up now.')
        label_sign_up.grid(column = 1, row = 10, pady = 5, sticky = W)
        label_sign_up.bind('<Button-1>', self.sign_up)

    def log_in(self) -> None:
        '''

        '''

        pass

    def sign_up(self, event) -> None:
        '''

        '''

        pass


# Test purposes only.
if __name__ == '__main__':
    login_window = Tk()
    LoginView(login_window)
    login_window.mainloop()