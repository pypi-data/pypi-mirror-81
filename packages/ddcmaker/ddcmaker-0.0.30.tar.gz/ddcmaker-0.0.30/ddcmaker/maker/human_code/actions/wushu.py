"""---------------------------- 五步拳----------------------"""


def gongbuyouchongquan_hand(robot, used_time=1):
    """五步拳 弓步右冲拳"""
    robot.set_servo(servo_infos=[
        (robot.left_wrist, -82),
        (robot.left_elbow, -90),
        (robot.left_shoulder, 90),
        (robot.right_wrist, 0),
        (robot.right_elbow, -90),
        (robot.right_shoulder, 98),
    ], used_time=used_time)


def gongbuyouchongquan_leg(robot, used_time=1):
    """五步拳 弓步右冲拳"""
    robot.set_servo(servo_infos=[
        (robot.left_sole, 0),
        (robot.left_ankle, -3),
        (robot.left_knee, -76),
        (robot.left_vertical_hip, 73),
        (robot.left_horizontal_hip, 0),
        (robot.right_sole, -2),
        (robot.right_ankle, 71),
        (robot.right_knee, -49),
        (robot.right_vertical_hip, -29),
        (robot.right_horizontal_hip, 0),
    ], used_time=used_time)


def kick_hand(robot, used_time=1):
    """五步拳 弹踢冲拳"""
    robot.set_servo(servo_infos=[
        (robot.left_wrist, 0),
        (robot.left_elbow, -90),
        (robot.left_shoulder, 87),
        (robot.right_wrist, -60),
        (robot.right_elbow, -62),
        (robot.right_shoulder, 0),
    ], used_time=used_time)


def kick_leg(robot, used_time=1):
    """五步拳 弹踢冲拳"""
    robot.set_servo(servo_infos=[
        (robot.left_sole, 17),
        (robot.left_ankle, 0),
        (robot.left_knee, 15),
        (robot.left_vertical_hip, -32),
        (robot.left_horizontal_hip, 0),
        (robot.right_sole, -42),
        (robot.right_ankle, -40),
        (robot.right_knee, 0),
        (robot.right_vertical_hip, 35),
        (robot.right_horizontal_hip, 0),
    ], used_time=used_time)


def split_palm_hand(robot, used_time=1):
    """五步拳 插步盖掌"""
    robot.set_servo(servo_infos=[
        (robot.left_wrist, -87),
        (robot.left_elbow, -42),
        (robot.left_shoulder, 0),
        (robot.right_wrist, 0),
        (robot.right_elbow, -90),
        (robot.right_shoulder, 140),
    ], used_time=used_time)


def split_palm_leg(robot, used_time=1):
    """五步拳 插步盖掌"""
    robot.set_servo(servo_infos=[
        (robot.left_sole, 2),
        (robot.left_ankle, 22),
        (robot.left_knee, 0),
        (robot.left_vertical_hip, -22),
        (robot.left_horizontal_hip, 0),
        (robot.right_sole, 0),
        (robot.right_ankle, -25),
        (robot.right_knee, 2),
        (robot.right_vertical_hip, 22),
        (robot.right_horizontal_hip, 0),
    ], used_time=used_time)


def horse_steps_hand(robot, used_time=1):
    """五步拳  马步架打"""
    robot.set_servo(servo_infos=[
        (robot.left_wrist, 0),
        (robot.left_elbow, -25),
        (robot.left_shoulder, 0),
        (robot.right_wrist, 37),
        (robot.right_elbow, 0),
        (robot.right_shoulder, 5),
    ], used_time=used_time)


def horse_steps_leg(robot, used_time=1):
    """五步拳  马步架打"""
    robot.set_servo(servo_infos=[
        (robot.left_sole, -7),
        (robot.left_ankle, 50),
        (robot.left_knee, -122),
        (robot.left_vertical_hip, 75),
        (robot.left_horizontal_hip, 10),
        (robot.right_sole, -10),
        (robot.right_ankle, 50),
        (robot.right_knee, -122),
        (robot.right_vertical_hip, 75),
        (robot.right_horizontal_hip, 10),
    ], used_time=used_time)


