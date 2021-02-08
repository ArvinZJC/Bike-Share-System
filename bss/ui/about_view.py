from tkinter import *

window=Tk()
window.title("AboutBikeSims")
window.geometry("300x500")

label1 = Label(text = "BikeSims")
label1.place(x=50,y=100)

label2 = Label(text = "Version 1.0.0")
label2.place(x=50,y=130)

label3 = Label(text = "Copyright©2021 LAB01_2D.")
label3.place(x=50,y=160)

label4 = Label(text = "All Rights Reserved")
label4.place(x=50,y=180)
window.mainloop()