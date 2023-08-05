from ddcmaker.basic.device.robot import PWMServo
from ddcmaker.decorator.safety import args_check


class Palm:
    """控制手掌的手指(前后运动)"""

    def __init__(self, finger: PWMServo):
        """
        :param finger: 负责控制手指弯曲的舵机
        """
        self.finger = finger
        self.servos = (self.finger,)
        self.finger_action = (
            self.finger,
            0,
            self.finger.get_used_time(0)
        )

    @args_check([('angle', int, -180, 180)])
    def curve(self, angle):
        """负责手指向掌心的弯曲"""
        self.finger_action = (self.finger, angle, self.finger.get_used_time(angle))

    def __str__(self):
        return '\n'.join([str(servo) for servo in self.servos])


class   Wrist:
    """控制手腕(左右运动)"""

    def __init__(self, finesse: PWMServo):
        """
        :param finesse：负责手腕左右移动的舵机
        """
        self.finesse = finesse
        self.servos = (self.finesse,)
        self.finesse_action = (
            self.finesse,
            0,
            self.finesse.get_used_time(0)

        )

    @args_check([('angle', int, -180, 180)])
    def horizontal(self, angle):
        """负责手腕水平向左右运动"""
        self.finesse_action = (self.finesse, angle, self.finesse.get_used_time(angle))

    def __str__(self):
        return '\n'.join([str(servo) for servo in self.servos])
