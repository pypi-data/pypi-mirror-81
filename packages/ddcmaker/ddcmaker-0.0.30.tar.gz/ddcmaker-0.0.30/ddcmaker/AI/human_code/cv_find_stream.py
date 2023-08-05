# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-+
# -*- coding: utf-8 -*-                            |
# @Time    : 2019/12/11 17:11                      *
# @Author  : Bob He                                |
# @FileName: cv_find_stream.py                     *
# @Software: PyCharm                               |
# @Project : human_code                            *
# @Csdn    ：https://blog.csdn.net/bobwww123       |
# @Github  ：https://www.github.com/NocoldBob      *
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-+

# !/usr/bin/python3
# coding=utf8
import cv2
import time
import math
# import sys
# import socket
# import signal
import ddcmaker
import threading
# import PWMServo
import numpy as np
from ddcmaker.AI.cv_ImgAddText import cv2ImgAddText
from ddcmaker.AI.lab_conf import color_range
# import Serial_Servo_Running as SSR


# PWMServo.setServo(1, 850, 500)
# PWMServo.setServo(2, 1500, 500)
# SSR.run_ActionGroup('0', 1)
robot = ddcmaker.Robot()
debug = True


def read_data():
    in_file = open("/home/pi/human_code/share.txt", "r")
    state = in_file.readline()
    in_file.close()
    return state


def leMap(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def getAreaMaxContour(contours):
    contour_area_temp = 0
    contour_area_max = 0
    area_max_contour = None;

    for c in contours:
        contour_area_temp = math.fabs(cv2.contourArea(c))
        if contour_area_temp > contour_area_max:
            contour_area_max = contour_area_temp
            if contour_area_temp > 50:
                area_max_contour = c

    return area_max_contour

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

SSR.start_action_thread()
last_centerX = 0
step = 1
count = 0
centerX = 0
centerY = 0
xc = False
x_dev = 70


# 执行动作组
def logic():
    global xc
    global centerX
    global centerY
    global Running
    global step
    global last_centerX
    global x_dev
    while True:
        if Running is True:
            if xc is True or (last_centerX != x_dev and step == 3):
                if step == 1:
                    if 640 >= centerX > 400:
                        # SSR.run_ActionGroup('right_move', 1)
                        robot.run_action_file('right_move')
                        # robot.right_slide()
                        print('1')
                        xc = False
                    elif 0 <= centerX < 200:
                        # SSR.run_ActionGroup('left_move', 1)
                        robot.run_action_file('left_move')
                        # robot.left_slide()
                        print('2')
                        xc = False
                    else:
                        step = 2
                elif step == 2:
                    if 0 <= centerY <= 450:
                        sta = read_data()
                        if sta == 'True':
                            # SSR.change_action_value('go', 1)
                            robot.run_action_file('go')
                            # robot.forward()
                    else:
                        # SSR.stop_action_group()
                        # SSR.run_ActionGroup('go', 1)
                        robot.run_action_file('go')
                        # robot.forward()
                        xc = False
                        step = 3
                elif step == 3:

                    if 640 >= centerX > 600 or 340 < centerX < 500:
                        # SSR.run_ActionGroup('right_move', 1)
                        robot.run_action_file('right_move')
                        # robot.right_slide()
                        print('1')
                        xc = False
                    elif 0 < centerX < 240:
                        # SSR.run_ActionGroup('left_move', 1)
                        robot.run_action_file('left_move')
                        # robot.left_slide()
                        print('2')
                        xc = False
                    elif 500 <= centerX <= 600 or 320 <= last_centerX <= 640:
                        print('3')
                        # SSR.run_ActionGroup('stand_slow', 1)
                        # SSR.run_ActionGroup('shor_right', 1)
                        robot.run_action_file('stand_slow')
                        robot.run_action_file('shor_right')
                        step = 1
                        xc = False
                    elif 240 <= centerX <= 340 or 0 < last_centerX <= 320:
                        # SSR.run_ActionGroup('stand_slow', 1)
                        # SSR.run_ActionGroup('shot_left', 1)
                        robot.run_action_file('stand_slow')
                        robot.run_action_file('shot_left')
                        step = 1
                        print('4')
                        xc = False
                    else:
                        time.sleep(0.01)
            else:
                time.sleep(0.01)
        else:
            time.sleep(0.01)


th2 = threading.Thread(target=logic)
th2.setDaemon(True)
th2.start()

range_rgb = {'red': (0, 0, 255),
             'blue': (255, 0, 0),
             'green': (0, 255, 0),
             }
print('''
--程序正常运行中......
--分辨率:{0}                                                                                         
'''.format(resolution))

circles_list = []
while True:
    if orgFrame is not None and ret:
        if Running:
            t1 = cv2.getTickCount()
            orgframe = cv2.resize(orgFrame, (width, height), interpolation=cv2.INTER_CUBIC)
            gray_img = cv2.cvtColor(orgframe, cv2.COLOR_BGR2GRAY)
            img = cv2.medianBlur(gray_img, 11)
            circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 400, param1=100, param2=20, minRadius=10,
                                       maxRadius=60)
            if circles is not None:
                circles = np.uint16(np.around(circles))
                circle = circles[0, :][0]
                centerX, centerY, rad = circle[0], circle[1], circle[2]
                circles_list.append([centerX, centerY])
                if len(circles_list) == 10:
                    var = np.mean(np.var(circles_list, axis=0))
                    circles_list = []
                    if var <= 1:
                        xc = True

                        last_centerX = centerX
                cv2.circle(orgframe, (centerX, centerY), rad, (255, 0, 0), 2)
                centerX = int(leMap(centerX, 0.0, width, 0.0, 640.0))  # 将数据从0-width 映射到 0-640
                centerY = int(leMap(centerY, 0.0, height, 0.0, 480.0))
            else:
                centerX, centerY = 0, 0
            centerX = centerX + x_dev
            t2 = cv2.getTickCount()
            time_r = (t2 - t1) / cv2.getTickFrequency()
            fps = 1.0 / time_r
            if debug:
                print(centerX)
                orgframe = cv2ImgAddText(orgframe, "点球射门", 10, 10, textColor=(0, 0, 0), textSize=20)
                cv2.putText(orgframe, "FPS:" + str(int(fps)),
                            (10, orgframe.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255),
                            2)  # (0, 0, 255)BGR
                cv2.imshow("orgFframe", orgframe)
                cv2.waitKey(1)
        else:
            time.sleep(0.01)
    else:
        time.sleep(0.01)
cap.release()
cv2.destroyAllWindows()


