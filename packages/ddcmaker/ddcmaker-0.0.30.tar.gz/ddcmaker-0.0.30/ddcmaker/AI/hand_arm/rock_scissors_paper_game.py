import sys
import threading
import time

import cv2

from . import LeArm
from . import img_pro

count_down_time = 30
count_down_time_flag = count_down_time
Deviation = (1500, 1500, 1500, 1400, 1500, 1460)
new_hand_num = None
last_hand_num = None
reset = False
debug = True
get_angle_ok = False
game_list = ['石头', '剪刀', '布']
game_action_list = ['rock', 'scissors', 'paper']  # 石头 ， 剪刀， 布
stream = "http://127.0.0.1:8080/?action=stream?dummy=param.mjpg"
orgFrame = None
orgframe = None
get_image_ok = False
rz = 60
ori_width = int(rz * 4)  # 原始图像640x480
ori_height = int(rz * 3)

cap = cv2.VideoCapture(stream)


def get_image():
    global orgframe, cap, orgFrame
    global ori_width, ori_height, stream
    while True:
        try:
            if cap.isOpened():
                ret, orgFrame = cap.read()
                if ret:
                    org = cv2.resize(orgFrame, (ori_width, ori_height), interpolation=cv2.INTER_CUBIC)
                    orgframe = cv2.flip(org, 0)
                    RockPaperScissor(orgframe)
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


# 石头剪刀布识别函数
def RockPaperScissor(frame):
    global get_angle_ok, new_hand_num
    # 查找轮廓，返回最大轮廓
    binary = img_pro.image_process(frame)
    # cv2.imshow('bin', binary)
    # 获取手指个数
    hand_num = img_pro.get_hand_number(binary, frame)
    if hand_num is not None:
        new_hand_num = hand_num
        get_angle_ok = True
    else:
        get_angle_ok = False


# 做出相应动作的函数
def run_action():
    global new_hand_num, last_hand_num
    global reset
    while True:
        if reset:
            reset = False
            LeArm.runActionGroup('0_0', 1)
        if last_hand_num != new_hand_num:
            # 没有检测到手
            if new_hand_num is not None and get_angle_ok is not False:
                # 判断是否是有效
                game_state = img_pro.rock_paper_scissors(new_hand_num)
                if game_state is not None:
                    print('你出:' + game_list[game_state])
                # 执行石头、剪刀、布动作组
                if game_state == 0:  # 你出石头
                    LeArm.runActionGroup(game_action_list[2], 1)  # 布
                elif game_state == 1:  # 你出剪刀
                    LeArm.runActionGroup(game_action_list[0], 1)  # 石头
                elif game_state == 2:  # 你出布
                    LeArm.runActionGroup(game_action_list[1], 1)  # 剪刀
                last_hand_num = new_hand_num
            else:
                time.sleep(0.01)
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


def rock_scissors_paper():
    global count_down_time, count_down_time_flag
    while True:
        if count_down_time == 0:
            print(f"程序终止，系统默认时间为{count_down_time_flag}s")
            return
        try:
            t1 = cv2.getTickCount()
            cv2.putText(orgframe, "Mode: RockPaperScissor",
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
