#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pySendMessageToDingTalk.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2021/3/5
Create Time:            8:50
Description:            send message to external or internal chat group of "DingTalk" App using OpenAPI
Long Description:       
References:             
Prerequisites:          pip install requests
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3
Topic:                  Utilities
 """
import hashlib
import json

import base64
import hmac

try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus

import time
import requests

DEBUG = True


def print_if_debug(value):
    if DEBUG:
        print(value)


def send_message_to_dingtalk(message):
    """
    使用钉钉群自定义机器人发送消息到钉钉群的步骤：
        前提：注册企业微信，目前无需企业实名认证
        1. 创建钉钉群聊（至少1个人，可以添加无关人再删除无关人达到至少1人的情况），使用PC端登录打开群聊，添加机器人
        2. 建议使用“加签”安全设置，记录下签名密钥，如：SECc10***dc2
        3. 创建完成后，记录好webhook地址，如：https://oapi.dingtalk.com/robot/send?access_token=40d***c37
        4. webhook地址中有access_token，后续会使用到。
        参考文档：[自定义机器人接入](https://developers.dingtalk.com/document/app/custom-robot-access)

    :param message: str
    :type message:
    :return: status code
    :rtype: bool
    """

    timestamp = str(int(round(time.time() * 1000)))
    secret = 'SECc10***dc2'
    secret_enc = secret.encode("utf-8")
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode("utf-8")
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = quote_plus(base64.b64encode(hmac_code))

    url = "https://oapi.dingtalk.com/robot/send"

    querystring = {
        "access_token": '40d***c37',
        "timestamp": timestamp,
        "sign": sign
    }

    payload_type_markdown = {
        "msgtype": "markdown",
        "markdown": {
            "title": "需要关注的消息",
            "text": "#### 发现可能需要注意的消息\n{message}".format(message=message),
        },
        "at": {
            "atMobiles": ["1***2", ],
            "isAtAll": False
        }
    }

    payload = payload_type_markdown

    headers = {
        'content-type': "application/json",
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers, params=querystring)

    result_string = response.text
    result_dict = json.loads(result_string)
    if result_dict["errcode"] == 0:
        print_if_debug("send ok")
        print_if_debug(json.dumps(result_dict, indent=4))
    else:
        print_if_debug("send failed")
        print_if_debug(json.dumps(result_dict, indent=4))

    return response.ok
