from PIL import Image, ImageTk
from tkinter import Tk, Toplevel, ttk
from tkinter.constants import E, N, S, W, X

from bss.conf import attrs
from bss.customer import Customer
from bss.ui.conf import attrs as ui_attrs, styles
from bss.ui.img_path import get_img_path


class HomeView:
    '''
    The class for creating a home view.
    '''

    def __init__(self, parent, user) -> None:
        '''
        The constructor of the class for creating a home view.
        Customers and operators can have access to this view.

        Parameters
        ----------
        parent : the parent window for the home view to display
        user : a `Customer` or `OperatorWorker` object
        '''

        self.__parent = parent
        screen_width = self.__parent.winfo_screenwidth()
        screen_height = self.__parent.winfo_screenheight()
        parent_width = 800
        parent_height = 600

        self.__parent.geometry('%dx%d+%d+%d' % (parent_width, parent_height, (screen_width - parent_width) / 2, (screen_height - parent_height) / 2))  # Centre the parent window.
        self.__parent.title('Home')
        self.__parent.iconbitmap(get_img_path(attrs.APP_ICON_FILENAME))
        self.__parent.minsize(parent_width, parent_height)

        self.__parent.rowconfigure(0, weight = 1)
        styles.apply_style()

        # New row: a frame for the dashboard area.
        column_index = 0  # Make it convenient to index the column of the grid.
        frame_dashboard = ttk.Frame(self.__parent)
        frame_dashboard.grid(padx = ui_attrs.PADDING_X, row = 0, sticky = (E, N, S, W))
        self.__parent.columnconfigure(column_index, weight = 1)

        ttk.Label(frame_dashboard, style = styles.PLACEHOLDER_LABEL).pack()  # New row in the frame: placeholder.

        # New row in the frame: the avatar image label.
        label_avatar = ttk.Label(frame_dashboard)
        label_avatar.pack(pady = ui_attrs.PADDING_Y)

        if isinstance(user, Customer):
            image_avatar = Image.open(get_img_path(attrs.CUSTOMER_AVATAR_FILENAME))
        else:
            image_avatar = Image.open(get_img_path(attrs.OPERATOR_AVATAR_FILENAME))

        image_avatar = image_avatar.resize((50, 50), Image.ANTIALIAS)
        label_avatar.image = ImageTk.PhotoImage(image_avatar)
        label_avatar['image'] = label_avatar.image  # Keep a reference to prevent GC.

        ttk.Label(frame_dashboard, style = styles.PRIMARY_LABEL, text = user.name).pack()  # New row in the frame: the username label.
        ttk.Label(frame_dashboard, style = styles.EXPLANATION_LABEL, text = 'Balance: ￡' + '%.2f' % user.balance).pack()  # New row in the frame: the balance label.
        ttk.Label(frame_dashboard, style = styles.PLACEHOLDER_LABEL).pack()  # New row in the frame: placeholder.
        ttk.Button(frame_dashboard, text = 'Top up').pack(fill = X)  # New row in the frame: the top-up button. TODO: image and text?
        ttk.Label(frame_dashboard, style = styles.PLACEHOLDER_LABEL).pack()  # New row in the frame: placeholder.
        ttk.Button(frame_dashboard, text = 'Pick up the bike').pack(fill = X)  # New row in the frame: the button for picking up/dropping a bike. TODO: image and text?

        # Same row, new column: a frame for the map area.
        column_index += 1
        frame_map = ttk.Frame(self.__parent)
        frame_map.grid(column = column_index, padx = ui_attrs.PADDING_X, row = 0, sticky = (E, N, S, W))
        self.__parent.columnconfigure(column_index, weight = 4)

        '''
        user_info = ttk.Label(text="User Information")  # .grid(row=0)
        user_info.place(x=10, y=10)

        username = ttk.Label(text="Username: Tony")  # .grid(row=1)
        username.place(x=10, y=30)

        password = ttk.Label(text="Password: 123456")  # .grid(row=2)
        password.place(x=10, y=50)

        wallet_info = ttk.Label(text="Wallet Information")  # .grid(row=3)
        wallet_info.place(x=10, y=100)

        wallet_balance = ttk.Label(text="wallet balance: 0.0 GBD")  # .grid(row=4)
        wallet_balance.place(x=10, y=120)

        map_show = ttk.Label(text="map")  # .grid(row=0, column=1)
        map_show.place(x=200, y=10)
        map_image = Text(width=10, height=10, bg="grey")
        map_image.place(x=200, y=50)

        rent_bike = ttk.Button(text="Rent Bike", command=self.rent)  # .grid(row=0, column=2)
        rent_bike.place(x=300, y=10)
        return_bike = ttk.Button(text="Return Bike", command=self.return_bike)  # .grid(row=1, column=2)
        return_bike.place(x=300, y=50)
        defective = ttk.Button(text="defective bike", command=self.defective)  # .grid(row=2, column=2)
        defective.place(x=300, y=100)
        pay = ttk.Button(text="pay the bill", command=self.pay)  # .grid(row=3, column=2)
        pay.place(x=300, y=150)
        about = ttk.Button(text="About BikeSims", command=self.about)  # .grid(row=3, column=2)
        about.place(x=300, y=200)

    def rent(self):
        top = Toplevel()
        top.title("Rent Bike")

    def return_bike(self):
        top = Toplevel()
        top.title("Return Bike")

    def defective(self):
        top = Toplevel()
        top.title("Return a defective")

    def pay(self):
        top = Toplevel()
        top.title("Pay the bill")

    def about(self):
        top = Toplevel()
        top.title("About BikeSims")
    '''


if __name__ == '__main__':
    home_window = Tk()
    HomeView(home_window, Customer(2, 'jichen', '12345', 232.5, [0, 1]))
    home_window.mainloop()