import sys
import threading
import time

import cv2

from . import LeArm
from . import img_pro

Deviation = (1500, 1500, 1500, 1400, 1500, 1460)
# 偏差
count_down_time = 30
count_down_time_flag = count_down_time
last_hand_num = None
two_last_hand_num = 0
count = 0
hand_num = None
get_hand_num = False
reset = False
debug = True

stream = "http://127.0.0.1:8080/?action=stream?dummy=param.mjpg"
orgFrame = None
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
                    CvHandNumber(orgframe)
                    get_image_ok = True
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


def CvHandNumber(frame):
    global get_hand_num, hand_num
    binary = img_pro.image_process(frame)
    # cv2.imshow('bin', binary)
    # 获取手指个数
    hand_num = img_pro.get_hand_number(binary, frame)
    get_hand_num = True


def run_action():
    global get_hand_num
    global last_hand_num, count, two_last_hand_num, hand_num
    global reset
    while True:
        if reset:
            reset = False
            LeArm.runActionGroup('0_0', 1)
        if get_hand_num:
            get_hand_num = False
            if hand_num == last_hand_num:
                count += 1
                if count >= 2:
                    count = 0
                    last_hand_num = -1
                    # 判断是否和上一次 手指个数相同
                    if two_last_hand_num == hand_num:
                        pass
                    else:
                        if hand_num == 0:
                            LeArm.runActionGroup('zero', 1)
                            print("发现零根手指")
                        if hand_num == 1:
                            LeArm.runActionGroup('one', 1)
                            print("发现一根手指")
                        if hand_num == 2:
                            LeArm.runActionGroup('two', 1)
                            print("发现二根手指")
                        if hand_num == 3:
                            LeArm.runActionGroup('three', 1)
                            print("发现三根手指")
                        if hand_num == 4:
                            LeArm.runActionGroup('four', 1)
                            print("发现四根手指")
                        if hand_num == 5:
                            LeArm.runActionGroup('five', 1)
                            print("发现五根手指")
                    two_last_hand_num = hand_num
            else:
                count = 0
            last_hand_num = hand_num
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


def get_finger_num():
    global orgframe, count_down_time, count_down_time_flag
    while True:
        if count_down_time == 0:
            print(f"程序终止，系统默认时间为{count_down_time_flag}s")
            return
        try:
            t1 = cv2.getTickCount()
            cv2.putText(orgframe, "Mode: CvHandNumber",
                        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)  # (0, 0, 255)BGR
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
