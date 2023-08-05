# !/usr/bin/python3
# coding=utf8
import cv2
import numpy as np
import time
import math
import threading
from ddcmaker.AI.lab_conf import color_range

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


# global Running
# Running = True


def get_image():
    global orgFrame
    global ret
    global cap
    global width, height
    while True:
        if cap.isOpened():
            ret, orgFrame = cap.read()
        else:
            ret = False
            time.sleep(0.01)


th1 = threading.Thread(target=get_image)
th1.setDaemon(True)
th1.start()

global color_max
global action_finish

Color_BGR = (0, 0, 0)
COLOR = 'None'


def get_color():
    while True:
        if orgFrame is not None and ret:

            orgframe = cv2.resize(orgFrame, (width, height), interpolation=cv2.INTER_CUBIC)
            frame = cv2.GaussianBlur(orgframe, (3, 3), 0)
            Frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

            rad = 0
            areaMaxContour = 0
            max_area = 0
            area_max = 0
            centerX = 0
            centerY = 0
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
                if color_max != 'None':
                    return color_max
                else:
                    return "None"
            else:
                Color_BGR = (0, 0, 0)
                COLOR = "None"
                return 'None'
        else:
            time.sleep(0.01)



