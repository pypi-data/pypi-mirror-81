from ddcmaker.basic.abc import get_maker_type, Maker

maker_type = get_maker_type()
if maker_type == Maker.CAR:
    from ddcmaker.maker.car import Car
    from ddcmaker.maker.car import init
    from ddcmaker.maker.car.actions import normal
    from ddcmaker.maker.car.actions import ai
    from ddcmaker.maker.car import AI_FEATURES

    init()

elif maker_type == Maker.HUMAN_CODE:
    from ddcmaker.maker.human_code import Robot
    from ddcmaker.maker.human_code import init
    from ddcmaker.maker.human_code.actions import ai
    from ddcmaker.maker.human_code.actions import normal
    from ddcmaker.maker.human_code.actions import head
    from ddcmaker.maker.human_code.actions import gymnastic
    from ddcmaker.maker.human_code import AI_FEATURES

    init()

elif maker_type == Maker.HUMAN:
    from ddcmaker.maker.human import Robot
    from ddcmaker.maker.human import init
    from ddcmaker.maker.human import AI_FEATURES

    init()

elif maker_type == Maker.SPIDER:
    from ddcmaker.maker.spider import Spider
    from ddcmaker.maker.spider import init
    from ddcmaker.maker.spider.actions import normal
    from ddcmaker.maker.spider.actions import ai
    from ddcmaker.maker.spider import AI_FEATURES

    init()

elif maker_type == Maker.HUMAN_HAND:
    from ddcmaker.maker.human_hand import Hand
    from ddcmaker.maker.human_hand import init
    from ddcmaker.maker.human_hand.actions import normal
    from ddcmaker.maker.human_hand.actions import ai
    from ddcmaker.maker.human_hand import AI_FEATURES

    init()
elif maker_type == Maker.UNKNOWN:
    print("该创客设备暂不支持")
    AI_FEATURES = []
