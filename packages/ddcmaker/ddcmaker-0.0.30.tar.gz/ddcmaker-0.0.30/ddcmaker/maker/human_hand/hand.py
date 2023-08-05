import pathlib
import sqlite3 as sql

import pigpio
from ddcmaker.basic.abc.basic_maker import BasicMaker
from ddcmaker.basic.device.robot import PWMServo, HumanHandPWMServo
from ddcmaker.maker.human_hand.actions.normal import *
from ddcmaker.maker.human_hand.part import Palm, Wrist


class Hand(BasicMaker):
    def __init__(self):
        super().__init__("手掌", sleep_time=1)
        self.pi = pigpio.pi()

        self.thumb = Palm(
            finger=PWMServo(self.pi, pin=12, init_value=1500, min_value=1000, max_value=2100)
        )
        self.index_finger = Palm(
            finger=PWMServo(self.pi, pin=16, init_value=1500, min_value=1000, max_value=2100)
        )
        self.middle_finger = Palm(
            finger=PWMServo(self.pi, pin=20, init_value=1500, min_value=1000, max_value=2100)
        )
        self.ring_finger = Palm(
            finger=PWMServo(self.pi, pin=21, init_value=1500, min_value=1000, max_value=2100)
        )
        self.little_finger = Palm(
            finger=PWMServo(self.pi, pin=19, init_value=1500, min_value=1000, max_value=2100)
        )
        self.wrist = Wrist(
            finesse=PWMServo(self.pi, pin=13, init_value=1500, min_value=500, max_value=2500)
        )
        self.servo1 = HumanHandPWMServo(self.pi, 12, deviation=0, control_speed=True)
        self.servo2 = HumanHandPWMServo(self.pi, 16, deviation=0, control_speed=True)
        self.servo3 = HumanHandPWMServo(self.pi, 20, deviation=0, control_speed=True)
        self.servo4 = HumanHandPWMServo(self.pi, 21, deviation=0, control_speed=True)
        self.servo5 = HumanHandPWMServo(self.pi, 19, deviation=0, control_speed=True)
        self.servo6 = HumanHandPWMServo(self.pi, 13, deviation=0, control_speed=True)
        self.servos = (self.servo1, self.servo2, self.servo3, self.servo4, self.servo5, self.servo6)
        self.file_path = pathlib.Path("/home/pi/Hand_Arm_Pi/ActionGroups/").absolute()
        self.action_status = False
        self.stop_action = False

    def run_action_file(self, action_file_name, step=1, msg=None):
        """
        执行动作组
        :param action_file_name:动作名
        :param step: 运行次数
        :param msg: 运行信息
        :return:
        """

        if action_file_name is None:
            return
        if self.action_status:
            print("上一个动作还未完成")
            return
        d6a_file = self.file_path.joinpath(f'{action_file_name}.d6a')
        if d6a_file.exists():
            for _ in range(step):
                if self.action_status is False:
                    self.action_status = True
                connect = sql.connect(d6a_file.as_posix())
                cursor = connect.cursor()
                cursor.execute("select * from ActionGroup")
                while True:
                    action = cursor.fetchone()
                    if self.stop_action:
                        print('stop')
                        self.stop_action = False
                        break

                    if action is None:
                        break

                    for i in range(0, len(action) - 2, 1):
                        self.servos[i].set_position(action[2 + i], action[1])
                    time.sleep(float(action[1]) / 1000.0)
                self.action_status = False
                cursor.close()
                connect.close()
        else:
            print("未能找到动作组文件")

    def set_servo(self, servo_infos, used_time: int):
        """
        执行动作
        :param servo_infos:舵机信息,[(servo_id,angle)]
        :param used_time:耗时，单位为s
        :return:
        """
        pass

    # 测试动作
    def test(self):
        pass

    """AI组"""

    def rock_scissors_paper_game(self):
        """石头剪刀布游戏"""
        self.logger("石头剪刀布游戏")
        from ddcmaker.AI.hand_arm.rock_scissors_paper_game import rock_scissors_paper
        rock_scissors_paper()

    def get_ball_color(self):
        """获取球体颜色"""
        self.logger("获取球体颜色")
        from ddcmaker.AI.hand_arm.ballcolor import get_ball_color
        get_ball_color()

    def get_ball_track(self):
        """球体视觉追踪"""
        self.logger("球体视觉追踪")
        from ddcmaker.AI.hand_arm.balltrack import get_ball_track
        get_ball_track()

    def cv_hand(self):
        """手掌识别"""
        self.logger("手掌识别")
        from ddcmaker.AI.hand_arm.cvhand import get_cv_hand
        get_cv_hand()

    def face_detection(self):
        """人脸识别"""
        self.logger("人脸识别")
        from ddcmaker.AI.hand_arm.face_detection import get_face_detection
        get_face_detection()

    def face_track(self):
        """人脸追踪"""
        self.logger("人脸追踪")
        from ddcmaker.AI.hand_arm.face_track import get_face_track
        get_face_track()

    def finger_num(self):
        """手指识别"""
        self.logger("手指识别")
        from ddcmaker.AI.hand_arm.finger_num import get_finger_num
        get_finger_num()

    def shape_recognition(self):
        """形状识别"""
        self.logger("形状识别")
        from ddcmaker.AI.hand_arm.shape_recognition import get_shape_recognition
        get_shape_recognition()

    def qc_code(self):
        """qc_code"""
        self.logger("qc_code")
        from ddcmaker.AI.hand_arm.qc_code import get_qc_code
        get_qc_code()
