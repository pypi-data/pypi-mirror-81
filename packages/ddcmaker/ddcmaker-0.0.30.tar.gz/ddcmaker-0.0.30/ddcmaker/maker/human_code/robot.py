import time
from typing import List, Tuple

import pigpio

from ddcmaker.basic.device.serial import SerialServoController
from ddcmaker.basic.device.robot import PWMServo, Servo
from ddcmaker.basic.abc.basic_maker import BasicMaker
from ddcmaker.maker.human_code.actions import dance
from ddcmaker.maker.human_code.actions import normal
from ddcmaker.maker.human_code.actions import head
from ddcmaker.maker.human_code.actions import ai
from ddcmaker.maker.human_code.part import Hand, Head, Leg


class Robot(BasicMaker):
    def __init__(self):
        super().__init__("机器人", sleep_time=1)
        self.pi = pigpio.pi()
        self.serial_controller = SerialServoController("/home/pi/human_code/ActionGroups/")
        self.serial = self.serial_controller.serial
        # 头部舵机编号
        self.head = Head(
            vertical=PWMServo(pi=self.pi, pin=5),
            horizontal=PWMServo(pi=self.pi, pin=6)
        )

        self.left_leg = Leg(
            sole=Servo(self.serial, servo_id=1, min_value=420, max_value=740, reverse=True),
            ankle=Servo(self.serial, servo_id=2, reverse=True),
            knee=Servo(self.serial, servo_id=3, init_value=303, min_value=63, max_value=943, reverse=True),
            vertical_hip=Servo(self.serial, servo_id=4),
            horizontal_hip=Servo(self.serial, servo_id=5),
        )

        self.left_hand = Hand(
            wrist=Servo(self.serial, servo_id=6, reverse=True),
            elbow=Servo(self.serial, servo_id=7, reverse=True),
            shoulder=Servo(self.serial, servo_id=8, init_value=725, min_value=85, max_value=985, reverse=True)
        )

        self.right_leg = Leg(
            sole=Servo(self.serial, servo_id=9, min_value=260, max_value=580),
            ankle=Servo(self.serial, servo_id=10),
            knee=Servo(self.serial, servo_id=11, init_value=697, min_value=57, max_value=937),
            vertical_hip=Servo(self.serial, servo_id=12, reverse=True),
            horizontal_hip=Servo(self.serial, servo_id=13, reverse=True),
        )

        self.right_hand = Hand(
            wrist=Servo(self.serial, servo_id=14),
            elbow=Servo(self.serial, servo_id=15),
            shoulder=Servo(self.serial, servo_id=16, init_value=275, min_value=15, max_value=915)
        )

    def finish(self):
        action_info = [
            self.head.horizontal_action, self.head.vertical_action,
            self.left_leg.sole_action, self.left_leg.ankle_action, self.left_leg.knee_action,
            self.left_leg.vertical_hip_action, self.left_leg.horizontal_hip_action,
            self.left_hand.wrist_action, self.left_hand.elbow_action, self.left_hand.shoulder_action,
            self.right_leg.sole_action, self.right_leg.ankle_action, self.right_leg.knee_action,
            self.right_leg.vertical_hip_action, self.right_leg.horizontal_hip_action,
            self.right_hand.wrist_action, self.right_hand.elbow_action, self.right_hand.shoulder_action,
        ]

        # 获取最大运行时间
        max_used_time = max(action_info, key=lambda info: info[-1])[-1]
        actions = [info[:-1] for info in action_info]
        self.set_servo(actions, max_used_time)

    def run_action_file(self, action_file_name, step=1, msg=None):
        """
        执行动作组文件
        :param action_file_name:
        :param step:
        :param msg:
        :return:
        """
        for i in range(step):
            self.serial_controller.run_action_file(action_file_name)
            time.sleep(self.sleep_time)
            if msg is not None:
                self.logger(msg)

    def set_servo(self, servo_infos: List[Tuple], used_time: int, msg=None):
        """
        执行动作
        :param servo_infos:舵机信息,[(servo_id,angle)]
        :param used_time:耗时，单位为ms
        :param msg: 提示信息
        :return:
        """

        for servo, angle in servo_infos:
            # 舵机执行命令
            if servo in self.head.servos:
                servo.run(angle)

            elif servo in self.left_leg.servos:
                self.serial_controller.set_servo(
                    servo.servo_id, servo.convert_to_value(angle), used_time)
            elif servo in self.left_hand.servos:
                self.serial_controller.set_servo(
                    servo.servo_id, servo.convert_to_value(angle), used_time)
            elif servo in self.right_leg.servos:
                self.serial_controller.set_servo(
                    servo.servo_id, servo.convert_to_value(angle), used_time)
            elif servo in self.right_hand.servos:
                self.serial_controller.set_servo(
                    servo.servo_id, servo.convert_to_value(angle), used_time)
            else:
                print("非法舵机号")
                return

        time.sleep(used_time / 1000)

        if msg is not None:
            self.logger(msg)

    def check(self):
        """
        通用组——机器人自检
        """
        normal.check(self)

    def init_body(self):
        """
        通用组——初始化机器人
        """
        normal.init_body(self)

    """基本动作"""

    def up(self):
        """
        通用组——机器人站立
        """
        normal.up(self)

    def down(self):
        """
        通用组——机器人蹲下
        """
        normal.down(self)

    def forward(self, step):
        """
        通用组——机器人前进
        """
        normal.forward(self, step)

    def backward(self, step):
        """
        通用组——机器人后退
        """
        normal.backward(self, step)

    def left(self, step):
        """
        通用组——机器人左转
        """
        normal.left(self, step)

    def right(self, step):
        """
        通用组——机器人右转
        """
        normal.right(self, step)

    def left_slide(self, step):
        """
        通用组——机器人左滑
        """
        normal.left_slide(self, step)

    def right_slide(self, step):
        """
        通用组——机器人右滑
        """
        normal.right_slide(self, step)

    """高级动作"""

    def wave(self, step):
        """
        通用组——机器人挥手┏(＾0＾)┛
        """
        normal.wave(self, step)

    def bow(self, step):
        """
        通用组——机器人鞠躬╰(￣▽￣)╭
        """
        normal.bow(self, step)

    def nod(self, step):
        """
        头部——机器人点头
        """
        head.nod(self, step)

    def shaking_head(self, step):
        """
        头部——机器人摇头
        """
        head.shaking_head(self, step)

    def init_head(self, step):
        """
        头部——机器人正视前方
        """
        head.init_head(self, step)

    def laugh(self):
        """
        通用组——机器人哈哈大笑o(*￣▽￣*)o
        """
        normal.laugh(self, step=1)

    def push_up(self):
        """
        通用组——机器人俯卧撑
        """
        normal.push_up(self, step=1)

    def abdominal_curl(self):
        """
        通用组——机器人仰卧起坐
        """
        normal.abdominal_curl(self, step=1)

    def supine_stand(self):
        """仰卧站立"""
        normal.supine_stand(self)

    def prone_stand(self):
        """俯卧站立"""
        normal.prone_stand(self)

    """武术动作"""

    def straight_boxing(self, step):
        """
        通用组——机器人直拳
        """
        normal.straight_boxing(self, step)

    def lower_hook_combo(self, step):
        """
        通用组——机器人下勾拳
        """
        normal.lower_hook_combo(self, step)

    def left_hook(self, step):
        """
        通用组——机器人左勾拳
        """
        normal.left_hook(self, step)

    def right_hook(self, step):
        """
        通用组——机器人右勾拳
        """
        normal.right_hook(self, step)

    def punching(self, step):
        """
        通用组——机器人弓步冲拳
        """
        normal.punching(self, step)

    def crouching(self, step):
        """
        通用组——机器人八字蹲拳
        """
        normal.crouching(self, step)

    def yongchun(self, step):
        """
        通用组——机器人咏春拳
        """
        normal.yongchun(self, step)

    def beat_chest(self, step):
        """
        通用组——机器人捶胸
        """
        normal.beat_chest(self, step)

    """体育动作"""

    def left_foot_shot(self):
        """
        通用组——机器人左脚射门
        """
        normal.left_foot_shot(self, step=1)

    def right_foot_shot(self):
        """
        通用组——机器人右脚射门
        """
        normal.right_foot_shot(self, step=1)

    def inverted_standing(self):
        """
        通用组——机器人前倒站立
        """
        normal.inverted_standing(self, step=1)

    def rear_stand_up(self):
        """
        通用组——机器人后倒站立
        """
        normal.rear_stand_up(self, step=1)

    """舞蹈组"""

    # def hip_hop(self): 已弃用
    #     """
    #     舞蹈组——街舞
    #     """
    #     dance.hiphop(self, step=1)

    def jiang_nan_style(self):
        """
        舞蹈组——江南style
        """
        dance.jiangnanstyle(self, step=1)

    def small_apple(self):
        """
        舞蹈组——小苹果
        """
        dance.smallapple(self, step=1)

    def la_song(self):

        """
        舞蹈组——lasong
        """
        dance.lasong(self, step=1)

    def feel_good(self):
        """
        舞蹈组——倍儿爽
        """
        dance.feelgood(self, step=1)

    def fantastic_baby(self):
        """
        舞蹈组——fantastic_baby
        """
        dance.fantastic_baby(self, step=1)

    def super_champion(self):
        """
        舞蹈组——super_champion
        """
        dance.super_champion(self, step=1)

    def youth_cultivation(self):
        """
        舞蹈组——青春修炼手册
        """
        dance.youth_cultivation(self, step=1)

    def love_starts(self):
        """
        舞蹈组——爱出发
        """
        dance.Love_starts(self, step=1)

    """AI模块"""

    def find_color(self):
        """
        AI组——颜色识别
        """
        ai.identifying(self)

    def find_hand(self):
        """
        AI组——手势识别
        """
        ai.find_hand(self)

    def line_follow(self):
        """
        AI组——自动寻迹
        """
        ai.line_follow(self)

    def tracking(self, color: str):
        """
        AI组——云台跟踪
        """
        ai.tracking(self, color)

    def __str__(self):
        return '\n'.join(
            [str(servo) for servo in [self.head, self.left_hand, self.right_hand, self.left_leg, self.right_leg]]
        )

    """项目组"""

    def move_with_ball(self):
        """机器人抱球移动"""

        normal.move_with_ball(self)
