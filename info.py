from tkinter import *

def info():
    window=Toplevel()
    window.geometry("300x150")
    window.title("info")
    label1=Label(window,text="CPU:Intel i18 10990k")
    label2=Label(window,text="None")
    label3=Label(window,text="RAM:1T")
    #label1.place(x=50,y=30,width=150)
    label2.place(x=50,y=60,width=150)
    #label3.place(x=50,y=90,width=150)
    window.mainloop()