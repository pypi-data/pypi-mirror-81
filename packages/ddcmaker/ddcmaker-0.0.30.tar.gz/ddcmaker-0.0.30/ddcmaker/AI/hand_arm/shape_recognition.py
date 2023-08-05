import random
import sys
import threading
import time

import cv2
import numpy as np

from . import LeArm
from . import img_pro

Deviation = (1500, 1500, 1500, 1400, 1500, 1460)
count_down_time = 30
count_down_time_flag = count_down_time
color_shape_list = []
run_one_ok = False
run_number = 0
step = 0
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
cv_ok = False
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
                    ShapeRecognition(orgframe)
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

# 要识别的颜色字典
color_dist = {'red': {'Lower': np.array([0, 60, 60]), 'Upper': np.array([6, 255, 255])},
              'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
              'green': {'Lower': np.array([35, 43, 46]), 'Upper': np.array([77, 255, 255])},
              }


def ShapeRecognition(frame):
    global color_dist, cv_ok

    img_h, img_w = frame.shape[:2]
    # 高斯模糊
    gs_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    # 转换颜色空间
    hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)
    for i in color_dist:
        # 查找颜色
        mask = cv2.inRange(hsv, color_dist[i]['Lower'], color_dist[i]['Upper'])
        # 腐蚀
        mask = cv2.erode(mask, None, iterations=2)
        # 膨胀
        mask = cv2.dilate(mask, None, iterations=2)
        # 查找轮廓
        cnts = img_pro.find_contours(mask, 3000)
        if cnts is not None:
            cv2.drawContours(orgframe, cnts, -1, (0, 0, 255), 2)
            # 识别形状
            # 周长  0.035 根据识别情况修改，识别越好，越小
            epsilon = 0.035 * cv2.arcLength(cnts, True)
            # 轮廓相似
            approx = cv2.approxPolyDP(cnts, epsilon, True)
            # print len(approx)
            color_shape_list.append([i, len(approx)])
            cv_ok = True


def run_action():
    global cv_ok, run_number, run_one_ok, color_shape_list, step
    global reset

    while True:
        if reset:
            reset = False
            LeArm.runActionGroup('0_0', 1)
        if cv_ok:
            if step == 0:
                if 0 < len(color_shape_list) < 3:
                    if run_one_ok is False:
                        run_number = random.randint(0, len(color_shape_list) - 1)
                        run_one_ok = True
                        step = 1
            if step == 1:  # 执行动作组
                if color_shape_list[run_number][1] == 3:  # 三角形
                    print("三角形")
                    LeArm.runActionGroup('three', 1)  # 执行动作组
                elif color_shape_list[run_number][1] == 4:  # 矩形
                    print("矩形")
                    LeArm.runActionGroup('four', 1)
                elif color_shape_list[run_number][1] >= 6:  # 圆形
                    print("圆形")
                    LeArm.runActionGroup('zero', 1)
                step = 0
                run_one_ok = False
                run_number = 0
            color_shape_list = []
            cv_ok = False
        else:
            time.sleep(0.01)


# 启动动作在运行线程
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


def get_shape_recognition():
    global orgframe, count_down_time, count_down_time_flag
    while True:
        if count_down_time == 0:
            print(f"程序终止，系统默认时间为{count_down_time_flag}s")
            return
        try:
            t1 = cv2.getTickCount()
            cv2.putText(orgframe, "Mode: ShapeRecognition",
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