"""———————————————————咏春—————————————————————"""


def up_cut_hand(robot, used_time=1):
    """咏春 上切"""
    robot.set_servo(servo_infos=[
        (robot.left_wrist, -37),
        (robot.left_elbow, -90),
        (robot.left_shoulder, 97),
        (robot.right_wrist, -37),
        (robot.right_elbow, -90),
        (robot.right_shoulder, 130),
    ], used_time=used_time)


def up_cut_leg(robot, used_time=1):
    """咏春 上切"""
    robot.set_servo(servo_infos=[
        (robot.left_sole, 0),
        (robot.left_ankle, 26),
        (robot.left_knee, -49),
        (robot.left_vertical_hip, 23),
        (robot.left_horizontal_hip, 0),
        (robot.right_sole, 0),
        (robot.right_ankle, 26),
        (robot.right_knee, -49),
        (robot.right_vertical_hip, 23),
        (robot.right_horizontal_hip, 0),
    ], used_time=used_time)


def down_cut_hand(robot, used_time=1):
    """咏春 下切"""
    robot.set_servo(servo_infos=[
        (robot.left_wrist, -37),
        (robot.left_elbow, -90),
        (robot.left_shoulder, 115),
        (robot.right_wrist, -37),
        (robot.right_elbow, -90),
        (robot.right_shoulder, 63),
    ], used_time=used_time)


def down_cut_leg(robot, used_time=1):
    """咏春 下切"""
    robot.set_servo(servo_infos=[
        (robot.left_sole, 0),
        (robot.left_ankle, 26),
        (robot.left_knee, -49),
        (robot.left_vertical_hip, 23),
        (robot.left_horizontal_hip, 0),
        (robot.right_sole, 0),
        (robot.right_ankle, 26),
        (robot.right_knee, -49),
        (robot.right_vertical_hip, 23),
        (robot.right_horizontal_hip, 0),
    ], used_time=used_time)


def akimbo_hand(robot, used_time=1):
    """咏春 叉腰"""
    robot.set_servo(servo_infos=[
        (robot.left_wrist, -18),
        (robot.left_elbow, -56),
        (robot.left_shoulder, 0),
        (robot.right_wrist, -18),
        (robot.right_elbow, -56),
        (robot.right_shoulder, 0),
    ], used_time=used_time)


def akimbo_leg(robot, used_time=1):
    """咏春 叉腰"""
    robot.set_servo(servo_infos=[
        (robot.left_sole, 0),
        (robot.left_ankle, 26),
        (robot.left_knee, -49),
        (robot.left_vertical_hip, 23),
        (robot.left_horizontal_hip, 0),
        (robot.right_sole, 0),
        (robot.right_ankle, 26),
        (robot.right_knee, -49),
        (robot.right_vertical_hip, 23),
        (robot.right_horizontal_hip, 0),
    ], used_time=used_time)


"""---------------大洪拳----------------------"""


def right_boxing_hand(robot, used_time=1):
    """大洪拳 弓步右冲拳"""
    robot.set_servo(servo_infos=[
        (robot.left_wrist, -87),
        (robot.left_elbow, -90),
        (robot.left_shoulder, 95),
        (robot.right_wrist, 0),
        (robot.right_elbow, -90),
        (robot.right_shoulder, 95),
    ], used_time=used_time)


def right_boxing_leg(robot, used_time=1):
    """大洪拳 弓步右冲拳"""
    robot.set_servo(servo_infos=[
        (robot.left_sole, 0),
        (robot.left_ankle, 50),
        (robot.left_knee, 0),
        (robot.left_vertical_hip, -52),
        (robot.left_horizontal_hip, 0),
        (robot.right_sole, 0),
        (robot.right_ankle, 0),
        (robot.right_knee, -80),
        (robot.right_vertical_hip, 72),
        (robot.right_horizontal_hip, 0),
    ], used_time=used_time)


