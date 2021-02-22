from tkinter import messagebox, Toplevel, ttk
from tkinter.constants import E, N, RAISED, S, SOLID, W

from PIL import Image, ImageTk

from bss.temp import account  # TODO
from bss.conf import attrs
from bss.temp.manager import Manager  # TODO
from bss.ui.about_view import AboutView
from bss.ui.conf import attrs as ui_attrs, colours, styles
from bss.ui.utils import img_path as img

from bss.ui.utils.tooltip import Tooltip
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

        image_avatar = Image.open(img.get_img_path(attrs.MANAGER_AVATAR_FILENAME)).resize((ui_attrs.AVATAR_LENGTH, ui_attrs.AVATAR_LENGTH), Image.ANTIALIAS)
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

        ttk.Button(frame_dashboard, command=self.__user.image1(), text='Growth of company over time').grid(
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
        ttk.Button(frame_dashboard, command=self.__user.image2(), text='User Behaviour Statistics v1').grid(
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
        ttk.Button(frame_dashboard, command=self.__user.image3(), text='User Behaviour Statistics v2').grid(
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
        ttk.Button(frame_dashboard, command=self.__user.image4(), text='Bike Statistics').grid(columnspan=frame_column_num,
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
        ttk.Button(frame_dashboard, command=self.__user.image5(), text='Daily Usage Frequency Analysis').grid(
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
        ttk.Button(frame_dashboard, command=self.__user.image6(), text='Response Time from Workers').grid(
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
        button_about = ttk.Button(frame_dashboard, command = self.__goto_about)
        image_about = Image.open(img.get_img_path(attrs.ABOUT_FILENAME)).resize((ui_attrs.PRIMARY_FONT_SIZE, ui_attrs.PRIMARY_FONT_SIZE), Image.ANTIALIAS)
        button_about.image = ImageTk.PhotoImage(image_about)
        button_about['image'] = button_about.image  # Keep a reference to prevent GC.
        button_about.grid(column = frame_column_index, padx = ui_attrs.PADDING_X, row = frame_row_index, sticky = (E, S))
        Tooltip(button_about, 'About ' + attrs.APP_NAME)

        # Bind events.
        self.__parent.protocol('WM_DELETE_WINDOW', lambda: self.__log_out(False))
        self.__parent.bind('<Configure>', self.__resize_frames)

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

    def __log_out(self, is_logout_button = True) -> None:
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
