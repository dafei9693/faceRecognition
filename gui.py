from tkinter import *
from  tkinter import ttk
from test import video
from info import info
from make_datasets import add

def start():
    video()

def record():
    import os
    os.startfile("E:/work")

window=Tk()
window.title("菜单")
window.geometry("1000x500")
button1=Button(window,text="开始",command=start)
button2=Button(window,text="关于",command=info)
button3=Button(window,text="退出",command=quit)
button4=Button(window,text="增加人脸",command=add)
button5=Button(window,text="记录",command=record)
lab1=Label(window,text="人脸识别系统",font="STKaiki 25 bold")
s=ttk.Separator(window,orient=HORIZONTAL)





lab1.pack()
s.pack(fill=X)
button1.place(x=440,y=100,width=150,height=40)
button2.place(x=440,y=150,width=150,height=40)
button5.place(x=440,y=200,width=150,height=40)
button4.place(x=440,y=250,width=150,height=40)
button3.place(x=440,y=300,width=150,height=40)

window.mainloop()


