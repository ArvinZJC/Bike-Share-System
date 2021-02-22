'''
Description: the definition of a bike tracking view
Version: 1.0.0.20210222
Author: Arvin Zhao
Date: 2021-02-22 05:06:32
Last Editors: Arvin Zhao
LastEditTime: 2021-02-22 05:06:45
'''

from tkinter import ttk
from tkinter.constants import BOTH, BOTTOM, E, END, HORIZONTAL, RIGHT, VERTICAL, X, Y

from bss.temp import rental  # TODO
from bss.conf import attrs
from bss.ui.conf import attrs as ui_attrs, styles
from bss.ui.utils import img_path as img


class TrackingView:
    '''
    The class for creating a bike tracking view.
    '''

    def __init__(self, parent) -> None:
        '''
        The constructor of the class for creating a bike tracking view.
        Only operators can have access to this view.

        Parameters
        ----------
        parent : the parent window for the bike tracking view to display
        '''

        self.__TOTAL_TEXT = 'Total number of bikes: '
        self.__AVAILABLE = 'Available'
        self.__BUSY = 'Busy'
        self.__DEFECTIVE = 'Defective'

        self.__parent = parent
        screen_width = self.__parent.winfo_screenwidth()
        screen_height = self.__parent.winfo_screenheight()
        parent_width = 800
        parent_height = 500

        self.__parent.geometry('%dx%d+%d+%d' % (parent_width, parent_height, (screen_width - parent_width) / 2, (screen_height - parent_height) / 2))  # Centre the parent window.
        self.__parent.title('Bike tracking report')
        self.__parent.iconbitmap(img.get_img_path(attrs.APP_ICON_FILENAME))
        self.__parent.minsize(parent_width, parent_height)

        styles.apply_style()
        self.__bike_data = rental.track_bikes()

        # Scrollbars.
        scrollbar_x = ttk.Scrollbar(self.__parent, orient = HORIZONTAL)
        scrollbar_y = ttk.Scrollbar(self.__parent, orient = VERTICAL)

        ttk.Label(self.__parent, style=styles.PLACEHOLDER_LABEL).pack()  # New row: placeholder.

        # New row: a label for the total number of bikes.
        self.__label_total = ttk.Label(self.__parent, style = styles.PRIMARY_LABEL)
        self.__label_total['text'] = self.__TOTAL_TEXT + str(len(self.__bike_data))
        self.__label_total.pack(fill = X, padx = ui_attrs.PADDING_X, pady = ui_attrs.PADDING_Y)

        # New row: a bike table.
        self.__table_column_list = ['ID', 'Damage level (est.)', 'Location', 'Status']
        self.__treeview_bike = ttk.Treeview(self.__parent, columns = self.__table_column_list, show = 'headings', xscrollcommand = scrollbar_x.set, yscrollcommand = scrollbar_y.set)

        for col in self.__table_column_list:
            self.__treeview_bike.heading(col, text = col, command = '' if col == self.__table_column_list[2] else (lambda _col = col: self.__sort(_col, True)))
            self.__treeview_bike.column(col, anchor = E)

        self.__insert()
        self.__sort(self.__table_column_list[0], False)  # Sort by ID in ascending order first.
        scrollbar_x['command'] = self.__treeview_bike.xview
        scrollbar_y['command'] = self.__treeview_bike.yview
        scrollbar_x.pack(fill = X, side = BOTTOM)
        scrollbar_y.pack(fill = Y, side = RIGHT)
        self.__treeview_bike.pack(expand = True, fill = BOTH, padx = ui_attrs.PADDING_X, pady = ui_attrs.PADDING_Y)

        ttk.Label(self.__parent, style=styles.PLACEHOLDER_LABEL).pack()  # New row: placeholder.

        self.__parent.after(attrs.REFRESHING_INTERVAL, self.__refresh_table)  # Refresh the table regularly.

    def __insert(self) -> None:
        '''
        Insert data to the table.
        '''

        for bike in self.__bike_data:
            status = (self.__AVAILABLE if bike[4] == attrs.AVAILABLE_BIKE_CODE else self.__BUSY) if bike[1] < attrs.DEFECTIVE_BIKE_THRESHOLD else self.__DEFECTIVE
            self.__treeview_bike.insert('', END, values = (bike[0], bike[1], '(' + str(bike[2]) + ',' + str(bike[3]) + ')', status))

    def __sort(self, col: str, reverse: bool) -> None:
        '''
        Sort data when a specified column header is clicked.

        Parameters
        ----------
        col : a column name
        reverse : a flag indicating if it should be in reverse order or not
        '''

        if col == self.__table_column_list[0]:
            col_value_key_list = [(int(self.__treeview_bike.set(key, col)), key) for key in self.__treeview_bike.get_children('')]
        elif col == self.__table_column_list[1]:
            col_value_key_list = [(float(self.__treeview_bike.set(key, col)), key) for key in self.__treeview_bike.get_children('')]
        else:
            col_value_key_list = [(self.__treeview_bike.set(key, col), key) for key in self.__treeview_bike.get_children('')]

        col_value_key_list.sort(reverse = reverse)

        for index, (_, key) in enumerate(col_value_key_list):
            self.__treeview_bike.move(key, '', index)

        self.__treeview_bike.heading(col, command = lambda: self.__sort(col, not reverse))

    def __refresh_table(self) -> None:
        '''
        Refresh the table when necessary.
        '''

        new_bike_data = rental.track_bikes()

        if new_bike_data != self.__bike_data:
            [self.__treeview_bike.delete(record) for record in self.__treeview_bike.get_children()]
            self.__bike_data = new_bike_data
            self.__insert()

        self.__parent.after(attrs.REFRESHING_INTERVAL, self.__refresh_table)  # It is needed here to ensure the table can be refreshed regularly.


# Test purposes only.
if __name__ == '__main__':
    from tkinter import Tk

    tracking_window = Tk()
    TrackingView(tracking_window)
    tracking_window.mainloop()