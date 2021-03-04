#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pySendMessageByDingTalk.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/11/20
Create Time:            11:03
Description:            send alter message to somebody over DingTalk(Ali DingDing)
Long Description:

    使用钉钉群自定义机器人发送消息到钉钉群的步骤：
        创建钉钉群聊（至少1个人，可以添加无关人再删除无关人达到至少1人的情况），使用PC端登录打开群聊，添加机器人
        建议使用“加签”安全设置，记录下签名密钥，如：SECc10***dc2
        参考文档：[自定义机器人接入](https://developers.dingtalk.com/document/app/custom-robot-access)
        创建完成后，记录好webhook地址，如：https://oapi.dingtalk.com/robot/send?access_token=40d654***c37
        webhook地址中有access_token，后续会使用到。

References:             https://open-doc.dingtalk.com/docs/doc.htm?spm=a219a.7629140.0.0.karFPe&treeId=257&articleId=105735&docType=1
Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 2.6
Programming Language:   Python :: 2.7
Topic:                  Utilities
 """
import json
import sys

import requests


def usage():
    print("""
    Function: send email to somebody using smtp protocol
    Usage: python %s <mailto> <subject> <message body>
    Zabbix setting: 'Administration' -> 'Media types' 
                    https://hostname/zabbix.php?action=mediatype.edit&mediatypeid=4
                    Script parameters: {ALERT.SENDTO} {ALERT.SUBJECT} {ALERT.MESSAGE}
    Example: python %s "admin@example.domain" "Test email from Python" "Python rules them all!"
""" % (__file__, sys.argv[0]))
    sys.exit(0)


def send_message(access_token, title, content, mobile, enable_at_all=False):
    url = "https://oapi.dingtalk.com/robot/send"

    querystring = {"access_token": access_token}

    payload_type_text = {
        "msgtype": "text",
        "text": {
            "content": content
        },
        "at": {
            "atMobiles": mobile.strip().split(" "),
            "isAtAll": enable_at_all
        }
    }

    payload_type_markdown = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": "### {title}\n".format(title=title) +
                    content +
                    "\n"
        },
        "at": {
            "atMobiles": mobile.strip().split(" "),
            "isAtAll": enable_at_all
        }
    }

    payload = payload_type_markdown
    del payload_type_text

    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
    }

    response = requests.request("POST", url, data=json.dumps(payload), headers=headers, params=querystring)

    result_string = response.text
    result_dict = json.loads(result_string)
    if result_dict["errcode"] == 0:
        print("send ok")
        print(json.dumps(result_dict, indent=4))
    else:
        print("send failed")
        print(json.dumps(result_dict, indent=4))


if __name__ == '__main__':
    token = "35c6fc4a5bf7916ab3e74ac497c0fcc0df57877940a7a1f0ebec1a150d7635b2"

    argv_length = len(sys.argv)
    if not (argv_length == 1 or argv_length == 4):
        print("bad call")
        usage()
    if argv_length == 1:
        subject = "Test Message"
        message = "Test message sent by Python over DingTalk"
        phone_number = '183xxxx1212'  # if there are more than one phone number to at, use space spilt them
        at_all = False
    else:
        phone_number = sys.argv[1]
        subject = sys.argv[2]
        message = sys.argv[3]

    send_message(access_token=token, mobile=phone_number, title=subject, content=message, enable_at_all=False)
