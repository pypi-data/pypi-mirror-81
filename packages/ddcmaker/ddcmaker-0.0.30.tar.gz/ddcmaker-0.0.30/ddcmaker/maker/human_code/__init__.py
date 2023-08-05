from ddcmaker.maker.human_code.actions import normal
from ddcmaker.maker.human_code.actions import head
from ddcmaker.maker.human_code.robot import Robot
from ddcmaker.maker.human_code.actions.ai import AI_FEATURES


def init():
    normal_robot = Robot()
    normal_robot.run_action(normal.init_body)
    normal_robot.run_action(head.init_head)
