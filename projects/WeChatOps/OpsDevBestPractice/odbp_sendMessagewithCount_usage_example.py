#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:odbp_sendMessagewithCount_usage_example.py
User:               Guodong
Create Date:        2016/8/16
Create Time:        11:54
 """
import odbp_sendMessagewithCount

msg = odbp_sendMessagewithCount.WeiXinSendMsgClass()
msg.send("dingguodong", "Python 大魔王！")
