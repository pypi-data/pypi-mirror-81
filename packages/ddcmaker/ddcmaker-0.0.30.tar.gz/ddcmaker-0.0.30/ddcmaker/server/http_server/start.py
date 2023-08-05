# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-+
# -*- coding: utf-8 -*-                            |
# @Time    : 2020/3/4 17:55                       *
# @Author  : Bob He                                |
# @FileName: start.py                              *
# @Software: PyCharm                               |
# @Project : refactor                                *
# @Csdn    ：https://blog.csdn.net/bobwww123       |
# @Github  ：https://www.github.com/NocoldBob      *
# --*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*-+

# !/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import platform
from bottle import template, Bottle, request, response
import threading

root = Bottle()


@root.hook('before_request')
def validate():
    REQUEST_METHOD = request.environ.get('REQUEST_METHOD')

    HTTP_ACCESS_CONTROL_REQUEST_METHOD = request.environ.get('HTTP_ACCESS_CONTROL_REQUEST_METHOD')
    if REQUEST_METHOD == 'OPTIONS' and HTTP_ACCESS_CONTROL_REQUEST_METHOD:
        request.environ['REQUEST_METHOD'] = HTTP_ACCESS_CONTROL_REQUEST_METHOD


@root.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    # response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = '*'


@root.route('/hello/')
def index():
    return template('<b>Hello {{name}}</b>!', name="world")


@root.route('/show/')
def callback():
    return template('<body style="display: flex;align-items: center;justify-content: center;"><div '
                    'style="background-color: sandybrown;text-align: center;position: absolute;/*top: 0%;*/width: '
                    '300px;height: 300px;"><h1>一点寒光万丈芒，<br>杀尽天下有何妨？<br>深埋不改凌锐志，<br>一遇风云便是皇。<br>——{{ '
                    'name}}</h1></div></body>', name="风凌天下")


@root.route('/robot', method=['post', 'OPTIONS'])
def create_module():
    if request.method == 'OPTIONS':
        print(request.body.read())
        res = {"msg": "", "code": 500, "data": {}}
        return json.dumps(res)
    else:
        data = request.body.read()
    # 判断系统环境，然后自动选择使用方法
    from ddcmaker.server.http_server.makeros import linux_maker
    from ddcmaker.server.http_server.makeros import windows_maker
    from ddcmaker.server.http_server.makeros import Mac_maker
    from ddcmaker.server.http_server.makeros import other_maker
    if platform.system() == "Windows":
        return windows_maker(data)
    elif platform.system() == "Linux":
        return linux_maker(data)
    elif platform.system() == "Darwin":
        return Mac_maker()
    else:
        return other_maker()


def http_server():
    root.run(host="0.0.0.0", port=8083)
