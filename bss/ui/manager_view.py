import sqlite3
import tkinter
from tkinter import messagebox, Toplevel, ttk
from tkinter.constants import E, N, RAISED, S, SOLID, W

import matplotlib
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from bss import account
from bss.conf import attrs
from bss.manager import Manager
from bss.ui.about_view import AboutView
from bss.ui.conf import attrs as ui_attrs, colours, styles
from bss.ui.utils import img_path as img
from bss.ui.utils.tooltip import Tooltip
from datetime import datetime
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
from bss.data import db_path as db



class ManagerView:
    '''
    The class for creating a manager view.
    '''

    def __init__(self, parent, user, toplevel=None) -> None:
        '''
        The constructor of the class for creating a manager view.
        Only managers can have access to this view.

        Parameters
        ----------
        parent : the parent window for the manager view to display
        user : a `Manager` object
        toplevel : the top-level widget of the manager view
        '''

        self.__parent = parent
        self.__user = user
        self.__toplevel = toplevel
        screen_width = self.__parent.winfo_screenwidth()
        screen_height = self.__parent.winfo_screenheight()
        self.__parent_width = 900
        self.__parent_height = 600
        self.__db_path = db.get_db_path()

        self.__parent.geometry(
            '%dx%d+%d+%d' % (self.__parent_width, self.__parent_height, (screen_width - self.__parent_width) / 2,
                             (screen_height - self.__parent_height) / 2))  # Centre the parent window.

        self.__parent.title('Manager')
        self.__parent.iconbitmap(img.get_img_path(attrs.APP_ICON_FILENAME))
        self.__parent.minsize(self.__parent_width, self.__parent_height)
        self.__parent.maxsize(int(self.__parent_width * 1.5), int(self.__parent_height * 1.5))

        self.__parent.rowconfigure(0, weight=1)
        #self.move_figure
        self.image1
        self.image1
        self.image2
        self.image3
        self.image4
        self.image4
        self.image6
        styles.apply_style()

        # New row: a dashboard frame.

        column_index = 0  # Make it convenient to index the column of the grid.
        frame_column_num = 2
        frame_dashboard = ttk.Frame(self.__parent, relief=RAISED)
        frame_dashboard.grid(row=0, sticky=(E, N, S, W))
        frame_dashboard.columnconfigure(0, weight=1)

        # New row in the dashboard frame: placeholder.
        frame_row_index = 0  # Make it convenient to index the row of the grid in the dashboard frame.
        ttk.Label(frame_dashboard, style=styles.PLACEHOLDER_LABEL).grid(columnspan=frame_column_num,
                                                                        row=frame_row_index)
        frame_dashboard.rowconfigure(frame_row_index, weight=0)

        # New row in the dashboard frame: the avatar image label.
        frame_row_index += 1
        label_avatar = ttk.Label(frame_dashboard)
        label_avatar.grid(columnspan=frame_column_num, padx=ui_attrs.PADDING_X, pady=ui_attrs.PADDING_Y,
                          row=frame_row_index)
        frame_dashboard.rowconfigure(frame_row_index, weight=0)

        image_avatar = Image.open(img.get_img_path(attrs.MANAGER_AVATAR_FILENAME)).resize(
            (ui_attrs.AVATAR_LENGTH, ui_attrs.AVATAR_LENGTH), Image.ANTIALIAS)
        label_avatar.image = ImageTk.PhotoImage(image_avatar)
        label_avatar['image'] = label_avatar.image  # Keep a reference to prevent GC.

        # New row in the dashboard frame: the username label.
        frame_row_index += 1
        ttk.Label(frame_dashboard, style=styles.PRIMARY_LABEL, text=user.name).grid(columnspan=frame_column_num,
                                                                                    padx=ui_attrs.PADDING_X,
                                                                                    row=frame_row_index)
        frame_dashboard.rowconfigure(frame_row_index, weight=0)

        # New row in the dashboard frame: placeholder.
        frame_row_index += 1
        ttk.Label(frame_dashboard, style=styles.PLACEHOLDER_LABEL).grid(row=frame_row_index)
        frame_dashboard.rowconfigure(frame_row_index, weight=0)

        # New row in the dashboard frame: the report label.
        frame_row_index += 1
        ttk.Label(frame_dashboard, style=styles.EXPLANATION_LABEL, text='manager report list').grid(
            columnspan=frame_column_num, padx=ui_attrs.PADDING_X, row=frame_row_index)
        frame_dashboard.rowconfigure(frame_row_index, weight=0)

        # New row in the dashboard frame: placeholder.
        frame_row_index += 1
        ttk.Label(frame_dashboard, style=styles.PLACEHOLDER_LABEL).grid(row=frame_row_index)
        frame_dashboard.rowconfigure(frame_row_index, weight=0)

        # New row in the dashboard frame: the growth over time image.
        frame_row_index += 1

        ttk.Button(frame_dashboard, command=self.image1, text='Growth of company over time').grid(
            columnspan=frame_column_num,
            padx=ui_attrs.PADDING_X,
            row=frame_row_index, sticky=(E, W))
        frame_dashboard.rowconfigure(frame_row_index, weight=0)

        # New row in the dashboard frame: placeholder.
        frame_row_index += 1
        ttk.Label(frame_dashboard, style=styles.PLACEHOLDER_LABEL).grid(row=frame_row_index)
        frame_dashboard.rowconfigure(frame_row_index, weight=0)

        # New row in the dashboard frame: User Behaviour Statistics v1.
        frame_row_index += 1
        ttk.Button(frame_dashboard, command=self.image2, text='User Behaviour Statistics v1').grid(
            columnspan=frame_column_num,
            padx=ui_attrs.PADDING_X,
            row=frame_row_index, sticky=(E, W))
        frame_dashboard.rowconfigure(frame_row_index, weight=0)

        # New row in the dashboard frame: placeholder.
        frame_row_index += 1
        ttk.Label(frame_dashboard, style=styles.PLACEHOLDER_LABEL).grid(row=frame_row_index)
        frame_dashboard.rowconfigure(frame_row_index, weight=0)

        # New row in the dashboard frame: Duration of Trips Image.
        frame_row_index += 1
        ttk.Button(frame_dashboard, command=self.image3, text='User Behaviour Statistics v2').grid(
            columnspan=frame_column_num,
            padx=ui_attrs.PADDING_X,
            row=frame_row_index, sticky=(E, W))
        frame_dashboard.rowconfigure(frame_row_index, weight=0)

        # New row in the dashboard frame: placeholder.
        frame_row_index += 1
        ttk.Label(frame_dashboard, style=styles.PLACEHOLDER_LABEL).grid(row=frame_row_index)
        frame_dashboard.rowconfigure(frame_row_index, weight=0)

        # New row in the dashboard frame: Cost of Trips Image.
        frame_row_index += 1
        ttk.Button(frame_dashboard, command=self.image4, text='Bike Statistics').grid(
            columnspan=frame_column_num,
            padx=ui_attrs.PADDING_X,
            row=frame_row_index,
            sticky=(E, W))
        frame_dashboard.rowconfigure(frame_row_index, weight=0)

        # New row in the dashboard frame: placeholder.
        frame_row_index += 1
        ttk.Label(frame_dashboard, style=styles.PLACEHOLDER_LABEL).grid(row=frame_row_index)
        frame_dashboard.rowconfigure(frame_row_index, weight=0)

        # New row in the dashboard frame: Breaking point of Bikes Image.
        frame_row_index += 1
        ttk.Button(frame_dashboard, command=self.image5, text='Daily Usage Frequency Analysis').grid(
            columnspan=frame_column_num,
            padx=ui_attrs.PADDING_X,
            row=frame_row_index, sticky=(E, W))
        frame_dashboard.rowconfigure(frame_row_index, weight=0)

        # New row in the dashboard frame: placeholder.
        frame_row_index += 1
        ttk.Label(frame_dashboard, style=styles.PLACEHOLDER_LABEL).grid(row=frame_row_index)
        frame_dashboard.rowconfigure(frame_row_index, weight=0)

        # New row in the dashboard frame: Number of Movements VS Times of Day Image.
        frame_row_index += 1
        ttk.Button(frame_dashboard, command=self.image6, text='Response Time from Workers').grid(
            columnspan=frame_column_num,
            padx=ui_attrs.PADDING_X,
            row=frame_row_index,
            sticky=(E, W))
        frame_dashboard.rowconfigure(frame_row_index, weight=0)

        # New row in the dashboard frame: placeholder.
        frame_row_index += 1
        ttk.Label(frame_dashboard, style=styles.PLACEHOLDER_LABEL).grid(row=frame_row_index)
        frame_dashboard.rowconfigure(frame_row_index, weight=0)

        # New row in the dashboard frame: the log-out button
        frame_row_index += 1
        frame_column_index = 0
        ttk.Button(frame_dashboard, command=self.__log_out, text='Log out').grid(column=frame_column_index,
                                                                                 padx=ui_attrs.PADDING_X,
                                                                                 row=frame_row_index, sticky=(S, W))
        frame_dashboard.rowconfigure(frame_row_index, weight=1)

        # Same row, new column in the dashboard frame: the about-app button.
        frame_column_index += 1
        button_about = ttk.Button(frame_dashboard, command=self.__goto_about)
        image_about = Image.open(img.get_img_path(attrs.ABOUT_FILENAME)).resize(
            (ui_attrs.PRIMARY_FONT_SIZE, ui_attrs.PRIMARY_FONT_SIZE), Image.ANTIALIAS)
        button_about.image = ImageTk.PhotoImage(image_about)
        button_about['image'] = button_about.image  # Keep a reference to prevent GC.
        button_about.grid(column=frame_column_index, padx=ui_attrs.PADDING_X, row=frame_row_index, sticky=(E, S))
        Tooltip(button_about, 'About ' + attrs.APP_NAME)

        # Bind events.
        self.__parent.protocol('WM_DELETE_WINDOW', lambda: self.__log_out(False))
        self.__parent.bind('<Configure>', self.__resize_frames)

    '''def move_figure(self, fig, x, y):
        """Move figure's upper left corner to pixel (x, y)"""
        backend = matplotlib.get_backend()
        if backend == 'TkAgg':
            fig.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
        elif backend == 'WXAgg':
            fig.canvas.manager.window.SetPosition((x, y))
        else:
            # This works for QT and GTK
            # You can also use window.setGeometry
            fig.canvas.manager.window.move(x, y)'''

    def image1(self):
        try:
            self.object.get_tk_widget().grid_forget()
        except AttributeError:
            pass

        frame_row_index = 0
        frame_column_num = 2

        conn = sqlite3.connect(self.__db_path)
        c = conn.cursor()

        transactions = pd.read_sql('Select * from transactions', conn)
        transactions['timeOfEvent'] = [datetime.strptime(i, "%b %d %Y %H:%M:%S").strftime('%b %d %Y') for i in
                                       transactions['timeOfEvent']]

        transactions = transactions.iloc[0:623]
        total = transactions['sumOfMoney'].cumsum() + 1000

        transactions_plot = transactions.groupby(['timeOfEvent']).sum()
        fig, ax = plt.subplots(1, 1, figsize=(7, 4))

        transactions_plot = transactions_plot.cumsum() + 1000
        ax.plot(total[::10], 'r-o', markeredgecolor='k', label='Growth over time')

        ax.grid()
        transactions_plot.head()
        ax.legend(loc='best')

        plt.title("Growth over time")
        plt.ylabel("Money in company's account")
        plt.xlabel("Dates")
        ax.set_xticklabels(transactions['timeOfEvent'][::80], rotation='vertical')
        plt.show()

        conn.close()
        self.object = FigureCanvasTkAgg(fig, master=manager_window)  # A tk.DrawingArea.
        self.object.draw()
        self.object.get_tk_widget().grid(columnspan=frame_column_num,
             row=frame_row_index)




    def image2(self):
        try:
            self.object.get_tk_widget().grid_forget()
        except AttributeError:
            pass

        frame_row_index = 0
        frame_column_num = 2

        conn = sqlite3.connect(self.__db_path)
        c = conn.cursor()

        transactions = pd.read_sql('Select distance from movement', conn)
        duration = pd.read_sql('Select duration from movement', conn)
        mins = [round((datetime.strptime(i, "%H:%M:%S") - datetime(1900, 1, 1)).total_seconds() / 60, 2) for i in
                duration[duration.columns[0]]]
        charges = pd.read_sql('Select sumOfMoney from transactions', conn)
        charges = charges[charges > 0].dropna()

        fig, ax = plt.subplots(1, 3, figsize=(5, 2))
        plt.subplot(1, 3, 1)
        plt.boxplot(transactions, notch=True, showmeans=True, meanline=True)
        plt.text(0.8, 28, s=str(round(transactions.values.max(), 2)))
        plt.text(0.8, 12, s=str(round(transactions.values.mean(), 2)))
        plt.text(0.8, 2, s=str(round(transactions.values.min(), 2)))

        plt.ylabel('Distance in Miles')
        plt.title('Distance Travelled')
        plt.xticks([])
        plt.grid('k', linewidth=2)

        plt.subplot(1, 3, 2)
        plt.boxplot(mins, notch=True, showmeans=True, meanline=True)
        plt.text(0.8, 66, s=str(round(pd.DataFrame(mins).values.max(), 2)))
        plt.text(0.8, 26, s=str(round(pd.DataFrame(mins).values.mean(), 2)))
        plt.text(0.8, 2, s=str(round(pd.DataFrame(mins).values.min(), 2)))

        plt.ylabel('Duration in Minutes')
        plt.title('Duration of Trips')
        plt.xticks([])
        plt.grid('k', linewidth=2)

        plt.subplot(1, 3, 3)
        plt.boxplot(charges, notch=True, showmeans=True, meanline=True)
        plt.text(0.8, 31, s=str(round(charges.values.max(), 2)))
        plt.text(0.8, 13, s=str(round(charges.values.mean(), 2)))
        plt.text(0.8, 2, s=str(round(charges.values.min(), 2)))

        plt.ylabel('Money')
        plt.title('Cost of Trips')
        plt.xticks([])
        plt.grid('k', linewidth=2)

        plt.show()

        conn.close()

        #root = tkinter.Tk()
        self.object = FigureCanvasTkAgg(fig, master=manager_window)  # A tk.DrawingArea.
        self.object.draw()
        self.object.get_tk_widget().grid(columnspan=frame_column_num,
             row=frame_row_index)

    def image3(self):
        try:
            self.object.get_tk_widget().grid_forget()
        except AttributeError:
            pass
        frame_row_index = 0
        frame_column_num = 2

        conn = sqlite3.connect(self.__db_path)
        c = conn.cursor()

        transactions = pd.read_sql('Select distance from movement', conn)
        duration = pd.read_sql('Select duration from movement', conn)
        duration = duration.iloc[0:430]
        transactions = transactions.iloc[0:430]

        mins = [round((datetime.strptime(i, "%H:%M:%S") - datetime(1900, 1, 1)).total_seconds() / 60, 2) for i in
                duration[duration.columns[0]]]
        charges = pd.read_sql('Select sumOfMoney from transactions', conn)
        charges = charges.iloc[0:623]
        charges = charges[charges > 0].dropna()

        fig, ax = plt.subplots(1, 3, figsize=(10, 4))
        plt.subplot(1, 3, 1)
        plt.hist(transactions, bins=10, color='b')
        plt.xlabel('Distance in Miles')
        plt.title('Distance Travelled Per Trip')
        plt.ylabel('Number of trips')
        plt.axvline(x=transactions.median()[0], color='r')
        plt.axvline(x=transactions.values.mean(), color='g')

        plt.text(7, 110, s='Median')
        plt.text(13, 100, s='Mean')
        plt.grid('k', axis='both', linewidth=2)

        plt.subplot(1, 3, 2)
        plt.hist(mins, bins=15, color='r')
        plt.axvline(x=transactions.median()[0], color='b', linewidth=2.0)
        plt.text(13, 65, s='Mean')

        plt.text(3, 60, s='Median')
        plt.text(13, 68, s='Mean')

        plt.xlabel('Duration in Minutes')
        plt.ylabel('Number of Trips')
        plt.title('Duration of Trips')
        plt.grid(axis='both', linewidth=1)

        plt.subplot(1, 3, 3)
        plt.hist(charges, bins=10, color='y')
        plt.xlabel('Money')
        plt.title('Cost Per Trip')
        plt.ylabel('Number of trips')
        plt.axvline(x=charges.median()[0], color='r')
        plt.axvline(x=charges.values.mean(), color='g')

        plt.text(8.5, 94, s='Median')
        plt.text(14, 90, s='Mean')
        plt.grid('k', axis='both', linewidth=2)

        plt.show()

        conn.close()

        #root = tkinter.Tk()
        self.object = FigureCanvasTkAgg(fig, master=manager_window)  # A tk.DrawingArea.
        self.object.draw()
        self.object.get_tk_widget().grid(columnspan=frame_column_num,
             row=frame_row_index)

    def image4(self):
        try:
            self.object.get_tk_widget().grid_forget()
        except AttributeError:
            pass

        frame_row_index = 0
        frame_column_num = 2

        conn = sqlite3.connect(self.__db_path)
        c = conn.cursor()

        point_of_break = pd.read_sql('Select defective_start from bike_status where defective_start<1', conn)
        point_of_break = point_of_break * 100
        point_of_break = point_of_break.iloc[0:200]

        fig, ax = plt.subplots(2, 1, figsize=(5, 4))
        plt.subplot(2, 1, 1)
        plt.boxplot(point_of_break, notch=True, vert=False, showmeans=True, meanline=True)
        plt.text(94.2, 1.2, s=str(round(point_of_break.values.max(), 2)))
        plt.text(82, 1.2, s=str(round(point_of_break.values.mean(), 2)))
        plt.text(32, 1.2, s=str(round(point_of_break.values.min(), 2)))

        plt.axvline(x=point_of_break.values.min(), color='r')
        plt.axvline(x=point_of_break.values.max(), color='b')
        plt.axvline(x=point_of_break.values.mean(), color='g')
        plt.title("Breaking Point of Bikes")
        plt.yticks([])
        plt.xticks([])

        plt.subplot(2, 1, 2)
        plt.hist(point_of_break, color='c')
        plt.ylabel('Number of Trips')
        plt.xlabel("% Defective")

        plt.show()

        conn.close()

        #root = tkinter.Tk()
        self.object = FigureCanvasTkAgg(fig, master=manager_window)  # A tk.DrawingArea.
        self.object.draw()
        self.object.get_tk_widget().grid(columnspan=frame_column_num,
             row=frame_row_index)

    def image5(self):
        try:
            self.object.get_tk_widget().grid_forget()
        except AttributeError:
            pass

        frame_row_index = 0
        frame_column_num = 2

        conn = sqlite3.connect(self.__db_path)
        c = conn.cursor()

        movements = pd.read_sql('Select endTime from movement', conn)
        movements = movements.iloc[0:430]

        movements = pd.DataFrame([datetime.strptime(i, "%b %d %Y %H:%M:%S").hour for i in movements['endTime']])
        movements = movements.value_counts().sort_index()
        indexes = [i[0] for i in movements.index.values]
        #fig, ax = plt.figure(figsize=(7, 3.5))
        fig, ax = plt.subplots(figsize=(7, 3.5))
        plt.bar(indexes, height=movements.values, color='c')
        plt.plot(indexes, movements.values, color='k', linestyle='--')
        plt.xticks(indexes)
        plt.yticks([10, 20, 30, 40, 50])
        plt.grid(axis='both')
        plt.title("Number of Movements vs Time of Day")
        plt.xlabel("Hours of a Day")
        plt.ylabel('No. Of Movements')

        plt.show()

        conn.close()

        #root = tkinter.Tk()
        self.object = FigureCanvasTkAgg(fig, master=manager_window)  # A tk.DrawingArea.
        self.object.draw()
        self.object.get_tk_widget().grid(columnspan=frame_column_num,
             row=frame_row_index)

    def image6(self):
        try:
            self.object.get_tk_widget().grid_forget()
        except AttributeError:
            pass

        frame_row_index = 0
        frame_column_num = 2

        conn = sqlite3.connect(self.__db_path)
        c = conn.cursor()

        start_time = pd.read_sql('Select id,time_of_event from bike_status where defective_start<1', conn)
        end_time = pd.read_sql('Select id,time_of_event from bike_status where defective_start=1', conn)
        start_time = start_time.iloc[0:198]
        end_time = end_time.iloc[0:198]
        start_time['end'] = 0
        for i in start_time['id'].unique():
            start_time['end'][start_time['id'] == i] = list(end_time['time_of_event'][end_time['id'] == i])

        broke_time = [datetime.strptime(i, "%b %d %Y %H:%M:%S") for i in start_time['time_of_event']]
        fixed_time = [datetime.strptime(i, "%b %d %Y %H:%M:%S") for i in start_time['end']]
        response_time = [j - i for i, j in zip(broke_time, fixed_time)]
        response_time = pd.DataFrame(
            [round(divmod(i.seconds, 3600)[0] + divmod(i.seconds, 3600)[1] / 3600) for i in response_time])
        response_time = response_time.value_counts().sort_index()
        indexes = [i[0] for i in response_time.index.values]
        response_time = list(response_time)
        for i in range(24):
            if i not in indexes:
                indexes.append(i)
                response_time.append(0)

        response_time = pd.DataFrame(response_time, index=indexes)
        response_time = response_time.sort_index()[0].values
        sorted(indexes)
        #fig, ax = plt.figure(figsize=(7, 3.5))#
        fig, ax = plt.subplots(figsize=(7, 3.5))
        plt.bar(indexes, height=response_time, color='g')
        plt.xticks(indexes)
        plt.yticks([5, 10, 15, 20, 25, 30, 35])
        plt.grid(axis='both')
        plt.title("Response_time")
        plt.xlabel("Hours")
        plt.ylabel('Times')
        plt.show()

        conn.close()

        #root = tkinter.Tk()
        self.object = FigureCanvasTkAgg(fig, master=manager_window)  # A tk.DrawingArea.
        self.object.draw()
        self.object.get_tk_widget().grid(columnspan=frame_column_num,
             row=frame_row_index)

    def __resize_frames(self, event) -> None:
        '''
        Auto-resize the two frames.

        Parameters
        ----------
        event : the event bound to the widget calling this function
        '''

        parent_width_new = self.__parent.winfo_width()
        parent_height_new = self.__parent.winfo_height()

        # Try to ensure the square map can take up as much space as possible.
        if parent_width_new - parent_height_new > self.__parent_width - self.__parent_height:
            self.__parent.columnconfigure(0, minsize=parent_width_new - parent_height_new, weight=1)
            self.__parent.columnconfigure(1, minsize=parent_height_new, weight=1)
        else:
            self.__parent.columnconfigure(0, minsize=self.__parent_width - self.__parent_height, weight=1)
            self.__parent.columnconfigure(1, minsize=self.__parent_height, weight=1)

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


if __name__ == '__main__':
    from tkinter import Tk

    manager_window = Tk()
    ManagerView(manager_window, Manager(3, 'xiaoran', '666666'))
    manager_window.mainloop()
