#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:usernameCapitalize.py
User:               Guodong
Create Date:        2016/10/14
Create Time:        11:07
 """


# using map/reduce to capitalize a username

def usernameFormat(username):
    return str(username).lower().capitalize()


def usernameComb(usernamePart1, usernamePartN):
    return (str(usernamePart1) + " " + str(usernamePartN)).strip()


print reduce(usernameComb, map(usernameFormat, ['linus', 'benedict', 'TORVALDS']))
