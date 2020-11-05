#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:get-content-type-01.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/11/5
Create Time:            16:23
Description:            get wanted content using regex
Long Description:

题目来源：http://bbs.chinaunix.net/thread-4316570-1-1.html

某个更新日志，会以V数字做为版本号，每次取出最新版本号的更新内容（只以Vxx为准）
现在问题是这个版本号不一定是按顺序的，最新版本可能在中间，也可能在第一段或者最后一段。

需求取出：
   V0.4-张三-2020/11/4 12：00
   去掉发邮件步骤
   调整流程（由并行改为串行）


原始文本示例：
   V0.1-张三-2020/11/4 14：00
   增加AAAA
   V0.2-张三-2020/11/4 12：00
   调整子工作流流程（由并行改为串行）
   V0.4-张三-2020/11/4 12：00
   去掉发邮件步骤
   调整流程（由并行改为串行）
   V0.3-张三-2020/11/4 12：00
   去掉发邮件步骤
   调整流程（由并行改为串行）

References:             
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
import re

in_str = '''V0.1-张三-2020/11/4 14：00
   增加AAAA
   V0.2-张三-2020/11/4 12：00
   调整子工作流流程（由并行改为串行）
   V0.4-张三-2020/11/4 12：00
   去掉发邮件步骤
   调整流程（由并行改为串行）
   V0.3-张三-2020/11/4 12：00
   去掉发邮件步骤
   调整流程（由并行改为串行）
   '''


def split_by_regex_pattern():
    # split a string and keep the separators
    # https://stackoverflow.com/questions/2136556/in-python-how-do-i-split-a-string-and-keep-the-separators
    pattern = re.compile(r"([Vv]\d\.\d.*?\n)")
    res = pattern.split(in_str)
    return res


def find_versions():
    pattern = re.compile(r"([Vv]\d\.\d)")
    res = pattern.findall(in_str)  # type: list

    return [float(re.sub("[Vv]", "", x)) for x in res]


def find_latest_version():
    version_list = find_versions()
    return max(version_list)


def find_right_next_version():
    version_list = find_versions()
    latest_version_index = version_list.index(max(version_list))
    if len(version_list) > latest_version:
        right_next = version_list[latest_version_index + 1]
        return right_next


if __name__ == '__main__':
    latest_version = find_latest_version()
    right_next_version = find_right_next_version()

    split_list = split_by_regex_pattern()

    selected_version_line = ""
    for item in split_list:
        if item.strip().startswith("V" + str(latest_version)):
            selected_version_line = item
            break

    selected_version_index = split_list.index(selected_version_line)

    if right_next_version is not None:
        right_next_version_line = ""
        for item in split_list:
            if item.strip().startswith("V" + str(right_next_version)):
                right_next_version_line = item
                break

        right_next_version_index = split_list.index(right_next_version_line)

        print("".join(split_list[selected_version_index:right_next_version_index]))
    else:
        print("".join(split_list[selected_version_index:]))
