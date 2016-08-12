#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:odbp_sendMessage_usage_example.py
User:               Guodong
Create Date:        2016/8/12
Create Time:        16:45
 """
import odbp_sendMessage

msg = odbp_sendMessage.WeiXinSendMsgClass()
msg.send("dingguodong", "Python 大魔王！")
