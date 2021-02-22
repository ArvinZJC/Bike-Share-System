from tkinter import Tk
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from bss.ui.login_view import LoginView


def main() -> None:
    '''
    The entry of the system.
    '''

    login_window = Tk()
    LoginView(login_window)
    login_window.mainloop()


if __name__ == '__main__':
    main()