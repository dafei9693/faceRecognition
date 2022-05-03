#from face_recognize import face_rec
import numpy as np

def get_data():
    face_names=[]
    face_encodings=[]

    f = open("data.txt","r")
    line = f.readline()
    while line:
        data=line.split(" ")
        if data[0] is not "\n":
            face_names.append(data[0])
        face_encodings.append(data[1:-1])
        line = f.readline()

    f.close()
    for i in range(len(face_encodings)):
        for j in range(len(face_encodings[i])):
            if face_encodings[i][j] == "\n":
                continue
            face_encodings[i][j]=float(face_encodings[i][j])
    for i in range(len(face_encodings)):
        face_encodings[i]=np.array(face_encodings[i],dtype='float32')
    return face_encodings,face_names

