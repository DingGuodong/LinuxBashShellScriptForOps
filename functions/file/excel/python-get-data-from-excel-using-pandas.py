#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:python-get-data-from-excel-using-pandas.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/11/29
Create Time:            16:11
Description:            get data from Excel using pandas
Long Description:       row read performance: pandas > xlrd > openpyxl
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

dest_filename = u'example.xlsx'
sheet_name = 'example_sheet_name'

# pandas读取Excel
df = pd.read_excel(dest_filename, sheet_name=sheet_name)  # using 'xlrd' as io engine

row_start = 2
row_end = df.shape[0]
column_start = 0
column_end = df.shape[1]

# 使用iloc读取Excel中指定的位置到df
wanted_df = df.iloc[row_start:row_end, column_start:column_end]  # __getitem__

# Iterate over DataFrame rows as namedtuples.
for row in wanted_df.itertuples():  # df.iterrows(), df.iteritems()
    print(row)

# # 将df数据写入csv，提高下次读取速度
# wanted_df.to_csv(sheet_name + ".csv", encoding='utf-8', index=False)
