import sys
import threading
import time

import cv2
import numpy as np

from . import LeArm
from . import pid

count_down_time = 30
count_down_time_flag = count_down_time
Deviation = (1500, 1500, 1500, 1400, 1500, 1460)
ball_track_color = 'green'
x1_dis = 1500
dis1_ok = False
x1_pid = pid.PID(P=0.3, I=0.1, D=0)
reset = False
debug = True
stream = "http://127.0.0.1:8080/?action=stream?dummy=param.mjpg"
orgFrame = None
orgframe = None
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
                    BallTrack(orgframe)
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

range_rgb = {'red': (0, 0, 255), 'blue': (255, 0, 0), 'green': (0, 255, 0), 'black': (0, 0, 0)}

# 要识别的颜色字典
color_dist = {'red': {'Lower': np.array([0, 60, 60]), 'Upper': np.array([6, 255, 255])},
              'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
              'green': {'Lower': np.array([35, 43, 46]), 'Upper': np.array([77, 255, 255])},
              }


def BallTrack(frame):
    global dis1_ok, x1_dis
    global range_rgb, color_dist
    img_h, img_w = frame.shape[:2]
    # 获取图像中心点坐标x, y
    img_center_x = img_w / 2
    img_center_y = img_h / 2
    # print(img_center_x, img_center_y)
    # 高斯模糊
    gs_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    # 转换颜色空间
    hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)
    # 查找颜色
    mask = cv2.inRange(hsv, color_dist[ball_track_color]['Lower'], color_dist[ball_track_color]['Upper'])
    # 腐蚀
    mask = cv2.erode(mask, None, iterations=2)
    # 膨胀
    mask = cv2.dilate(mask, None, iterations=2)
    # 查找轮廓
    # cv2.imshow('mask', mask)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        # 求出最小外接圆  原点坐标x, y  和半径
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if radius >= 5:  #
            cv2.circle(frame, (int(x), int(y)), int(radius), range_rgb[ball_track_color], 2)
            cv2.circle(frame, (int(x), int(y)), 5, range_rgb[ball_track_color], -1)
            # print(x, y, radius)
            # 设置要保持的点的位置
            x1_pid.SetPoint = img_center_x
            # pid计算
            x1_pid.update(x)
            # pid输出
            x_pwm = x1_pid.output
            # 反方向，所以 负
            x1_dis -= x_pwm
            x1_dis = int(x1_dis)
            if x1_dis < 500:
                x1_dis = 500
            elif x1_dis > 2500:
                x1_dis = 2500
            dis1_ok = True
        else:
            dis1_ok = False


# 做出相应动作的函数
def run_action():
    global dis1_ok, x1_dis
    global reset
    while True:
        if reset:
            reset = False
            # LeArm.runActionGroup('0_0', 1)
        if dis1_ok is True:
            LeArm.setServo(6, x1_dis, 30)
            dis1_ok = False
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


def get_ball_track():
    global orgframe, count_down_time, count_down_time_flag
    while True:
        if count_down_time == 0:
            print(f"程序终止，系统默认时间为{count_down_time_flag}s")
            return
        try:
            t1 = cv2.getTickCount()
            cv2.putText(orgframe, "Mode: BallTrack",
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
