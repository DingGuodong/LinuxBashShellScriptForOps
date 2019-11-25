#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyProcessMonitor.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/11/25
Create Time:            14:42
Description:            A simple process monitor for the Windows platform
Long Description:       可用于定期采集电脑中运行的程序，什么时候打开的，谁打开的，什么时候关闭的，
                            比如可以监控小侄子有没有玩游戏，游戏玩了多久。/笑哭 /偷笑
                            也可以用于发现定期出来作恶的程序
                        Tips:
                            可利用Windows自带的“计划任务程序”实现定期运行或
                                在下面代码的基础上添加循环定时器（可用库：apscheduler或schedule）
References:             
Prerequisites:          pip install psutil
                        pip install pytz
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
import datetime
import os
import sqlite3

import psutil
import pytz


def show_human_readable_process_info(proc):
    print(proc.name(), proc.pid, proc.ppid(), proc.status(), proc.username(), proc.cmdline()[
        0], datetime.datetime.fromtimestamp(proc.create_time(), pytz.timezone('Asia/Shanghai')).strftime(
        '%Y-%m-%d %H:%M:%S %Z%z'), proc.memory_info().rss / 1024.0 / 1024.0, proc.cpu_percent())


def init_sqlite_database():
    """
    初始化sqlite数据库，如创建适当的表结构
        NAME             进程名称
        PID              进程PID
        PPID             进程PPID
        STATUS           进程状态
        USERNAME         用户名
        CMDLINE          命令行（不包含参数）
        CREATED          进程创建时间（进程启动时间）
        MEMORY           进程工作集（内存）
        CPU              进程占用的CPU百分比
        UPDATED          进程更新时间（注：数据库生成的时间戳一般是UTC时间戳）
        UPDATE_TIMES     进程更新次数
        REAL_STATUS      进程真实状态
    注：进程运行总时间约等于进程更新次数*脚本运行周期
    :return:
    """
    if not os.path.exists(sqlite_db_file):
        sqlite_conn = sqlite3.connect(sqlite_db_file)
        c = sqlite_conn.cursor()
        c.execute('''CREATE TABLE info
               (
                   ID               INTEGER             NOT NULL PRIMARY KEY AUTOINCREMENT,
                   NAME             CHAR(20)            NOT NULL,
                   PID              INT                 NOT NULL,
                   PPID             INT,
                   STATUS           CHAR(10),
                   USERNAME         CHAR(50),
                   CMDLINE          TEXT,
                   CREATED          TIMESTAMP,
                   MEMORY           FLOAT,
                   CPU              FLOAT,
                   UPDATED          TIMESTAMP,
                   UPDATE_TIMES     INT,
                   REAL_STATUS      BOOL
               );''')
        sqlite_conn.commit()
        sqlite_conn.close()


def insert_new_process_records():
    """
    将采集到的进程信息写入数据库，如果进程已存在（pid和name相同）则略过
    :return:
    """
    conn = sqlite3.connect(sqlite_db_file)
    for process in psutil.process_iter():
        c = conn.cursor()
        current_process_name = process.name()
        current_process_pid = process.pid

        result = c.execute('''
                SELECT NAME, PID from info WHERE NAME="{name}" and PID={pid};
                '''.format(name=current_process_name, pid=current_process_pid)
                           )
        if (current_process_name, current_process_pid) == result.fetchone():
            continue

        try:
            c.execute(
                '''INSERT INTO info
                (
                    "NAME",
                    "PID",
                    "PPID",
                    "STATUS",
                    "USERNAME",
                    "CMDLINE",
                    "CREATED",
                    "MEMORY",
                    "CPU",
                    "UPDATED",
                    "UPDATE_TIMES",
                    "REAL_STATUS")
                 VALUES
                 (
                     "{name}",
                     {pid},
                     {ppid},
                     "{status}",
                     "{username}",
                     "{cmdline}",
                     {created},
                     {memory},
                     {cpu},
                     CURRENT_TIMESTAMP,
                     1,
                     1
                 );'''.format(
                    name=current_process_name,
                    pid=current_process_pid,
                    ppid=process.ppid(),
                    status=process.status(),
                    username=process.username(),
                    cmdline=process.cmdline()[0] if len(process.cmdline()) > 0 else "",
                    created=process.create_time(),
                    memory=process.memory_info().rss,
                    cpu=process.cpu_percent()
                ))
            conn.commit()
        except psutil.AccessDenied:
            pass
    conn.close()


def is_process_exist(pid, name):
    # type: (int, str) -> bool
    """
    判断进程是否在运行中（存在）
    :param pid: process pid
    :param name: process name
    :return:
    """
    try:
        name_by_pid = psutil.Process(pid=pid).name()
        if name == name_by_pid:
            return True
        else:
            return False
    except psutil.NoSuchProcess:
        return False


def update_process_record():
    """
    更新数据库中已有的进程的信息
    1. 对于数据库中已有的进程判断是否是运行中，
        运行中，则更新进程的信息（更新时间（UPDATED），更新次数（UPDATE_TIMES），进程真实状态（REAL_STATUS））
        没有运行，则将进程真实状态（REAL_STATUS）标记为0

    :return:
    """
    conn = sqlite3.connect(sqlite_db_file)
    c = conn.cursor()
    result = c.execute('''
        SELECT pid, name FROM info WHERE real_status is 1;
    ''')
    for res in result.fetchall():
        current_process_pid, current_process_name = res[0], res[1]
        if is_process_exist(pid=current_process_pid, name=current_process_name):
            c.execute('''
                    UPDATE info 
                    SET UPDATE_TIMES=UPDATE_TIMES+1, UPDATED=CURRENT_TIMESTAMP, REAL_STATUS=1 
                    WHERE id=(SELECT id FROM info WHERE pid={pid} AND name="{name}")
                '''.format(pid=current_process_pid, name=current_process_name))
        else:
            c.execute('''
                    UPDATE info SET REAL_STATUS=0
                    WHERE id=(SELECT id FROM info WHERE pid={pid} AND name="{name}")
                '''.format(pid=current_process_pid, name=current_process_name))

    conn.commit()
    conn.close()


if __name__ == '__main__':
    sqlite_db_file = "process.db.sqlite3"
    init_sqlite_database()
    insert_new_process_records()
    update_process_record()