def hook_boxing_hand(robot, used_time=1):
    """大洪拳 震脚冲拳"""
    robot.set_servo(servo_infos=[
        (robot.left_wrist, 0),
        (robot.left_elbow, 87),
        (robot.left_shoulder, 0),
        (robot.right_wrist, -87),
        (robot.right_elbow, -90),
        (robot.right_shoulder, 92),
    ], used_time=used_time)


def hook_boxing_leg(robot, used_time=1):
    """大洪拳 震脚冲拳"""
    robot.set_servo(servo_infos=[
        (robot.left_sole, 0),
        (robot.left_ankle, 0),
        (robot.left_knee, 0),
        (robot.left_vertical_hip, 0),
        (robot.left_horizontal_hip, 0),
        (robot.right_sole, 0),
        (robot.right_ankle, 0),
        (robot.right_knee, 0),
        (robot.right_vertical_hip, 0),
        (robot.right_horizontal_hip, 0),
    ], used_time=used_time)


def level_boxing_hand(robot, used_time=1):
    """大洪拳 弓步双冲拳"""
    robot.set_servo(servo_infos=[
        (robot.left_wrist, 0),
        (robot.left_elbow, 0),
        (robot.left_shoulder, 0),
        (robot.right_wrist, 0),
        (robot.right_elbow, 0),
        (robot.right_shoulder, 0),
    ], used_time=used_time)


def level_boxing_leg(robot, used_time=1):
    """大洪拳 弓步双冲拳"""
    robot.set_servo(servo_infos=[
        (robot.left_sole, 0),
        (robot.left_ankle, 20),
        (robot.left_knee, -85),
        (robot.left_vertical_hip, 72),
        (robot.left_horizontal_hip, 0),
        (robot.right_sole, -30),
        (robot.right_ankle, 27),
        (robot.right_knee, -62),
        (robot.right_vertical_hip, 40),
        (robot.right_horizontal_hip, 32),
    ], used_time=used_time)


def squat_hand(robot, used_time=1):
    """大洪拳 扑步单切"""
    robot.set_servo(servo_infos=[
        (robot.left_wrist, 0),
        (robot.left_elbow, -70),
        (robot.left_shoulder, -2),
        (robot.right_wrist, -75),
        (robot.right_elbow, -47),
        (robot.right_shoulder, 10),
    ], used_time=used_time)


def squat_leg(robot, used_time=1):
    """大洪拳 扑步单切"""
    robot.set_servo(servo_infos=[
        (robot.left_sole, -27),
        (robot.left_ankle, 0),
        (robot.left_knee, 0),
        (robot.left_vertical_hip, 0),
        (robot.left_horizontal_hip, 30),
        (robot.right_sole, -5),
        (robot.right_ankle, 15),
        (robot.right_knee, -72),
        (robot.right_vertical_hip, 67),
        (robot.right_horizontal_hip, 0),
    ], used_time=used_time)


def top_palm_hand(robot, used_time=1):
    """大洪拳 白云盖顶"""
    robot.set_servo(servo_infos=[
        (robot.left_wrist, 0),
        (robot.left_elbow, 87),
        (robot.left_shoulder, 5),
        (robot.right_wrist, -75),
        (robot.right_elbow, -50),
        (robot.right_shoulder, 7),
    ], used_time=used_time)


def top_palm_leg(robot, used_time=1):
    """大洪拳 白云盖顶"""
    robot.set_servo(servo_infos=[
        (robot.left_sole, 0),
        (robot.left_ankle, 0),
        (robot.left_knee, -65),
        (robot.left_vertical_hip, 57),
        (robot.left_horizontal_hip, 0),
        (robot.right_sole, 2),
        (robot.right_ankle, 35),
        (robot.right_knee, 17),
        (robot.right_vertical_hip, -42),
        (robot.right_horizontal_hip, 0),
    ], used_time=used_time)


