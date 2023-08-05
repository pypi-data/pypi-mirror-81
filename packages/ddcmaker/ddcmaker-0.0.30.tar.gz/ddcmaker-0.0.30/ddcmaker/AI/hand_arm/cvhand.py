import sys
import threading
import time

import cv2

from . import LeArm
from . import img_pro

Deviation = (1500, 1500, 1500, 1400, 1500, 1460)
count_down_time = 30
count_down_time_flag = count_down_time
count = 0
get_hand = False
last_hand = 0
hand_count = 0
hand_location = None
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
                    CvHand(orgframe)
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


def CvHand(frame):
    global get_hand, hand_location
    binary = img_pro.image_process(frame)
    # cv2.imshow('bin', binary)
    # 模板比较，摄像头图像和，文件夹中的样张比较
    hand_location = img_pro.template_matching(binary, frame, '/home/pi/Hand_Arm_Pi/bmp100')
    if hand_location is not None and hand_location is not False:
        get_hand = True


def run_action():
    global get_hand
    global last_hand
    global hand_count
    global hand_location
    global count
    global reset
    while True:
        if reset:
            reset = False
            LeArm.runActionGroup('0_0', 1)
        if get_hand:
            get_hand = False
            if hand_location == last_hand:
                hand_count += 1
                if hand_count >= 5:  # 识别5次
                    hand_count = 0
                    last_hand = 0
                    if hand_location == '0_0':
                        print('0_0')
                        LeArm.runActionGroup('0_0', 1)
                    elif hand_location == '5_12345':
                        print('5_12345')
                        LeArm.runActionGroup('5_12345', 1)
                    elif hand_location == '1_1':
                        print('1_1')
                        LeArm.runActionGroup('1_1', 1)
                    elif hand_location == '1_2':
                        print('1_2')
                        LeArm.runActionGroup('1_2', 1)
                    elif hand_location == '1_5':
                        print('1_5')
                        LeArm.runActionGroup('1_5', 1)
                    elif hand_location == '2_12':
                        print('2_12')
                        LeArm.runActionGroup('2_12', 1)
                    elif hand_location == '2_23':
                        print('2_23')
                        LeArm.runActionGroup('2_23', 1)
                    elif hand_location == '2_25':
                        print('2_25')
                        LeArm.runActionGroup('2_25', 1)
                    elif hand_location == '2_15':
                        print('2_15')
                        LeArm.runActionGroup('2_15', 1)
                    elif hand_location == '2_45':
                        print('2_45')
                        LeArm.runActionGroup('2_45', 1)
                    elif hand_location == '3_123':
                        print('3_123')
                        LeArm.runActionGroup('3_123', 1)
                    elif hand_location == '3_234':
                        print('3_234')
                        LeArm.runActionGroup('3_234', 1)
                    elif hand_location == '3_235':
                        print('3_235')
                        LeArm.runActionGroup('3_235', 1)
                    elif hand_location == '3_345':
                        print('3_345')
                        LeArm.runActionGroup('3_345', 1)
                    elif hand_location == '4_2345':
                        print('4_2345')
                        LeArm.runActionGroup('4_2345', 1)
            else:
                hand_count = 0
            last_hand = hand_location
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


def get_cv_hand():
    global orgframe, count_down_time, count_down_time_flag
    while True:
        if count_down_time == 0:
            print(f"程序终止，系统默认时间为{count_down_time_flag}s")
            return
        try:
            t1 = cv2.getTickCount()
            cv2.putText(orgframe, "Mode: CvHand",
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
