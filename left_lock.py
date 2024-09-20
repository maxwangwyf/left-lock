
from PIL import Image
from pystray import MenuItem,Icon
import cv2
from ctypes import *
import threading
import win32gui,win32con
def get_hwnd_from_name(name):
    hWnd_list = []
    win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWnd_list)
    for hwnd in hWnd_list:
        title = win32gui.GetWindowText(hwnd)
        if title == name:
            return hwnd
        else:
            continue
def left_lock():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
        # 调用摄像头摄像头
    cap = cv2.VideoCapture(0)
    #绝对路径
    # face_cascade = cv2.CascadeClassifier(rf'{cv2.data.haarcascades}\haarcascade_frontalface_default.xml')
    # eye_cascade = cv2.CascadeClassifier(rf'{cv2.data.haarcascades}\haarcascade_eye.xml')
    #相对路径
    i=0
    while(True): 
        # 获取摄像头拍摄到的画面
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        faces = face_cascade.detectMultiScale(frame, 1.3, 5)

        if  isinstance(faces,tuple):
            i=i+1
        else:
            i=0
        if i>=100:
            user32 = windll.LoadLibrary('user32.dll')
            user32.LockWorkStation()
            i=0    
        img = frame
        for (x,y,w,h) in faces:
            # 画出人脸框，蓝色，画笔宽度微
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            # 框选出人脸区域，在人脸区域而不是全图中进行人眼检测，节省计算资源
            face_area = img[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(face_area)
            # 用人眼级联分类器引擎在人脸区域进行人眼识别，返回的eyes为眼睛坐标列表
            for (ex,ey,ew,eh) in eyes:
                #画出人眼框，绿色，画笔宽度为1
                cv2.rectangle(face_area,(ex,ey),(ex+ew,ey+eh),(0,255,0),1)       
        # 实时展示效果画面
        # cv2.namedWindow('image',cv2.WINDOW_NORMAL)
        cv2.imshow('image',img)
        k=cv2.waitKey(1)
    # 点击窗口X按钮关闭窗口，窗口名字要对应
        if cv2.getWindowProperty('image',cv2.WND_PROP_VISIBLE) < 1.0: 
            break 
        if k == 27:
            break
        elif k == ord('s'):    
            cv2.imwrite('D:/project1/1.jpg', img)
    # 最后，关闭所有窗口
    cap.release()
    cv2.destroyAllWindows()


def quit(icon, item):
    hwnd=get_hwnd_from_name('image')
    if hwnd :
        
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)  # 发送关闭消息
    icon.stop()
    

def on_start(icon, item):
    thread1 = threading.Thread(target=left_lock)
    thread1.start()
    thread1.join()

def main():
    menu = (MenuItem(text='启用此功能', action=on_start),MenuItem(text='退出', action=quit),)
    image = Image.open("leave.png")
    icon = Icon("name", image, "点击【启用此功能】打开人脸识别，需要有摄像头", menu)
    icon.run()
if __name__=='__main__':
    main()
