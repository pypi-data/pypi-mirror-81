#!/usr/bin/python3
# encoding: utf-8
import time
import sqlite3 as sql
import pigpio
from .LeServo import PWM_Servo
import os

Servos = ()
runningAction = False
pi = None
stopRunning = False


def setServo(servoId, pos, time):
    '''
    控制单个舵机
    :param servoId:    舵机ID
    :param pos:     位置
    :param time:    运行时间
    :return:
    '''
    global runningAction
    if servoId < 1 or servoId > 6:
        return
    #  舵机限位，手指舵机堵转会复位！！！！！！！！！
    if servoId == 6:    # 云台舵机
        if pos > 2500:
            pos = 2500
        elif pos < 500:
            pos = 500
    else:
        if pos > 2200:
            pos = 2200
        elif pos < 900:
            pos = 900
    if time > 30000:
        time = 30000
    elif time < 20:
        time = 20
    else:
        pass
    if runningAction is False:
        Servos[servoId - 1].setPosition(pos, time)


def setServo_CMP(servoId, pos, time):
    #print(servoId, pos, time)
    if servoId < 1 or servoId > 6:
        return
    #print(Servos[servoId-1].getPosition())
    setServo(servoId, Servos[servoId - 1].getPosition() + pos, time)


def setDeviation(servoId, d):
    '''
    设置偏差
    :param servoId:
    :param d:
    :return:
    '''
    global runningAction
    if servoId < 1 or servoId > 6:
        return
    if d < -300 or d > 300:
        return
    if runningAction is False:
        Servos[servoId - 1].setDeviation(d)


def stopActionGroup():
    '''
    停止动作组运行
    :return:
    '''
    global stopRunning
    stopRunning = True


def runActionGroup(actNum, times):
    '''
    运行动作组
    :param actNum:  动作组文件名
    :param times:   运行次数，没有实现， 自行可以for循环实现
    :return:
    '''
    global runningAction
    global stopRunning
    actNum = "/home/pi/Hand_Arm_Pi/ActionGroups/" + actNum + ".d6a"
    if os.path.exists(actNum) is True:
        ag = sql.connect(actNum)
        cu = ag.cursor()
        cu.execute("select * from ActionGroup")
        if runningAction is False:
            runningAction = True
            while True:
                if stopRunning is True:
                    stopRunning = False
                    runningAction = False
                    cu.close()
                    ag.close()
                    break
                act = cu.fetchone()
                if act is not None:
                    # print(act)
                    for i in range(0, 6, 1):
                        Servos[i].setPosition(act[2 + i], act[1])
                    time.sleep(float(act[1])/1000.0)
                else:
                    runningAction = False
                    cu.close()
                    ag.close()
                    break
    else:
        runningAction = False
        print("未能找到动作组文件")


def initLeArm(d):
    '''
    初始舵机
    :param d:
    :return:
    '''
    global Servos
    global pi
    pi = pigpio.pi()
    servo1 = PWM_Servo(pi, 12,  deviation=d[0], control_speed=True)
    servo2 = PWM_Servo(pi, 16, deviation=d[1], control_speed=True)
    servo3 = PWM_Servo(pi, 20, deviation=d[2], control_speed=True)
    servo4 = PWM_Servo(pi, 21, deviation=d[3], control_speed=True)
    servo5 = PWM_Servo(pi, 19, deviation=d[4], control_speed=True)
    servo6 = PWM_Servo(pi, 13, deviation=d[5], control_speed=True)
    Servos = (servo1, servo2, servo3, servo4, servo5, servo6)

def stopLeArm():
    print("停止机械臂")
    pi.write(12, 1)
    pi.write(16, 1)
    pi.write(20, 1)
    pi.write(21, 1)
    pi.write(19, 1)
    pi.write(13, 1)
    pi.stop()

if __name__ == '__main__':
    initLeArm([0, 0, 0, 0, 0, 0])







