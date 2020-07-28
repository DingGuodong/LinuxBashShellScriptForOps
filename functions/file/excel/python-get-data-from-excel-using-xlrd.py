#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:python-get-data-from-excel-using-xlrd.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/11/29
Create Time:            16:06
Description:            get data from Excel using xlrd
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
import xlrd
from openpyxl.utils import column_index_from_string

dest_filename = u'example.xlsx'
wanted_sheet_name = 'example_sheet_name'

wb = xlrd.open_workbook(dest_filename)

wanted_sheet = wb.sheet_by_name(wanted_sheet_name)

max_row = wanted_sheet.nrows  # get max row number
max_column = wanted_sheet.ncols  # get max column number

start_coordinate = column_index_from_string('A')  # start_colx
ends_coordinate = max_column  # end_colx

for row_index in range(max_row)[1::]:
    for row_obj in wanted_sheet.row_values(row_index, start_coordinate, ends_coordinate):
        print(row_obj),
