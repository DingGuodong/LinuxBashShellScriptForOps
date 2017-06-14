#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyStartWinApps.py
User:               Guodong
Create Date:        2017/6/7
Create Time:        16:30
 """
import win32api
import time


def get_system_encoding():
    import codecs
    import locale
    """
    The encoding of the default system locale but falls back to the given
    fallback encoding if the encoding is unsupported by python or could
    not be determined.  See tickets #10335 and #5846
    """
    try:
        encoding = locale.getdefaultlocale()[1] or 'ascii'
        codecs.lookup(encoding)
    except Exception:
        encoding = 'ascii'
    return encoding


DEFAULT_LOCALE_ENCODING = get_system_encoding()

'''
# standard user
win32api.ShellExecute(0, 'open', 'notepad.exe', '', '', 1)
# administrative user
win32api.ShellExecute(0, 'runas', 'notepad.exe', '', '', 1)
'''

run_app_list = [
    "C:\Program Files (x86)\Tencent\QQ\Bin\QQScLauncher.exe",
    "C:\Program Files (x86)\Tencent\WeChat\WeChat.exe",
    "C:\Program Files\Sublime Text 2\sublime_text.exe",
    "C:\Program Files\Everything\Everything.exe",
    "C:\Program Files (x86)\NetSarang\Xmanager Enterprise 4\Xshell.exe",
    "C:\Program Files (x86)\Evernote\Evernote\Evernote.exe",
    "C:\Program Files (x86)\Skype\Phone\Skype.exe",
    r'C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE',
    "C:\Users\Guodong\Desktop\XX-Net-3.2.8\start.vbs"
]

win32api.ShellExecute(0, 'open', r'C:\Windows\system32\taskmgr.exe', '/7', '', 1)

win32api.ShellExecute(0, 'open', r'C:\Windows\explorer.exe',
                      r'D:\C盘桌面未整理\EBT\admin-playbook'.decode('utf-8').encode(DEFAULT_LOCALE_ENCODING), '', 1)

win32api.ShellExecute(0, 'open', r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
                      r'D:\C盘桌面未整理\EBT\20170508-EBT-Chris丁国栋-2017年周报.xlsx'.decode('utf-8').encode(
                          DEFAULT_LOCALE_ENCODING), '', 1)

try:
    for app in run_app_list:
        win32api.ShellExecute(0, 'open', app, '', '', 1)
        time.sleep(2)
except Exception as e:
    print e
    for item in list(e):
        if isinstance(item, str):
            print item.decode(DEFAULT_LOCALE_ENCODING),
        else:
            print item,
