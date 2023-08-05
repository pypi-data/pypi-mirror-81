#!/usr/bin/env python
# -*- coding:utf-8 -*-
from ddcmaker.server.wss_server.constant import SERVER_IP, SERVER_PORT

import base64
import json
import logging
import os.path
import socket
import traceback
import uuid
import weakref
import paramiko
import tornado.web
import tornado.websocket
from tempfile import mkstemp
from tornado.ioloop import IOLoop
from tornado.iostream import _ERRNO_CONNRESET
from tornado.options import define, options, parse_command_line
from tornado.util import errno_from_exception

USER = 'pi'
PASSWORD = 'zsyl8888'
PORT = 22

define('address', default=SERVER_IP, help='listen address')
define('port', default=SERVER_PORT, help='listen port', type=int)

BUF_SIZE = 512
DELAY = 1
base_dir = os.path.dirname(__file__)
workers = {}


def get_code(request):
    info = json.loads(request.body)
    if info.get('code', None) is None:
        raise ValueError('json must include code')

    code = str(base64.b64decode(info['code']), encoding="u8")
    return code


def recycle(worker):
    if worker.handler:
        return
    logging.debug('Recycling worker {}'.format(worker.id))
    workers.pop(worker.id, None)
    worker.close()


class Worker(object):
    def __init__(self, ssh, chan, dst_addr):
        self.loop = IOLoop.current()
        self.ssh = ssh
        self.chan = chan
        self.dst_addr = dst_addr
        self.fd = chan.fileno()
        self.id = str(id(self))
        self.data_to_dst = []
        self.handler = None
        self.mode = IOLoop.READ
        self.tmp_fp = None
        self.tmp_file = None
        self.msg_intercepted = False

    def __call__(self, fd, events):
        if events & IOLoop.READ:
            self.on_read()
        if events & IOLoop.WRITE:
            self.on_write()
        if events & IOLoop.ERROR:
            self.close()

    def set_handler(self, handler):
        if not self.handler:
            self.handler = handler

    def update_handler(self, mode):
        if self.mode != mode:
            self.loop.update_handler(self.fd, mode)
            self.mode = mode

    def on_read(self):
        logging.debug('worker {} on read'.format(self.id))
        try:
            data = self.chan.recv(BUF_SIZE)
            # 不显示注销
            if isinstance(data, bytes) and '注销\r\n' in data.decode('utf-8'):
                return
            # 不显示 建立连接的信息
            if 'Linux zsylmaker' in data.decode('utf-8') or 'Last login' in data.decode('utf-8'):
                return
            # 不显示主动输入的命令
            if 'python3' in data.decode('utf-8'):
                return
            if 'pi@zsylmaker' in data.decode('utf-8'):
                return
        except UnicodeDecodeError:
            return
        except (OSError, IOError) as e:
            logging.error(e)
            if errno_from_exception(e) in _ERRNO_CONNRESET:
                self.close()
        else:
            logging.debug('"{}" from {}'.format(data, self.dst_addr))
            if not data:
                self.close()
                return

            logging.debug('"{}" to {}'.format(data, self.handler.src_addr))
            try:
                self.handler.write_message(data)
            except tornado.websocket.WebSocketClosedError:
                self.close()

    def on_write(self):
        logging.debug('worker {} on write'.format(self.id))
        if not self.data_to_dst:
            return

        data = ''.join(self.data_to_dst)
        logging.debug('"{}" to {}'.format(data, self.dst_addr))

        try:
            sent = self.chan.send(data)
        except (OSError, IOError) as e:
            logging.error(e)
            if errno_from_exception(e) in _ERRNO_CONNRESET:
                self.close()
            else:
                self.update_handler(IOLoop.WRITE)
        else:
            self.data_to_dst = []
            data = data[sent:]
            if data:
                self.data_to_dst.append(data)
                self.update_handler(IOLoop.WRITE)
            else:
                self.update_handler(IOLoop.READ)

    def rm_tmp_file(self):
        # 移除临时文件
        if self.tmp_fp:
            os.close(self.tmp_fp)
            os.remove(self.tmp_file)

    def close(self):
        logging.debug('Closing worker {}'.format(self.id))

        if self.handler:
            self.loop.remove_handler(self.fd)
            self.handler.close()

        self.chan.close()
        self.ssh.close()
        logging.info('Connection to {} lost'.format(self.dst_addr))


