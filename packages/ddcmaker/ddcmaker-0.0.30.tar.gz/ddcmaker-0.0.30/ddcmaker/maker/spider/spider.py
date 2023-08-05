import time
from typing import List, Tuple

import pigpio

from ddcmaker.basic.device.robot import PWMServo, Servo
from ddcmaker.maker.spider.actions import ai, normal

from ddcmaker.basic.device.serial import SerialServoController
from ddcmaker.basic.abc.basic_maker import BasicMaker
from ddcmaker.maker.spider.part import Head, Leg


class Spider(BasicMaker):
    def __init__(self):
        super().__init__("蜘蛛", sleep_time=1)
        self.serial_controller = SerialServoController("/home/pi/hexapod/ActionGroups/")
        self.serial = self.serial_controller.serial
        self.pi = pigpio.pi()
        # 头部舵机
        # self.head = Head(
        #     vertical=PWMServo(pi=self.pi, pin=5),
        #     horizontal=PWMServo(pi=self.pi, pin=6)
        # )
        self.left_fore_leg = Leg(
            basal_node=Servo(self.serial, servo_id=7, min_value=100, max_value=900, init_value=500, reverse=True),
            leg_section=Servo(self.serial, servo_id=8, min_value=100, max_value=900, init_value=320, reverse=True),
            tarsal=Servo(self.serial, servo_id=9, min_value=100, max_value=1000, init_value=170, reverse=True)
        )
        self.left_middle_leg = Leg(
            basal_node=Servo(self.serial, servo_id=4, min_value=100, max_value=900, init_value=500, reverse=True),
            leg_section=Servo(self.serial, servo_id=5, min_value=100, max_value=900, init_value=320, reverse=True),
            tarsal=Servo(self.serial, servo_id=6, min_value=100, max_value=1000, init_value=170, reverse=True)
        )
        self.left_hind_leg = Leg(
            basal_node=Servo(self.serial, servo_id=1, min_value=300, max_value=900, init_value=500, reverse=True),
            leg_section=Servo(self.serial, servo_id=2, min_value=100, max_value=900, init_value=320, reverse=True),
            tarsal=Servo(self.serial, servo_id=3, min_value=100, max_value=1000, init_value=170, reverse=True)
        )
        self.right_fore_leg = Leg(
            basal_node=Servo(self.serial, servo_id=16, min_value=100, max_value=900, init_value=500),
            leg_section=Servo(self.serial, servo_id=17, min_value=100, max_value=900, init_value=670),
            tarsal=Servo(self.serial, servo_id=18, min_value=100, max_value=1000, init_value=800)
        )
        self.right_middle_leg = Leg(
            basal_node=Servo(self.serial, servo_id=13, min_value=100, max_value=900, init_value=500),
            leg_section=Servo(self.serial, servo_id=14, min_value=100, max_value=900, init_value=670),
            tarsal=Servo(self.serial, servo_id=15, min_value=100, max_value=1000, init_value=800)
        )
        self.right_hind_leg = Leg(
            basal_node=Servo(self.serial, servo_id=10, min_value=100, max_value=900, init_value=500),
            leg_section=Servo(self.serial, servo_id=11, min_value=100, max_value=900, init_value=670),
            tarsal=Servo(self.serial, servo_id=12, min_value=100, max_value=1000, init_value=800)
        )

    def finish(self):
        action_info = [
            self.left_fore_leg.leg_section_action, self.left_fore_leg.tarsal_action,
            self.left_fore_leg.basal_node_action, self.right_fore_leg.basal_node_action,
            self.right_fore_leg.leg_section_action, self.right_fore_leg.tarsal_action,
            self.left_middle_leg.leg_section_action, self.left_middle_leg.tarsal_action,
            self.left_middle_leg.basal_node_action, self.right_middle_leg.basal_node_action,
            self.right_middle_leg.leg_section_action, self.right_middle_leg.tarsal_action,
            self.left_hind_leg.basal_node_action, self.left_hind_leg.leg_section_action,
            self.left_hind_leg.tarsal_action, self.right_hind_leg.basal_node_action,
            self.right_hind_leg.leg_section_action, self.right_hind_leg.tarsal_action
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
            # if servo in self.head.servos:
            #     servo.run(angle)

            if servo in self.left_fore_leg.servos:
                self.serial_controller.set_servo(
                    servo.servo_id, servo.convert_to_value(angle), used_time)
            elif servo in self.right_fore_leg.servos:
                self.serial_controller.set_servo(
                    servo.servo_id, servo.convert_to_value(angle), used_time)
            elif servo in self.left_middle_leg.servos:
                self.serial_controller.set_servo(
                    servo.servo_id, servo.convert_to_value(angle), used_time)
            elif servo in self.right_middle_leg.servos:
                self.serial_controller.set_servo(
                    servo.servo_id, servo.convert_to_value(angle), used_time)
            elif servo in self.left_hind_leg.servos:
                self.serial_controller.set_servo(
                    servo.servo_id, servo.convert_to_value(angle), used_time)
            elif servo in self.right_hind_leg.servos:
                self.serial_controller.set_servo(
                    servo.servo_id, servo.convert_to_value(angle), used_time)
            else:
                print("非法舵机号")
                return

        time.sleep(used_time / 1000)

        if msg is not None:
            self.logger(msg)

    """ai动作"""

    def find_color(self):
        ai.identifying(self)

    def tracking(self, color: str):
        ai.tracking(self, color)

    def follow(self):
        ai.follow(self)

    def linefollow(self):
        ai.line_follow(self)

    def balance(self):
        ai.balance(self)

    def sonar(self):
        ai.sonar(self)

    """基本动作"""

    def init_body(self):
        normal.init_body(self)

    def creeping(self):
        normal.creeping(self)

    def creeping_forward(self):
        normal.creeping_forward(self)

    def creeping_backward(self):
        normal.creeping_backward(self)

    def creeping_left(self):
        normal.creeping_left(self)

    def creeping_right(self):
        normal.creeping_right(self)

    def stand(self):
        normal.stand(self)

    def forward(self):
        normal.forward(self)

    def backward(self):
        normal.backward(self)

    def left(self):
        normal.left(self)

    def right(self):
        normal.right(self)

    def towering(self):
        normal.towering(self)

    def towering_forward(self):
        normal.towering_forward(self)

    def towering_backward(self):
        normal.towering_backward(self)

    def towering_left(self):
        normal.towering_left(self)

    def towering_right(self):
        normal.towering_right(self)

    def forward_flutter(self):
        normal.forward_flutter(self)

    def backward_flutter(self):
        normal.backward_flutter(self)

    def left_shift(self):
        normal.left_shift(self)

    def right_shift(self):
        normal.right_shift(self)

    def twisting(self):
        normal.twisting(self)

    def fighting(self):
        normal.fighting(self)

    def break_forward(self):
        """
        碎步前进
        """
        normal.break_forward(self, step=1)

    def minor_steering(self):
        """
        小转向(右)
        """
        normal.minor_steering(self, step=1)
