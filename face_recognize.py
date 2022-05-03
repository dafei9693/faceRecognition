import cv2
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import numpy as np
from net.mtcnn import mtcnn
import utils.utils as utils
from net.inception import InceptionResNetV1
from read_data import get_data

class face_rec():
    def __init__(self):
        # 创建mtcnn对象
        # 检测图片中的人脸
        self.mtcnn_model = mtcnn()
        # 门限函数
        self.threshold = [0.5,0.8,0.9]

        # 载入facenet
        # 将检测到的人脸转化为128维的向量
        self.facenet_model = InceptionResNetV1()
        # model.summary()
        model_path = 'D:/PycharmProjects/System/recognition/model_data/facenet_keras.h5'
        self.facenet_model.load_weights(model_path)

        #-----------------------------------------------#
        #   对数据库中的人脸进行编码
        #   known_face_encodings中存储的是编码后的人脸
        #   known_face_names为人脸的名字
        #-----------------------------------------------#
        face_list = os.listdir("D:/PycharmProjects/System/recognition/face_dataset/111")

        self.known_face_encodings=[]

        self.known_face_names=[]

        num=0
        for face in face_list:
            num+=1
            print(num,"have loaded")
            name = face.split(".")[0]

            img = cv2.imread("D:/PycharmProjects/System/recognition/face_dataset/111/"+face)
            try:
                img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            except Exception:
                print("read fail")
                continue

            # 检测人脸
            rectangles = self.mtcnn_model.detectFace(img, self.threshold)

            # 转化成正方形
            try :
                rectangles = utils.rect2square(np.array(rectangles))
            except Exception:
                print("capture fail")
                continue
            # facenet要传入一个160x160的图片
            rectangle = rectangles[0]
            # 记下他们的landmark
            landmark = (np.reshape(rectangle[5:15],(5,2)) - np.array([int(rectangle[0]),int(rectangle[1])]))/(rectangle[3]-rectangle[1])*160

            crop_img = img[int(rectangle[1]):int(rectangle[3]), int(rectangle[0]):int(rectangle[2])]
            try:
                crop_img = cv2.resize(crop_img,(160,160))
            except:
                print("resize fail")
                continue

            new_img,_ = utils.Alignment_1(crop_img,landmark)

            new_img = np.expand_dims(new_img,0)
            # 将检测到的人脸传入到facenet的模型中，实现128维特征向量的提取
            face_encoding = utils.calc_128_vec(self.facenet_model,new_img)

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(name)

    def recognize(self,draw):
        #-----------------------------------------------#
        #   人脸识别
        #   先定位，再进行数据库匹配
        #-----------------------------------------------#
        height,width,_ = np.shape(draw)
        draw_rgb = cv2.cvtColor(draw,cv2.COLOR_BGR2RGB)

        # 检测人脸
        rectangles = self.mtcnn_model.detectFace(draw_rgb, self.threshold)

        if len(rectangles)==0:
            return draw,None

        # 转化成正方形
        rectangles = utils.rect2square(np.array(rectangles,dtype=np.int32))
        rectangles[:,0] = np.clip(rectangles[:,0],0,width)
        rectangles[:,1] = np.clip(rectangles[:,1],0,height)
        rectangles[:,2] = np.clip(rectangles[:,2],0,width)
        rectangles[:,3] = np.clip(rectangles[:,3],0,height)
        #-----------------------------------------------#
        #   对检测到的人脸进行编码
        #-----------------------------------------------#
        face_encodings = []
        for rectangle in rectangles:
            landmark = (np.reshape(rectangle[5:15],(5,2)) - np.array([int(rectangle[0]),int(rectangle[1])]))/(rectangle[3]-rectangle[1])*160

            crop_img = draw_rgb[int(rectangle[1]):int(rectangle[3]), int(rectangle[0]):int(rectangle[2])]
            crop_img = cv2.resize(crop_img,(160,160))

            new_img,_ = utils.Alignment_1(crop_img,landmark)
            new_img = np.expand_dims(new_img,0)

            face_encoding = utils.calc_128_vec(self.facenet_model,new_img)
            face_encodings.append(face_encoding)

        face_names = []
        for face_encoding in face_encodings:
            # 取出一张脸并与数据库中所有的人脸进行对比，计算得分
            matches = utils.compare_faces(self.known_face_encodings, face_encoding, tolerance = 0.75)
            name = "Unknown"
            # 找出距离最近的人脸
            face_distances = utils.face_distance(self.known_face_encodings, face_encoding)
            # 取出这个最近人脸的评分
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            face_names.append(name)

        rectangles = rectangles[:,0:4]
        #-----------------------------------------------#
        #   画框~!~
        #-----------------------------------------------#
        for (left, top, right, bottom), name in zip(rectangles, face_names):
            cv2.rectangle(draw, (left, top), (right, bottom), (0, 0, 255), 2)
            
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(draw, name, (left , bottom - 15), font, 0.75, (255, 255, 255), 2)
        return draw,face_names

    def get(self):
        return self.known_face_names,self.known_face_encodings