def left_boxing_hand(robot, used_time=1):
    """大洪拳 弓步擒打"""
    robot.set_servo(servo_infos=[
        (robot.left_wrist, 0),
        (robot.left_elbow, 87),
        (robot.left_shoulder, 0),
        (robot.right_wrist, -87),
        (robot.right_elbow, -90),
        (robot.right_shoulder, 95),
    ], used_time=used_time)


def left_boxing_leg(robot, used_time=1):
    """大洪拳 弓步擒打"""
    robot.set_servo(servo_infos=[
        (robot.left_sole, 0),
        (robot.left_ankle, 52),
        (robot.left_knee, 0),
        (robot.left_vertical_hip, -60),
        (robot.left_horizontal_hip, 0),
        (robot.right_sole, 0),
        (robot.right_ankle, 0),
        (robot.right_knee, -80),
        (robot.right_vertical_hip, 75),
        (robot.right_horizontal_hip, 0),
    ], used_time=used_time)


def hands_together_hand(robot, used_time=1):
    """大洪拳 双手合十"""
    robot.set_servo(servo_infos=[
        (robot.left_wrist, -60),
        (robot.left_elbow, -87),
        (robot.left_shoulder, 95),
        (robot.right_wrist, -60),
        (robot.right_elbow, -87),
        (robot.right_shoulder, 95),
    ], used_time=used_time)


def hands_together_leg(robot, used_time=1):
    """大洪拳 双手合十 """
    robot.set_servo(servo_infos=[
        (robot.left_sole, 0),
        (robot.left_ankle, 0),
        (robot.left_knee, 0),
        (robot.left_vertical_hip, 0),
        (robot.left_horizontal_hip, 0),
        (robot.right_sole, 0),
        (robot.right_ankle, 0),
        (robot.right_knee, 0),
        (robot.right_vertical_hip, 0),
        (robot.right_horizontal_hip, 0),
    ], used_time=used_time)


"""--------------------太祖长拳--------------------"""


def boxing_palm_hand(robot, used_time=1):
    """太祖长拳 拳后藏掌"""
    robot.set_servo(servo_infos=[
        (robot.left_wrist, -90),
        (robot.left_elbow, -90),
        (robot.left_shoulder, 102),
        (robot.right_wrist, -2),
        (robot.right_elbow, -90),
        (robot.right_shoulder, 97),
    ], used_time=used_time)


def boxing_palm_leg(robot, used_time=1):
    """太祖长拳 拳后藏掌"""
    robot.set_servo(servo_infos=[
        (robot.left_sole, 2),
        (robot.left_ankle, 0),
        (robot.left_knee, -75),
        (robot.left_vertical_hip, 69),
        (robot.left_horizontal_hip, 0),
        (robot.right_sole, -5),
        (robot.right_ankle, 40),
        (robot.right_knee, 5),
        (robot.right_vertical_hip, -47),
        (robot.right_horizontal_hip, 0),
    ], used_time=used_time)


def fd_palm_hand(robot, used_time=1):
    """太祖长拳 弓步推掌"""
    robot.set_servo(servo_infos=[
        (robot.left_wrist, -2),
        (robot.left_elbow, -90),
        (robot.left_shoulder, 102),
        (robot.right_wrist, -70),
        (robot.right_elbow, -42),
        (robot.right_shoulder, 5),
    ], used_time=used_time)


def fd_palm_leg(robot, used_time=1):
    """太祖长拳 弓步推掌"""
    robot.set_servo(servo_infos=[
        (robot.left_sole, -5),
        (robot.left_ankle, 40),
        (robot.left_knee, 5),
        (robot.left_vertical_hip, -47),
        (robot.left_horizontal_hip, 0),
        (robot.right_sole, 2),
        (robot.right_ankle, 0),
        (robot.right_knee, -75),
        (robot.right_vertical_hip, 66),
        (robot.right_horizontal_hip, 0),
    ], used_time=used_time)


