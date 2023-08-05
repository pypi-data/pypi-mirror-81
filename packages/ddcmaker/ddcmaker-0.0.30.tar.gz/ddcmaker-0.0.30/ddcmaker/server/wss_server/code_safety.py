def check_package(code: str):
    """检查是否引入了不允许引入的包"""
    packages = ["os", "shutil"]
    infos = code.split(' ')
    while '' in infos:
        infos.remove('')

    for package in packages:
        if f'import {package}' in ' '.join(infos):
            return False, f"不允许导入{package}"

    return True, ''


def check_code(code):
    """代码检测"""
    status, info = check_package(code)
    if not status:
        return False, info
    return True, ''
