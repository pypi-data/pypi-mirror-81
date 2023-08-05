import sys
import threading
import time

import cv2
from pyzbar import pyzbar

from . import LeArm

barcodeData = None
Deviation = (1500, 1500, 1500, 1400, 1500, 1460)
get_qrcode = False
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
count_down_time = 30
count_down_time_flag = count_down_time
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
                    QcCode(orgFrame, 240, 180)
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


def QcCode(frame, rw=160, rh=120):
    global barcodeData, get_qrcode
    global ori_width

    frame = cv2.flip(frame, -1)
    frame = cv2.resize(frame, (rw, rh), interpolation=cv2.INTER_CUBIC)
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        x, y, w, h = picture_box(x, y, w, h, rw, rh)
        cv2.rectangle(orgframe, (ori_width - x, y), (ori_width - x - w, y + h), (0, 0, 255), 2)  # 画框
        barcodeData = barcode.data.decode("utf-8")
        cv2.putText(orgframe, barcodeData, (ori_width - x - w, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        if barcodeData == 'run1':
            get_qrcode = True
        elif barcodeData == 'run2':
            get_qrcode = True
        else:
            continue


def run_action():
    global get_qrcode
    global reset
    while True:
        if reset:
            reset = False
            LeArm.runActionGroup('0_0', 1)
        if get_qrcode:
            get_qrcode = False
            if barcodeData == 'run1':
                LeArm.runActionGroup('hello', 1)
            if barcodeData == 'run2':
                LeArm.runActionGroup('red', 1)
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


def get_qc_code():
    global orgframe, count_down_time, count_down_time_flag
    while True:
        if count_down_time == 0:
            print(f"程序终止，系统默认时间为{count_down_time_flag}s")
            return
        try:
            t1 = cv2.getTickCount()
            cv2.putText(orgframe, "Mode: QcCode",
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
