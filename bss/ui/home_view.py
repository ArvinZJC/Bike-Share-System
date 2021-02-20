from tkinter import messagebox, Tk, ttk
from tkinter.constants import E, N, RAISED, S, SOLID, W

from PIL import Image, ImageTk
import numpy as np

from bss.conf import attrs
from bss.temp.customer.customer import Customer  # TODO
from bss.temp.customer import renter  # TODO
from bss.temp.mapping import Mapping  # TODO
from bss.ui.conf import attrs as ui_attrs, colours, styles
from bss.ui.utils import img_path as img
from bss.ui.utils.simpledialog import FloatDialogue
from bss.ui.utils.tooltip import Tooltip


class HomeView:
    '''
    The class for creating a home view.
    '''

    def __init__(self, parent, user) -> None:
        '''
        The constructor of the class for creating a home view.
        Customers and operator can have access to this view.

        Parameters
        ----------
        parent : the parent window for the home view to display
        user : a `Customer` or `OperatorWorker` object
        '''

        self.__parent = parent
        self.__user = user
        screen_width = self.__parent.winfo_screenwidth()
        screen_height = self.__parent.winfo_screenheight()
        self.__parent_width = 900
        self.__parent_height = 600
        self.__PICKUP_BIKE_TEXT = 'Pick up the bike'
        self.__DROP_BIKE_TEXT = 'Drop the bike'
        self.__can_move = True  # A flag used to control the ability of moving during some operations,

        self.__parent.geometry('%dx%d+%d+%d' % (self.__parent_width, self.__parent_height, (screen_width - self.__parent_width) / 2, (screen_height - self.__parent_height) / 2))  # Centre the parent window.
        self.__parent.title('Home')
        self.__parent.iconbitmap(img.get_img_path(attrs.APP_ICON_FILENAME))
        self.__parent.minsize(self.__parent_width, self.__parent_height)
        self.__parent.maxsize(int(self.__parent_width * 1.5), int(self.__parent_height * 1.5))

        self.__parent.rowconfigure(0, weight = 1)
        styles.apply_style()

        # New row: a dashboard frame.
        column_index = 0  # Make it convenient to index the column of the grid.
        frame_column_num = 2
        frame_dashboard = ttk.Frame(self.__parent, relief = RAISED)
        frame_dashboard.grid(row = 0, sticky = (E, N, S, W))
        frame_dashboard.columnconfigure(0, weight = 1)

        # New row in the dashboard frame: placeholder.
        frame_row_index = 0  # Make it convenient to index the row of the grid in the dashboard frame.
        ttk.Label(frame_dashboard, style = styles.PLACEHOLDER_LABEL).grid(columnspan = frame_column_num, row = frame_row_index)
        frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # New row in the dashboard frame: the avatar image label.
        frame_row_index += 1
        label_avatar = ttk.Label(frame_dashboard)
        label_avatar.grid(columnspan = frame_column_num, padx = ui_attrs.PADDING_X, pady = ui_attrs.PADDING_Y, row = frame_row_index)
        frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        if isinstance(self.__user, Customer):
            image_avatar = Image.open(img.get_img_path(attrs.CUSTOMER_AVATAR_FILENAME))
        else:
            image_avatar = Image.open(img.get_img_path(attrs.OPERATOR_AVATAR_FILENAME))

        image_avatar = image_avatar.resize((ui_attrs.AVATAR_LENGTH, ui_attrs.AVATAR_LENGTH), Image.ANTIALIAS)
        label_avatar.image = ImageTk.PhotoImage(image_avatar)
        label_avatar['image'] = label_avatar.image  # Keep a reference to prevent GC.

        # New row in the dashboard frame: the username label.
        frame_row_index += 1
        ttk.Label(frame_dashboard, style = styles.PRIMARY_LABEL, text = self.__user.get_name()).grid(columnspan = frame_column_num, padx = ui_attrs.PADDING_X, row = frame_row_index)
        frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # New row in the dashboard frame: the balance label.
        frame_row_index += 1
        self.__label_balance = ttk.Label(frame_dashboard, style = styles.EXPLANATION_LABEL)
        self.__label_balance.grid(columnspan = frame_column_num, padx = ui_attrs.PADDING_X, row = frame_row_index)
        self.__label_balance['text'] = self.__get_balance_text()
        frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # New row in the dashboard frame: placeholder.
        frame_row_index += 1
        ttk.Label(frame_dashboard, style = styles.PLACEHOLDER_LABEL).grid(row = frame_row_index)
        frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # New row in the dashboard frame: the top-up button.
        frame_row_index += 1
        ttk.Button(frame_dashboard, command = self.__topup, text = 'Top up').grid(columnspan = frame_column_num, padx = ui_attrs.PADDING_X, row = frame_row_index, sticky = (E, W))
        frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # New row in the dashboard frame: placeholder.
        frame_row_index += 1
        ttk.Label(frame_dashboard, style = styles.PLACEHOLDER_LABEL).grid(row = frame_row_index)
        frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # New row in the dashboard frame: a separator.
        frame_row_index += 1
        ttk.Separator(frame_dashboard).grid(columnspan = frame_column_num, padx = ui_attrs.PADDING_Y, row = frame_row_index, sticky = (E, W))
        frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # New row in the dashboard frame: placeholder.
        frame_row_index += 1
        ttk.Label(frame_dashboard, style = styles.PLACEHOLDER_LABEL).grid(row = frame_row_index)
        frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # New row in the dashboard frame: the button for picking up/dropping a bike.
        frame_row_index += 1
        self.__button_use_bike = ttk.Button(frame_dashboard, command = self.__use_bike, text = self.__PICKUP_BIKE_TEXT)
        self.__button_use_bike.grid(columnspan = frame_column_num, padx = ui_attrs.PADDING_X, row = frame_row_index, sticky = (E, W))
        frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # New row in the dashboard frame: TODO: bike renting info area
        frame_row_index += 1
        ttk.Label(frame_dashboard, style = styles.CONTENT_LABEL, text = 'Hint: use arrow keys to move.').grid(columnspan = frame_column_num, padx = ui_attrs.PADDING_X, pady = ui_attrs.PADDING_Y, row = frame_row_index)
        frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # New row in the dashboard frame: TODO: the log-out area
        frame_row_index += 1
        frame_column_index = 0
        ttk.Label(frame_dashboard, style = styles.CONTENT_LABEL, text = 'Log out').grid(column = frame_column_index, padx = ui_attrs.PADDING_X, row = frame_row_index, sticky = (S, W))
        frame_dashboard.rowconfigure(frame_row_index, weight = 1)

        # Same row, new column in the dashboard frame: TODO: the settings area
        frame_column_index += 1
        ttk.Label(frame_dashboard, style = styles.CONTENT_LABEL, text = 'Settings').grid(column = frame_column_index, padx = ui_attrs.PADDING_X, row = frame_row_index, sticky = (E, S))

        # New row in the dashboard frame: placeholder.
        frame_row_index += 1
        ttk.Label(frame_dashboard, style = styles.PLACEHOLDER_LABEL).grid(row = frame_row_index, pady = ui_attrs.PADDING_Y)
        frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # Same row, new column: a frame for the map area.
        column_index += 1
        frame_map_area = ttk.Frame(self.__parent, relief = RAISED)
        frame_map_area.grid(column = column_index, row = 0, sticky = (E, N, S, W))

        # In the frame for the map area: a map frame.
        frame_map = ttk.Frame(frame_map_area)
        frame_map.pack(expand = 1)

        # Map labels in the map frame.
        self.__mapping = Mapping(self.__user)
        self.__map_array = self.__mapping.get_state()
        self.__map_element_list = []  # Store rows of map elements.
        self.__image_empty_cell = Image.new('1', (ui_attrs.MAP_CELL_LENGTH, ui_attrs.MAP_CELL_LENGTH), color = colours.EMPTY_CELL_BACKGROUND)
        self.__image_avatar_cell = image_avatar.copy().resize((ui_attrs.MAP_CELL_LENGTH, ui_attrs.MAP_CELL_LENGTH), Image.ANTIALIAS)
        self.__image_available_bike = Image.open(img.get_img_path(attrs.AVAILABLE_BIKE_FILENAME)).resize((ui_attrs.MAP_CELL_LENGTH, ui_attrs.MAP_CELL_LENGTH), Image.ANTIALIAS)
        self.__image_bike_with_rider = Image.open(img.get_img_path(attrs.BIKE_WITH_RIDER_FILENAME)).resize((ui_attrs.MAP_CELL_LENGTH, ui_attrs.MAP_CELL_LENGTH), Image.ANTIALIAS)
        self.__image_defective_bike = Image.open(img.get_img_path(attrs.DEFECTIVE_BIKE_FILENAME)).resize((ui_attrs.MAP_CELL_LENGTH, ui_attrs.MAP_CELL_LENGTH), Image.ANTIALIAS)

        for row in range(attrs.MAP_LENGTH):
            map_element_row_list = []  # Store map elements of a row.

            for col in range(attrs.MAP_LENGTH):
                map_cell_list = []  # Store a label (Index 0) and its tooltip (Index 1) of this cell.
                label_map_cell = ttk.Label(frame_map, relief = SOLID)
                label_map_cell.grid(row = row, column = col)
                map_cell_list.append(label_map_cell)
                tooltip_text = 'Location: (%d, %d)' % (row, col)

                if self.__map_array[row, col] == attrs.AVATAR_CODE:
                    available_bike_count = len(renter.check_bikes([row, col]))
                    label_map_cell.image = ImageTk.PhotoImage(self.__image_avatar_cell)

                    if available_bike_count > 0:
                        tooltip_text = 'Location: (%d, %d)\nAvailable bike(s): %d' % (row, col, available_bike_count)
                elif self.__map_array[row, col] == attrs.AVAILABLE_BIKE_CODE:
                    label_map_cell.image = ImageTk.PhotoImage(self.__image_available_bike)
                    tooltip_text = 'Location: (%d, %d)\nAvailable bike(s): %d' % (row, col, len(renter.check_bikes([row, col])))
                elif self.__map_array[row, col] == attrs.DEFECTIVE_BIKE_CODE:
                    label_map_cell.image = ImageTk.PhotoImage(self.__image_defective_bike)
                else:
                    label_map_cell.image = ImageTk.PhotoImage(self.__image_empty_cell)

                label_map_cell['image'] = label_map_cell.image  # Keep a reference to prevent GC.
                tooltip_map_cell = Tooltip(label_map_cell, tooltip_text)
                map_cell_list.append(tooltip_map_cell)
                map_element_row_list.append(map_cell_list)

            self.__map_element_list.append(map_element_row_list)

        # Bind events.
        self.__parent.bind('<Configure>', self.__resize_frames)
        self.__parent.bind('<Left>', self.__move)
        self.__parent.bind('<Right>', self.__move)
        self.__parent.bind('<Up>', self.__move)
        self.__parent.bind('<Down>', self.__move)

        self.__parent.after(attrs.REFRESHING_INTERVAL, self.__refresh_map)  # Refresh the map regularly.

    def __get_balance_text(self) -> str:
        '''
        Get the balance text.

        Returns
        -------
        balance_text : the balance text
        '''

        return 'Balance: ￡' + '%.2f' % self.__user.get_balance()

    def __topup(self) -> None:
        '''
        Top up a customer account.
        '''

        result = FloatDialogue.askfloat('Top up', 'Enter the amount you want to top up (￡)\n(Please note that a maximum of 2 decimal places will be processed.)', minvalue = 0.01)

        if result is not None:
            amount_split = str(result).split('.')
            amount = float(amount_split[0] + '.' + amount_split[1][:2])
            self.__user.update_balance(amount)
            self.__label_balance['text'] = self.__get_balance_text()
            messagebox.showinfo(attrs.APP_NAME, 'Hurray! Your wallet has been topped up successfully.')

    def __use_bike(self) -> None:
        '''
        TODO: what about operators?
        '''

        if self.__user.get_balance() > 0:
            location = self.__user.get_location()

            # Drop a bike.
            if self.__user.get_flag():
                #self.__button_use_bike['text'] = self.__PICKUP_BIKE_TEXT
                pass
            # Attempt to pick up a bike.
            else:
                bike_result = renter.get_closest_bike(location)

                if isinstance(bike_result, list):
                    if len(bike_result) > 1:
                        pass
                    elif len(bike_result) == 1:
                        rented_bike = renter.renting(bike_result[0], location)

                        if rented_bike is None:
                            messagebox.showerror(attrs.APP_NAME, 'Oops! Your preferred bike may have been taken by someone else.')
                        else:
                            self.__button_use_bike['text'] = self.__DROP_BIKE_TEXT
                            self.__user.is_using_bike(True)
                            label_map_element = self.__map_element_list[location[0]][location[1]][0]
                            tooltip_map_element = self.__map_element_list[location[0]][location[1]][1]
                            label_map_element.image = ImageTk.PhotoImage(self.__image_bike_with_rider)
                            label_map_element['image'] = label_map_element.image
                            tooltip_map_element.set_text('Location: (%d, %d)' % (location[0], location[1]))
                    else:
                        messagebox.showerror(attrs.APP_NAME, 'Oops! Your preferred bike may have been taken by someone else.')
                else:
                    messagebox.showwarning(attrs.APP_NAME, bike_result)
        else:
            messagebox.showwarning(attrs.APP_NAME, 'Oops! Low balance! Please top up your wallet.')

    def __refresh_map(self) -> None:
        '''
        Refresh the map when necessary.
        '''

        new_map_array = self.__mapping.download()

        # Apply changes if any.
        if not np.array_equal(self.__map_array, new_map_array):
            for row in range(attrs.MAP_LENGTH):
                for col in range(attrs.MAP_LENGTH):
                    tooltip_map_element = self.__map_element_list[row][col][1]

                    # Reset the possible tooltips containing the number of available bikes regardless of any existing change.
                    if new_map_array[row, col] == self.__map_array[row][col]:
                        if new_map_array[row, col] == attrs.AVATAR_CODE:
                            available_bike_count = len(renter.check_bikes([row, col]))

                            if available_bike_count > 0:
                                tooltip_map_element.set_text('Location: (%d, %d)\nAvailable bike(s): %d' % (row, col, available_bike_count))
                        elif new_map_array[row, col] == attrs.AVAILABLE_BIKE_CODE:
                            tooltip_map_element.set_text('Location: (%d, %d)\nAvailable bike(s): %d' % (row, col, len(renter.check_bikes([row, col]))))
                    # Change the background image where necessary.
                    else:
                        label_map_element = self.__map_element_list[row][col][0]
                        tooltip_text = 'Location: (%d, %d)' % (row, col)

                        if new_map_array[row, col] == attrs.AVATAR_CODE:
                            available_bike_count = len(renter.check_bikes([row, col]))
                            label_map_element.image = ImageTk.PhotoImage(self.__image_bike_with_rider) if self.__user.get_flag() else ImageTk.PhotoImage(self.__image_avatar_cell)

                            if available_bike_count > 0:
                                tooltip_text = 'Location: (%d, %d)\nAvailable bike(s): %d' % (row, col, available_bike_count)
                        elif new_map_array[row, col] == attrs.AVAILABLE_BIKE_CODE:
                            label_map_element.image = ImageTk.PhotoImage(self.__image_available_bike)
                            tooltip_text = 'Location: (%d, %d)\nAvailable bike(s): %d' % (row, col, len(renter.check_bikes([row, col])))
                        elif new_map_array[row, col] == attrs.DEFECTIVE_BIKE_CODE:
                            label_map_element.image = ImageTk.PhotoImage(self.__image_defective_bike)
                        else:
                            label_map_element.image = ImageTk.PhotoImage(self.__image_empty_cell)

                        label_map_element['image'] = label_map_element.image
                        tooltip_map_element.set_text(tooltip_text)

            self.__mapping.set_map_array(new_map_array)
            self.__map_array = new_map_array

        self.__parent.after(attrs.REFRESHING_INTERVAL, self.__refresh_map)  # It is needed here to ensure the map can be refreshed regularly.

    # noinspection PyUnusedLocal
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
            self.__parent.columnconfigure(0, minsize = parent_width_new - parent_height_new, weight = 1)
            self.__parent.columnconfigure(1, minsize = parent_height_new, weight = 1)
        else:
            self.__parent.columnconfigure(0, minsize = self.__parent_width - self.__parent_height, weight = 1)
            self.__parent.columnconfigure(1, minsize = self.__parent_height, weight = 1)

    def __move(self, event) -> None:
        '''
        Move the avatar of a customer, or move a bike if the user is an operator.

        Parameters
        ----------
        event : the event bound to the widget calling this function
        '''

        if self.__can_move:
            if isinstance(self.__user, Customer):
                location = self.__user.get_location()
                label_map_element = self.__map_element_list[location[0]][location[1]][0]
                tooltip_map_element = self.__map_element_list[location[0]][location[1]][1]

                if (event.keysym == 'Left' and location[1] > 0)\
                        or (event.keysym == 'Right' and location[1] < attrs.MAP_LENGTH - 1)\
                        or (event.keysym == 'Up' and location[0] > 0)\
                        or (event.keysym == 'Down' and location[0] < attrs.MAP_LENGTH - 1):
                    available_bike_id_list = renter.check_bikes(location)
                    available_bike_count = len(available_bike_id_list)

                    if available_bike_count == 0:
                        defective_bike_id_list = renter.check_bikes(location, attrs.DEFECTIVE_BIKE_CODE)

                        if len(defective_bike_id_list) == 0:
                            label_map_element.image = ImageTk.PhotoImage(self.__image_empty_cell)
                            label_map_element['image'] = label_map_element.image
                        else:
                            label_map_element.image = ImageTk.PhotoImage(self.__image_defective_bike)
                            label_map_element['image'] = label_map_element.image
                    else:
                        label_map_element.image = ImageTk.PhotoImage(self.__image_available_bike)
                        label_map_element['image'] = label_map_element.image
                        tooltip_map_element.set_text('Location: (%d, %d)\nAvailable bike(s): %d' % (location[0], location[1], available_bike_count))

                    if event.keysym == 'Left':
                        location[1] -= 1
                    elif event.keysym == 'Right':
                        location[1] += 1
                    elif event.keysym == 'Up':
                        location[0] -= 1
                    else:
                        location[0] += 1

                    self.__user.set_location(location)
                    self.__mapping.set_state(location, attrs.AVATAR_CODE)
                    label_map_element = self.__map_element_list[location[0]][location[1]][0]
                    tooltip_map_element = self.__map_element_list[location[0]][location[1]][1]
                    label_map_element.image = ImageTk.PhotoImage(self.__image_bike_with_rider) if self.__user.get_flag() else ImageTk.PhotoImage(self.__image_avatar_cell)
                    label_map_element['image'] = label_map_element.image
                    available_bike_count = len(renter.check_bikes(location))

                    if available_bike_count > 0:
                        tooltip_map_element.set_text('Location: (%d, %d)\nAvailable bike(s): %d' % (location[0], location[1], available_bike_count))
            else:
                pass  # TODO: operator actions


# Test purposes only.
if __name__ == '__main__':
    from bss.temp.login import logging  # TODO

    home_window = Tk()
    HomeView(home_window, logging(attrs.CUSTOMER, 'jichen', '12345'))
    home_window.mainloop()