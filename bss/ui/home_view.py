from tkinter import *
window = Tk()
window.title("home page")
window.geometry('300x500')

user_info = Label(text="User Information")#.grid(row=0)
user_info.place(x=10, y=10)

username = Label(text="Username: Tony")#.grid(row=1)
username.place(x=10, y=30)

password = Label(text="Password: 123456")#.grid(row=2)
password.place(x=10, y=50)

wallet_info = Label(text="Wallet Information")#.grid(row=3)
wallet_info.place(x=10, y=100)

wallet_balance = Label(text="wallet balance: 0.0 GBD")#.grid(row=4)
wallet_balance.place(x=10, y=120)

map_show=Label(text="map")#.grid(row=0, column=1)
map_show.place(x=200, y=10)
rent_bike = Button(text="Rent Bike")#.grid(row=0, column=2)
rent_bike.place(x=300, y=10)
return_bike = Button(text="Return Bike")#.grid(row=1, column=2)
return_bike.place(x=300, y=50)
defective = Button(text="defective bike")#.grid(row=2, column=2)
defective.place(x=300, y=100)
pay = Button(text="pay the bill")#.grid(row=3, column=2)
pay.place(x=300, y=150)

window.mainloop()