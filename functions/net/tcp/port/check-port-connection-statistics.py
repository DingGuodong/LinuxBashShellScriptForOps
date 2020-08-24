#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:check-port-connection-statistics.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/5/21
Create Time:            16:00
Description:            keep checking port connection and timestamp, writing statistics into a log file
Long Description:       持续查询某个端口如22的网络连接情况，将连接信息+时间戳写入文件，要求链接信息中的IP不重复。
                        应用场景：
                            1. 对外攻击，查被攻击对象；遭受攻击，查攻击对象
References:             
Prerequisites:          pip install psutil
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
import psutil
import time

# from collections import namedtuple
# addr = namedtuple('addr', ['ip', 'port'])
# from psutil._common import addr

statistics_file = "statistics.txt"
port = 993
max_records = 1000  # max records size

wanted_res_list = list()
remote_addr_set = set()
try:
    while 1:
        if len(wanted_res_list) >= max_records:
            break

        now = time.time()
        sconn_list = psutil.net_connections(kind='tcp')

        # my_sconn_list = [sconn for sconn in sconn_list if
        #                  isinstance(sconn.raddr,
        #                             addr) and sconn.raddr.port == port and sconn.status == 'ESTABLISHED']

        # see: https://github.com/giampaolo/psutil/issues/1513
        my_sconn_list = [sconn for sconn in sconn_list if
                         sconn.status == 'ESTABLISHED' and sconn.raddr.port == port]

        for my_sconn in my_sconn_list:
            ip = my_sconn.raddr.ip
            if ip not in remote_addr_set:
                remote_addr_set.add(ip)
                wanted_res_list.append((now, my_sconn))

                print(wanted_res_list)
                with open(statistics_file, 'w') as fp:
                    fp.write("\n".join([str(x) for x in wanted_res_list]))
        time.sleep(1)

except (KeyboardInterrupt, SystemExit):
    print("exited")
