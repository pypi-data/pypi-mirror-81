# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-+
# -*- coding: utf-8 -*-                            |
# @Time    : 2019/12/11 16:39                      *
# @Author  : Bob He                                |
# @FileName: cv_find_hand.py                       *
# @Software: PyCharm                               |
# @Project : human_code                            *
# @Csdn    ：https://blog.csdn.net/bobwww123       |
# @Github  ：https://www.github.com/NocoldBob      *
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-+
# !/usr/bin/python3
# coding:utf8
import cv2
import sys
import ddcmaker
import numpy as np
import time
import math
# import socket
# import signal
import threading
# import PWMServo
from ddcmaker.AI.cv_ImgAddText import cv2ImgAddText
# from ddcmaker.ai.lab_conf import color_range
# import Serial_Servo_Running as SSR


# PWMServo.setServo(1, 1500, 500)
# PWMServo.setServo(2, 1500, 500)
# SSR.run_ActionGroup('0', 1)
robot = ddcmaker.Robot()
debug = True


class Point(object):
    x = 0
    y = 0

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Line(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2


def GetCrossAngle(l1, l2):

    arr_0 = np.array([(l1.p2.x - l1.p1.x), (l1.p2.y - l1.p1.y)])
    arr_1 = np.array([(l2.p2.x - l2.p1.x), (l2.p2.y - l2.p1.y)])
    cos_value = (float(arr_0.dot(arr_1)) / (np.sqrt(arr_0.dot(arr_0)) * np.sqrt(arr_1.dot(arr_1))))  # 注意转成浮点数运算
    return np.arccos(cos_value) * (180 / np.pi)


def two_distance(start, end):

    s_x = start[0]
    s_y = start[1]
    e_x = end[0]
    e_y = end[1]
    x = s_x - e_x
    y = s_y - e_y
    return math.sqrt((x ** 2) + (y ** 2))


def image_process(image):
    YCC = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)
    Y, Cr, Cb = cv2.split(YCC)
    # Cr = cv2.inRange(Cr, 138, 175)
    Cr = cv2.inRange(Cr, 132, 175)
    Cb = cv2.inRange(Cb, 100, 140)
    Cb = cv2.bitwise_and(Cb, Cr)

    open_element = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    opend = cv2.morphologyEx(Cb, cv2.MORPH_OPEN, open_element)

    kernel = np.ones((3, 3), np.uint8)
    erosion = cv2.erode(opend, kernel, iterations=1)
    # cv.imshow('1', erosion)
    return erosion


def get_defects_far(defects, contours, img):

    if defects is None and contours is None:
        return None
    far_list = []
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(contours[s][0])
        end = tuple(contours[e][0])
        far = tuple(contours[f][0])

        a = two_distance(start, end)
        b = two_distance(start, far)
        c = two_distance(end, far)

        angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180 / math.pi

        if angle <= 75:  # 90:
            far_list.append(far)
    return far_list


def get_max_coutour(cou, max_area):

    max_coutours = 0
    r_c = None
    if len(cou) < 1:
        return None
    else:
        for c in cou:
            # 计算面积
            temp_coutours = math.fabs(cv2.contourArea(c))
            if temp_coutours > max_coutours:
                max_coutours = temp_coutours
                cc = c
        # 判断所有轮廓中最大的面积
        if max_coutours > max_area:
            r_c = cc
        return r_c


def find_contours(binary, max_area):
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    return get_max_coutour(contours, max_area)


