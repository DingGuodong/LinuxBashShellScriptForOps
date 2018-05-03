#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyCheckIDCardNumber.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/5/3
Create Time:            11:55
Description:            中华人民共和国公民身份号码校验码计算方法, verify the validity of id card number
Long Description:       中华人民共和国公民身份号码是中华人民共和国为中国大陆每个公民从出生之日起编定的唯一的、
                        终身不变的身份代码，在中华人民共和国公民办理涉及政治、经济、社会生活等权益事务方面广泛使用。
                        中华人民共和国国家标准GB 11643-1999《公民身份号码》中规定：公民身份号码是特征组合码，
                        由十七位数字本体码和一位校验码组成。

                        最后一位是校验码，这里采用的是ISO 7064:1983,MOD 11-2校验码系统。校验码为一位数，
                        但如果最后采用校验码系统计算的校验码是“10”，碍于身份证号码为18位的规定，
                        则以“X”代替校验码“10”。

                        [应用]
                        标记在中华人民共和国居民身份证上和所配套的数据库中。（因此，1999年后“居民身份证号”就是“公民身份号码”）
                        标记在居民户口簿上和所配套的数据库中。
                        标记在中华人民共和国机动车驾驶证上和所配套的数据库中。
                        标记在中华人民共和国残疾人证上和所配套的数据库中。

References:             https://zh.wikipedia.org/wiki/中华人民共和国公民身份号码
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


def check_id_number(number):
    """
    check if id card number is a valid
    :param number: id card number
    :type number: str
    :return: bool
    """
    number = number.lower()
    sums = 0
    for index, value in enumerate(('x' + number[:-1:])):
        if index >= 1:
            sums += int(value) * ((2 ** (18 - index)) % 11)
            # sums += int(value) * ((1 << (18 - index)) % 11)
            # print(index, value, (2 ** (18 - index)) % 11)
    last_number = (12 - (sums % 11)) % 11
    if last_number < 10:
        return str(last_number) == number[-1]
    else:
        return 'x' == number[-1]


def check_id_number1(number):
    """
    check if id card number is a valid
    :param number: id card number
    :type number: str
    :return: bool
    """
    number = number.lower()
    sums = 0
    for index, value in enumerate(number[:-1:], start=1):
        sums += int(value) * ((2 ** (18 - index)) % 11)
        # sums += int(value) * ((1 << (18 - index)) % 11)
        # print(index, value, (2 ** (18 - index)) % 11)
    last_number = (12 - (sums % 11)) % 11
    if last_number < 10:
        return str(last_number) == number[-1]
    else:
        return 'x' == number[-1]


def check_id_number2(number):
    """
    check if id card number is a valid
    :param number: id card number
    :type number: str
    :return: bool
    """
    number = number.lower()
    sums = 0
    for index, value in enumerate(number[::-1]):
        if index >= 1:
            sums += int(value) * ((2 ** index) % 11)
            # sums += int(value) * ((1 << index) % 11)
            # print(index, value, (2 ** index) % 11)
    last_number = (12 - (sums % 11)) % 11
    if last_number < 10:
        return str(last_number) == number[-1]
    else:
        return 'x' == number[-1]


def check_id_number3(number):
    """
    check if id card number is a valid
    :param number: id card number
    :type number: str
    :return: bool
    """
    number = number.lower()
    sums = 0
    for index, value in enumerate(number[::-1][1::], start=1):
        sums += int(value) * ((2 ** index) % 11)
        # sums += int(value) * ((1 << index) % 11)
        # print(index, value, (2 ** index) % 11)
    last_number = (12 - (sums % 11)) % 11
    if last_number < 10:
        return str(last_number) == number[-1]

    else:
        return 'x' == number[-1]


if __name__ == '__main__':
    print(check_id_number('370284199001123321'))
    print(check_id_number1('370284199001123321'))
    print(check_id_number2('370284199001123321'))
    print(check_id_number3('370284199001123321'))

    print(check_id_number('21130219970323340X'))
    print(check_id_number1('21130219970323340X'))
    print(check_id_number2('21130219970323340X'))
    print(check_id_number3('21130219970323340X'))
