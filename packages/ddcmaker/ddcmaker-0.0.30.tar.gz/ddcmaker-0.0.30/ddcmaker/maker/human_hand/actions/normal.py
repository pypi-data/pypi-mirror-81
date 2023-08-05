import time


def init_body(hand, step: int = 1):
    hand.run_action_file("2_23", step=step)
    time.sleep(1)


def thumb(hand, angle: int):
    """拇指动作"""
    hand.thumb.finger.run(angle)
    time.sleep(0.2)


def index_finger(hand, angle: int):
    """食指动作"""
    hand.index_finger.finger.run(angle)
    time.sleep(0.2)


def middle_finger(hand, angle: int):
    """中指动作"""
    hand.middle_finger.finger.run(angle)
    time.sleep(0.2)


def ring_finger(hand, angle: int):
    """无名指动作"""
    hand.ring_finger.finger.run(angle)
    time.sleep(0.2)


def little_finger(hand, angle: int):
    """小指动作"""
    hand.little_finger.finger.run(angle)
    time.sleep(0.2)


def wrist(hand, angle: int):
    """手腕动作"""
    hand.wrist.finesse.run(angle)
    time.sleep(0.2)


def test_action_fun(hand):
    def step_1(hand):
        thumb(hand, -39)
        index_finger(hand, 50)
        middle_finger(hand, 50)
        ring_finger(hand, 56)
        little_finger(hand, 58)
        wrist(hand, -12)

    def step_2(hand):
        thumb(hand, 12)
        index_finger(hand, -2)
        middle_finger(hand, -12)
        ring_finger(hand, -2)
        little_finger(hand, 10)
        wrist(hand, -12)

    def step_3(hand):
        thumb(hand, 56)
        index_finger(hand, -48)
        middle_finger(hand, -44)
        ring_finger(hand, -41)
        little_finger(hand, -42)
        wrist(hand, -12)

    def step_4(hand):
        thumb(hand, 31)
        index_finger(hand, -10)
        middle_finger(hand, -16)
        ring_finger(hand, 1)
        little_finger(hand, 4)
        wrist(hand, -12)

    def step_5(hand):
        thumb(hand, -35)
        index_finger(hand, 41)
        middle_finger(hand, 31)
        ring_finger(hand, 50)
        little_finger(hand, 46)
        wrist(hand, -12)

    step_1(hand)
    time.sleep(1)
    step_2(hand)
    time.sleep(1)
    step_3(hand)
    time.sleep(1)
    step_4(hand)
    time.sleep(1)
    step_5(hand)


def action_test_file(hand):
    test_action_fun(hand)
