from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from urllib import request
from config import config
import json
import smtplib
import time

# 主播之前的状态
pervStreamState = {}


def loginEmailServer(option):
    # 登录邮箱
    server = smtplib.SMTP_SSL(option["host"], option["port"])
    # server.set_debuglevel(1)
    server.login(option["auth"]["user"], option["auth"]["pass"])
    return server


def assembleEmailMessage(content, title="某主播", fromAddr=config["sender"], toAddr="406386343@qq.com"):
    # 组装邮件信息
    msg = MIMEText(content, "plain", "utf-8")
    msg["From"] = formataddr(["斗鱼开播提醒", fromAddr], "utf-8")
    msg["To"] = formataddr(["收件人昵称", toAddr], "utf-8")
    msg["Subject"] = title
    return msg


def sendMail(server, msg, fromAddr=config["sender"], toAddr=config["receiver"]):
    # 发送邮件
    server.sendmail(fromAddr, toAddr, msg.as_string())


def isOnStream(roomId):
    # 判断是否正在直播
    with request.urlopen(config["douyu"]["roomApi"]+roomId) as f:
        # 转为json对象格式
        data = json.loads(f.read())
        # 判断是否开播 1=>开播,2=>关播
        if data["data"]["room_status"] == str(1):
            return True, data["data"]
        else:
            return False, data["data"]


def checkStateByRoomId(roomId):
    isOnStreamFlag, roomData = isOnStream(roomId)
    if isOnStreamFlag:
        print("{}开播,开播时间 {}".format(
            roomData["owner_name"], roomData["start_time"]))
        msg = assembleEmailMessage(
            roomData["room_name"]+roomData["start_time"], roomData["owner_name"])

        if not pervStreamState.get(roomData["owner_name"]):
            sendMail(server, msg)
            # 保存状态
            pervStreamState[roomData["owner_name"]] = True
        else:
            print("{}直播间状态未改变,不发送邮件".format(roomData["owner_name"]))
    else:
        pervStreamState[roomData["owner_name"]] = False
        print("{}未开播,上次开播时间 {}".format(
            roomData["owner_name"], roomData["start_time"]))


def monitor(server, config):
    # 监听直播间状态
    # TODO: perf: 同步网络请求,改为异步
    try:
        [checkStateByRoomId(roomId) for roomId in config["douyu"]["roomId"]]
    except Exception as e:
        print(e)
    finally:
        # print(pervStreamState)
        time.sleep(config["delayTime"])
        # 重复监听
        monitor(server, config)


# 主函数
if __name__ == "__main__":
    server = loginEmailServer(config["transporter"])
    monitor(server, config)
