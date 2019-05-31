#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:emptyRecycleBin.py
User:               Guodong
Create Date:        2017/4/25
Create Time:        9:53
 """

import winshell

recycle_bin = winshell.recycle_bin()

if len(list(recycle_bin.items())) != 0:
    print("回收站里的内容有：\n", list(recycle_bin.items()))
    try:
        recycle_bin.empty(confirm=False, show_progress=False, sound=False)
    except Exception as e:
        print(e)
else:
    print("回收站已经是空的了。")
