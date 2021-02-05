from tkinter import *

from bss.conf import attrs
from bss.ui.img_path import get_img_path


class HomeView:
    def __init__(self, parent):
        self.__parent = parent
        screen_width = self.__parent.winfo_screenwidth()
        screen_height = self.__parent.winfo_screenheight()
        parent_width = 500
        parent_height = 480

        self.__parent.geometry('%dx%d+%d+%d' % (parent_width, parent_height, (screen_width - parent_width) / 2, (screen_height - parent_height) / 2))  # Centre the parent window.
        self.__parent.title('Home')
        self.__parent.iconbitmap(get_img_path(attrs.APP_ICON_FILENAME))

        user_info = Label(text="User Information")  # .grid(row=0)
        user_info.place(x=10, y=10)

        username = Label(text="Username: Tony")  # .grid(row=1)
        username.place(x=10, y=30)

        password = Label(text="Password: 123456")  # .grid(row=2)
        password.place(x=10, y=50)

        wallet_info = Label(text="Wallet Information")  # .grid(row=3)
        wallet_info.place(x=10, y=100)

        wallet_balance = Label(text="wallet balance: 0.0 GBD")  # .grid(row=4)
        wallet_balance.place(x=10, y=120)

        map_show = Label(text="map")  # .grid(row=0, column=1)
        map_show.place(x=200, y=10)
        map_image = Text(width=10, height=10, bg="grey")
        map_image.place(x=200, y=50)

        rent_bike = Button(text="Rent Bike", command=self.rent)  # .grid(row=0, column=2)
        rent_bike.place(x=300, y=10)
        return_bike = Button(text="Return Bike", command=self.return_bike)  # .grid(row=1, column=2)
        return_bike.place(x=300, y=50)
        defective = Button(text="defective bike", command=self.defective)  # .grid(row=2, column=2)
        defective.place(x=300, y=100)
        pay = Button(text="pay the bill", command=self.pay)  # .grid(row=3, column=2)
        pay.place(x=300, y=150)
        about = Button(text="About BikeSims", command=self.about)  # .grid(row=3, column=2)
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


if __name__ == '__main__':
    home_window = Tk()
    HomeView(home_window)
    home_window.mainloop()