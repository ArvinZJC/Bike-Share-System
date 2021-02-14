from tkinter import Tk, ttk
from tkinter.constants import E, N, RAISED, S, W

from PIL import Image, ImageTk

from bss.conf import attrs
from bss.temp.customer.customer import Customer
from bss.ui.conf import attrs as ui_attrs, styles
from bss.ui.img_path import get_img_path


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
        screen_width = self.__parent.winfo_screenwidth()
        screen_height = self.__parent.winfo_screenheight()
        self.__parent_width = 900
        self.__parent_height = 600

        self.__parent.geometry('%dx%d+%d+%d' % (self.__parent_width, self.__parent_height, (screen_width - self.__parent_width) / 2, (screen_height - self.__parent_height) / 2))  # Centre the parent window.
        self.__parent.title('Home')
        self.__parent.iconbitmap(get_img_path(attrs.APP_ICON_FILENAME))
        self.__parent.minsize(self.__parent_width, self.__parent_height)
        self.__parent.maxsize(self.__parent_width * 2, self.__parent_height * 2)

        self.__parent.rowconfigure(0, weight = 1)
        styles.apply_style()

        # New row: a frame for the dashboard area.
        column_index = 0  # Make it convenient to index the column of the grid.
        frame_column_num = 2
        frame_dashboard = ttk.Frame(self.__parent, relief = RAISED)
        frame_dashboard.grid(row = 0, sticky = (E, N, S, W))
        frame_dashboard.columnconfigure(0, weight = 1)

        # New row in the frame: placeholder.
        frame_row_index = 0  # Make it convenient to index the row of the grid in the frame.
        ttk.Label(frame_dashboard, style = styles.PLACEHOLDER_LABEL).grid(columnspan = frame_column_num, row = frame_row_index)
        frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # New row in the frame: the avatar image label.
        frame_row_index += 1
        __label_avatar = ttk.Label(frame_dashboard)
        __label_avatar.grid(columnspan = frame_column_num, padx = ui_attrs.PADDING_X, pady = ui_attrs.PADDING_Y, row = frame_row_index)
        frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        if isinstance(user, Customer):
            __image_avatar = Image.open(get_img_path(attrs.CUSTOMER_AVATAR_FILENAME))
        else:
            __image_avatar = Image.open(get_img_path(attrs.OPERATOR_AVATAR_FILENAME))

        __image_avatar = __image_avatar.resize((ui_attrs.AVATAR_LENGTH, ui_attrs.AVATAR_LENGTH), Image.ANTIALIAS)
        __label_avatar.image = ImageTk.PhotoImage(__image_avatar)
        __label_avatar['image'] = __label_avatar.image  # Keep a reference to prevent GC.

        # New row in the frame: the username label.
        frame_row_index += 1
        ttk.Label(frame_dashboard, style = styles.PRIMARY_LABEL, text = user.name).grid(columnspan = frame_column_num, padx = ui_attrs.PADDING_X, row = frame_row_index)
        frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # New row in the frame: the balance label.
        frame_row_index += 1
        ttk.Label(frame_dashboard, style = styles.EXPLANATION_LABEL, text = 'Balance: ￡' + '%.2f' % user.balance).grid(columnspan = frame_column_num, padx = ui_attrs.PADDING_X, row = frame_row_index)
        frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # New row in the frame: placeholder.
        frame_row_index += 1
        ttk.Label(frame_dashboard, style = styles.PLACEHOLDER_LABEL).grid(row = frame_row_index)
        frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # New row in the frame: the top-up button. TODO: image and text?
        frame_row_index += 1
        ttk.Button(frame_dashboard, text = 'Top up').grid(columnspan = frame_column_num, padx = ui_attrs.PADDING_X, row = frame_row_index, sticky = (E, W))
        frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # New row in the frame: placeholder.
        frame_row_index += 1
        ttk.Label(frame_dashboard, style = styles.PLACEHOLDER_LABEL).grid(row = frame_row_index)
        frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # New row in the frame: a separator.
        frame_row_index += 1
        ttk.Separator(frame_dashboard).grid(columnspan = frame_column_num, padx = ui_attrs.PADDING_Y, row = frame_row_index, sticky = (E, W))
        frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # New row in the frame: placeholder.
        frame_row_index += 1
        ttk.Label(frame_dashboard, style = styles.PLACEHOLDER_LABEL).grid(row = frame_row_index)
        frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # New row in the frame: the button for picking up/dropping a bike. TODO: image and text?
        frame_row_index += 1
        ttk.Button(frame_dashboard, text = 'Pick up the bike').grid(columnspan = frame_column_num, padx = ui_attrs.PADDING_X, row = frame_row_index, sticky = (E, W))
        frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # New row in the frame: TODO: bike renting info area
        frame_row_index += 1
        ttk.Label(frame_dashboard, style = styles.CONTENT_LABEL, text = '(TODO: Bike renting info area)').grid(columnspan = frame_column_num, padx = ui_attrs.PADDING_X, pady = ui_attrs.PADDING_Y, row = frame_row_index)
        frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # New row in the frame: TODO: the log-out area
        frame_row_index += 1
        frame_column_index = 0
        ttk.Label(frame_dashboard, style = styles.CONTENT_LABEL, text = 'Log out').grid(column = frame_column_index, padx = ui_attrs.PADDING_X, row = frame_row_index, sticky = (S, W))
        frame_dashboard.rowconfigure(frame_row_index, weight = 1)

        # Same row, new column in the frame: TODO: the settings area
        frame_column_index += 1
        ttk.Label(frame_dashboard, style = styles.CONTENT_LABEL, text = 'Settings').grid(column = frame_column_index, padx = ui_attrs.PADDING_X, row = frame_row_index, sticky = (E, S))

        # New row in the frame: placeholder.
        frame_row_index += 1
        ttk.Label(frame_dashboard, style = styles.PLACEHOLDER_LABEL).grid(row = frame_row_index, pady = ui_attrs.PADDING_Y)
        frame_dashboard.rowconfigure(frame_row_index, weight = 0)

        # Same row, new column: a frame for the map area.
        column_index += 1
        frame_map = ttk.Frame(self.__parent, relief = 'raised')
        frame_map.grid(column = column_index, row = 0, sticky = (E, N, S, W))

        # Bind events.
        self.__parent.bind('<Configure>', self.__resize_frames)

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


if __name__ == '__main__':
    home_window = Tk()
    HomeView(home_window, Customer(2, 'jichen', '12345', 232.5, [0, 1]))
    home_window.mainloop()