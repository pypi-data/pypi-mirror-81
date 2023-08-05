import functools
import inspect
from typing import List, Tuple


def args_check(args_info: List[Tuple]):
    """
    参数检查
    :param args_info:待检查的参数信息，[(参数名,参数类型,参数最小值,参数最大值)]
    :return:
    """

    def wrapper(func):
        @functools.wraps(func)
        def inner(self, *args, **kwargs):
            func_args = inspect.getcallargs(func, self, *args, **kwargs)
            annotations = inspect.getfullargspec(func).annotations
            checked = []
            for info in args_info:
                name, arg_type, arg_min, arg_max = info
                value = func_args.get(name)
                if not isinstance(arg_type, list):
                    arg_type = [arg_type]

                if type(value) not in arg_type:
                    raise ValueError(f"参数{name} 预期类型是：{arg_type}，实际是{type(value)}")

                if arg_min is not None:
                    if type(arg_min) not in arg_type:
                        raise ValueError(f"参数{name} 类型错误，预期：{arg_type}，实际：{type(arg_min)}")
                    if value < arg_min:
                        raise ValueError(f"参数{name} 预期最小值是：{arg_min}，实际是{value}")

                if arg_max is not None:
                    if type(arg_max) not in arg_type:
                        raise ValueError(f"参数{name} 类型错误，预期：{arg_type}，实际：{type(arg_max)}")
                    if value > arg_max:
                        raise ValueError(f"参数{name} 预期最大值是：{arg_max}，实际是{value}")
                checked.append(name)

            # 检查剩余的注解
            for annotation in annotations.items():
                name, arg_type = annotation
                if name not in checked:
                    value = func_args.get(name)
                    if not isinstance(value, arg_type):
                        raise ValueError(f"参数{name} 预期类型是：{arg_type}，实际是{type(value)}")

            return func(self, *args, **kwargs)

        return inner

    return wrapper
