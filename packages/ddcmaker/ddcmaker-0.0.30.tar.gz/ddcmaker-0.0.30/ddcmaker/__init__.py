import platform

__version__ = '0.0.30'
__metaclass__ = type
__all__ = [
    '__init__', "Robot", "Spider", "Car", "Hand"
]
NAME = 'ddcmaker'

if platform.system() == "Linux":
    from ddcmaker.server import *
    from ddcmaker.maker import *
elif platform.system() == "Windows":
    from ddcmaker.server import *
else:
    print("当前系统暂不支持！")