class IndexHandler(tornado.web.RequestHandler):
    # 处理跨域请求
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, OPTIONS')
        self.set_header('Access-Control-Allow-Headers', '*')

    # 处理跨域时的options请求
    def options(self):
        self.set_status(204)
        self.finish()

    def ssh_connect(self):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        dst_addr = f"{SERVER_IP}:{PORT}"
        logging.info('Connecting to {}'.format(dst_addr))
        try:
            ssh.connect(hostname=SERVER_IP, port=PORT, username=USER, password=PASSWORD, timeout=6)
        except socket.error:
            raise ValueError('Unable to connect to {}'.format(dst_addr))
        except paramiko.BadAuthenticationType:
            raise ValueError('Authentication failed.')
        chan = ssh.invoke_shell(term='xterm')
        chan.setblocking(0)
        worker = Worker(ssh, chan, dst_addr)
        IOLoop.current().call_later(DELAY, recycle, worker)
        return worker

    def get(self):
        self.render('ws.html')

    def post(self):
        worker_id = None
        cmd = None
        worker = None
        try:
            # 建立连接
            worker = self.ssh_connect()
            worker_id = worker.id
            workers[worker_id] = worker

            # 创建可执行文件
            code = get_code(self.request)
            tmp_fp, file_name = mkstemp(suffix=".py", text=True)
            with open(file_name, 'w+', encoding='u8') as file:
                file.write(code)
            worker.tmp_fp = tmp_fp
            worker.tmp_file = file_name

            cmd = f"sudo python3 {file_name};exit;\n"
            worker.cmd = cmd
            code = 0
            msg = "执行成功"
        except Exception as e:
            logging.error(traceback.format_exc())
            msg = f'执行失败\n,错误信息：{str(e)}'
            if worker and worker.tmp_file:
                os.close(worker.tmp_fp)
                os.remove(worker.tmp_file)
            code = -1
        self.write(dict(
            msg=msg,
            code=code,
            data=dict(
                id=worker_id,
                cmd=cmd
            )))


class WebsocketHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        self.loop = IOLoop.current()
        self.worker_ref = None
        super(self.__class__, self).__init__(*args, **kwargs)

    def check_origin(self, origin):
        return True

    def get_addr(self):
        ip = self.request.headers.get_list('X-Real-Ip')
        port = self.request.headers.get_list('X-Real-Port')
        addr = ':'.join(ip + port)
        if not addr:
            # addr = '{}:{}'.format(*self.stream.socket.getpeername())
            addr = f"{self.request.host}:8087"
        return addr

    def open(self):
        self.src_addr = self.get_addr()
        logging.info('Connected from {}'.format(self.src_addr))
        worker = workers.pop(self.get_argument('id'), None)
        if not worker:
            self.close(reason='Invalid worker id')
            return
        self.set_nodelay(True)
        worker.set_handler(self)
        self.worker_ref = weakref.ref(worker)
        self.loop.add_handler(worker.fd, worker, IOLoop.READ)
        worker.chan.send(worker.cmd)

    def on_message(self, message):
        logging.debug('"{}" from {}'.format(message, self.src_addr))
        worker = self.worker_ref()
        worker.data_to_dst.append(message)
        worker.on_write()

    def on_close(self):
        logging.info('Disconnected from {}'.format(self.src_addr))
        worker = self.worker_ref() if self.worker_ref else None
        if worker:
            worker.rm_tmp_file()
            worker.close()


def wss_server():
    settings = {
        'template_path': os.path.join(base_dir, 'templates'),
        'static_path': os.path.join(base_dir, 'static'),
        'cookie_secret': uuid.uuid1().hex,
        'xsrf_cookies': False,
        'debug': True
    }

    handlers = [
        (r'/robot', IndexHandler),
        (r'/ws', WebsocketHandler)
    ]

    parse_command_line()
    app = tornado.web.Application(handlers, **settings)
    app.listen(port=SERVER_PORT, address=SERVER_IP)
    logging.info('Listening on {}:{}'.format(options.address, options.port))
    IOLoop.current().start()