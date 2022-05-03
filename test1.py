import cv2
video = "rtsp://192.168.1.4:8899/user=admin&password=&channel=1&stream=0.sdp?"
cap=cv2.VideoCapture(video)
print(cap.isOpened())
if cap.isOpened() == False:
    cap.open(video)
print(cap.isOpened())

while True:
    ret, draw = cap.read()
    #dududu.recognize(draw)
    cv2.imshow('Video', draw)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()