def bk_boxing_hand(robot, used_time=1):
    """太祖长拳 马步后冲拳"""
    robot.set_servo(servo_infos=[
        (robot.left_wrist, -87),
        (robot.left_elbow, -87),
        (robot.left_shoulder, 95),
        (robot.right_wrist, 0),
        (robot.right_elbow, -82),
        (robot.right_shoulder, -50),
    ], used_time=used_time)


def bk_boxing_leg(robot, used_time=1):
    """太祖长拳 马步后冲拳"""
    robot.set_servo(servo_infos=[
        (robot.left_sole, -5),
        (robot.left_ankle, 40),
        (robot.left_knee, 5),
        (robot.left_vertical_hip, -47),
        (robot.left_horizontal_hip, 0),
        (robot.right_sole, 2),
        (robot.right_ankle, 0),
        (robot.right_knee, -75),
        (robot.right_vertical_hip, 66),
        (robot.right_horizontal_hip, 0),
    ], used_time=used_time)


def bend_boxing_middle_hand(robot, used_time=1):
    """太祖长拳 马步勾拳过渡"""
    robot.set_servo(servo_infos=[
        (robot.left_wrist, 0),
        (robot.left_elbow, -87),
        (robot.left_shoulder, 10),
        (robot.right_wrist, 0),
        (robot.right_elbow, -87),
        (robot.right_shoulder, 12),
    ], used_time=used_time)


def bend_boxing_middle_leg(robot, used_time=1):
    """太祖长拳 马步勾拳过渡"""
    robot.set_servo(servo_infos=[
        (robot.left_sole, -10),
        (robot.left_ankle, 0),
        (robot.left_knee, -47),
        (robot.left_vertical_hip, 50),
        (robot.left_horizontal_hip, 10),
        (robot.right_sole, -10),
        (robot.right_ankle, 0),
        (robot.right_knee, -47),
        (robot.right_vertical_hip, 50),
        (robot.right_horizontal_hip, 10),
    ], used_time=used_time)


def bend_boxing_hand(robot, used_time=1):
    """太祖长拳 马步勾拳"""
    robot.set_servo(servo_infos=[
        (robot.left_wrist, 0),
        (robot.left_elbow, -70),
        (robot.left_shoulder, -47),
        (robot.right_wrist, -67),
        (robot.right_elbow, -90),
        (robot.right_shoulder, 90),
    ], used_time=used_time)


def bend_boxing_leg(robot, used_time=1):
    """太祖长拳 马步勾拳 """
    robot.set_servo(servo_infos=[
        (robot.left_sole, -10),
        (robot.left_ankle, 0),
        (robot.left_knee, -47),
        (robot.left_vertical_hip, 50),
        (robot.left_horizontal_hip, 10),
        (robot.right_sole, -10),
        (robot.right_ankle, 0),
        (robot.right_knee, -47),
        (robot.right_vertical_hip, 50),
        (robot.right_horizontal_hip, 10),
    ], used_time=used_time)


"""------------------降龙十八掌---------------------"""


def dragon_kicking_hand(robot, used_time=1):
    """降龙十八掌 履霜冰至"""
    robot.set_servo(servo_infos=[
        (robot.left_wrist, 2),
        (robot.left_elbow, -52),
        (robot.left_shoulder, 20),
        (robot.right_wrist, 0),
        (robot.right_elbow, -30),
        (robot.right_shoulder, 155),
    ], used_time=used_time)


def dragon_kicking_leg(robot, used_time=1):
    """降龙十八掌 履霜冰至"""
    robot.set_servo(servo_infos=[
        (robot.left_sole, -32),
        (robot.left_ankle, 5),
        (robot.left_knee, -85),
        (robot.left_vertical_hip, 82),
        (robot.left_horizontal_hip, 12),
        (robot.right_sole, 15),
        (robot.right_ankle, 12),
        (robot.right_knee, -57),
        (robot.right_vertical_hip, 52),
        (robot.right_horizontal_hip, -7),
    ], used_time=used_time)


