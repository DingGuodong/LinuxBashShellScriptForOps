#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:check-task-scheduler-status.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/8/19
Create Time:            10:59
Description:            check task scheduler status
Long Description:       
References:             [Python check for Completed and failed Task Windows scheduler](https://stackoverflow.com/questions/36634214/python-check-for-completed-and-failed-task-windows-scheduler)
Prerequisites:          pip install pywin32
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

import os

import pywintypes
import win32com.client

TASK_ENUM_HIDDEN = 1
TASK_STATE = {0: 'Unknown',
              1: 'Disabled',
              2: 'Queued',
              3: 'Ready',
              4: 'Running'}


def get_all_tasks():
    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()

    n = 0
    folders = [scheduler.GetFolder('\\')]
    while folders:
        folder = folders.pop(0)
        folders += list(folder.GetFolders(0))
        tasks = list(folder.GetTasks(TASK_ENUM_HIDDEN))
        n += len(tasks)
        for task in tasks:
            settings = task.Definition.Settings
            print('Path       : %s' % task.Path)
            print('Hidden     : %s' % settings.Hidden)
            print('State      : %s' % TASK_STATE[task.State])
            print('Last Run   : %s' % task.LastRunTime)
            print('Last Result: %s\n' % task.LastTaskResult)
    print('Listed %d tasks.' % n)


def _walk_tasks_internal(top, topdown, onerror, flags):
    try:
        folders = list(top.GetFolders(0))
        tasks = list(top.GetTasks(flags))
    except pywintypes.com_error as error:
        if onerror is not None:
            onerror(error)
        return

    if not topdown:
        for d in folders:
            for entry in _walk_tasks_internal(d, topdown, onerror, flags):
                yield entry

    yield top, folders, tasks

    if topdown:
        for d in folders:
            for entry in _walk_tasks_internal(d, topdown, onerror, flags):
                yield entry


def walk_tasks(top, topdown=True, onerror=None, include_hidden=True,
               server_name=None, user=None, domain=None, password=None):
    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect(server_name, user, domain, password)
    if isinstance(top, bytes):
        if hasattr(os, 'fsdecode'):
            top = os.fsdecode(top)
        else:
            top = top.decode('mbcs')
    if u'/' in top:
        top = top.replace(u'/', u'\\')
    include_hidden = TASK_ENUM_HIDDEN if include_hidden else 0
    try:
        top = scheduler.GetFolder(top)
    except pywintypes.com_error as error:
        if onerror is not None:
            onerror(error)
        return
    for entry in _walk_tasks_internal(top, topdown, onerror, include_hidden):
        yield entry


def call_walk_tasks():
    n = 0
    for folder, subfolders, tasks in walk_tasks('/'):
        n += len(tasks)
        for task in tasks:
            settings = task.Definition.Settings
            print('Path       : %s' % task.Path)
            print('Hidden     : %s' % settings.Hidden)
            print('State      : %s' % TASK_STATE[task.State])
            print('Last Run   : %s' % task.LastRunTime)
            print('Last Result: %s\n' % task.LastTaskResult)
    print('Listed %d tasks.' % n)


if __name__ == '__main__':
    for top_path, dirs, task_names in walk_tasks('/'):
        for item in task_names:
            if str(item) == r'\clean-old-backup-files-v2-task-exported':
                # UserParameter=com.check.python.microsoft.task.status[*],C:\check-task-scheduler-status.py
                print(item.LastTaskResult)  # for zabbix agent
                exit(0)

    print(1)
    exit(1)
