#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyHandleStdin.py
User:               Guodong
Create Date:        2017/7/11
Create Time:        10:54
Description:        example for python handle stdin, such as
                    python autoban.py < /var/log/shadowsocks.log
                    nohup tail -F /var/log/shadowsocks.log | python autoban.py >log 2>log &
References:         https://github.com/shadowsocks/shadowsocks/wiki/Ban-Brute-Force-Crackers
                    https://github.com/shadowsocks/shadowsocks/blob/master/utils/autoban.py
 """

# !/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2015 clowwindy
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.



import os
import sys
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='See README')
    parser.add_argument('-c', '--count', default=3, type=int,
                        help='with how many failure times it should be '
                             'considered as an attack')
    config = parser.parse_args()
    ips = {}
    banned = set()
    for line in sys.stdin:
        if 'can not parse header when' in line:
            ip = line.split()[-1].split(':')[-2]
            if ip not in ips:
                ips[ip] = 1
                print(ip)
                sys.stdout.flush()
            else:
                ips[ip] += 1
            if ip not in banned and ips[ip] >= config.count:
                banned.add(ip)
                cmd = 'iptables -A INPUT -s %s -j DROP' % ip
                print(cmd, file=sys.stderr)
                sys.stderr.flush()
                os.system(cmd)
