#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyShutitOps.py
User:               Guodong
Create Date:        2017/6/29
Create Time:        16:12

shutit: An programmable automation tool designed for complex builds
        An programmable shell-based (pexpect) automation tool designed for complex builds.
        See: http://ianmiell.github.io/shutit
see also: expect or pexpect
note: works on posix system only

 """
import shutit


def shutit_example_1():
    # use shutit for ssh
    session = shutit.create_session('bash')
    password = session.get_input('', ispass=True)
    session.login('root@10.20.0.7', user='root', password=password)
    session.send('hostname', echo=True)
    session.logout()


def shutit_example_2():
    # use shutit for ssh then command
    capacity_command = """df / | awk '{print $5}' | tail -1 | sed s/[^0-9]//"""
    session1 = shutit.create_session('bash')
    session2 = shutit.create_session('bash')
    password1 = session1.get_input('Password for server1', ispass=True)
    password2 = session2.get_input('Password for server2', ispass=True)
    session1.login('ssh you@one.example.com', user='you', password=password1)
    session2.login('ssh you@two.example.com', user='you', password=password2)
    capacity = session1.send_and_get_output(capacity_command)
    if int(capacity) < 10:
        print('RUNNING OUT OF SPACE ON server1!')
    capacity = session2.send_and_get_output(capacity_command)
    if int(capacity) < 10:
        print('RUNNING OUT OF SPACE ON server2!')
    session1.logout()
    session2.logout()


def shutit_example_3():
    # use shutit for telnet
    session = shutit.create_session('bash')
    session.send('telnet', expect='>', echo=True)
    session.send('open google.com 80', expect='scape character', echo=True)
    session.send('GET /', echo=True, check_exit=False)
    session.logout()
