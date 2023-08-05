# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-+
# -*- coding: utf-8 -*-                            |
# @Time    : 2019/12/11 17:18                      *
# @Author  : Bob He                                |
# @FileName: cv_track_stream.py                    *
# @Software: PyCharm                               |
# @Project : human_code                            *
# @Csdn    ：https://blog.csdn.net/bobwww123       |
# @Github  ：https://www.github.com/NocoldBob      *
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-+

# !/usr/bin/python3
# coding=utf8
# 颜色跟踪:识别对应颜色的小球,让摄像头跟随小球转动
import cv2
import sys
import numpy as np
from ddcmaker.AI import pid
import time
import math
import signal
import socket
import threading
# import PWMServo
from ddcmaker.AI.cv_ImgAddText import cv2ImgAddText
from ddcmaker.AI.lab_conf import color_range
# import Serial_Servo_Running as SSR
import ddcmaker
from ddcmaker.maker.human_code.controller import PWMServoController
pwm = PWMServoController()
robot = ddcmaker.Robot()

# PWMServo.setServo(1, 1500, 500)
# PWMServo.setServo(2, 1500, 500)
# SSR.run_ActionGroup('0', 1)

# debug = True
target_color = "blue"
if len(sys.argv) == 3:
    if sys.argv[1] == 'display':
        Running = True
        debug = True
        target_color = sys.argv[2]
        if target_color == "red":
            target_color = "red"
        elif target_color == "green":
            target_color = "green"
        elif target_color == "blue":
            target_color = "blue"
        else:
            print("异常：颜色参数输入错误！")
            sys.exit()
    elif sys.argv[1] == 'no_display':
        Running = True
        debug = False
        target_color = sys.argv[2]
        if target_color == "red":
            target_color = "red"
        elif target_color == "green":
            target_color = "green"
        elif target_color == "blue":
            target_color = "blue"
        else:
            print("异常：颜色参数输入错误！")
            sys.exit()
    else:
        print("异常：模式参数输入错误！")
        sys.exit()
elif len(sys.argv) == 2:
    if sys.argv[1] == 'display':
        Running = True
        debug = True
    elif sys.argv[1] == 'no_display':
        Running = True
        debug = False
    else:
        print("异常：模式参数输入错误！")
        sys.exit()
else:
    debug = False
    Running = False


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
            if contour_area_temp > 100:
                area_max_contour = c

    return area_max_contour

c = 80
width, height = c * 4, c * 3
resolution = str(width) + "x" + str(height)

print('''
--程序正常运行中......
--分辨率:{0}                                              
--识别颜色:{1}                                            
'''.format(resolution, target_color))

stream = "http://127.0.0.1:8080/?action=stream?dummy=param.mjpg"
cap = cv2.VideoCapture(stream)
orgFrame = None
# Running = True
ret = False


# 获取图像`
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

dis_ok = False
action_finish = True
servo_1 = 1
servo_2 = 2


def Move():
    global servo_1
    global servo_2
    global dis_ok, x_dis, y_dis
    global action_finish
    while True:
        # 云台跟踪
        if dis_ok is True:
            dis_ok = False
            action_finish = False
            pwm.set_servo(servo_1, y_dis, 20)
            pwm.set_servo(servo_2, x_dis, 20)
            time.sleep(0.02)
            action_finish = True
        else:
            time.sleep(0.01)


th2 = threading.Thread(target=Move)
th2.setDaemon(True)
th2.start()

x_pid = pid.PID(P=0.1, I=0.02, D=0.01)
y_pid = pid.PID(P=0.2, I=0.02, D=0.01)
x_dis = 1500
y_dis = 1500

range_rgb = {'red': (0, 0, 255),
             'blue': (255, 0, 0),
             'green': (0, 255, 0),
             }
print('''
--程序正常运行中......
--分辨率:{0}                                              
--识别颜色:{1}                                            
'''.format(resolution, target_color))

while True:
    if orgFrame is not None and ret:
        if Running:
            t1 = cv2.getTickCount()
            orgframe = cv2.resize(orgFrame, (width, height), interpolation=cv2.INTER_CUBIC)
            img_center_x = orgframe.shape[:2][1] / 2
            img_center_y = orgframe.shape[:2][0] / 2
            frame = cv2.GaussianBlur(orgframe, (3, 3), 0)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

            frame = cv2.inRange(frame, color_range[target_color][0], color_range[target_color][1])
            opened = cv2.morphologyEx(frame, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
            closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
            contours = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]
            areaMaxContour = getAreaMaxContour(contours)

            centerX = 0
            centerY = 0
            radius = 0

            if areaMaxContour is not None:
                (centerX, centerY), radius = cv2.minEnclosingCircle(areaMaxContour)
                cv2.circle(orgframe, (int(centerX), int(centerY)), int(radius), range_rgb[target_color], 2)
                if radius >= 3:
                    x_pid.SetPoint = img_center_x
                    x_pid.update(centerX)
                    x_pwm = x_pid.output
                    x_dis += x_pwm
                    x_dis = int(x_dis)
                    if x_dis < 500:
                        x_dis = 500
                    elif x_dis > 2500:
                        x_dis = 2500
                    y_pid.SetPoint = img_center_y
                    y_pid.update(2 * img_center_y - centerY)
                    y_pwm = y_pid.output
                    y_dis -= y_pwm
                    y_dis = int(y_dis)
                    if y_dis < 1100:
                        y_dis = 1100
                    elif y_dis > 1800:
                        y_dis = 1800
                    if action_finish:
                        dis_ok = True

            t2 = cv2.getTickCount()
            time_r = (t2 - t1) / cv2.getTickFrequency()
            fps = 1.0 / time_r
            if debug:
                orgframe = cv2ImgAddText(orgframe, "云台跟踪", 10, 10, textColor=(0, 0, 0), textSize=20)
                cv2.putText(orgframe, "FPS:" + str(int(fps)),
                            (10, orgframe.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255),
                            2)  # (0, 0, 255)BGR
                cv2.imshow("orgframe", orgframe)
                cv2.waitKey(1)
        else:
            time.sleep(0.01)
    else:
        time.sleep(0.01)
cap.release()
cv2.destroyAllWindows()


