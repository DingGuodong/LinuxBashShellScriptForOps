#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:use-pandas-to-analyze-nginx-log.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/11/7
Create Time:            10:42
Description:            using pandas to get clients which connected to nginx
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

import pandas as pd

# [syntax](https://www.pypandas.cn/docs/user_guide/io.html#csv-%E6%96%87%E6%9C%AC%E6%96%87%E4%BB%B6)
# [syntax in En](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-read-csv-table)
raw_reader = pd.read_csv("netstat_anopt_20191022_prod_nginx01.txt", sep=r"\s+", iterator=True, header=None)  # 注意header

raw_df = pd.concat(raw_reader)

tcp_est_df = raw_df.iloc[:, 3:6][raw_df[5] != "LISTEN"]  # pandas按索引选择列，并选择索引为5的状态不是LISTEN的行

port_listened = [x[1] for x in raw_df[raw_df[5] == "LISTEN"][3].str.split(":")]


def is_obj_endswith_iterable(obj):
    return any(map(str(obj).endswith, port_listened))


wanted_df = tcp_est_df[map(is_obj_endswith_iterable, tcp_est_df[3])]

wanted_df["src"], wanted_df["src_port"] = wanted_df[3].str.split(":").str  # 将第3列拆成两列，分别命名为"src"和"src_port"
wanted_df["dst"], wanted_df["dst_port"] = wanted_df[4].str.split(":").str  # 将第4列拆成两列，分别命名为"dst"和"dst_port"

# 打印80端口的行
print wanted_df[wanted_df["src_port"] == "80"]

# 打印443端口连接的客户端IP的统计信息
print wanted_df[wanted_df["src_port"] == "443"]["dst"].value_counts().head(10)
