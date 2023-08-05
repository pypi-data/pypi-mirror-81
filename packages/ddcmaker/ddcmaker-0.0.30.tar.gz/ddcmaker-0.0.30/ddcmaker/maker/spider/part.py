from ddcmaker.decorator.safety import args_check
from ddcmaker.basic.device.robot import PWMServo, Servo


class Head(object):
    def __init__(self, horizontal: PWMServo, vertical: PWMServo):
        """
        :param horizontal: 控制头部左右移动的舵机
        :param vertical: 控制头部上下移动的舵机
        """
        self.horizontal = horizontal
        self.vertical = vertical
        self.servos = (horizontal, vertical)
        self.horizontal_action = (
            self.horizontal,
            0,
            self.horizontal.get_used_time(0)
        )
        self.vertical_action = (
            self.vertical,
            0,
            self.vertical.get_used_time(0)
        )

    @args_check([('angle', int, -90, 90)])
    def left(self, angle):
        """异步操作，直接返回需要的执行时间，需要调用者自行等待"""
        self.horizontal_action = (self.horizontal, angle, self.horizontal.get_used_time(angle))

    @args_check([('angle', int, -90, 90)])
    def right(self, angle):
        """异步操作，直接返回需要的执行时间，需要调用者自行等待"""
        self.horizontal_action = (self.horizontal, -angle, self.horizontal.get_used_time(angle))

    @args_check([('angle', int, -45, 45)])
    def up(self, angle):
        """异步操作，直接返回需要的执行时间，需要调用者自行等待"""
        self.vertical_action = (self.vertical, angle, self.vertical.get_used_time(angle))

    @args_check([('angle', int, -45, 45)])
    def down(self, angle):
        """异步操作，直接返回需要的执行时间，需要调用者自行等待"""
        self.vertical_action = (self.vertical, -angle, self.vertical.get_used_time(angle))

    def __str__(self):
        return '\n'.join([str(servo) for servo in self.servos])


class Leg:
    def __init__(self, basal_node: Servo, leg_section: Servo, tarsal: Servo):
        """
        控制蜘蛛的6条腿
        :param basal_node:蜘蛛腿基节，控制腿部水平移动
        :param leg_section:蜘蛛腿的腿节，控制腿部的上下移动
        :param tarsal:蜘蛛腿前掌，控制腿部的前掌部分的上下移动
        """
        self.basal_node = basal_node
        self.leg_section = leg_section
        self.tarsal = tarsal
        self.servos = (basal_node, leg_section, tarsal)
        self.basal_node_action = (
            self.basal_node,
            0,
            self.basal_node.get_used_time(0)
        )
        self.leg_section_action = (
            self.leg_section,
            10,
            self.leg_section.get_used_time(10)
        )
        self.tarsal_action = (
            self.tarsal,
            -20,
            self.tarsal.get_used_time(-20)
        )

    @args_check([('angle', int, -150, 150)])
    def horizontal_move(self, angle):
        """负责水平运动"""
        self.basal_node_action = (self.basal_node, angle, self.basal_node.get_used_time(angle))

    @args_check([('angle', int, -150, 150)])
    def curve(self, angle):
        """负责腿部弯曲"""
        self.leg_section_action = (self.leg_section, angle, self.leg_section.get_used_time(angle))

    @args_check([('angle', int, -150, 150)])
    def sole_curve(self, angle):
        """负责脚掌的弯曲"""
        self.tarsal_action = (self.tarsal, angle, self.tarsal.get_used_time(angle))

    def __str__(self):
        return '\n'.join([str(servo) for servo in self.servos])
