#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:getOpenedPortsOnRemoteHost.py
User:               Guodong
Create Date:        2017/7/12
Create Time:        20:20
Description:        A utility to scan which ports are used on IP host you input.
References:         https://docs.python.org/2/library/threading.html
                    https://docs.python.org/2/library/string.html#formatspec

Example output:
    A utility to scan which ports are used on IP host.
    Input the ip you want to scan: 127.0.0.1
    Scanning ip 127.0.0.1 ...
    Port opened: [53, 135, 445, 902, 912, 953, 1536, 1537, 1538, 1540, 1544, 1572, 1760, 1761, 4300, ...
    Finished with 24.4770 seconds.

 """
import socket
import threading
import time

timeout = 3
truncate_line = False  # truncate line when line is too long


def try_connect(ip, port):
    port = int(port)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        return_code = s.connect_ex((ip, port))
        if return_code == 0:
            with lock:  # use lock here is not essential
                port_opened_list.append(port)
        s.close()
    except Exception as _:
        del _
        pass


def scan_port(ip):
    try:
        print("Scanning ip {0} ...".format(ip))
        start_time = time.time()
        for thread in [threading.Thread(target=try_connect, args=(ip, port), ) for port in range(1, 65535)]:
            thread.setDaemon(True)
            thread.start()
        thread.join()

        if truncate_line:  # truncate line when line is too long
            if len(port_opened_list) <= 10:  # 10 items per line
                print("Port opened: %s" % sorted(port_opened_list))
            else:
                print("Port opened:\n", "\n".join(
                    ["    " + str(port_opened_list[i:i + 10]) for i in range(0, len(port_opened_list), 10)]))
        else:
            print("Port opened: %s" % sorted(port_opened_list))

        print("Finished with {seconds:.4f} seconds.".format(seconds=(time.time() - start_time)))
    except Exception as e:
        print(e, e.args, e.message, end=' ')


if __name__ == '__main__':
    print("A utility to scan which ports are used on IP host.")
    host = input('Input the ip you want to scan: ')
    port_opened_list = list()
    lock = threading.Lock()
    scan_port(host)
