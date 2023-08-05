import time


def head_to_left(robot):
    value = robot.head.horizontal.convert_to_value(-45)
    robot.head.horizontal.set_position(value, 100)
    time.sleep(0.2)


def head_to_right(robot):
    value = robot.head.horizontal.convert_to_value(45)
    robot.head.horizontal.set_position(value, 100)
    time.sleep(0.2)


def head_to_horizontal_middle(robot):
    value = robot.head.horizontal.convert_to_value(0)
    robot.head.horizontal.set_position(value, 100)
    time.sleep(0.2)


def head_to_up(robot):
    value = robot.head.vertical.convert_to_value(45)
    robot.head.vertical.set_position(value, 100)
    time.sleep(0.2)


def head_to_down(robot):
    value = robot.head.vertical.convert_to_value(-45)
    robot.head.vertical.set_position(value, 100)
    time.sleep(0.2)


def head_to_vertical_middle(robot):
    value = robot.head.vertical.convert_to_value(0)
    robot.head.vertical.set_position(value, 100)
    time.sleep(0.2)


def shaking_head(robot, step: int = 1):
    for _ in range(step):
        head_to_left(robot)
        head_to_right(robot)
        head_to_horizontal_middle(robot)
        robot.logger("摇头")
        time.sleep(0.2)


def nod(robot, step: int = 1):
    for _ in range(step):
        head_to_up(robot)
        head_to_down(robot)
        head_to_vertical_middle(robot)
        robot.logger("点头")
        time.sleep(0.2)


def init_head(robot, step: int = 1):
    for _ in range(step):
        head_to_vertical_middle(robot)
        head_to_horizontal_middle(robot)
