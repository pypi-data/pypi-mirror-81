#!/usr/bin/python3
# encoding: utf-8
"""
舵机
"""
from abc import abstractmethod
import time
import threading

from ddcmaker.basic.constant import lobot_servo_constant

USED_TIME_MIN = 20
USED_TIME_MAX = 30000
DEVIATION_MIN = -300
DEVIATION_MAX = 300


class ABCServo(object):
    @abstractmethod
    def convert_to_value(self, angle: int) -> int:
        """
        将角度转换为舵机运行值
        :param angle: 角度
        """

    @abstractmethod
    def run(self, angle) -> float:
        """
        运行到指定角度
        :param angle: 角度
        :return :预期耗时
        """


class Servo(ABCServo):
    def __init__(self, serial, servo_id: int, min_value: int = 140,
                 max_value: int = 860, init_value: int = 500,
                 proportion: int = 4, rate=20, reverse=False):
        """
        初始化pwm总线舵机
        :param servo_id:引脚号
        :param min_value:舵机最小范围
        :param max_value:舵机最大范围
        :param init_value:初始值
        :param proportion:角度转舵机值的比例
        :param reverse:舵机是否是反转
        :param rate:每度转动的耗时，单位为毫秒，默认20毫秒1°
        """
        self._min_value = min_value
        self._max_value = max_value
        self.init_value = init_value
        self._proportion = proportion
        self.servo_id = servo_id
        self.serial = serial
        self._position = self.serial.get_position(self.servo_id)
        self.rate = rate

        if reverse is True:
            self._max_angle = (init_value - min_value) / proportion
            self._min_angle = (init_value - max_value) / proportion
        else:
            self._max_angle = (max_value - init_value) / proportion
            self._min_angle = (min_value - init_value) / proportion

        self._reverse = reverse

    @property
    def position(self):
        self._position = self.serial.get_position(self.servo_id)
        return self._position

    @position.setter
    def position(self, value):
        self._position += value

    def convert_to_value(self, angle: int):
        """
        将角度转换为舵机运行值
        """
        if angle > self._max_angle or angle < self._min_angle:
            print(f"angle参数，非法{angle},合法值{self._min_angle}-{self._max_angle}")
            return
        if self._reverse:
            value = self.init_value - angle * self._proportion
        else:
            value = self.init_value + angle * self._proportion
        value = int(min(max(self._min_value, value), self._max_value))
        return int(min(max(self._min_value, value), self._max_value))

    def get_used_time(self, angle):
        """获得当前位置运行到目标位置的耗时，单位毫秒"""
        if angle > self._max_angle or angle < self._min_angle:
            print(f"angle参数，非法{angle},合法值{self._min_angle}-{self._max_angle}")
            return

        value = self.convert_to_value(angle)

        return int(abs(value - self.position) / self._proportion) * self.rate

    def run(self, angle):
        """
        运行到指定角度
        """
        used_time = abs(angle * self.rate)
        value = self.convert_to_value(angle)
        cmd = lobot_servo_constant.LOBOT_SERVO_MOVE_TIME_WRITE
        used_time += int(abs(value - self.position) / self._proportion) * self.rate
        self.serial.write(self.servo_id, cmd, value, used_time)
        return used_time

    def __str__(self):
        return f"{self.servo_id}:{self.position}"


