#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pySshPortScanner.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/11/21
Create Time:            15:46
Description:            scan ssh port with given IP address(Test Purpose Only)
Long Description:       
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

import logging
import socket
import sys
import threading
from multiprocessing import Pool
from socket import timeout as timeoutException

import paramiko
from paramiko.ssh_exception import AuthenticationException, NoValidConnectionsError, SSHException, BadAuthenticationType


def try_connect(ip, port):
    port = int(port)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        return_code = s.connect_ex((ip, port))
        if return_code == 0:
            port_opened_list.append(port)
        s.close()
    except Exception as _:
        del _
        pass


def scan_port_alive(ip):
    # TODO(GuodongDing): run this function without limit thread number will cause high CPU usage
    # 1. using queue.Queue. Pain Point: complex, and need create threads manually
    # 2. using multiprocessing.Pool. Pain Point: can not display any kind of UI
    # 3. Others?
    try:
        for thread in [threading.Thread(target=try_connect, args=(ip, port), ) for port in xrange(1, 65535)]:
            # do NOT set thread.setDaemon(True), especially if you don't need it
            thread.start()
        thread.join()
    except Exception as e:
        print e, e.args, e.message,


def ssh_connect(port):
    username = 'root'
    password = 'not-a-passwd'

    logging.basicConfig()
    paramiko_logger = logging.getLogger("paramiko.transport")
    paramiko_logger.disabled = True

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh_client.connect(hostname=host, port=port, username=username, password=password, timeout=timeout)
    except AuthenticationException or BadAuthenticationType:
        # paramiko.ssh_exception.AuthenticationException, Authentication failed.
        # BadAuthenticationType: ('Bad authentication type', [u'publickey'])(allowed_types=[u'publickey'])
        print "port %s can be connected." % port
    except NoValidConnectionsError:
        pass
    except timeoutException:
        # socket.timeout, timed out
        pass
    except SSHException as e:
        if e.args[0] == 'Negotiation failed.':  # https://github.com/paramiko/paramiko/issues/1222
            print "port %s can be connected." % port
        pass
    finally:
        ssh_client.close()


def scan_ssh_port_alive():
    if 'win32' in sys.platform:
        try:
            for thread in [threading.Thread(target=ssh_connect, args=(port,)) for port in port_opened_list]:
                thread.start()
            thread.join()
        except Exception as e:
            print e, e.args, e.message,

    else:
        pool = Pool(4)
        pool.map(ssh_connect, port_opened_list)
        # https://docs.python.org/2/library/multiprocessing.html#windows
        # Global variables
        # Bear in mind that if code run in a child process tries to access a global variable,
        # then the value it sees (if any) may not be the same as
        # the value in the parent process at the time that Process.start was called.
        # However, global variables which are just module level constants cause no problems.


if __name__ == '__main__':
    host = '192.168.88.19'
    timeout = 2  # set timeout (in seconds) for the TCP connect

    # using a list to save opened ports
    port_opened_list = list()

    # scan ports opened
    scan_port_alive(host)
    print "port opened: ", port_opened_list

    # scan ports can be ssh
    scan_ssh_port_alive()
