#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:ping-nodes-with-thread-and-save-results.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/1/19
Create Time:            11:07
Description:            ping nodes with multi-threading and save results into a file
Long Description:       
References:             
Prerequisites:          pip install ping
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
import time
from multiprocessing.pool import ThreadPool
from threading import Lock

import ping


def is_node_alive_with_icmp_ping(ip):
    percent_lost, mrtt, artt = ping.quiet_ping(ip, timeout=1, count=1, psize=64)
    if percent_lost == 0:
        return True
    else:
        lock.acquire()
        with open(dbf, 'a') as fp:
            fp.write(ip + " " + now + "\n" * 2)
        lock.release()
        return False


if __name__ == '__main__':
    nodes_list = [
        '192.168.88.3',
        '192.168.88.12',
        '192.168.88.4',
        '192.168.88.8',
        '192.168.88.15',
    ]

    dbf = "ping_nodes_result.txt"
    now = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

    with open(dbf, 'w') as fp_init:
        fp_init.write(now + "\n")

    lock = Lock()

    try:
        while True:
            processes_count = 254 if len(nodes_list) > 254 else len(nodes_list)
            pool = ThreadPool(processes=processes_count)
            pool.map(is_node_alive_with_icmp_ping, nodes_list)
            pool.close()
            pool.join()
            time.sleep(1)
    except KeyboardInterrupt:
        print("canceled")
