from tkinter import messagebox, Toplevel, ttk
from tkinter.constants import E, N, RAISED, S, SOLID, W
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

from PIL import Image, ImageTk

from bss import rental, account, account as account_test
from bss.conf import attrs
from bss.customer import Customer
from bss.mapping import Mapping
from bss.operator import OperatorWorker
from bss.ui.about_view import AboutView
from bss.ui.conf import attrs as ui_attrs, colours, styles
from bss.ui.tracking_view import TrackingView
from bss.ui.utils import img_path as img
from bss.ui.utils.simpledialog import FloatDialogue, IntegerDialogue
from bss.ui.utils.tooltip import Tooltip


class HomeView:
    '''
    The class for creating a home view.
    '''

    def __init__(self, parent, user, toplevel = None) -> None:
        '''
        The constructor of the class for creating a home view.
        Customers and operators can have access to this view.

        Parameters
        ----------
        parent : the parent window for the home view to display
        user : a `Customer` or `OperatorWorker` object
        toplevel : the top-level widget of the home view
        '''

        self.__PICKUP_BIKE_TEXT = 'Pick up the bike'
        self.__DROP_BIKE_PAY_TEXT = 'Drop the bike and pay'
        self.__MOVE_BIKE_TEXT = 'Move the bike'
        self.__DROP_BIKE_TEXT = 'Drop the bike'
        self.__HINT_INFO = '\nHint: use arrow keys to move.\n'

        self.__parent = parent
        self.__user = user
        self.__toplevel = toplevel
        screen_width = self.__parent.winfo_screenwidth()
        screen_height = self.__parent.winfo_screenheight()
        self.__parent_width = 900
        self.__parent_height = 600
        self.__rented_bike = None
        self.__tracking_window = None

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
        self.__frame_dashboard = ttk.Frame(self.__parent, relief = RAISED)
        self.__frame_dashboard.grid(row = 0, sticky = (E, N, S, W))
        self.__frame_dashboard.columnconfigure(0, weight = 1)

        # New row in the dashboard frame: placeholder.
        frame_row_index = 0  # Make it convenient to index the row of the grid in the dashboard frame.
        ttk.Label(self.__frame_dashboard, style = styles.PLACEHOLDER_LABEL).grid(columnspan = frame_column_num, row = frame_row_index)
        self.__frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # New row in the dashboard frame: the avatar image label.
        frame_row_index += 1
        label_avatar = ttk.Label(self.__frame_dashboard)
        label_avatar.grid(columnspan = frame_column_num, padx = ui_attrs.PADDING_X, pady = ui_attrs.PADDING_Y, row = frame_row_index)
        self.__frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        if isinstance(self.__user, Customer):
            image_avatar = Image.open(img.get_img_path(attrs.CUSTOMER_AVATAR_FILENAME))
        else:
            image_avatar = Image.open(img.get_img_path(attrs.OPERATOR_AVATAR_FILENAME))

        image_avatar = image_avatar.resize((ui_attrs.AVATAR_LENGTH, ui_attrs.AVATAR_LENGTH), Image.ANTIALIAS)
        label_avatar.image = ImageTk.PhotoImage(image_avatar)
        label_avatar['image'] = label_avatar.image  # Keep a reference to prevent GC.

        # New row in the dashboard frame: the username label.
        frame_row_index += 1
        ttk.Label(self.__frame_dashboard, style = styles.PRIMARY_LABEL, text = self.__user.get_name()).grid(columnspan = frame_column_num, padx = ui_attrs.PADDING_X, row = frame_row_index)
        self.__frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        if isinstance(self.__user, OperatorWorker):
            # New row in the dashboard frame: the skill level label.
            frame_row_index += 1
            ttk.Label(self.__frame_dashboard, style = styles.EXPLANATION_LABEL, text = 'Skill level: ' + str(self.__user.get_skill_level())).grid(columnspan = frame_column_num, padx = ui_attrs.PADDING_X, row = frame_row_index)
            self.__frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # New row in the dashboard frame: the balance label.
        frame_row_index += 1
        self.__label_balance = ttk.Label(self.__frame_dashboard, style = styles.EXPLANATION_LABEL)
        self.__label_balance.grid(columnspan = frame_column_num, padx = ui_attrs.PADDING_X, row = frame_row_index)
        self.__update_balance_text()
        self.__frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        if isinstance(self.__user, Customer):
            # New row in the dashboard frame: placeholder.
            frame_row_index += 1
            ttk.Label(self.__frame_dashboard, style = styles.PLACEHOLDER_LABEL).grid(row = frame_row_index)
            self.__frame_dashboard.rowconfigure(frame_row_index, weight = 0)

            # New row in the dashboard frame: the top-up button.
            frame_row_index += 1
            ttk.Button(self.__frame_dashboard, command = self.__topup, text = 'Top up').grid(columnspan = frame_column_num, padx = ui_attrs.PADDING_X, row = frame_row_index, sticky = (E, W))
            self.__frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # New row in the dashboard frame: placeholder.
        frame_row_index += 1
        ttk.Label(self.__frame_dashboard, style = styles.PLACEHOLDER_LABEL).grid(row = frame_row_index)
        self.__frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # New row in the dashboard frame: a separator.
        frame_row_index += 1
        ttk.Separator(self.__frame_dashboard).grid(columnspan = frame_column_num, padx = ui_attrs.PADDING_Y, row = frame_row_index, sticky = (E, W))
        self.__frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # New row in the dashboard frame: placeholder.
        frame_row_index += 1
        ttk.Label(self.__frame_dashboard, style = styles.PLACEHOLDER_LABEL).grid(row = frame_row_index)
        self.__frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # New row in the dashboard frame: the button for picking up/moving/dropping a bike.
        frame_row_index += 1
        self.__button_use_bike = ttk.Button(self.__frame_dashboard, command = self.__use_bike, text = self.__PICKUP_BIKE_TEXT if isinstance(self.__user, Customer) else self.__MOVE_BIKE_TEXT)
        self.__button_use_bike.grid(columnspan = frame_column_num, padx = ui_attrs.PADDING_X, row = frame_row_index, sticky = (E, W))
        self.__frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        if isinstance(self.__user, OperatorWorker):
            # New row in the dashboard frame: placeholder.
            frame_row_index += 1
            ttk.Label(self.__frame_dashboard, style = styles.PLACEHOLDER_LABEL).grid(row = frame_row_index)
            self.__frame_dashboard.rowconfigure(frame_row_index, weight = 0)

            # New row in the dashboard frame: the button for overhauling a bike.
            frame_row_index += 1
            self.__button_overhaul_bike = ttk.Button(self.__frame_dashboard, command = self.__overhaul_bike, text = 'Overhaul the bike')
            self.__button_overhaul_bike.grid(columnspan = frame_column_num, padx = ui_attrs.PADDING_X, row = frame_row_index, sticky = (E, W))
            self.__frame_dashboard.rowconfigure(frame_row_index, weight = 0)

            # New row in the dashboard frame: placeholder.
            frame_row_index += 1
            ttk.Label(self.__frame_dashboard, style = styles.PLACEHOLDER_LABEL).grid(row = frame_row_index)
            self.__frame_dashboard.rowconfigure(frame_row_index, weight = 0)

            # New row in the dashboard frame: the button for tracking all bikes.
            frame_row_index += 1
            self.__button_overhaul_bike = ttk.Button(self.__frame_dashboard, command = self.__goto_tracking, text = 'Track all bikes')
            self.__button_overhaul_bike.grid(columnspan = frame_column_num, padx = ui_attrs.PADDING_X, row = frame_row_index, sticky = (E, W))
            self.__frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # New row in the dashboard frame: the info label.
        frame_row_index += 1
        self.__label_info = ttk.Label(self.__frame_dashboard, style = styles.CONTENT_LABEL)
        self.__label_info.grid(columnspan = frame_column_num, padx = ui_attrs.PADDING_X, pady = ui_attrs.PADDING_Y, row = frame_row_index)
        self.__update_ride_info()
        self.__frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # New row in the dashboard frame: the log-out button.
        frame_row_index += 1
        frame_column_index = 0
        ttk.Button(self.__frame_dashboard, command = self.__log_out, text = 'Log out').grid(column = frame_column_index, padx = ui_attrs.PADDING_X, row = frame_row_index, sticky = (S, W))
        self.__frame_dashboard.rowconfigure(frame_row_index, weight = 1)

        # Same row, new column in the dashboard frame: the about-app button.
        frame_column_index += 1
        button_about = ttk.Button(self.__frame_dashboard, command = self.__goto_about)
        image_about = Image.open(img.get_img_path(attrs.ABOUT_FILENAME)).resize((ui_attrs.PRIMARY_FONT_SIZE, ui_attrs.PRIMARY_FONT_SIZE), Image.ANTIALIAS)
        button_about.image = ImageTk.PhotoImage(image_about)
        button_about['image'] = button_about.image  # Keep a reference to prevent GC.
        button_about.grid(column = frame_column_index, padx = ui_attrs.PADDING_X, row = frame_row_index, sticky = (E, S))
        Tooltip(button_about, 'About ' + attrs.APP_NAME)

        # New row in the dashboard frame: placeholder.
        frame_row_index += 1
        ttk.Label(self.__frame_dashboard, style = styles.PLACEHOLDER_LABEL).grid(row = frame_row_index, pady = ui_attrs.PADDING_Y)
        self.__frame_dashboard.rowconfigure(frame_row_index, weight = 0)

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
                    available_bike_count = len(rental.check_bikes([row, col]))
                    label_map_cell.image = ImageTk.PhotoImage(self.__image_avatar_cell)

                    if isinstance(self.__user, OperatorWorker):
                        defective_bike_count = len(rental.check_bikes([row, col], attrs.DEFECTIVE_BIKE_CODE))

                        if defective_bike_count > 0:
                            tooltip_text += '\nDefective bike(s): %d' % defective_bike_count

                    if available_bike_count > 0:
                        tooltip_text += '\nAvailable bike(s): %d' % available_bike_count
                elif self.__map_array[row, col] == attrs.AVAILABLE_BIKE_CODE:
                    label_map_cell.image = ImageTk.PhotoImage(self.__image_available_bike)
                    tooltip_text += '\nAvailable bike(s): %d' % len(rental.check_bikes([row, col]))
                elif self.__map_array[row, col] == attrs.DEFECTIVE_BIKE_CODE:
                    label_map_cell.image = ImageTk.PhotoImage(self.__image_defective_bike)

                    if isinstance(self.__user, OperatorWorker):
                        available_bike_count = len(rental.check_bikes([row, col]))
                        tooltip_text += '\nDefective bike(s): %d' % len(
                            rental.check_bikes([row, col], attrs.DEFECTIVE_BIKE_CODE))

                        if available_bike_count > 0:
                            tooltip_text += '\nAvailable bike(s): %d' % available_bike_count
                else:
                    label_map_cell.image = ImageTk.PhotoImage(self.__image_empty_cell)

                label_map_cell['image'] = label_map_cell.image
                tooltip_map_cell = Tooltip(label_map_cell, tooltip_text)
                map_cell_list.append(tooltip_map_cell)
                map_element_row_list.append(map_cell_list)

            self.__map_element_list.append(map_element_row_list)

        # Bind events.
        self.__parent.protocol('WM_DELETE_WINDOW', lambda: self.__log_out(False))
        self.__parent.bind('<Configure>', self.__resize_frames)
        self.__parent.bind('<Left>', self.__move)
        self.__parent.bind('<Right>', self.__move)
        self.__parent.bind('<Up>', self.__move)
        self.__parent.bind('<Down>', self.__move)

        self.__parent.after(attrs.REFRESHING_INTERVAL, self.__refresh_map)  # Refresh the map regularly.

    def __goto_tracking(self) -> None:
        '''
        Go to the bike tracking view.
        '''

        if self.__tracking_window is None:
            self.__tracking_window = Toplevel(self.__parent)
            self.__tracking_window.protocol('WM_DELETE_WINDOW', self.__reset_tracking)
            self.__tracking_window.focus()
            TrackingView(self.__tracking_window)
            self.__tracking_window.mainloop()
        else:
            self.__tracking_window.focus()

    def __reset_tracking(self) -> None:
        '''
        Reset the bike tracking view.
        '''

        self.__tracking_window.destroy()
        self.__tracking_window = None

    def __goto_about(self) -> None:
        '''
        Go to the about-app view.
        '''

        self.__parent.focus()
        about_window = Toplevel(self.__parent)
        about_window.focus()
        about_window.grab_set()
        AboutView(about_window, attrs.CUSTOMER if isinstance(self.__user, Customer) else attrs.OPERATOR)
        about_window.mainloop()

    def __update_balance_text(self) -> None:
        '''
        Update the text of the balance label.
        '''

        self.__label_balance['text'] = ('Balance' if isinstance(self.__user, Customer) else 'Bonus') + ': ￡' + '%.2f' % self.__user.get_balance()

    def __topup(self) -> None:
        '''
        Top up a customer account.
        '''

        topup_result = FloatDialogue.askfloat('Top up', 'Enter the amount you want to top up (￡)\n(Please note that a maximum of 2 decimal places will be processed.)', minvalue = 0.01, parent = self.__parent)

        if topup_result is not None:
            amount_split = str(topup_result).split('.')
            amount = float(amount_split[0] + '.' + amount_split[1][:2])
            self.__user.update_balance(amount)
            self.__update_balance_text()
            messagebox.showinfo(attrs.APP_NAME, 'Hurray! Your wallet has been topped up successfully.', parent = self.__parent)

    def __use_bike(self) -> None:
        '''
        Pick up/Drop a bike as a customer.
        Move/Drop a bike as an operator.
        '''

        if isinstance(self.__user, Customer):
            if self.__user.get_balance() > 0:
                # Drop a bike.
                if self.__user.get_flag():
                    if self.__user.get_balance() < rental.calculate_charge(self.__rented_bike.get_extra_time()):
                        messagebox.showerror(attrs.APP_NAME, "Oops! You haven't got enough money. Please top up your wallet first.", parent = self.__parent)
                    else:
                        self.__button_use_bike['text'] = self.__PICKUP_BIKE_TEXT
                        self.__user, transaction_date = rental.drop_bike(self.__user, self.__rented_bike)

                        if self.__rented_bike.is_defective():
                            messagebox.askyesno(attrs.APP_NAME, 'Thanks for your using! The bike you dropped will be unavailable and overhauled.\n\nDid the bike work fine?', parent = self.__parent)
                            rental.report_break(self.__rented_bike, transaction_date)
                        else:
                            if not messagebox.askyesno(attrs.APP_NAME, 'Thanks for your using!\n\nDid the bike work fine?', parent = self.__parent):
                                rental.report_break(self.__rented_bike, transaction_date)

                        self.__rented_bike.set_is_being_used()
                        location = self.__user.get_location()
                        label_map_element = self.__map_element_list[location[0]][location[1]][0]
                        tooltip_map_element = self.__map_element_list[location[0]][location[1]][1]
                        label_map_element.image = ImageTk.PhotoImage(self.__image_avatar_cell)
                        label_map_element['image'] = label_map_element.image
                        available_bike_count = len(rental.check_bikes(location))
                        tooltip_map_element.set_text('Location: (%d, %d)' % (location[0], location[1]) + ('\nAvailable bike(s): %d' % available_bike_count if available_bike_count > 0 else ''))
                        self.__update_balance_text()
                        self.__update_ride_info()
                # Attempt to pick up a bike.
                else:
                    bike_result = rental.get_closest_bike(self.__user.get_location())

                    if isinstance(bike_result, list):
                        bike_id_list = [bike[0] for bike in bike_result]
                        available_bike_count = len(bike_id_list)

                        if available_bike_count > 1:
                            bike_choice = None

                            while bike_choice not in bike_id_list:
                                bike_choice = IntegerDialogue.askinteger('Select a bike', 'Enter the ID of the bike you want to pick up\nIDs of any available bike: ' + ', '.join(str(bike_id) for bike_id in sorted(bike_id_list)), parent = self.__parent)

                                if bike_choice is None:
                                    break

                            if bike_choice is not None:
                                self.__operate_bike(bike_choice)
                        elif available_bike_count == 1:
                            self.__operate_bike(bike_id_list[0])
                        else:
                            messagebox.showerror(attrs.APP_NAME, 'Oops! Your preferred bike may have been taken by someone else.', parent = self.__parent)
                    else:
                        messagebox.showwarning(attrs.APP_NAME, bike_result, parent = self.__parent)
            else:
                messagebox.showwarning(attrs.APP_NAME, 'Oops! Empty wallet. Please top up it.', parent = self.__parent)
        else:
            # Drop a bike.
            if self.__user.get_flag():
                self.__button_use_bike['text'] = self.__MOVE_BIKE_TEXT
                self.__user.move_bikes(self.__rented_bike.get_id())
                self.__user.is_using_bike(False)
                location = self.__user.get_location()
                label_map_element = self.__map_element_list[location[0]][location[1]][0]
                tooltip_map_element = self.__map_element_list[location[0]][location[1]][1]
                label_map_element.image = ImageTk.PhotoImage(self.__image_avatar_cell)
                label_map_element['image'] = label_map_element.image
                defective_bike_count = len(rental.check_bikes(location, attrs.DEFECTIVE_BIKE_CODE))
                available_bike_count = len(rental.check_bikes(location))
                tooltip_text_supplement = ('\nDefective bike(s): %d' % defective_bike_count if defective_bike_count > 0 else '') \
                    + ('\nAvailable bike(s): %d' % available_bike_count if available_bike_count > 0 else '')
                tooltip_map_element.set_text('Location: (%d, %d)' % (location[0], location[1]) + tooltip_text_supplement)
                self.__update_ride_info()
            # Attempt to move a bike.
            else:
                defective_bike_results = rental.check_bikes(self.__user.get_location(), attrs.DEFECTIVE_BIKE_CODE)
                available_bike_results = rental.check_bikes(self.__user.get_location())
                defective_bike_id_list = [bike[0] for bike in defective_bike_results]
                available_bike_id_list = [bike[0] for bike in available_bike_results]
                defective_bike_count = len(defective_bike_id_list)
                available_bike_count = len(available_bike_id_list)

                if defective_bike_count + available_bike_count > 1:
                    dialogue_text = 'Enter the ID of the bike you want to move'
                    bike_choice = None

                    if defective_bike_count > 0:
                        dialogue_text += ('\nID(s) of any defective bike: ' + ', '.join(str(bike_id) for bike_id in sorted(defective_bike_id_list)))

                    if available_bike_count > 0:
                        dialogue_text += ('\nID(s) of any available bike: ' + ', '.join(str(bike_id) for bike_id in sorted(available_bike_id_list)))

                    while bike_choice not in defective_bike_id_list + available_bike_id_list:
                        bike_choice = IntegerDialogue.askinteger('Select a bike', dialogue_text, parent = self.__parent)

                        if bike_choice is None:
                            break

                    if bike_choice is not None:
                        self.__operate_bike(bike_choice)
                elif defective_bike_count + available_bike_count == 1:
                    bike_choice = available_bike_id_list[0] if defective_bike_count == 0 else defective_bike_id_list[0]
                    self.__operate_bike(bike_choice)
                else:
                    messagebox.showerror(attrs.APP_NAME, 'Oops! No defective or available bike here.', parent = self.__parent)

    def __operate_bike(self, bike_id: int) -> None:
        '''
        Attempt to pick up/move a bike and update the properties of relevant widgets.

        Parameters
        ----------
        bike_id : the ID of a bike
        '''

        location = self.__user.get_location()
        self.__rented_bike = rental.renting(bike_id, location)

        if self.__rented_bike is None:
            messagebox.showerror(attrs.APP_NAME, 'Oops! Your preferred bike may have been taken by someone else.', parent = self.__parent)
        else:
            self.__button_use_bike['text'] = self.__DROP_BIKE_PAY_TEXT if isinstance(self.__user, Customer) else self.__DROP_BIKE_TEXT
            self.__user.is_using_bike(True)
            label_map_element = self.__map_element_list[location[0]][location[1]][0]
            tooltip_map_element = self.__map_element_list[location[0]][location[1]][1]
            label_map_element.image = ImageTk.PhotoImage(self.__image_bike_with_rider)
            label_map_element['image'] = label_map_element.image
            defective_bike_count = 0
            available_bike_count = len(rental.check_bikes(self.__user.get_location()))

            if isinstance(self.__user, OperatorWorker):
                defective_bike_count = len(rental.check_bikes(self.__user.get_location(), attrs.DEFECTIVE_BIKE_CODE))

            tooltip_text_supplement = ('\nDefective bike(s): %d' % defective_bike_count if isinstance(self.__user, OperatorWorker) and defective_bike_count > 0 else '') \
                + ('\nAvailable bike(s): %d' % available_bike_count if available_bike_count > 0 else '')
            tooltip_map_element.set_text('Location: (%d, %d)' % (location[0], location[1]) + tooltip_text_supplement)
            self.__update_ride_info()

    def __overhaul_bike(self) -> None:
        '''
        Overhaul a specified bike.
        '''

        if self.__user.get_flag():
            messagebox.showerror(attrs.APP_NAME, 'Oops! You are moving a bike.\nPlease drop it and then pick up a bike to overhaul.')
        else:
            defective_bike_results = rental.check_bikes(self.__user.get_location(), attrs.DEFECTIVE_BIKE_CODE)
            defective_bike_count = len(defective_bike_results)

            if defective_bike_count >= 1:
                defective_bike_id_list = [bike[0] for bike in defective_bike_results]
                bike_choice = None

                if defective_bike_count > 1:
                    while bike_choice not in defective_bike_id_list:
                        bike_choice = IntegerDialogue.askinteger('Select a bike', 'Enter the ID of the bike you want to overhaul\nIDs of any defective bike: ' + ', '.join(str(bike_id) for bike_id in sorted(defective_bike_id_list)), parent = self.__parent)

                        if bike_choice is None:
                            break
                else:
                    bike_choice = defective_bike_id_list[0]

                if bike_choice is not None:
                    to_repair, time_begin, how_broken, time_to_fix = self.__user.repair_bikes(bike_choice)
                    messagebox.showinfo(attrs.APP_NAME, 'Working hard...\n\nPretend that some time has passed away. XD\n\nAs you read this line, you are good to go. Well done!', parent = self.__parent)
                    self.__user.record_repair(to_repair, time_begin, how_broken, time_to_fix)
                    self.__update_balance_text()
                    self.__update_ride_info()
            else:
                messagebox.showerror(attrs.APP_NAME, 'Oops! No defective bike here.', parent = self.__parent)

    def __update_ride_info(self) -> None:
        '''
        Update the riding info in the info label.
        '''

        if isinstance(self.__user, Customer):
            if self.__user.get_flag():
                defective = self.__rented_bike.get_defective()
                bike_status_info = '\n\nBike conditions (est.): '

                if defective < attrs.FINE_BIKE_THRESHOLD:
                    bike_status_info += attrs.FINE_STATUS
                elif defective < attrs.DEFECTIVE_BIKE_THRESHOLD:
                    bike_status_info += attrs.GOOD_STATUS
                else:
                    bike_status_info += attrs.DEFECTIVE_STATUS

                self.__label_info['text'] = \
                    self.__HINT_INFO \
                    + '\n\nBike ID: ' + str(self.__rented_bike.get_id()) \
                    + bike_status_info \
                    + '\n\nDistance: ' + str(self.__rented_bike.get_distance()) \
                    + '\n\nCharge: ￡' + '%.2f' % rental.calculate_charge(self.__rented_bike.get_extra_time())
            else:
                self.__label_info['text'] = self.__HINT_INFO
        else:
            self.__label_info['text'] = \
                self.__HINT_INFO \
                + '\n\nAll defective bike(s): ' + str(len(rental.check_bikes(bike_code = attrs.DEFECTIVE_BIKE_CODE))) \
                + '\n\nAll busy non-defective bike(s): ' + str(len(
                    rental.check_bikes(bike_code = attrs.BUSY_BIKE_CODE))) \
                + '\n\nAll available bike(s): ' + str(len(rental.check_bikes()))

    def __log_out(self, is_logout_button = True) -> None:
        '''
        Log out the account.

        Parameters
        ----------
        is_logout_button : a flag indicating if a user tries to log out himself/herself by clicking the log-out button
        '''

        if self.__user.get_flag():
            messagebox.showerror(attrs.APP_NAME, 'You cannot be logged out until dropping the bike' + (' and paying.' if isinstance(self.__user, Customer) else '.'), parent = self.__parent)
        else:
            if not is_logout_button and not messagebox.askyesno(attrs.APP_NAME, 'Are you sure you want to log out?', parent = self.__parent):
                return

            account.log_out(self.__user)
            self.__parent.destroy()
            self.__parent = None

            if self.__toplevel is not None:
                self.__toplevel.deiconify()

    def __refresh_map(self) -> None:
        '''
        Refresh the map.
        '''

        new_map_array = self.__mapping.download()

        for row in range(attrs.MAP_LENGTH):
            for col in range(attrs.MAP_LENGTH):
                # Change the background image if there is an update.
                if new_map_array[row, col] != self.__map_array[row, col]:
                    label_map_element = self.__map_element_list[row][col][0]

                    if new_map_array[row, col] == attrs.AVATAR_CODE:
                        label_map_element.image = ImageTk.PhotoImage(self.__image_bike_with_rider) if self.__user.get_flag() else ImageTk.PhotoImage(self.__image_avatar_cell)
                    elif new_map_array[row, col] == attrs.AVAILABLE_BIKE_CODE:
                        label_map_element.image = ImageTk.PhotoImage(self.__image_available_bike)
                    elif new_map_array[row, col] == attrs.DEFECTIVE_BIKE_CODE:
                        label_map_element.image = ImageTk.PhotoImage(self.__image_defective_bike)
                    else:
                        label_map_element.image = ImageTk.PhotoImage(self.__image_empty_cell)

                    label_map_element['image'] = label_map_element.image

                # Refresh tooltips, whether any update happens or not.
                tooltip_map_element = self.__map_element_list[row][col][1]
                tooltip_text = 'Location: (%d, %d)' % (row, col)

                if new_map_array[row, col] == attrs.AVATAR_CODE:
                    available_bike_count = len(rental.check_bikes([row, col]))
                    tooltip_text = 'Location: (%d, %d)' % (row, col)

                    if isinstance(self.__user, OperatorWorker):
                        defective_bike_count = len(rental.check_bikes([row, col], attrs.DEFECTIVE_BIKE_CODE))

                        if defective_bike_count > 0:
                            tooltip_text += '\nDefective bike(s): %d' % defective_bike_count

                    if available_bike_count > 0:
                        tooltip_text += '\nAvailable bike(s): %d' % available_bike_count
                elif new_map_array[row, col] == attrs.AVAILABLE_BIKE_CODE:
                    tooltip_text += '\nAvailable bike(s): %d' % len(rental.check_bikes([row, col]))
                elif new_map_array[row, col] == attrs.DEFECTIVE_BIKE_CODE:
                    if isinstance(self.__user, OperatorWorker):
                        available_bike_count = len(rental.check_bikes([row, col]))
                        tooltip_text += '\nDefective bike(s): %d' % len(
                            rental.check_bikes([row, col], attrs.DEFECTIVE_BIKE_CODE))

                        if available_bike_count > 0:
                            tooltip_text += '\nAvailable bike(s): %d' % available_bike_count

                tooltip_map_element.set_text(tooltip_text)

        self.__mapping.set_map_array(new_map_array)
        self.__map_array = new_map_array

        if isinstance(self.__user, OperatorWorker):
            self.__update_ride_info()

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

        self.__label_info['wraplength'] = self.__frame_dashboard.winfo_width() - ui_attrs.PADDING_X * 2

    def __move(self, event) -> None:
        '''
        Move the avatar or a bike.

        Parameters
        ----------
        event : the event bound to the widget calling this function
        '''

        location = self.__user.get_location()
        label_map_element = self.__map_element_list[location[0]][location[1]][0]
        tooltip_map_element = self.__map_element_list[location[0]][location[1]][1]

        if (event.keysym == 'Left' and location[1] > 0) \
                or (event.keysym == 'Right' and location[1] < attrs.MAP_LENGTH - 1) \
                or (event.keysym == 'Up' and location[0] > 0) \
                or (event.keysym == 'Down' and location[0] < attrs.MAP_LENGTH - 1):
            new_location = location.copy()

            if event.keysym == 'Left':
                new_location[1] -= 1
            elif event.keysym == 'Right':
                new_location[1] += 1
            elif event.keysym == 'Up':
                new_location[0] -= 1
            else:
                new_location[0] += 1

            if self.__user.get_flag():
                self.__rented_bike.set_location(new_location, False if isinstance(self.__user, Customer) else True)

                if isinstance(self.__user, Customer):
                    self.__rented_bike.add_distance()
                    self.__rented_bike.add_extra_time()
                    self.__update_ride_info()

            defective_bike_results = rental.check_bikes(location, attrs.DEFECTIVE_BIKE_CODE)
            available_bike_results = rental.check_bikes(location)
            defective_bike_count = len(defective_bike_results)
            available_bike_count = len(available_bike_results)
            tooltip_text = 'Location: (%d, %d)' % (location[0], location[1])

            if isinstance(self.__user, Customer):
                if available_bike_count == 0:
                    if defective_bike_count == 0:
                        label_map_element.image = ImageTk.PhotoImage(self.__image_empty_cell)
                        label_map_element['image'] = label_map_element.image
                    else:
                        label_map_element.image = ImageTk.PhotoImage(self.__image_defective_bike)
                        label_map_element['image'] = label_map_element.image
                else:
                    label_map_element.image = ImageTk.PhotoImage(self.__image_available_bike)
                    label_map_element['image'] = label_map_element.image
                    tooltip_text += '\nAvailable bike(s): %d' % available_bike_count
            else:
                if defective_bike_count == 0:
                    if available_bike_count == 0:
                        label_map_element.image = ImageTk.PhotoImage(self.__image_empty_cell)
                        label_map_element['image'] = label_map_element.image
                    else:
                        label_map_element.image = ImageTk.PhotoImage(self.__image_available_bike)
                        label_map_element['image'] = label_map_element.image
                        tooltip_text += '\nAvailable bike(s): %d' % available_bike_count
                else:
                    label_map_element.image = ImageTk.PhotoImage(self.__image_defective_bike)
                    label_map_element['image'] = label_map_element.image
                    tooltip_text += '\nDefective bike(s): %d' % defective_bike_count \
                        + ('\nAvailable bike(s): %d' % available_bike_count if available_bike_count > 0 else '')

            tooltip_map_element.set_text(tooltip_text)
            self.__user.set_location(new_location)
            self.__mapping.set_state(new_location, attrs.AVATAR_CODE)
            label_map_element = self.__map_element_list[new_location[0]][new_location[1]][0]
            tooltip_map_element = self.__map_element_list[new_location[0]][new_location[1]][1]
            label_map_element.image = ImageTk.PhotoImage(self.__image_bike_with_rider) if self.__user.get_flag() else ImageTk.PhotoImage(self.__image_avatar_cell)
            label_map_element['image'] = label_map_element.image
            defective_bike_count = len(rental.check_bikes(new_location, attrs.DEFECTIVE_BIKE_CODE))
            available_bike_count = len(rental.check_bikes(new_location))
            tooltip_text_supplement = ('\nDefective bike(s): %d' % defective_bike_count if isinstance(self.__user, OperatorWorker) and defective_bike_count > 0 else '') \
                + ('\nAvailable bike(s): %d' % available_bike_count if available_bike_count > 0 else '')
            tooltip_map_element.set_text('Location: (%d, %d)' % (location[0], location[1]) + tooltip_text_supplement)


# Test purposes only.
if __name__ == '__main__':
    from tkinter import Tk

    home_window = Tk()
    # HomeView(home_window, account_test.logging(attrs.CUSTOMER, 'jichen', '12345'))
    HomeView(home_window, account_test.logging(attrs.OPERATOR, 'jiamin', '1234'))
    home_window.mainloop()