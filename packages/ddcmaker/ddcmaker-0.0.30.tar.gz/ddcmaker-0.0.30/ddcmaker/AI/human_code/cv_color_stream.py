# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-+
# -*- coding: utf-8 -*-                            |
# @Time    : 2019/12/11 16:32                      *
# @Author  : Bob He                                |
# @FileName: cv_color_stream.py                    *
# @Software: PyCharm                               |
# @Project : human_code                            *
# @Csdn    ：https://blog.csdn.net/bobwww123       |
# @Github  ：https://www.github.com/NocoldBob      *
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-+
# !/usr/bin/python3
# coding=utf8
import cv2
import ddcmaker
import numpy as np
import time
import math
import threading
from ddcmaker.AI.cv_ImgAddText import cv2ImgAddText
from ddcmaker.AI.lab_conf import color_range
debug = True
robot = ddcmaker.Robot()


def leMap(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def getAreaMaxContour(contours):
    contour_area_temp = 0
    contour_area_max = 0
    area_max_contour = None

    for c in contours:
        contour_area_temp = math.fabs(cv2.contourArea(c))
        if contour_area_temp > contour_area_max:
            contour_area_max = contour_area_temp
            if contour_area_temp > 300:
                area_max_contour = c

    return area_max_contour, contour_area_max


c = 80
width, height = c * 4, c * 3
resolution = str(width) + "x" + str(height)
stream = "http://127.0.0.1:8080/?action=stream?dummy=param.mjpg"
cap = cv2.VideoCapture(stream)
orgFrame = None
ret = False
Running = True


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

get_color = False
color_max = None
action_finish = True


def runAction():
    global get_color, action_finish
    global color_max
    while True:
        if get_color:
            get_color = False
            action_finish = False
            if color_max == 'red':
                robot.nod()
                time.sleep(1)
                action_finish = True
            elif color_max == 'green' or color_max == 'blue':
                robot.shaking_head()
                time.sleep(1)
                action_finish = True
            else:
                get_color = False
                time.sleep(0.01)
        else:
            time.sleep(0.01)


th2 = threading.Thread(target=runAction)
th2.setDaemon(True)
th2.start()

print('''
--程序正常运行中......
--分辨率:{0}                                              
'''.format(resolution))

range_rgb = {'red': (0, 0, 255),
             'blue': (255, 0, 0),
             'green': (0, 255, 0),
             'black': (0, 0, 0),
             }

Color_BGR = (0, 0, 0)
COLOR = 'None'
color_list = []
while True:
    if orgFrame is not None and ret:
        if Running:
            t1 = cv2.getTickCount()
            orgframe = cv2.resize(orgFrame, (width, height), interpolation=cv2.INTER_CUBIC)
            frame = cv2.GaussianBlur(orgframe, (3, 3), 0)
            Frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

            rad = 0
            areaMaxContour = 0
            max_area = 0
            area_max = 0
            centerX = 0
            centerY = 0
            if action_finish:
                for i in color_range:
                    frame = cv2.inRange(Frame, color_range[i][0], color_range[i][1])
                    opened = cv2.morphologyEx(frame, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
                    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
                    contours = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]
                    areaMaxContour, area_max = getAreaMaxContour(contours)
                    if areaMaxContour is not None:
                        if area_max > max_area:
                            max_area = area_max
                            color_max = i
                            areaMaxContour_max = areaMaxContour
            if max_area != 0:
                ((centerX, centerY), rad) = cv2.minEnclosingCircle(areaMaxContour_max)
                centerX, centerY, rad = int(centerX), int(centerY), int(rad)
                cv2.circle(orgframe, (centerX, centerY), rad, (0, 255, 0), 2)
                if color_max == 'red':  # 红色最大
                    color = 1
                elif color_max == 'green':  # 绿色最大
                    color = 2
                elif color_max == 'blue':  # 蓝色最大
                    color = 3
                else:
                    color = 0
                color_list.append(color)
                if len(color_list) == 10:
                    color = int(round(np.mean(color_list)))
                    color_list = []
                    if color == 1:
                        COLOR = 'red'
                        Color_BGR = range_rgb["red"]
                    elif color == 2:
                        COLOR = 'green'
                        Color_BGR = range_rgb["green"]
                    elif color == 3:
                        COLOR = 'blue'
                        Color_BGR = range_rgb["blue"]
                    else:
                        color_max = 'None'
                        Color_BGR = range_rgb["black"]
                    get_color = True
            else:
                if action_finish:
                    Color_BGR = (0, 0, 0)
                    COLOR = "None"

            t2 = cv2.getTickCount()
            time_r = (t2 - t1) / cv2.getTickFrequency()
            fps = 1.0 / time_r
            if debug:
                orgframe = cv2ImgAddText(orgframe, "颜色识别", 10, 10, textColor=(0, 0, 0), textSize=20)
                cv2.putText(orgframe, "Color: " + COLOR, (10, orgframe.shape[0] - 35), cv2.FONT_HERSHEY_SIMPLEX, 0.65,
                            Color_BGR, 2)
                cv2.putText(orgframe, "FPS:" + str(int(fps)),
                            (10, orgframe.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255),
                            2)  # (0, 0, 255)BGR
                cv2.namedWindow('orgframe')
                cv2.imshow("orgframe", orgframe)
                cv2.waitKey(1)
        else:
            time.sleep(0.01)
    else:
        time.sleep(0.01)
cap.release()
cv2.destroyAllWindows()
