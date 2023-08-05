from ddcmaker.maker.car.car import Car
from ddcmaker.maker.car.actions import normal
from ddcmaker.maker.car.actions import ai
from ddcmaker.maker.car.actions.ai import AI_FEATURES


def init():
    normal_car = Car()
    normal_car.run_action(normal.stop)
