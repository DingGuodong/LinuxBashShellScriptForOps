#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:performanceOps.py
User:               Guodong
Create Date:        2016/9/21
Create Time:        18:11
 """
import psutil
import prettytable

ps_result = list()
top_lines = 10

for proc in psutil.process_iter():
    ps_result.append({'name': proc.name(), 'pid': proc.pid, 'cpu_percent': proc.cpu_percent(),
                      'memory_percent': proc.memory_percent()})

table = prettytable.PrettyTable()
table.field_names = ["No.", "Name", "Pid", "Memory percent"]
total_memory_usage = list()
for i, item in enumerate(sorted(ps_result, key=lambda x: x['memory_percent'], reverse=True)):
    if i >= top_lines:
        break
    table.add_row([i + 1, item['name'], item['pid'], format(item['memory_percent'] / 100, '.2%')])
    total_memory_usage.append(item['memory_percent'])
print table
print "Total memory is %s GB" % format(psutil.virtual_memory().total / 1024.00 / 1024 / 1024, '.2f')
print "Sum of Top %s memory percent is %s" % (i, format(sum(total_memory_usage) / 100, '.2%'))