class face_recognition():
    def __init__(self):
        self.mtcnn_model = mtcnn()
        self.threshold = [0.5, 0.8, 0.9]
        self.facenet_model = InceptionResNetV1()
        model_path = 'D:/PycharmProjects/System/recognition/model_data/facenet_keras.h5'
        self.facenet_model.load_weights(model_path)
        self.known_face_encodings,self.known_face_names = get_data()



    def recognize(self, draw):
        # -----------------------------------------------#
        #   人脸识别
        #   先定位，再进行数据库匹配
        # -----------------------------------------------#
        height, width, _ = np.shape(draw)
        draw_rgb = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)

        # 检测人脸
        rectangles = self.mtcnn_model.detectFace(draw_rgb, self.threshold)

        if len(rectangles) == 0:
            return draw, None

        # 转化成正方形
        rectangles = utils.rect2square(np.array(rectangles, dtype=np.int32))
        rectangles[:, 0] = np.clip(rectangles[:, 0], 0, width)
        rectangles[:, 1] = np.clip(rectangles[:, 1], 0, height)
        rectangles[:, 2] = np.clip(rectangles[:, 2], 0, width)
        rectangles[:, 3] = np.clip(rectangles[:, 3], 0, height)
        # -----------------------------------------------#
        #   对检测到的人脸进行编码
        # -----------------------------------------------#
        face_encodings = []
        for rectangle in rectangles:
            landmark = (np.reshape(rectangle[5:15], (5, 2)) - np.array([int(rectangle[0]), int(rectangle[1])])) / (
                        rectangle[3] - rectangle[1]) * 160

            crop_img = draw_rgb[int(rectangle[1]):int(rectangle[3]), int(rectangle[0]):int(rectangle[2])]
            crop_img = cv2.resize(crop_img, (160, 160))

            new_img, _ = utils.Alignment_1(crop_img, landmark)
            new_img = np.expand_dims(new_img, 0)

            face_encoding = utils.calc_128_vec(self.facenet_model, new_img)
            face_encodings.append(face_encoding)

        face_names = []
        for face_encoding in face_encodings:
            # 取出一张脸并与数据库中所有的人脸进行对比，计算得分
            matches = utils.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.75)
            name = "Unknown"
            # 找出距离最近的人脸
            face_distances = utils.face_distance(self.known_face_encodings, face_encoding)
            # 取出这个最近人脸的评分
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            face_names.append(name)

        rectangles = rectangles[:, 0:4]
        # -----------------------------------------------#
        #   画框~!~
        # -----------------------------------------------#
        for (left, top, right, bottom), name in zip(rectangles, face_names):
            cv2.rectangle(draw, (left, top), (right, bottom), (0, 0, 255), 2)

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(draw, name, (left, bottom - 15), font, 0.75, (255, 255, 255), 2)
        return draw, face_names





if __name__ == "__main__":

    dududu = face_recognition()
    #video = "http://dafei:dafei@192.168.43.54:8081/"  # 此处@后的ipv4 地址需要修改为自己的地址
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, draw = video_capture.read()
        dududu.recognize(draw) 
        cv2.imshow('Video', draw)
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()