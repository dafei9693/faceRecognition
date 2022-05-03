from openpyxl import load_workbook
from tkinter import *
from tkinter import messagebox
import numpy as np
from net.mtcnn import mtcnn
import utils.utils as utils
from net.inception import InceptionResNetV1
import cv2
from tkinter.filedialog import askopenfilename

class add_Data():
    def __init__(self,img):
        self.mtcnn_model = mtcnn()
        self.threshold = [0.5, 0.8, 0.9]
        self.facenet_model = InceptionResNetV1()
        model_path = 'D:/PycharmProjects/System/recognition/model_data/facenet_keras.h5'
        self.facenet_model.load_weights(model_path)
        self.known_face_encodings = []
        self.img=img

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        rectangles = self.mtcnn_model.detectFace(img, self.threshold)

        rectangles = utils.rect2square(np.array(rectangles))
        # facenet要传入一个160x160的图片
        rectangle = rectangles[0]
        # 记下他们的landmark
        landmark = (np.reshape(rectangle[5:15], (5, 2)) - np.array([int(rectangle[0]), int(rectangle[1])])) / (
                    rectangle[3] - rectangle[1]) * 160

        crop_img = img[int(rectangle[1]):int(rectangle[3]), int(rectangle[0]):int(rectangle[2])]
        crop_img = cv2.resize(crop_img, (160, 160))
        new_img, _ = utils.Alignment_1(crop_img, landmark)
        new_img = np.expand_dims(new_img, 0)
        face_encoding = utils.calc_128_vec(self.facenet_model, new_img)
        self.known_face_encodings.append(face_encoding)

    def done(self):
        return self.known_face_encodings



def add():
    def add_data(filepath, name,Name):
        try:
            img = cv2.imread(filepath)
            make = add_Data(img)
            encodings = make.done()
            for i in range(len(encodings)):
                with open("data.txt", "a") as f:
                    f.write(str(name) + " ")
                    for j in encodings[i]:
                        f.write(str(j) + " ")
                    f.write("\n")
                    f.close()
            wb=load_workbook("E:/Work/信息.xlsx")
            ws=wb["Sheet1"]
            ws.append([str(Name),str(name)])
            wb.save("E:/Work/信息.xlsx")
            messagebox.showinfo(title="提示",message="增加成功")
        except:
            print(name + "failed")
    def select_path():
        path_ = askopenfilename()
        path.set(path_)

    win=Toplevel()
    win.title("增加")
    path=StringVar()
    name=StringVar()
    number=StringVar()
    Label(win,text="图片路径").grid(row=0,column=0)
    Entry(win,textvariable=path,width=50).grid(row=0,column=1)
    Button(win,text="选择图片",command=select_path).grid(row=0,column=2)
    Label(win,text="姓名").grid(row=1,column=0)
    Entry(win,textvariable=name).grid(row=1,column=1)
    Label(win,text="学号").grid(row=2,column=0)
    Entry(win,textvariable=number).grid(row=2,column=1)
    Button(win,text="确定",command=lambda :add_data(path.get(),number.get(),name.get())).grid(row=3,column=1)



    win.mainloop()




