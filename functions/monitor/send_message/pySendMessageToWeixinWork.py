#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pySendMessageToWeixinWork.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2021/3/5
Create Time:            8:49
Description:            send message to internal chat group of "WeiXin Work" App using OpenAPI
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
import json

import requests

DEBUG = True


def print_if_debug(value):
    if DEBUG:
        print(value)


def send_message_to_work_weixin(message):
    """
    使用企业微信群机器人发送消息到企业内部群的步骤：
        前提：注册企业微信，目前无需企业实名认证
        1. 创建企业微信内部群聊，
        2. 添加群机器人，记录下Webhook地址即可
        注意：企业微信群聊机器人只能用在企业微信内部群聊，不能添加到外部群聊
        配置参考：[如何配置群机器人](https://work.weixin.qq.com/help?person_id=1&doc_id=13376&helpType=undefined)

    :param message:
    :type message: str
    :return:
    :rtype: bool
    """
    url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send"

    querystring = {
        "key": 'ca9***5b6',
    }

    payload_type_markdown = {
        "msgtype": "markdown",
        "markdown": {
            "content": "#### 发现可能需要注意的消息\n{message}".format(message=message)
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
