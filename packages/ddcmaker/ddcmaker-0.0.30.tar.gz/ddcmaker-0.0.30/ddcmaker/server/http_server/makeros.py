import json
import subprocess
import time
import os
import base64
from ddcmaker.server.http_server.code_check.code_safety import settime
from tempfile import mkstemp


def linux_maker(data, settime=settime):
    res = {"msg": "", "code": 1, "data": {}}

    # print(data)
    # data = json.loads(request)
    # print(type(data))

    data = str(data, encoding="u8").replace('    ', '')
    # print(data)
    if not data:
        res.update(err="代码不能为空，请输入代码。")
        return json.dumps(res)
    try:
        code = eval(data)["code"]
        code = base64.b64decode(code)
        code = str(code, encoding="u8")
        # print("取出传入的值", code)
    except Exception as e:
        # print(e)
        res.update(err=e)
        # print(type(res))
        return json.dumps(res)
    if code == "":
        res.update(err="代码不能为空，请输入代码。")
        # print(type(res))
        return json.dumps(res)

    tmp_fp, file_name = mkstemp(suffix=".py", text=True)
    from ddcmaker.server.http_server.code_check.code_safety import check_mode
    offline_running = check_mode(code[:50])
    with open(file_name, "w+", encoding="u8") as f:
        # print(type(code))
        f.write(code)
        f.close()

    cmd = "python3  " + file_name
    if not offline_running:
        from ddcmaker.server.http_server.code_check.code_safety import check_package
        res = check_package(res, file_name)
        if res["code"] == 555:
            return json.dumps(res)
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        except Exception as e:
            res.update(err=e)
            return json.dumps(res)
        try:
            out, err = proc.communicate(timeout=settime)
        except Exception as e:
            print("捕捉错误", e)
            proc.kill()
            from ddcmaker.basic.abc import get_maker_name
            from ddcmaker.server.http_server.pro_name_list import kill_ai_pro_list
            makername = get_maker_name()
            kill_ai_pro_list()
            # from ddcmaker.public import killprocess
            # killprocess.kill_process(pyname)
            res.update(code=233, msg="超时主动中断",
                       err="运行超时，中断" + makername + "操作，" + makername + "一次最长允许运行动作" + str(settime) + "秒")
        else:
            if err:
                res.update(err=err.decode("u8"))
            else:
                res.update(code=0, msg="执行成功", data={
                    "moduleData": [out.decode("u8")],
                    "printData": out.decode("u8"),
                })
        finally:
            os.close(tmp_fp)
            os.remove(file_name)
        print(res)
        return json.dumps(res)
    else:
        print("当前设备脱机运行，不再受到平台约束！")
        res.update(code=777, msg="高级模式脱机运行",
                   err="警告：当前模式为高级模式，设备将执行脱机命令，设备将不会超时中断动作！\n请谨慎使用，仅限工程师调试使用！！\n若要停止，请等待设备运行结束或者关闭设备电源")

        def tuojires():
            try:
                proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                proc.communicate(timeout=1000)
            except Exception as error:
                print(error)
            finally:
                os.remove(file_name)

        import threading
        th1 = threading.Thread(target=tuojires)
        th1.setDaemon(True)
        th1.start()
        return json.dumps(res)


def windows_maker(data):
    res = {"msg": "", "code": 1, "data": {}}
    # print(data)
    # data = json.loads(request)
    # print(type(data))

    data = str(data, encoding="u8").replace('    ', '')
    print(data)
    try:
        code = eval(data)["code"]
        code = base64.b64decode(code)
        code = str(code, encoding="u8")
        print("取出传入的值", code)
    except Exception as e:
        print(e)
        res.update(err=e)
        # print(type(res))
        return json.dumps(res)
    if code == "":
        res.update(err="代码不能为空，请输入代码。")
        # print(type(res))
        return json.dumps(res)
    if code != "" and "stop" in code[:15]:
        # 终止机器人运动的函数
        print("终止机器人运动")
        res.update(code=666, msg="动作已经终止", err="前端请求主动中断动作，杀死运行进程。")
        return json.dumps(res)
    # fp, file_name = mkstemp(suffix=".py", text=True)
    file_name = str(time.time())[-6:] + ".py"
    print(file_name)
    with open(file_name, "w+", encoding="u8") as f:
        # print(type(code))
        f.write(code)
        f.close()

    cmd = "python " + file_name
    print(cmd)
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="u8", shell=False)
    except Exception as e:
        print(e)
        res.update(err=e)
        # print(type(res))
        return json.dumps(res)
    try:
        out, err = proc.communicate(timeout=60)
    except subprocess.TimeoutExpired:
        proc.kill()
        res.update(code=233, msg="机器运行超时，中断机器人链接。")
    else:
        if err:
            res.update(err=err)
        else:
            res.update(code=0, data={
                "moduleData": [out],
                "printData": out,
            })
    finally:
        os.remove(file_name)
    return json.dumps(res)


def Mac_maker():
    res = {"msg": "", "code": 1, "data": {}}
    res.update(err="当前系统为Mac,暂时不支持此系统！")
    return json.dumps(res)


def other_maker():
    res = {"msg": "", "code": 1, "data": {}}
    res.update(err="你这是啥系统呀，暂时不支持哟！")
    return json.dumps(res)
