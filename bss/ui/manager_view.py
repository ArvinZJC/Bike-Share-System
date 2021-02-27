from tkinter import messagebox, Toplevel, ttk
from tkinter.constants import E, S, W
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

from PIL import Image, ImageTk

from bss import account
from bss.conf import attrs
from bss.manager import Manager
from bss.ui.about_view import AboutView
from bss.ui.chart_view import ChartView
from bss.ui.conf import attrs as ui_attrs, styles
from bss.ui.utils import img_path as img
from bss.ui.utils.tooltip import Tooltip


class ManagerView:
    '''
    The class for creating a manager view which is the home view for managers.
    '''

    def __init__(self, parent, user: Manager, toplevel = None) -> None:
        '''
        The constructor of the class for creating a manager view.
        Only managers can have access to this view.

        Parameters
        ----------
        parent : the parent window for the manager view to display
        user : a `Manager` object
        toplevel : the top-level widget of the manager view
        '''

        chart_index = 0
        self.__COMPANY = chart_index
        self.__COMPANY_TITLE = 'Company growth over time'
        chart_index += 1
        self.__CUSTOMER_BOX = chart_index
        self.__CUSTOMER_BOX_TITLE = 'Customer behaviour (box charts)'
        chart_index += 1
        self.__CUSTOMER_HIST = chart_index
        self.__CUSTOMER_HIST_TITLE = 'Customer behaviour (histograms)'
        chart_index += 1
        self.__BIKE = chart_index
        self.__BIKE_TITLE = 'Bike quality'
        chart_index += 1
        self.__FREQUENCY = chart_index
        self.__FREQUENCY_TITLE = 'Daily usage frequency'
        chart_index += 1
        self.__OPERATOR = chart_index
        self.__OPERATOR_TITLE = "Operators' response time"

        self.__parent = parent
        self.__user = user
        self.__toplevel = toplevel
        screen_width = self.__parent.winfo_screenwidth()
        screen_height = self.__parent.winfo_screenheight()
        parent_width = 350
        parent_height = 600
        column_num = 2
        self.__chart_window_company = None
        self.__chart_window_customer_box = None
        self.__chart_window_customer_hist = None
        self.__chart_window_bike = None
        self.__chart_window_frequency = None
        self.__chart_window_operator = None

        self.__parent.geometry('%dx%d+%d+%d' % (parent_width, parent_height, (screen_width - parent_width) / 2, (screen_height - parent_height) / 2))  # Centre the parent window.
        self.__parent.title('Home')
        self.__parent.iconbitmap(img.get_img_path(attrs.APP_ICON_FILENAME))
        self.__parent.minsize(parent_width, parent_height)
        self.__parent.maxsize(int(parent_width * 1.5), parent_height + 50)

        for index in range(column_num):
            self.__parent.columnconfigure(index, weight = 1)

        styles.apply_style()

        # New row: placeholder.
        row_index = 0  # Make it convenient to index the row of the grid.
        ttk.Label(self.__parent, style = styles.PLACEHOLDER_LABEL).grid(columnspan = column_num, row = row_index)
        self.__parent.rowconfigure(row_index, weight = 0)

        # New row: the avatar image label.
        row_index += 1
        label_avatar = ttk.Label(self.__parent)
        image_avatar = Image.open(img.get_img_path(attrs.MANAGER_AVATAR_FILENAME)).resize((ui_attrs.AVATAR_LENGTH, ui_attrs.AVATAR_LENGTH), Image.ANTIALIAS)
        label_avatar.image = ImageTk.PhotoImage(image_avatar)
        label_avatar['image'] = label_avatar.image  # Keep a reference to prevent GC.
        label_avatar.grid(columnspan = column_num, padx = ui_attrs.PADDING_X, pady = ui_attrs.PADDING_Y, row = row_index)
        self.__parent.rowconfigure(row_index, weight = 0)

        # New row: the username label.
        row_index += 1
        ttk.Label(self.__parent, style = styles.PRIMARY_LABEL, text = self.__user.get_name()).grid(columnspan = column_num, padx = ui_attrs.PADDING_X, row = row_index)
        self.__parent.rowconfigure(row_index, weight = 0)

        # New row: placeholder.
        row_index += 1
        ttk.Label(self.__parent, style = styles.PLACEHOLDER_LABEL).grid(columnspan = column_num, row = row_index)
        self.__parent.rowconfigure(row_index, weight = 0)

        # New row: a separator.
        row_index += 1
        ttk.Separator(self.__parent).grid(columnspan = column_num, padx = ui_attrs.PADDING_Y, row = row_index, sticky = (E, W))
        self.__parent.rowconfigure(row_index, weight = 0)

        # New row: the info label.
        row_index += 1
        self.__label_info = ttk.Label(self.__parent, style = styles.CONTENT_LABEL, text = 'Hints:\n'
                                                                                          '1. Click a button to show a chart.\n'
                                                                                          '2. Multiple chart windows can be kept opening at the same time. You do not need to close a chart window to open another one.')
        self.__label_info.grid(columnspan = column_num, padx = ui_attrs.PADDING_X, row = row_index)
        self.__parent.rowconfigure(row_index, weight = 0)

        # New row: placeholder.
        row_index += 1
        ttk.Label(self.__parent, style = styles.PLACEHOLDER_LABEL).grid(columnspan = column_num, row = row_index)
        self.__parent.rowconfigure(row_index, weight = 0)

        # New row: the button for showing the company growth chart.
        row_index += 1
        ttk.Button(self.__parent, command = lambda: self.__goto_chart(self.__COMPANY), text = self.__COMPANY_TITLE).grid(columnspan = column_num, padx = ui_attrs.PADDING_X, row = row_index, sticky = (E, W))
        self.__parent.rowconfigure(row_index, weight = 0)

        # New row: placeholder.
        row_index += 1
        ttk.Label(self.__parent, style = styles.PLACEHOLDER_LABEL).grid(columnspan = column_num, row = row_index)
        self.__parent.rowconfigure(row_index, weight = 0)

        # New row: the button for showing the customer behaviour box chart.
        row_index += 1
        ttk.Button(self.__parent, command = lambda: self.__goto_chart(self.__CUSTOMER_BOX), text = self.__CUSTOMER_BOX_TITLE).grid(columnspan = column_num, padx = ui_attrs.PADDING_X, row = row_index, sticky = (E, W))
        self.__parent.rowconfigure(row_index, weight = 0)

        # New row: placeholder.
        row_index += 1
        ttk.Label(self.__parent, style = styles.PLACEHOLDER_LABEL).grid(columnspan = column_num, row = row_index)
        self.__parent.rowconfigure(row_index, weight = 0)

        # New row: the button for showing the customer behaviour histogram chart.
        row_index += 1
        ttk.Button(self.__parent, command = lambda: self.__goto_chart(self.__CUSTOMER_HIST), text = self.__CUSTOMER_HIST_TITLE).grid(columnspan = column_num, padx = ui_attrs.PADDING_X, row = row_index, sticky = (E, W))
        self.__parent.rowconfigure(row_index, weight = 0)

        # New row: placeholder.
        row_index += 1
        ttk.Label(self.__parent, style = styles.PLACEHOLDER_LABEL).grid(columnspan = column_num, row = row_index)
        self.__parent.rowconfigure(row_index, weight = 0)

        # New row: the button for showing the bike quality chart.
        row_index += 1
        ttk.Button(self.__parent, command = lambda: self.__goto_chart(self.__BIKE), text = self.__BIKE_TITLE).grid(columnspan = column_num, padx = ui_attrs.PADDING_X, row = row_index, sticky = (E, W))
        self.__parent.rowconfigure(row_index, weight = 0)

        # New row: placeholder.
        row_index += 1
        ttk.Label(self.__parent, style = styles.PLACEHOLDER_LABEL).grid(columnspan = column_num, row = row_index)
        self.__parent.rowconfigure(row_index, weight = 0)

        # New row: the button for showing the daily usage frequency chart.
        row_index += 1
        ttk.Button(self.__parent, command = lambda: self.__goto_chart(self.__FREQUENCY), text = self.__FREQUENCY_TITLE).grid(columnspan = column_num, padx = ui_attrs.PADDING_X, row = row_index, sticky = (E, W))
        self.__parent.rowconfigure(row_index, weight = 0)

        # New row: placeholder.
        row_index += 1
        ttk.Label(self.__parent, style = styles.PLACEHOLDER_LABEL).grid(columnspan = column_num, row = row_index)
        self.__parent.rowconfigure(row_index, weight = 0)

        # New row: the button for showing the operators' response time chart.
        row_index += 1
        ttk.Button(self.__parent, command = lambda: self.__goto_chart(self.__OPERATOR), text = self.__OPERATOR_TITLE).grid(columnspan = column_num, padx = ui_attrs.PADDING_X, row = row_index, sticky = (E, W))
        self.__parent.rowconfigure(row_index, weight = 0)

        # New row: the log-out button
        row_index += 1
        column_index = 0  # Make it convenient to index the column of the grid.
        ttk.Button(self.__parent, command = self.__log_out, text = 'Log out').grid(column = column_index, padx = ui_attrs.PADDING_X, row = row_index, sticky = (S, W))
        self.__parent.rowconfigure(row_index, weight = 1)

        # Same row, new column: the about-app button.
        column_index += 1
        button_about = ttk.Button(self.__parent, command = self.__goto_about)
        image_about = Image.open(img.get_img_path(attrs.ABOUT_FILENAME)).resize((ui_attrs.PRIMARY_FONT_SIZE, ui_attrs.PRIMARY_FONT_SIZE), Image.ANTIALIAS)
        button_about.image = ImageTk.PhotoImage(image_about)
        button_about['image'] = button_about.image  # Keep a reference to prevent GC.
        button_about.grid(column = column_index, padx = ui_attrs.PADDING_X, row = row_index, sticky = (E, S))
        Tooltip(button_about, 'About ' + attrs.APP_NAME)

        # New row: placeholder.
        row_index += 1
        ttk.Label(self.__parent, style = styles.PLACEHOLDER_LABEL).grid(row = row_index, pady = ui_attrs.PADDING_Y)
        self.__parent.rowconfigure(row_index, weight = 0)

        # Bind events.
        self.__parent.protocol('WM_DELETE_WINDOW', lambda: self.__log_out(False))
        self.__parent.bind('<Configure>', self.__resize_frames)

    # noinspection PyUnusedLocal
    def __resize_frames(self, event) -> None:
        '''
        Auto-resize the two frames.

        Parameters
        ----------
        event : the event bound to the widget calling this function
        '''

        self.__label_info['wraplength'] = self.__parent.winfo_width() - ui_attrs.PADDING_X * 2

    def __goto_about(self) -> None:
        '''
        Go to the about-app view.
        '''

        self.__parent.focus()
        about_window = Toplevel(self.__parent)
        about_window.focus()
        about_window.grab_set()
        AboutView(about_window, attrs.MANAGER)
        about_window.mainloop()

    def __log_out(self, is_logout_button=True) -> None:
        '''
        Log out the account.
        Parameters
        ----------
        is_logout_button : a flag indicating if a user tries to log out himself/herself by clicking the log-out button
        '''

        if not is_logout_button and not messagebox.askyesno(attrs.APP_NAME, 'Are you sure you want to log out?'):
            return

        account.log_out(self.__user)
        self.__parent.destroy()
        self.__parent = None

        if self.__toplevel is not None:
            self.__toplevel.deiconify()

    def __goto_chart(self, chart_code: int) -> None:
        '''
        Go to the chart view.

        Parameters
        ----------
        chart_code : a chart code to navigate to the chart view with the corresponding content
        '''

        if chart_code == self.__COMPANY:
            fig = self.__user.plot_company()

            if self.__chart_window_company is None:
                self.__chart_window_company = Toplevel(self.__parent)
                self.__chart_window_company.protocol('WM_DELETE_WINDOW', lambda: self.__reset_chart(chart_code))
                self.__chart_window_company.focus()
                ChartView(self.__chart_window_company, self.__COMPANY_TITLE, fig)
                self.__chart_window_company.mainloop()
            else:
                self.__chart_window_company.focus()

        if chart_code == self.__CUSTOMER_BOX:
            fig = self.__user.plot_customer_box()

            if self.__chart_window_customer_box is None:
                self.__chart_window_customer_box = Toplevel(self.__parent)
                self.__chart_window_customer_box.protocol('WM_DELETE_WINDOW', lambda: self.__reset_chart(chart_code))
                self.__chart_window_customer_box.focus()
                ChartView(self.__chart_window_customer_box, self.__CUSTOMER_BOX_TITLE, fig)
                self.__chart_window_customer_box.mainloop()
            else:
                self.__chart_window_customer_box.focus()

        if chart_code == self.__CUSTOMER_HIST:
            fig = self.__user.plot_customer_hist()

            if self.__chart_window_customer_hist is None:
                self.__chart_window_customer_hist = Toplevel(self.__parent)
                self.__chart_window_customer_hist.protocol('WM_DELETE_WINDOW', lambda: self.__reset_chart(chart_code))
                self.__chart_window_customer_hist.focus()
                ChartView(self.__chart_window_customer_hist, self.__CUSTOMER_HIST_TITLE, fig)
                self.__chart_window_customer_hist.mainloop()
            else:
                self.__chart_window_customer_hist.focus()

        if chart_code == self.__BIKE:
            fig = self.__user.plot_bike()

            if self.__chart_window_bike is None:
                self.__chart_window_bike = Toplevel(self.__parent)
                self.__chart_window_bike.protocol('WM_DELETE_WINDOW', lambda: self.__reset_chart(chart_code))
                self.__chart_window_bike.focus()
                ChartView(self.__chart_window_bike, self.__BIKE_TITLE, fig)
                self.__chart_window_bike.mainloop()
            else:
                self.__chart_window_bike.focus()

        if chart_code == self.__FREQUENCY:
            fig = self.__user.plot_frequency()

            if self.__chart_window_frequency is None:
                self.__chart_window_frequency = Toplevel(self.__parent)
                self.__chart_window_frequency.protocol('WM_DELETE_WINDOW', lambda: self.__reset_chart(chart_code))
                self.__chart_window_frequency.focus()
                ChartView(self.__chart_window_frequency, self.__FREQUENCY_TITLE, fig)
                self.__chart_window_frequency.mainloop()
            else:
                self.__chart_window_frequency.focus()

        if chart_code == self.__OPERATOR:
            fig = self.__user.plot_operator()

            if self.__chart_window_operator is None:
                self.__chart_window_operator = Toplevel(self.__parent)
                self.__chart_window_operator.protocol('WM_DELETE_WINDOW', lambda: self.__reset_chart(chart_code))
                self.__chart_window_operator.focus()
                ChartView(self.__chart_window_operator, self.__OPERATOR_TITLE, fig)
                self.__chart_window_operator.mainloop()
            else:
                self.__chart_window_operator.focus()

    def __reset_chart(self, chart_code: int) -> None:
        '''
        Reset the chart view.

        Parameters
        ----------
        chart_code : a chart code to reset the chart view with the corresponding content
        '''

        if chart_code == self.__COMPANY:
            self.__chart_window_company.destroy()
            self.__chart_window_company = None

        if chart_code == self.__CUSTOMER_BOX:
            self.__chart_window_customer_box.destroy()
            self.__chart_window_customer_box = None

        if chart_code == self.__CUSTOMER_HIST:
            self.__chart_window_customer_hist.destroy()
            self.__chart_window_customer_hist = None

        if chart_code == self.__BIKE:
            self.__chart_window_bike.destroy()
            self.__chart_window_bike = None

        if chart_code == self.__FREQUENCY:
            self.__chart_window_frequency.destroy()
            self.__chart_window_frequency = None

        if chart_code == self.__OPERATOR:
            self.__chart_window_operator.destroy()
            self.__chart_window_operator = None


# Test purposes only.
if __name__ == '__main__':
    from tkinter import Tk

    manager_window = Tk()
    ManagerView(manager_window, Manager(3, 'xiaoran', '666666'))
    manager_window.mainloop()