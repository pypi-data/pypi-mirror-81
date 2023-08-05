import time


def init_body(robot, step: int = 1):
    robot.run_action_file("0", step=step)


def up(robot, step: int = 1):
    robot.run_action_file("0", step=step, msg="站立")


def down(robot, step: int = 1):
    robot.run_action_file("14", step=step, msg="蹲下")


def check(robot, step: int = 1):
    robot.run_action_file("188", step=step, msg="自检")


def forward(robot, step: int = 1):
    for _ in range(step):
        robot.run_action_file("1", step=1, msg="前进")
        time.sleep(0.5)


def backward(robot, step: int = 1):
    for _ in range(step):
        robot.run_action_file("2", step=1, msg="后退")
        time.sleep(0.5)


def left(robot, step: int = 1):
    for _ in range(step):
        robot.run_action_file("3", step=1, msg="左转")
        time.sleep(0.5)


def right(robot, step: int = 1):
    for _ in range(step):
        robot.run_action_file("4", step=1, msg="右转")
        time.sleep(0.5)


def left_slide(robot, step: int = 1):
    for _ in range(step):
        robot.run_action_file("11", step=1, msg="左滑")
        time.sleep(0.5)


def right_slide(robot, step: int = 1):
    for _ in range(step):
        robot.run_action_file("12", step=1, msg="右滑")
        time.sleep(0.5)


def push_up(robot, step: int = 1):
    robot.run_action_file("7", step=step, msg="俯卧撑")


def abdominal_curl(robot, step: int = 1):
    robot.run_action_file("8", step=step, msg="仰卧起坐")


def wave(robot, step: int = 1):
    robot.run_action_file("9", step=step, msg="挥手┏(＾0＾)┛")


def bow(robot, step: int = 1):
    robot.run_action_file("10", step=step,
                          msg="鞠躬╰(￣▽￣)╭")


def spread_wings(robot, step: int = 1):
    robot.run_action_file("13", step=step, msg="大鹏展翅")


def laugh(robot, step: int = 1):
    robot.run_action_file("15", step=step,
                          msg="哈哈大笑o(*￣▽￣*)o")


def straight_boxing(robot, step: int = 1):
    robot.run_action_file("30", step=step, msg="直拳")


def lower_hook_combo(robot, step: int = 1):
    robot.run_action_file("31", step=step, msg="下勾拳")


def left_hook(robot, step: int = 1):
    robot.run_action_file("32", step=step, msg="左勾拳")


def right_hook(robot, step: int = 1):
    robot.run_action_file("33", step=step, msg="右勾拳")


def punching(robot, step: int = 1):
    robot.run_action_file("34", step=step, msg="攻步冲拳")


def crouching(robot, step: int = 1):
    robot.run_action_file("35", step=step, msg="八字蹲拳")


def yongchun(robot, step: int = 1):
    robot.run_action_file("36", step=step, msg="咏春拳")


def beat_chest(robot, step: int = 1):
    robot.run_action_file("37", step=step, msg="捶胸")


def left_side_kick(robot, step: int = 1):
    robot.run_action_file("50", step=step, msg="左侧踢")


def right_side_kick(robot, step: int = 1):
    robot.run_action_file("51", step=step, msg="右侧踢")


def left_foot_shot(robot, step: int = 1):
    robot.run_action_file("52", step=step, msg="左脚射门")


def right_foot_shot(robot, step: int = 1):
    robot.run_action_file("53", step=step, msg="右脚射门")


def show_poss(robot, step: int = 1):
    robot.run_action_file("60", step=step, msg="摆拍poss")


def inverted_standing(robot, step: int = 1):
    robot.run_action_file("101", step=step, msg="前倒站立")


def rear_stand_up(robot, step: int = 1):
    robot.run_action_file("102", step=step, msg="后倒站立")


