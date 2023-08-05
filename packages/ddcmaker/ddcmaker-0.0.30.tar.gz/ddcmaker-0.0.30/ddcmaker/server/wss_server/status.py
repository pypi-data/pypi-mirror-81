import json
import re
import requests
import socket
import time

import ddcmaker
from ddcmaker.basic.abc import get_type_int
from ddcmaker.maker import AI_FEATURES
from ddcmaker.basic.system.process import kill_process


def kill_ai_process():
    for name in AI_FEATURES:
        kill_process(name)


def get_mac():
    import uuid
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:].upper()
    return '%s:%s:%s:%s:%s:%s' % (mac[0:2], mac[2:4], mac[4:6], mac[6:8], mac[8:10], mac[10:])


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('www.baidu.com', 0))
        ip = s.getsockname()[0]
    except (socket.gaierror, Exception):
        print("无法连接到外网!")
        ip = "x.x.x.x"
    finally:
        s.close()
    return ip


def get_internet_ip():
    try:
        ip = requests.get("http://members.3322.org/dyndns/getip", timeout=3).text.strip()
        if len(str(ip)) > 7:
            return ip
    except (requests.exceptions.ConnectionError, Exception):
        text = requests.get("http://txt.go.sohu.com/ip/soip", timeout=2).text
        ip = re.findall(r'\d+.\d+.\d+.\d+', text)[0]
        if len(str(ip)) > 7:
            return ip
    print("暂时无法发出外网请求！")


def register_maker(url):
    """
    注册创客
    """
    data = json.dumps(
        {
            'inIp': get_ip(), 'macAddr': get_mac(), 'exIp': get_internet_ip(),
            'type': get_type_int(), 'ddcmaker_version': ddcmaker.__version__
        }
    )
    headers = {'content-type': 'application/json;charset=UTF-8'}
    print({
        'url': url,
        'data': data,
        'headers': headers
    })

    while True:
        response = requests.post(url, data, headers=headers)
        print(response.status_code)
        if response.status_code == 200:
            print("注册成功")
            return
        elif response.status_code == 504:
            print("当前服务器接口不通")
        time.sleep(15)


def update_status(url):
    """
    更新状态
    """
    data = json.dumps({'macAddr': get_mac(), 'onlineStatus': 1})
    headers = {'content-type': 'application/json;charset=UTF-8'}
    print({
        'url': url,
        'data': data,
        'headers': headers
    })
    while True:
        response = requests.post(url, data, headers=headers)
        print("更新状态", response.status_code)
        if response.status_code != 200:
            time.sleep(3)
            print({
                'response.headers': response.headers,
                "response.text": response.text
            })
        else:
            time.sleep(10)
