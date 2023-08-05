import re
import sys
import threading
import time

import cv2
import dlib

from . import LeArm
from . import pid

count_down_time = 30
count_down_time_flag = count_down_time
Deviation = (1500, 1500, 1500, 1400, 1500, 1460)
reset = False
debug = True
stream = "http://127.0.0.1:8080/?action=stream?dummy=param.mjpg"
orgFrame = None
orgframe = None
stop = False
get_image_ok = False
rz = 60
ori_width = int(rz * 4)  # 原始图像640x480
ori_height = int(rz * 3)
cap = cv2.VideoCapture(stream)


def get_image():
    global get_image_ok, orgframe, cap, orgFrame
    global ori_width, ori_height, stream
    while True:
        try:
            if cap.isOpened():
                ret, orgFrame = cap.read()
                if ret:
                    org = cv2.resize(orgFrame, (ori_width, ori_height), interpolation=cv2.INTER_CUBIC)
                    orgframe = cv2.flip(org, 0)
                    if rpi == 3:
                        FaceTrack(orgFrame, 120, 90)
                    elif rpi == 4:
                        Face_Track(orgframe)
                else:
                    time.sleep(0.01)
            else:
                time.sleep(0.01)
        except:
            cap = cv2.VideoCapture(stream)
            print('Restart Camera Successful!')


th1 = threading.Thread(target=get_image)
th1.setDaemon(True)
th1.start()

# 偏差
if not len(Deviation) == 6:
    print("偏差数量错误")
    sys.exit()
else:
    d = []
    for i in range(0, len(Deviation), 1):
        if Deviation[i] > 1800 or Deviation[i] < 1200:
            print("偏差值超出范围1200-1800")
            sys.exit()
        else:
            d.append(Deviation[i] - 1500)

LeArm.initLeArm(tuple(d))