def get_hand_number(binary_image, rgb_image):

    x = 0
    y = 0
    contours = find_contours(binary_image, 1000)
    coord_list = []

    if contours is not None:

        epsilon = 0.025 * cv2.arcLength(contours, True)

        approx = cv2.approxPolyDP(contours, epsilon, True)

        cv2.polylines(rgb_image, [approx], True, (0, 255, 0), 1)

        if approx.shape[0] >= 3:
            approx_list = []
            for j in range(approx.shape[0]):
                # cv2.circle(rgb_image, (approx[j][0][0],approx[j][0][1]), 5, [255, 0, 0], -1)
                approx_list.append(approx[j][0])
            approx_list.append(approx[0][0])  # 在末尾添加第一个点
            approx_list.append(approx[1][0])  # 在末尾添加第二个点

            for i in range(1, len(approx_list) - 1):
                p1 = Point(approx_list[i - 1][0], approx_list[i - 1][1])
                p2 = Point(approx_list[i][0], approx_list[i][1])
                p3 = Point(approx_list[i + 1][0], approx_list[i + 1][1])
                line1 = Line(p1, p2)
                line2 = Line(p2, p3)
                angle = GetCrossAngle(line1, line2)
                angle = 180 - angle  #
                # print angle
                if angle < 42:
                    # cv2.circle(rgb_image, tuple(approx_list[i]), 5, [255, 0, 0], -1)
                    coord_list.append(tuple(approx_list[i]))

        hull = cv2.convexHull(contours, returnPoints=False)

        defects = cv2.convexityDefects(contours, hull)

        hand_coord = get_defects_far(defects, contours, rgb_image)
        new_hand_list = []
        alike_flag = False
        if len(coord_list) > 0:
            for l in range(len(coord_list)):
                for k in range(len(hand_coord)):
                    if (-10 <= coord_list[l][0] - hand_coord[k][0] <= 10 and
                            -10 <= coord_list[l][1] - hand_coord[k][1] <= 10):
                        alike_flag = True
                        break  #
                if alike_flag is False:
                    new_hand_list.append(coord_list[l])
                alike_flag = False
            for i in new_hand_list:
                cv2.circle(rgb_image, tuple(i), 5, [0, 0, 100], -1)
        if new_hand_list is []:
            return 0
        else:
            return len(new_hand_list)
    else:
        return 0

c = 80
width, height = c * 4, c * 3
resolution = str(width) + "x" + str(height)
orgFrame = None
Running = True
ret = False
stream = "http://127.0.0.1:8080/?action=stream?dummy=param.mjpg"
cap = cv2.VideoCapture(stream)


def get_image():
    global orgFrame
    global ret
    global Running
    global cap
    global width, height
    while True:
        if Running:
            if cap.isOpened():
                ret, orgFrame = cap.read()
            else:
                ret = False
                time.sleep(0.01)
        else:
            time.sleep(0.01)


th1 = threading.Thread(target=get_image)
th1.setDaemon(True)
th1.start()

get_hand_num = False
action_finish = True


def runAction():
    global get_hand_num, action_finish
    global num_mean
    while True:
        if get_hand_num:
            get_hand_num = False
            action_finish = False
            if num_mean == 1:
                # print("1")
                num_maen = 0
                # SSR.run_ActionGroup('10', 1)  # 鞠躬
                robot.bow()
                time.sleep(2)
                action_finish = True

            elif num_mean == 2:
                # print("2")
                num_mean = 0
                # SSR.run_ActionGroup('9', 1)  # 挥手
                robot.wave()
                time.sleep(2)
                action_finish = True

            elif num_mean == 5:
                # print("5")
                num_mean = 0
                # SSR.run_ActionGroup('hand5', 1)  # 扭腰
                robot.down()
                time.sleep(3)
                action_finish = True
            else:
                action_finish = True
                time.sleep(0.01)
        else:
            time.sleep(0.01)


# 启动动作在运行线程
th2 = threading.Thread(target=runAction)
th2.setDaemon(True)
th2.start()

print('''
--程序正常运行中......
--分辨率:{0}                                              
'''.format(resolution))

num = []
num_mean = 0
while True:
    if orgFrame is not None and ret:
        if Running:
            t1 = cv2.getTickCount()  # 用来计算帧率
            orgframe = cv2.resize(orgFrame, (width, height), interpolation=cv2.INTER_CUBIC)  # 将图片缩放
            frame = orgframe
            binary = image_process(frame)  # 处理图像
            hand_num = get_hand_number(binary, frame)  # 获取手指个数
            num.append(hand_num)
            if len(num) == 60:
                num_mean = int(round(np.mean(num)))
                num = []
                if action_finish:
                    get_hand_num = True

            t2 = cv2.getTickCount()
            time_r = (t2 - t1) / cv2.getTickFrequency()
            fps = 1.0 / time_r  # 帧率计算
            if debug:
                orgframe = cv2ImgAddText(orgframe, "手势识别", 10, 10, textColor=(0, 0, 0), textSize=20)
                cv2.putText(orgframe, "Detect:" + str(num_mean),
                            (10, orgframe.shape[0] - 35), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255),
                            2)  # 显示最终检测到到手指个数，(0, 0, 255)BGR
                cv2.putText(orgframe, "FPS:" + str(int(fps)),
                            (10, orgframe.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255),
                            2)  # 显示帧率，(0, 0, 255)BGR
                cv2.imshow("orgframe", orgframe)
                cv2.waitKey(1)
        else:
            time.sleep(0.01)
    else:
        time.sleep(0.01)
cap.release()
cv2.destroyAllWindows()