class PWMServo(ABCServo):
    """控制pwm总线舵机"""

    def __init__(self, pi, pin: int, min_value: int = 500,
                 max_value: int = 2500, init_value: int = 1500,
                 proportion: int = 10, deviation: int = 0, rate: int = 20):
        """
        初始化pwm总线舵机
        :param pin:引脚号
        :param min_value:舵机最小范围
        :param max_value:舵机最大范围
        :param proportion:角度转舵机值的比例
        :param deviation:偏差值
        :param rate:每度转动的耗时，单位为毫秒，默认20毫秒1°
        """
        self.pi = pi
        self.pin = pin
        self.init_value = init_value
        self._target_position = init_value  # 舵机预期移动到的位置
        self._position = self.pi.get_servo_pulsewidth(self.pin)  # 舵机当前位置
        self._min = min_value
        self._min_angle = int((init_value - min_value) / proportion)
        self._max = max_value
        self._max_angle = int((max_value - init_value) / proportion)
        self._proportion = proportion
        self._deviation = deviation
        self.rate = rate
        self._used_time = 0

    @property
    def position(self):
        self._position = self.pi.get_servo_pulsewidth(self.pin)  # 舵机当前位置
        return self._position

    @position.setter
    def position(self, value):
        self._position += value

    def convert_to_value(self, angle: int) -> int:
        """将角度转换为舵机运行值"""
        return int(min(max(self._min, self.init_value + self._proportion * angle), self._max))

    def get_used_time(self, angle):
        """获得当前位置运行到目标位置的耗时，单位毫秒"""
        value = self.convert_to_value(angle)
        return int(abs(value - self.position) / self._proportion) * 2 * self.rate

    def run(self, angle) -> float:
        value = self.convert_to_value(angle)
        used_time = abs(angle * self.rate)
        used_time += int(abs(value - self.position) / self._proportion) * self.rate
        self.set_position(value, used_time)
        return used_time

    def set_position(self, pos, used_time=0):
        """
        转动舵机
        :param pos:目标舵机位置
        :param used_time:耗时
        :return:
        """
        if pos < self._min or pos > self._max:
            print(pos)
            return

        self._used_time = min(max(USED_TIME_MIN, used_time), USED_TIME_MAX)
        self._target_position = pos
        thread = threading.Thread(target=self.update_position)
        thread.start()

    @property
    def deviation(self):
        """
        获取当前偏差
        :return:
        """
        return self._deviation

    @deviation.setter
    def deviation(self, deviation: int = 0):
        """
        设置偏差，当deviation大于DEVIATION_MAX或小于DEVIATION_MIN时，设置失败
        :param deviation:偏差
        :raise:
        :return:
        """
        if deviation > DEVIATION_MAX or deviation < DEVIATION_MIN:
            print(f"deviation的允许范围为{DEVIATION_MIN}-{DEVIATION_MAX}")
            return
        self._deviation = deviation

    def update_position(self):
        """
        用于动态执行servo的动作
        :param self:pwm总线舵机
        :return:
        """
        if self._target_position == self.position:
            return
        # 舵机转动次数
        times = int(self._used_time / self.rate)

        if times == 1:
            position_inc = self._target_position - self.position
        else:
            # 计算每次转动的幅度
            position_inc = int(
                (self._target_position - self.position) / (times - 1))

        steps = [position_inc for _ in range(times - 1)]
        steps.append(
            self._target_position - self.position - position_inc * (times - 1))

        # 执行更新
        for step in steps:
            try:
                self.pi.set_servo_pulsewidth(self.pin, int(
                    self.position + step + self.deviation))
            except Exception as err:
                print(err)
            self.position += step
            time.sleep(self.rate / 1000)


class HumanHandPWMServo:
    """手掌控制pwm总线舵机"""

    def __init__(self, pi, pin, freq=50, min_width=500, max_width=2500, deviation=0, control_speed=False):
        """
        :param pin: 引脚号
        :param min_width: 最小值
        :param max_width: 最大值
        :param deviation: 偏差值
        :param control_speed: 是否控制速度
        """
        self.pi = pi
        self.SPin = pin
        self.Position = 1500
        self.positionSet = self.Position
        self.Freq = freq
        self.Min = min_width
        self.Max = max_width
        self.Deviation = deviation
        self.stepTime = 20
        self.positionInc = 0.0
        self.Time = 0
        self.Time_t = 0
        self.incTimes = 0
        self.speedControl = control_speed
        self.positionSet_t = 0
        self.posChanged = False
        self.servoRunning = False

        if control_speed is True:
            t = threading.Thread(target=HumanHandPWMServo.update_position, args=(self,))
            t.setDaemon(True)
            t.start()

    def set_position(self, pos, time=0):
        if pos < self.Min or pos > self.Max:
            print(pos)
            return
        if time == 0:
            self.Position = pos
            self.positionSet = self.Position
            self.pi.set_PWM_dutycycle(self.SPin, self.Position + self.Deviation)
        else:
            if time < 20:
                self.Time_t = 20
            elif time > 30000:
                self.Time_t = 30000
            else:
                self.Time_t = time
            self.positionSet_t = pos
            self.posChanged = True

    def get_position(self):
        return self.Position

    def update_position(self):
        while True:
            if self.posChanged is True:
                self.Time = self.Time_t
                self.positionSet = self.positionSet_t
                self.posChanged = False
                self.incTimes = int(self.Time / self.stepTime)
                self.positionInc = self.Position - self.positionSet
                self.positionInc = int(self.positionInc / self.incTimes)
                self.servoRunning = True

            if self.servoRunning is True:
                self.incTimes -= 1
                if self.incTimes == 0:
                    self.Position = self.positionSet
                    self.servoRunning = False
                else:
                    self.Position = self.positionSet + int(self.positionInc * self.incTimes)
                try:
                    self.pi.set_servo_pulsewidth(self.SPin, self.Position + self.Deviation)
                except BaseException as e:
                    pass
            time.sleep(0.02)

    def set_deviation(self, newD=0):
        if newD > 300 or newD < -300:
            return
        self.Deviation = newD