# 映射函数
def leMap(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def picture_box(x, y, w, h, resize_w, resize_h):
    global ori_width
    global ori_height

    x = int(leMap(x, 0, resize_w, 0, ori_width))
    y = int(leMap(y, 0, resize_h, 0, ori_height))
    w = int(leMap(w, 0, resize_w, 0, ori_width))
    h = int(leMap(h, 0, resize_h, 0, ori_height))
    return x, y, w, h


def get_cpu_mode():
    f_cpu_info = open("/proc/cpuinfo")
    for i in f_cpu_info:
        if re.search('Model', i):
            mode = re.findall('\d+', i)[0]
            break
    return mode


face_cascade = cv2.CascadeClassifier('/home/pi/Hand_Arm_Pi/opencv/haarcascades/haarcascade_frontalface_default.xml')
# 这个只有右侧脸数据，通过图片翻转获得左侧脸
side_face_cascade = cv2.CascadeClassifier('/home/pi/Hand_Arm_Pi/opencv/haarcascades/haarcascade_profileface.xml')  # 侧脸

rpi = int(get_cpu_mode())
count2 = 0
detector = dlib.get_frontal_face_detector()  # 获取人脸分类器
if rpi == 4:
    x2_pid = pid.PID(P=0.5, I=0.01, D=0)
x2_dis = 1500
dis2_ok = False


def Face_Track(frame):
    global x2_dis, dis2_ok, ori_width

    # 获取图像中心点坐标x, y
    img_center_x = ori_width / 2

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    dets = detector(gray)  # 使用detector进行人脸检测 dets为返回的结果
    if len(dets) == 1:
        for face in dets:
            cv2.rectangle(orgframe, (face.left(), face.top()), (face.right(), face.bottom()), (0, 255, 0), 2)
            center_x = (face.right() + face.left()) / 2
            center_y = (face.top() + face.bottom()) / 2
            # 设置要保持的点的位置
            x2_pid.SetPoint = img_center_x
            # pid计算
            x2_pid.update(center_x)
            cv2.circle(orgframe, (int(center_x), int(center_y)), 5, (0, 0, 255), -1)
            # pid输出
            x_pwm = x2_pid.output

            x2_dis -= x_pwm
            x2_dis = int(x2_dis)
            if x2_dis < 500:
                x2_dis = 500
            elif x2_dis > 2500:
                x2_dis = 2500
            dis2_ok = True
    else:
        dis2_ok = False


if rpi == 3:
    x2_pid = pid.PID(P=0.3, I=0, D=0)


def FaceTrack(frame, rw=120, rh=90):
    global x2_dis, dis2_ok, orgframe

    frame = cv2.flip(frame, 0)
    frame = cv2.resize(frame, (rw, rh), interpolation=cv2.INTER_CUBIC)
    left_frame = cv2.flip(frame, 1)
    img_h, img_w = frame.shape[:2]
    # 获取图像中心点坐标x, y
    img_center_x = img_w / 2
    img_center_y = img_h / 2
    # print(img_center_x, img_center_y)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 正脸 + 右侧脸
    left_gray = cv2.cvtColor(left_frame, cv2.COLOR_BGR2GRAY)  # 左侧脸

    faces = face_cascade.detectMultiScale(gray, 1.5, 5)  # 正脸
    r_side_face = side_face_cascade.detectMultiScale(gray, 1.5, 5)  # 右脸
    l_side_face = side_face_cascade.detectMultiScale(left_gray, 1.5, 5)  # 左脸
    y = 0
    x = 0
    w = 0
    h = 0
    if len(faces):
        for x, y, h, w in faces:
            x, y, h, w = picture_box(x, y, h, w, rw, rh)
            cv2.rectangle(orgframe, (x, y), (x + w, y + h), (200, 255, 0), 2)
    elif len(r_side_face):
        for x, y, h, w in r_side_face:
            x, y, h, w = picture_box(x, y, h, w, rw, rh)
            cv2.rectangle(orgframe, (x, y), (x + w, y + h), (0, 255, 0), 2)
    elif len(l_side_face):
        for x, y, h, w in l_side_face:
            x, y, h, w = picture_box(x, y, h, w, rw, rh)
            cv2.rectangle(orgframe, (img_w - x - w, y), (img_w - x, y + h), (200, 0, 0), 2)

    if len(faces) == 1 or len(l_side_face) == 1 or len(r_side_face) == 1:  # 只能有一个的时候跟随
        # print(x, y, radius)
        # 设置要保持的点的位置
        x2_pid.SetPoint = img_center_x
        # pid计算
        x2_pid.update(x - (w / 2))
        cv2.circle(orgframe, (int(x + (w / 2)), int(y + (h / 2))), 5, (0, 0, 255), -1)
        # pid输出
        x_pwm = x2_pid.output

        x2_dis -= x_pwm
        x2_dis = int(x2_dis)
        if x2_dis < 500:
            x2_dis = 500
        elif x2_dis > 2500:
            x2_dis = 2500
        dis2_ok = True
    else:
        dis2_ok = False


def run_action():
    global dis2_ok, x2_dis
    global reset
    while True:
        if reset:
            reset = False
            LeArm.runActionGroup('0_0', 1)
        if dis2_ok is True:

            LeArm.setServo(6, x2_dis, 30)
            dis2_ok = False
        else:
            time.sleep(0.01)


th2 = threading.Thread(target=run_action)
th2.setDaemon(True)
th2.start()


def count_down():
    global count_down_time
    """倒计时"""
    while True:
        time.sleep(1)
        count_down_time -= 1
        if count_down_time == 0:
            break


th3 = threading.Thread(target=count_down)
th3.setDaemon(True)
th3.start()


def get_face_track():
    global orgframe, count_down_time, count_down_time_flag
    while True:
        if count_down_time == 0:
            print(f"程序终止，系统默认时间为{count_down_time_flag}s")
            return
        try:
            t1 = cv2.getTickCount()
            cv2.putText(orgframe, "Mode: FaceTrack",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)  # (0, 0, 255)BGR

            t2 = cv2.getTickCount()
            time_r = (t2 - t1) / cv2.getTickFrequency()
            fps = 1.0 / time_r
            if debug:
                # 参数：图片, 起点, 终点, 颜色, 粗细
                # 画屏幕中心十字
                cv2.line(orgframe, (int(ori_width / 2) - 20, int(ori_height / 2)),
                         (int(ori_width / 2) + 20, int(ori_height / 2)), (255, 255, 0), 1)
                cv2.line(orgframe, (int(ori_width / 2), int(ori_height / 2) - 20),
                         (int(ori_width / 2), int(ori_height / 2) + 20), (255, 255, 0), 1)
                cv2.putText(orgframe, "fps:" + str(int(fps)),
                            (10, orgframe.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255),
                            2)  # (0, 0, 255)BGR
                cv2.waitKey(1)
        except:
            pass