def dragon_boxing_hand(robot, used_time=1):
    """降龙十八掌 损则有孚"""
    robot.set_servo(servo_infos=[
        (robot.left_wrist, -77),
        (robot.left_elbow, -17),
        (robot.left_shoulder, 155),
        (robot.right_wrist, 0),
        (robot.right_elbow, -25),
        (robot.right_shoulder, 12),
    ], used_time=used_time)


def dragon_boxing_leg(robot, used_time=1):
    """降龙十八掌 损则有孚"""
    robot.set_servo(servo_infos=[
        (robot.left_sole, 0),
        (robot.left_ankle, 12),
        (robot.left_knee, -57),
        (robot.left_vertical_hip, 50),
        (robot.left_horizontal_hip, 0),
        (robot.right_sole, -17),
        (robot.right_ankle, 12),
        (robot.right_knee, -57),
        (robot.right_vertical_hip, 50),
        (robot.right_horizontal_hip, 20),
    ], used_time=used_time)


def dragon_bend_hand(robot, used_time=1):
    """降龙十八掌 潜龙勿用"""
    robot.set_servo(servo_infos=[
        (robot.left_wrist, 0),
        (robot.left_elbow, -90),
        (robot.left_shoulder, 135),
        (robot.right_wrist, 0),
        (robot.right_elbow, -90),
        (robot.right_shoulder, 137),
    ], used_time=used_time)


def dragon_bend_leg(robot, used_time=1):
    """降龙十八掌 潜龙勿用"""
    robot.set_servo(servo_infos=[
        (robot.left_sole, -7),
        (robot.left_ankle, 12),
        (robot.left_knee, -57),
        (robot.left_vertical_hip, 75),
        (robot.left_horizontal_hip, 10),
        (robot.right_sole, -7),
        (robot.right_ankle, 12),
        (robot.right_knee, -57),
        (robot.right_vertical_hip, 75),
        (robot.right_horizontal_hip, 10),
    ], used_time=used_time)


def dragon_overlapping_hand(robot, used_time=1):
    """降龙十八掌 羝羊触蕃"""
    robot.set_servo(servo_infos=[
        (robot.left_wrist, 0),
        (robot.left_elbow, -90),
        (robot.left_shoulder, 92),
        (robot.right_wrist, 0),
        (robot.right_elbow, -90),
        (robot.right_shoulder, 92),
    ], used_time=used_time)


def dragon_overlapping_leg(robot, used_time=1):
    """降龙十八掌 羝羊触蕃"""
    robot.set_servo(servo_infos=[
        (robot.left_sole, -10),
        (robot.left_ankle, 12),
        (robot.left_knee, -57),
        (robot.left_vertical_hip, 50),
        (robot.left_horizontal_hip, 10),
        (robot.right_sole, -10),
        (robot.right_ankle, 12),
        (robot.right_knee, -57),
        (robot.right_vertical_hip, 50),
        (robot.right_horizontal_hip, 10),
    ], used_time=used_time)


def jianlongzaitian_hand(robot, used_time=1):
    """降龙十八掌 见龙在田"""
    robot.set_servo(servo_infos=[
        (robot.left_wrist, 0),
        (robot.left_elbow, -90),
        (robot.left_shoulder, 92),
        (robot.right_wrist, 0),
        (robot.right_elbow, -90),
        (robot.right_shoulder, 92),
    ], used_time=used_time)


def jianlongzaitian_leg(robot, used_time=1):
    """降龙十八掌 见龙在田"""
    robot.set_servo(servo_infos=[
        (robot.left_sole, 0),
        (robot.left_ankle, 0),
        (robot.left_knee, 0),
        (robot.left_vertical_hip, 0),
        (robot.left_horizontal_hip, 0),
        (robot.right_sole, 0),
        (robot.right_ankle, 0),
        (robot.right_knee, 0),
        (robot.right_vertical_hip, 0),
        (robot.right_horizontal_hip, 0),
    ], used_time=used_time)
