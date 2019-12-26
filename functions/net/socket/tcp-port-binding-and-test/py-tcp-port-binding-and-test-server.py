#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:py-tcp-port-binding-and-test-server.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/9/5
Create Time:            14:14
Description:            python test listen on the TCP port(create a simple TCP Server)
Long Description:       
References:             https://python3-cookbook.readthedocs.io/zh_CN/latest/c12/p07_creating_thread_pool.html
Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 2.7
Topic:                  Utilities
Notes:                  test passed on Python 2.7.17 (v2.7.17:c2f86d86e6, Oct 19 2019, 21:01:17)
 """
import os
import time

from socketserver import BaseRequestHandler, ForkingTCPServer, ThreadingTCPServer


class PlainTextEchoHandler(BaseRequestHandler):
    def handle(self):
        print(time.strftime('%Y-%m-%d %H:%M:%S'), 'Got connection from', self.client_address)
        while True:

            msg = self.request.recv(8192)
            if msg in ['exit', 'quit', '\x04']:
                break
            if not msg:
                break
            print(time.strftime('%Y-%m-%d %H:%M:%S'), self.client_address, msg)
            self.request.send(msg)

    def finish(self):
        self.request.send("bye\n")
        print(time.strftime('%Y-%m-%d %H:%M:%S'), 'Disconnect from', self.client_address)


if __name__ == '__main__':
    port = 20000
    ForkingTCPServer.allow_reuse_address = False
    if os.name == 'posix':
        serv = ForkingTCPServer(('', port), PlainTextEchoHandler)
    elif os.name == 'nt':
        serv = ThreadingTCPServer(('', port), PlainTextEchoHandler)
    else:
        raise OSError("system is not supported.")

    serv.allow_reuse_address = True
    serv.max_children = 2000
    print(
        time.strftime('%Y-%m-%d %H:%M:%S'),
        "port {port} is listened, try with 'telnet localhost {port}'".format(port=port)
    )
    serv.serve_forever()
