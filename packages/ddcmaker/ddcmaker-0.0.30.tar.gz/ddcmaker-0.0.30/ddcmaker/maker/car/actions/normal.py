import time
from ddcmaker.decorator.safety import args_check


@args_check([('used_time', [int, float], 0, 30), ('speed', int, 0, None)])
def left(car, used_time: [int, float] = 1, speed: int = 50):
    car.right_motor.forward(speed)
    car.left_motor.backward(speed)
    time.sleep(used_time)
    stop(car)


@args_check([('used_time', [int, float], 0, 30), ('speed', int, 0, None)])
def right(car, used_time: [int, float] = 1, speed: int = 50):
    car.right_motor.backward(speed)
    car.left_motor.forward(speed)
    time.sleep(used_time)
    stop(car)


@args_check([('used_time', [int, float], 0, 30), ('speed', int, 0, None)])
def forward(car, used_time: [int, float] = 1, speed: int = 50):
    car.left_motor.forward(speed)
    car.right_motor.forward(speed)
    time.sleep(used_time)
    stop(car)


@args_check([('used_time', [int, float], 0, 30), ('speed', int, 0, None)])
def backward(car, used_time: [int, float] = 1, speed: int = 50):
    car.left_motor.backward(speed)
    car.right_motor.backward(speed)
    time.sleep(used_time)
    stop(car)


def stop(car):
    car.right_motor.stop()
    car.left_motor.stop()
