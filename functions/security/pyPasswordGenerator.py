#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyPasswordGenerator.py
User:               Guodong
Create Date:        2017/8/14
Create Time:        9:35
Description:        Password Generator For Python
References:         How can I get around declaring an unused variable in a for loop?
                    https://stackoverflow.com/questions/5477134/how-can-i-get-around-declaring-an-unused-variable-in-a-for-loop
                    阿里云远程连接密码限制为6位。支持数字和大小写字母。不支持特殊字符。
 """


class PasswordGenerator(object):
    def __init__(self):
        self.strength_level_map = {
            'weak': 0,
            'norm': 1,
            'medium': 2,
            'good': 3,
        }
        self.strength_level = 0
        self.password = None

    def gen_password(self, length=6, strength_level=0):
        import os
        import random
        from random import sample
        import string

        chars_map = {
            0: string.ascii_letters + string.digits,
            1: string.ascii_letters + string.digits + '!@#$%^&*()',
            2: string.ascii_letters + string.digits + string.punctuation,
            3: string.ascii_letters + string.digits + string.printable,
        }

        chars = chars_map[strength_level]
        self.strength_level = strength_level

        random.seed = (os.urandom(1024))

        # # _ is a standard placeholder name for ignored members in a for-loop and tuple assignment, e.g.
        # # use _ as variable name,
        # # which is usually understood as "intentionally unused" (even PyLint etc. knows and respect this).
        # print ''.join(random.choice(chars) for _ in range(length))
        self.password = ''.join(sample(chars, length))
        print self.password

    def password_strength(self):
        # show password strength, weak or good
        pass


if __name__ == '__main__':
    p = PasswordGenerator()
    p.gen_password(length=6)
