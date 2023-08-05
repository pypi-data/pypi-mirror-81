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


class Hand(object):
    def __init__(self, wrist: Servo, elbow: Servo, shoulder: Servo):
        """
        :param wrist: 控制手掌上下的舵机
        :param elbow: 控制手臂上下的舵机
        :param shoulder:控制手臂前后的舵机
        """
        self.wrist = wrist
        self.elbow = elbow
        self.shoulder = shoulder
        self.servos = (wrist, elbow, shoulder)
        self.wrist_action = (
            self.wrist,
            -32,
            self.wrist.get_used_time(-32)
        )

        self.elbow_action = (
            self.elbow,
            -63,
            self.elbow.get_used_time(-63)
        )

        self.shoulder_action = (
            self.shoulder,
            0,
            self.shoulder.get_used_time(0)
        )

    @args_check([('angle', int, -90, 90)])
    def up(self, angle):
        """抬手"""
        self.elbow_action = (self.elbow, angle, self.elbow.get_used_time(angle))

    @args_check([('angle', int, -65, 160)])
    def forward(self, angle):
        """向前抬手"""
        self.shoulder_action = (self.shoulder, angle, self.shoulder.get_used_time(angle))

    @args_check([('angle', int, -90, 90)])
    def curve(self, angle):
        """弯曲"""
        self.wrist_action = (self.wrist, angle, self.wrist.get_used_time(angle))

    def __str__(self):
        return '\n'.join([str(servo) for servo in self.servos])


class Leg(object):
    def __init__(self, sole: Servo, ankle: Servo, knee: Servo,
                 vertical_hip: Servo, horizontal_hip: Servo):
        """
        :param sole: 控制脚掌左右倾斜的舵机
        :param ankle: 控制脚掌前后倾斜的舵机
        :param knee:控制膝盖的舵机
        :param vertical_hip:控制腿前后移动的舵机
        :param horizontal_hip:控制腿左右移动的舵机
        """
        self.sole = sole
        self.ankle = ankle
        self.knee = knee
        self.vertical_hip = vertical_hip
        self.horizontal_hip = horizontal_hip
        self.servos = (sole, ankle, knee, vertical_hip, horizontal_hip)
        self.sole_action = (
            self.sole,
            0,
            self.sole.get_used_time(0)
        )
        self.ankle_action = (
            self.ankle,
            33,
            self.ankle.get_used_time(33)
        )
        self.knee_action = (
            self.knee,
            -49,
            self.knee.get_used_time(-49)
        )
        self.vertical_hip_action = (
            self.vertical_hip,
            23,
            self.vertical_hip.get_used_time(23)
        )
        self.horizontal_hip_action = (
            self.horizontal_hip,
            3,
            self.horizontal_hip.get_used_time(3)
        )

    @args_check([('angle', int, -90, 90)])
    def up(self, angle):
        """向两侧抬腿"""
        self.horizontal_hip_action = (self.horizontal_hip, angle, self.horizontal_hip.get_used_time(angle))

    @args_check([('angle', int, -90, 90)])
    def forward(self, angle):
        """向前抬腿"""
        self.vertical_hip_action = (self.vertical_hip, angle, self.vertical_hip.get_used_time(angle))

    @args_check([('angle', int, -150, 90)])
    def curve(self, angle):
        """弯曲"""
        self.knee_action = (self.knee, angle, self.knee.get_used_time(angle))

    @args_check([('angle', int, -90, 90)])
    def lean(self, angle):
        """负责前后倾斜"""
        self.ankle_action = (self.ankle, angle, self.ankle.get_used_time(angle))

    @args_check([('angle', int, -90, 90)])
    def tilt(self, angle):
        """负责左右倾斜"""
        self.sole_action = (self.sole, angle, self.sole.get_used_time(angle))

    def __str__(self):
        return '\n'.join([str(servo) for servo in self.servos])
