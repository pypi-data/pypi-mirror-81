# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
import cv2 as cv
import numpy as np
import math
import os
from .compute_angle import *


def two_distance(start, end):
    """
    计算两点的距离
    :param start: 开始点
    :param end: 结束点
    :return: 返回两点之间的距离
    """
    s_x = start[0]
    s_y = start[1]
    e_x = end[0]
    e_y = end[1]
    x = s_x - e_x
    y = s_y - e_y
    return math.sqrt((x**2)+(y**2))


def two_dot_angle(start, end):
    '''
    求两点之间的角度
            -+  |   ++
           _____|_____
                |
            --  |   +-
    :param start:
    :param end:
    :return:
    '''
    x = end[0] - start[0]
    y = end[1] - start[1]
    hypotenuse = math.sqrt(x**2 + y**2)
    radian = math.acos(x/hypotenuse)
    angle = 180/(math.pi / radian)
    if y < 0:
        angle = -angle
    elif (y == 0) and x < 0:
        angle = 180
    return angle


def computing_defects_angle(defects, contours, center, img):

    if defects is None and center is None and contours is None:
        return None
    acute_angle_num = 0
    # cv.circle(img, center[0], 8, [0, 255, 255], -1)
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(contours[s][0])
        end = tuple(contours[e][0])
        far = tuple(contours[f][0])
        # 求两点之间的距离
        a = two_distance(start, end)
        b = two_distance(start, far)
        c = two_distance(end, far)
        # print('a=', a)
        # print('b= ', b)
        # print('c= ', c)
        # 求出手指之间的角度
        angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180 / math.pi
        # 手指之间的角度一般不会大于100度
        # 小于90度
        # if far[1] < center[0][1]:
        if angle <= 90:  # 90:
            # print('角度=', angle)
            acute_angle_num += 1
            cv.circle(img, far, 5, [0, 0, 255], -1)
            # cv.line(img, start, end, [255, 255, 0], 2)
            # cv.line(img, start, far, [100, 0, 128], 2)
            # cv.line(img, end, far, [100, 0, 128], 2)
            # cv.circle(img, start, 5, [0, 255, 0], -1)
            # # cv.circle(img, end, 5, [255, 0, 0], -1)
        cv.line(img, start, end, [255, 255, 0], 2)
    return acute_angle_num


def rock_paper_scissors(num):
    """
    # 根据返回的锐角个数判断  石头， 剪刀 ，布
    :param num: 手指个数
    :return:
    """
    status = None
    if num is None:
        return None
    if num < 1:
        status = 0  # 石头
    elif num == 2:
        status = 1  # 剪刀
    elif num > 3:
        status = 2
    return status


def image_process(image):
    YCC = cv.cvtColor(image, cv.COLOR_BGR2YCR_CB)  # 将图片转化为YCrCb
    Y, Cr, Cb = cv.split(YCC)  # 分割YCrCb
    # Cr = cv2.inRange(Cr, 138, 175)
    Cr = cv.inRange(Cr, 132, 175)
    Cb = cv.inRange(Cb, 100, 140)
    Cb = cv.bitwise_and(Cb, Cr)
    # 开运算，去除噪点
    open_element = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
    opend = cv.morphologyEx(Cb, cv.MORPH_OPEN, open_element)
    # 腐蚀
    kernel = np.ones((3, 3), np.uint8)
    erosion = cv.erode(opend, kernel, iterations=1)
    # cv.imshow('1', erosion)
    return erosion


def get_max_coutour(cou, max_area):

    max_coutours = 0
    r_c = None
    if len(cou) < 1:
        return None
    else:
        for c in cou:
            # 计算面积
            temp_coutours = math.fabs(cv.contourArea(c))
            if temp_coutours > max_coutours:
                max_coutours = temp_coutours
                cc = c
        # 判断所有轮廓中最大的面积
        # print(max_coutours)
        if max_coutours > max_area:
            r_c = cc
        return r_c


def find_contours(binary, max_area):

    # img, contours, hierarchy = cv.findContours(skin1, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    # 找出所有轮廓
    _, contours, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    # 返回最大轮廓
    return get_max_coutour(contours, max_area)