def supine_stand(robot):
    """仰卧站立"""

    def step_1(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(0)
        left_leg.lean(0)
        left_leg.curve(0)
        left_leg.forward(0)
        left_leg.up(0)

        left_hand = robot.left_hand
        left_hand.curve(-9)
        left_hand.up(-75)
        left_hand.forward(0)

        right_leg = robot.right_leg
        right_leg.tilt(0)
        right_leg.lean(0)
        right_leg.curve(0)
        right_leg.forward(0)
        right_leg.up(0)

        right_hand = robot.right_hand
        right_hand.curve(-9)
        right_hand.up(-75)
        right_hand.forward(0)

        robot.finish()

    def step_2(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(0)
        left_leg.lean(-2)
        left_leg.curve(-95)
        left_leg.forward(89)
        left_leg.up(0)

        left_hand = robot.left_hand
        left_hand.curve(-9)
        left_hand.up(-75)
        left_hand.forward(-21)

        right_leg = robot.right_leg
        right_leg.tilt(0)
        right_leg.lean(4)
        right_leg.curve(-98)
        right_leg.forward(89)
        right_leg.up(0)

        right_hand = robot.right_hand
        right_hand.curve(-9)
        right_hand.up(-75)
        right_hand.forward(-21)

        robot.finish()

    def step_3(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(0)
        left_leg.lean(0)
        left_leg.curve(-145)
        left_leg.forward(50)
        left_leg.up(0)

        left_hand = robot.left_hand
        left_hand.curve(-9)
        left_hand.up(-9)
        left_hand.forward(-21)

        right_leg = robot.right_leg
        right_leg.tilt(0)
        right_leg.lean(0)
        right_leg.curve(-146)
        right_leg.forward(51)
        right_leg.up(0)

        right_hand = robot.right_hand
        right_hand.curve(-9)
        right_hand.up(-9)
        right_hand.forward(-21)

        robot.finish()

    def step_4(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(0)
        left_leg.lean(23)
        left_leg.curve(-42)
        left_leg.forward(-89)
        left_leg.up(0)

        left_hand = robot.left_hand
        left_hand.curve(4)
        left_hand.up(90)
        left_hand.forward(56)

        right_leg = robot.right_leg
        right_leg.tilt(0)
        right_leg.lean(23)
        right_leg.curve(-42)
        right_leg.forward(-89)
        right_leg.up(0)

        right_hand = robot.right_hand
        right_hand.curve(4)
        right_hand.up(90)
        right_hand.forward(56)

        robot.finish()

    def step_5(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(0)
        left_leg.lean(61)
        left_leg.curve(-63)
        left_leg.forward(-89)
        left_leg.up(0)

        left_hand = robot.left_hand
        left_hand.curve(4)
        left_hand.up(90)
        left_hand.forward(84)

        right_leg = robot.right_leg
        right_leg.tilt(0)
        right_leg.lean(60)
        right_leg.curve(-63)
        right_leg.forward(-89)
        right_leg.up(0)

        right_hand = robot.right_hand
        right_hand.curve(4)
        right_hand.up(90)
        right_hand.forward(84)

        robot.finish()

    def step_6(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(0)
        left_leg.lean(56)
        left_leg.curve(-42)
        left_leg.forward(-89)
        left_leg.up(0)

        left_hand = robot.left_hand
        left_hand.curve(4)
        left_hand.up(-75)
        left_hand.forward(56)

        right_leg = robot.right_leg
        right_leg.tilt(0)
        right_leg.lean(56)
        right_leg.curve(-42)
        right_leg.forward(-89)
        right_leg.up(0)

        right_hand = robot.right_hand
        right_hand.curve(4)
        right_hand.up(-75)
        right_hand.forward(56)

        robot.finish()

    def step_7(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(0)
        left_leg.lean(26)
        left_leg.curve(-46)
        left_leg.forward(23)
        left_leg.up(0)

        left_hand = robot.left_hand
        left_hand.curve(-18)
        left_hand.up(-75)
        left_hand.forward(0)

        right_leg = robot.right_leg
        right_leg.tilt(0)
        right_leg.lean(26)
        right_leg.curve(-46)
        right_leg.forward(23)
        right_leg.up(0)

        right_hand = robot.right_hand
        right_hand.curve(-18)
        right_hand.up(-75)
        right_hand.forward(0)

        robot.finish()

    step_1(robot)
    step_2(robot)
    step_3(robot)
    step_4(robot)
    step_5(robot)
    step_6(robot)
    step_7(robot)
    print('仰卧站立')


def prone_stand(robot):
    """俯卧站立"""

    def step_1(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(0)
        left_leg.lean(26)
        left_leg.curve(-49)
        left_leg.forward(23)
        left_leg.up(0)

        left_hand = robot.left_hand
        left_hand.curve(0)
        left_hand.up(0)
        left_hand.forward(90)

        right_leg = robot.right_leg
        right_leg.tilt(0)
        right_leg.lean(26)
        right_leg.curve(-49)
        right_leg.forward(23)
        right_leg.up(0)

        right_hand = robot.right_hand
        right_hand.curve(0)
        right_hand.up(0)
        right_hand.forward(90)

        robot.finish()

    def step_2(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(0)
        left_leg.lean(0)
        left_leg.curve(0)
        left_leg.forward(0)
        left_leg.up(0)

        left_hand = robot.left_hand
        left_hand.curve(-75)
        left_hand.up(-21)
        left_hand.forward(93)

        right_leg = robot.right_leg
        right_leg.tilt(0)
        right_leg.lean(0)
        right_leg.curve(0)
        right_leg.forward(0)
        right_leg.up(0)

        right_hand = robot.right_hand
        right_hand.curve(-75)
        right_hand.up(-21)
        right_hand.forward(92)

        robot.finish()

    def step_3(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(0)
        left_leg.lean(0)
        left_leg.curve(0)
        left_leg.forward(0)
        left_leg.up(0)

        left_hand = robot.left_hand
        left_hand.curve(-75)
        left_hand.up(-21)
        left_hand.forward(93)

        right_leg = robot.right_leg
        right_leg.tilt(0)
        right_leg.lean(0)
        right_leg.curve(0)
        right_leg.forward(0)
        right_leg.up(0)

        right_hand = robot.right_hand
        right_hand.curve(-75)
        right_hand.up(-21)
        right_hand.forward(92)

        robot.finish()

    def step_4(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(0)
        left_leg.lean(-60)
        left_leg.curve(60)
        left_leg.forward(84)
        left_leg.up(0)

        left_hand = robot.left_hand
        left_hand.curve(0)
        left_hand.up(-90)
        left_hand.forward(119)

        right_leg = robot.right_leg
        right_leg.tilt(0)
        right_leg.lean(-61)
        right_leg.curve(60)
        right_leg.forward(84)
        right_leg.up(0)

        right_hand = robot.right_hand
        right_hand.curve(0)
        right_hand.up(-90)
        right_hand.forward(119)

        robot.finish()

    def step_5(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(0)
        left_leg.lean(-60)
        left_leg.curve(60)
        left_leg.forward(84)
        left_leg.up(0)

        left_hand = robot.left_hand
        left_hand.curve(0)
        left_hand.up(-90)
        left_hand.forward(119)

        right_leg = robot.right_leg
        right_leg.tilt(0)
        right_leg.lean(-61)
        right_leg.curve(60)
        right_leg.forward(84)
        right_leg.up(0)

        right_hand = robot.right_hand
        right_hand.curve(0)
        right_hand.up(-90)
        right_hand.forward(119)

        robot.finish()

    def step_6(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(0)
        left_leg.lean(-60)
        left_leg.curve(60)
        left_leg.forward(0)
        left_leg.up(0)

        left_hand = robot.left_hand
        left_hand.curve(0)
        left_hand.up(-90)
        left_hand.forward(84)

        right_leg = robot.right_leg
        right_leg.tilt(0)
        right_leg.lean(-61)
        right_leg.curve(60)
        right_leg.forward(0)
        right_leg.up(0)

        right_hand = robot.right_hand
        right_hand.curve(0)
        right_hand.up(-90)
        right_hand.forward(84)

        robot.finish()

    def step_7(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(0)
        left_leg.lean(0)
        left_leg.curve(0)
        left_leg.forward(0)
        left_leg.up(0)

        left_hand = robot.left_hand
        left_hand.curve(-9)
        left_hand.up(-75)
        left_hand.forward(0)

        right_leg = robot.right_leg
        right_leg.tilt(0)
        right_leg.lean(0)
        right_leg.curve(0)
        right_leg.forward(0)
        right_leg.up(0)

        right_hand = robot.right_hand
        right_hand.curve(-9)
        right_hand.up(-75)
        right_hand.forward(0)

        robot.finish()

    def step_8(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(0)
        left_leg.lean(26)
        left_leg.curve(-49)
        left_leg.forward(23)
        left_leg.up(0)

        left_hand = robot.left_hand
        left_hand.curve(-18)
        left_hand.up(-75)
        left_hand.forward(0)

        right_leg = robot.right_leg
        right_leg.tilt(0)
        right_leg.lean(26)
        right_leg.curve(-49)
        right_leg.forward(23)
        right_leg.up(0)

        right_hand = robot.right_hand
        right_hand.curve(-18)
        right_hand.up(-75)
        right_hand.forward(0)

        robot.finish()

    step_1(robot)
    step_2(robot)
    step_3(robot)
    step_4(robot)
    step_5(robot)
    step_6(robot)
    step_7(robot)
    step_8(robot)
    print('俯卧站立')


def new_down(robot):
    """机器人蹲下（函数）"""

    def step_1(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(2)
        left_leg.lean(77)
        left_leg.curve(-131)
        left_leg.forward(52)
        left_leg.up(0)

        left_hand = robot.left_hand
        left_hand.curve(0)
        left_hand.up(-72)
        left_hand.forward(6)

        right_leg = robot.right_leg
        right_leg.tilt(-2)
        right_leg.lean(72)
        right_leg.curve(-136)
        right_leg.forward(55)
        right_leg.up(0)

        right_hand = robot.right_hand
        right_hand.curve(0)
        right_hand.up(-77)
        right_hand.forward(6)

        robot.finish()

    step_1(robot)


def new_up(robot):
    """站立"""

    def step_1(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(2)
        left_leg.lean(45)
        left_leg.curve(-76)
        left_leg.forward(30)
        left_leg.up(0)

        left_hand = robot.left_hand
        left_hand.curve(5)
        left_hand.up(-80)
        left_hand.forward(-1)

        right_leg = robot.right_leg
        right_leg.tilt(-2)
        right_leg.lean(32)
        right_leg.curve(-69)
        right_leg.forward(27)
        right_leg.up(0)

        right_hand = robot.right_hand
        right_hand.curve(5)
        right_hand.up(-87)
        right_hand.forward(1)

        robot.finish()

    step_1(robot)


def hangs_hold(robot):
    """机器人双手抱"""

    def step_1(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(2)
        left_leg.lean(82)
        left_leg.curve(-146)
        left_leg.forward(67)
        left_leg.up(0)

        left_hand = robot.left_hand
        left_hand.curve(-7)
        left_hand.up(-87)
        left_hand.forward(78)

        right_leg = robot.right_leg
        right_leg.tilt(-2)
        right_leg.lean(80)
        right_leg.curve(-150)
        right_leg.forward(70)
        right_leg.up(0)

        right_hand = robot.right_hand
        right_hand.curve(-12)
        right_hand.up(-90)
        right_hand.forward(68)

        robot.finish()

    def step_2(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(2)
        left_leg.lean(82)
        left_leg.curve(-146)
        left_leg.forward(67)
        left_leg.up(0)

        left_hand = robot.left_hand
        left_hand.curve(-40)
        left_hand.up(-90)
        left_hand.forward(68)

        right_leg = robot.right_leg
        right_leg.tilt(-2)
        right_leg.lean(80)
        right_leg.curve(-150)
        right_leg.forward(70)
        right_leg.up(0)

        right_hand = robot.right_hand
        right_hand.curve(-10)
        right_hand.up(-90)
        right_hand.forward(80)

        robot.finish()

    def step_3(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(2)
        left_leg.lean(82)
        left_leg.curve(-146)
        left_leg.forward(67)
        left_leg.up(0)

        left_hand = robot.left_hand
        left_hand.curve(-47)
        left_hand.up(-90)
        left_hand.forward(53)

        right_leg = robot.right_leg
        right_leg.tilt(-2)
        right_leg.lean(80)
        right_leg.curve(-150)
        right_leg.forward(70)
        right_leg.up(0)

        right_hand = robot.right_hand
        right_hand.curve(-55)
        right_hand.up(-90)
        right_hand.forward(36)

        robot.finish()

    step_1(robot)
    step_2(robot)
    step_3(robot)


def stand_with_ball(robot):
    """机器人站立抱球（函数）"""

    def step_1(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(2)
        left_leg.lean(35)
        left_leg.curve(-74)
        left_leg.forward(40)
        left_leg.up(0)

        left_hand = robot.left_hand
        left_hand.curve(-47)
        left_hand.up(-90)
        left_hand.forward(53)

        right_leg = robot.right_leg
        right_leg.tilt(-2)
        right_leg.lean(27)
        right_leg.curve(-69)
        right_leg.forward(37)
        right_leg.up(0)

        right_hand = robot.right_hand
        right_hand.curve(-55)
        right_hand.up(-90)
        right_hand.forward(36)

        robot.finish()

    step_1(robot)


def down_with_ball(robot):
    """机器人抱球蹲下"""

    def step_1(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(2)
        left_leg.lean(77)
        left_leg.curve(-131)
        left_leg.forward(52)
        left_leg.up(0)

        left_hand = robot.left_hand
        left_hand.curve(-47)
        left_hand.up(-90)
        left_hand.forward(53)

        right_leg = robot.right_leg
        right_leg.tilt(-2)
        right_leg.lean(72)
        right_leg.curve(-136)
        right_leg.forward(55)
        right_leg.up(0)

        right_hand = robot.right_hand
        right_hand.curve(-55)
        right_hand.up(-90)
        right_hand.forward(36)

        robot.finish()

    step_1(robot)


def turn_right(robot):
    """机器人右转"""

    def step_1(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(-12)
        left_leg.lean(11)
        left_leg.curve(-55)
        left_leg.forward(45)
        left_leg.up(12)

        left_hand = robot.left_hand
        left_hand.curve(-47)
        left_hand.up(-90)
        left_hand.forward(53)

        right_leg = robot.right_leg
        right_leg.tilt(-12)
        right_leg.lean(45)
        right_leg.curve(-55)
        right_leg.forward(11)
        right_leg.up(12)

        right_hand = robot.right_hand
        right_hand.curve(-55)
        right_hand.up(-90)
        right_hand.forward(36)

        robot.finish()

    def step_2(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(0)
        left_leg.lean(36)
        left_leg.curve(-72)
        left_leg.forward(36)
        left_leg.up(0)

        left_hand = robot.left_hand
        left_hand.curve(-47)
        left_hand.up(-90)
        left_hand.forward(53)

        right_leg = robot.right_leg
        right_leg.tilt(0)
        right_leg.lean(36)
        right_leg.curve(-72)
        right_leg.forward(36)
        right_leg.up(0)

        right_hand = robot.right_hand
        right_hand.curve(-55)
        right_hand.up(-90)
        right_hand.forward(36)

        robot.finish()

    step_1(robot)
    step_2(robot)


def hands_open(robot):
    """蹲下双手张开"""

    def step_1(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(2)
        left_leg.lean(77)
        left_leg.curve(-131)
        left_leg.forward(52)
        left_leg.up(0)

        left_hand = robot.left_hand
        left_hand.curve(5)
        left_hand.up(-90)
        left_hand.forward(71)

        right_leg = robot.right_leg
        right_leg.tilt(-2)
        right_leg.lean(72)
        right_leg.curve(-136)
        right_leg.forward(55)
        right_leg.up(0)

        right_hand = robot.right_hand
        right_hand.curve(5)
        right_hand.up(-90)
        right_hand.forward(53)

        robot.finish()

    step_1(robot)


def go_with_ball(robot):
    """机器人抱球走"""

    def step_1(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(20)
        left_leg.lean(35)
        left_leg.curve(-74)
        left_leg.forward(40)
        left_leg.up(-10)

        left_hand = robot.left_hand
        left_hand.curve(-47)
        left_hand.up(-90)
        left_hand.forward(53)

        right_leg = robot.right_leg
        right_leg.tilt(-17)
        right_leg.lean(27)
        right_leg.curve(-69)
        right_leg.forward(37)
        right_leg.up(12)

        right_hand = robot.right_hand
        right_hand.curve(-55)
        right_hand.up(-90)
        right_hand.forward(46)

        robot.finish()

    def step_2(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(20)
        left_leg.lean(35)
        left_leg.curve(-74)
        left_leg.forward(40)
        left_leg.up(-10)

        left_hand = robot.left_hand
        left_hand.curve(-47)
        left_hand.up(-90)
        left_hand.forward(53)

        right_leg = robot.right_leg
        right_leg.tilt(-32)
        right_leg.lean(15)
        right_leg.curve(-66)
        right_leg.forward(57)
        right_leg.up(12)

        right_hand = robot.right_hand
        right_hand.curve(-55)
        right_hand.up(-90)
        right_hand.forward(46)

        robot.finish()

    def step_3(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(0)
        left_leg.lean(35)
        left_leg.curve(-74)
        left_leg.forward(40)
        left_leg.up(-2)

        left_hand = robot.left_hand
        left_hand.curve(-47)
        left_hand.up(-90)
        left_hand.forward(53)

        right_leg = robot.right_leg
        right_leg.tilt(-10)
        right_leg.lean(15)
        right_leg.curve(-66)
        right_leg.forward(57)
        right_leg.up(12)

        right_hand = robot.right_hand
        right_hand.curve(-55)
        right_hand.up(-90)
        right_hand.forward(46)

        robot.finish()

    def step_4(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(-7)
        left_leg.lean(40)
        left_leg.curve(-76)
        left_leg.forward(42)
        left_leg.up(-2)

        left_hand = robot.left_hand
        left_hand.curve(-47)
        left_hand.up(-90)
        left_hand.forward(53)

        right_leg = robot.right_leg
        right_leg.tilt(15)
        right_leg.lean(15)
        right_leg.curve(-66)
        right_leg.forward(62)
        right_leg.up(0)

        right_hand = robot.right_hand
        right_hand.curve(-55)
        right_hand.up(-90)
        right_hand.forward(46)

        robot.finish()

    def step_5(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(-17)
        left_leg.lean(5)
        left_leg.curve(-46)
        left_leg.forward(30)
        left_leg.up(-10)

        left_hand = robot.left_hand
        left_hand.curve(-47)
        left_hand.up(-90)
        left_hand.forward(53)

        right_leg = robot.right_leg
        right_leg.tilt(15)
        right_leg.lean(47)
        right_leg.curve(-84)
        right_leg.forward(30)
        right_leg.up(17)

        right_hand = robot.right_hand
        right_hand.curve(-55)
        right_hand.up(-90)
        right_hand.forward(46)

        robot.finish()

    def step_6(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(-22)
        left_leg.lean(10)
        left_leg.curve(-59)
        left_leg.forward(45)
        left_leg.up(-17)

        left_hand = robot.left_hand
        left_hand.curve(-47)
        left_hand.up(-90)
        left_hand.forward(53)

        right_leg = robot.right_leg
        right_leg.tilt(12)
        right_leg.lean(47)
        right_leg.curve(-84)
        right_leg.forward(30)
        right_leg.up(17)

        right_hand = robot.right_hand
        right_hand.curve(-55)
        right_hand.up(-90)
        right_hand.forward(46)

        robot.finish()

    def step_7(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(2)
        left_leg.lean(17)
        left_leg.curve(-59)
        left_leg.forward(45)
        left_leg.up(-5)

        left_hand = robot.left_hand
        left_hand.curve(-47)
        left_hand.up(-90)
        left_hand.forward(53)

        right_leg = robot.right_leg
        right_leg.tilt(-7)
        right_leg.lean(47)
        right_leg.curve(-84)
        right_leg.forward(30)
        right_leg.up(7)

        right_hand = robot.right_hand
        right_hand.curve(-55)
        right_hand.up(-90)
        right_hand.forward(46)

        robot.finish()

    def step_8(robot):
        head = robot.head
        head.up(0)
        head.left(0)

        left_leg = robot.left_leg
        left_leg.tilt(20)
        left_leg.lean(17)
        left_leg.curve(-59)
        left_leg.forward(45)
        left_leg.up(-5)

        left_hand = robot.left_hand
        left_hand.curve(-47)
        left_hand.up(-90)
        left_hand.forward(53)

        right_leg = robot.right_leg
        right_leg.tilt(-37)
        right_leg.lean(47)
        right_leg.curve(-84)
        right_leg.forward(30)
        right_leg.up(7)

        right_hand = robot.right_hand
        right_hand.curve(-55)
        right_hand.up(-90)
        right_hand.forward(46)

        robot.finish()

    step_1(robot)
    step_2(robot)
    step_3(robot)
    step_4(robot)
    step_5(robot)
    step_6(robot)
    step_7(robot)
    step_8(robot)


def move_with_ball(robot):
    """机器人抱球移动"""
    new_down(robot)
    hangs_hold(robot)
    stand_with_ball(robot)
    for _ in range(10):
        turn_right(robot)
        time.sleep(0.3)
    for _ in range(8):
        go_with_ball(robot)
        time.sleep(0.3)
    down_with_ball(robot)
    hands_open(robot)
    new_up(robot)