def get_acute_angle(contours, img, center):
    """
    获取手指间的锐角角度
    :param contours:
    :return:
    """
    hull = cv.convexHull(contours, returnPoints=False)
    # 找凸包缺陷点 。返回的数据， 【起点，终点， 最远的点， 到最远点的近似距离】
    defects = cv.convexityDefects(contours, hull)
    angle_list = []
    if defects is None:
        return None
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(contours[s][0])
        end = tuple(contours[e][0])
        far = tuple(contours[f][0])
        # 求两点之间的距离
        a = two_distance(start, end)
        b = two_distance(start, far)
        c = two_distance(end, far)
        # print('a=', a)
        # print('b= ', b)
        # print('c= ', c)
        # 求出手指之间的角度
        angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180 / math.pi
        if far[1] < center[1]:
            if angle <= 100:
                angle_list.append(int(angle))
                cv.circle(img, far, 2, [0, 0, 255], -1)
    return angle_list


def get_heart_palms(binary_image):
    """
    获取手掌掌心坐标, 外接圆半径
    :param binary_image: 图像的二值图像
    :return: 掌心坐标，和外接圆半径
    """
    dist_transform = cv.distanceTransform(binary_image, 1, 5)
    ret, sure_fg = cv.threshold(dist_transform, 0.8 * dist_transform.max(), 255, 0)
    # ret, sure_fg1 = cv2.threshold(dist_transform, 0.7*dist_transform.max(), 255, 1)
    sure_fg = np.uint8(sure_fg)
    element = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
    sure_fg = cv.morphologyEx(sure_fg, cv.MORPH_OPEN, element)  # 做开运算
    # sure_fg = cv.morphologyEx(sure_fg, cv.MORPH_CLOSE, element)  # 做开运算
    #cv.imshow("2", np.hstack([binary_image, sure_fg]))
    cnts = cv.findContours(sure_fg.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[-2]
    if len(cnts) > 0:
        cy = 0
        for i in cnts:
            ((x, y), radius) = cv.minEnclosingCircle(i)
            if y >= cy:
                cy = int(y)
                cx = int(x)
                maxdis = int(radius)
        return (cx, cy), maxdis
    else:
        return None


def get_defects_far(defects, contours, img):
    '''
    获取凸包中最远的点
    '''
    if defects is None and contours is None:
        return None
    far_list = []
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(contours[s][0])
        end = tuple(contours[e][0])
        far = tuple(contours[f][0])
        # 求两点之间的距离
        a = two_distance(start, end)
        b = two_distance(start, far)
        c = two_distance(end, far)
        # print('a=', a)
        # print('b= ', b)
        # print('c= ', c)
        # 求出手指之间的角度
        angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 180 / math.pi
        # 手指之间的角度一般不会大于100度
        # 小于90度
        if angle <= 75:  # 90:
            # cv.circle(img, far, 10, [0, 0, 255], 1)
            far_list.append(far)
    return far_list


def get_hand_number(binary_image, rgb_image):
    '''
    返回手指的个数
    :param binary_image:
    :param rgb_image:
    :return:
    '''
    # # 2、找出手指尖的位置
    # # 查找轮廓，返回最大轮廓
    contours = find_contours(binary_image, 1500)
    coord_list = []
    if contours is not None:
        # 周长  0.035 根据识别情况修改，识别越好，越小
        epsilon = 0.025 * cv.arcLength(contours, True)
        # 轮廓相似
        approx = cv.approxPolyDP(contours, epsilon, True)
        # print approx
        cv.polylines(rgb_image, [approx], True, (0, 255, 0), 1)
        if approx.shape[0] >= 3:  # 有三个点以上
            approx_list = []
            for j in range(approx.shape[0]):
                approx_list.append(approx[j][0])
            approx_list.append(approx[0][0])    # 在末尾添加第一个点
            approx_list.append(approx[1][0])    # 在末尾添加第二个点
            for i in range(1, len(approx_list) - 1):
                p1 = Point(approx_list[i - 1][0], approx_list[i - 1][1])    # 声明一个点
                p2 = Point(approx_list[i][0], approx_list[i][1])
                p3 = Point(approx_list[i + 1][0], approx_list[i + 1][1])
                line1 = Line(p1, p2)    # 声明一条直线
                line2 = Line(p2, p3)
                angle = GetCrossAngle(line1, line2)     # 获取两条直线的夹角
                angle = 180 - angle     #
                # print angle
                if angle < 42:  # 求出两线相交的角度，并小于37度的
                    # cv.circle(rgb_image, tuple(approx_list[i]), 5, [255, 0, 0], -1)
                    coord_list.append(tuple(approx_list[i]))
        ##############################################################################
        # 去除手指间的点
        # 1、获取凸包缺陷点，最远点点
        # cv.drawContours(rgb_image, contours, -1, (255, 0, 0), 1)
        hull = cv.convexHull(contours, returnPoints=False)
        # 找凸包缺陷点 。返回的数据， 【起点，终点， 最远的点， 到最远点的近似距离】
        defects = cv.convexityDefects(contours, hull)
        # 返回手指间的点
        hand_coord = get_defects_far(defects, contours, rgb_image)
        # print 'h', hand_coord
        # print 'c', coord_list
        # 2、从coord_list 去除最远点
        new_hand_list = []  # 获取最终的手指间坐标
        alike_flag = False
        if len(coord_list) > 0:
            for l in range(len(coord_list)):
                for k in range(len(hand_coord)):
                    if (-10 <= coord_list[l][0] - hand_coord[k][0] <= 10 and
                            -10 <= coord_list[l][1] - hand_coord[k][1] <= 10):    # 最比较X,Y轴, 相近的去除
                        alike_flag = True
                        break   #
                if alike_flag is False:
                    new_hand_list.append(coord_list[l])
                alike_flag = False

            # print new_hand_list
            # 获取指尖的坐标列表并显示
            for i in new_hand_list:
                cv.circle(rgb_image, tuple(i), 5, [0, 0, 100], -1)
        if new_hand_list is []:
            return 0
        else:
            return len(new_hand_list)
    else:
        return None


def file_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.bmp':
                L.append(os.path.join(root, file))
    return L


def template_matching(binary_image, rgb_image, temp_path):
    # 1、找出手掌掌心
    p = get_heart_palms(binary_image)
    if p is not None:
        # print(p)
        cv.circle(rgb_image, p[0], p[1], (0, 0, 255), 2)
        cv.circle(rgb_image, p[0], 3, (255, 0, 255), -1)
        # # 查找轮廓，返回最大轮廓
        contours = find_contours(binary_image, 1500)
        if contours is not None:
            # 绘制轮廓
            cv.drawContours(rgb_image, contours, -1, (255, 0, 0), 1)
            # 绘制凸包
            draw_hull = cv.convexHull(contours)
            cv.polylines(rgb_image, [draw_hull], True, (0, 255, 0), 1)
            # 获取指尖的坐标列表
            f = get_hand_number(binary_image, rgb_image)
            if f == 0:  # 0个手指
                path = temp_path + '/0'
            elif f == 1:  # 1个手指
                path = temp_path + '/1'
            elif f == 2:  # 2个手指.
                path = temp_path + '/2'
            elif f == 3:  # 3个手指
                path = temp_path + '/3'
            elif f == 4:  # 4个手指
                path = temp_path + '/4'
            elif f == 5:
                path = temp_path + '/5'
            else:
                return False
            # 获取文件夹下的所有文件路径
            list_name = file_name(path)
            # print(list_name)
            # 两个图片的相似度， 越小越相似
            list_sim = []
            for l in list_name:
                # print l
                # 读取模板图片
                temp_img = cv.imread(l)
                # 转换成二值图像
                t_binary = image_process(temp_img)
                # 找最大轮廓
                cnts = find_contours(t_binary, 1500)
                # 匹配
                d = cv.matchShapes(contours, cnts, 1, 0.0)
                # 保存相似度值
                list_sim.append(d)
            # 获取最小的相似度的索引号
            min_sim = list_sim.index(min(list_sim))
            # print(list_sim)
            # print(min_sim)
            # print(list_name[min_sim])
            # 获取样张图片的文件名
            hand_number = list_name[min_sim][list_name[min_sim].rfind('/') + 1:list_name[min_sim].rfind(".")]
            #print(hand_number)
            return hand_number
    else:
        return None


if __name__ == '__main__':
    pass


