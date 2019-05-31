#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyNetstatStatistic.py
User:               Guodong
Create Date:        2017/7/7
Create Time:        9:21
Description:        psutil examples - netstat
References:         https://github.com/giampaolo/psutil/blob/master/scripts/netstat.py
 """
import psutil


def print_all_conns():
    system_conns = psutil.net_connections()
    for conn in system_conns:
        print(conn)


def print_conns_by_proc_name(name):
    pid = get_process_pid_by_name(name)
    print_conns_by_proc_pid(pid)


def print_conns_by_proc_pid(pid):
    system_conns = psutil.net_connections()
    for conn in system_conns:
        if conn.pid == pid:
            print(conn)


def print_conns_by_remote_addr(addr):
    system_conns = psutil.net_connections()
    for conn in system_conns:
        if addr in conn.raddr:
            print(conn)


def get_process_name_by_pid(pid):
    pid = int(pid)
    for proc in psutil.process_iter():
        if proc.pid == pid:
            return proc.name()


def get_process_pid_by_name(name):
    for proc in psutil.process_iter():
        if name.lower() in proc.name().lower():
            return proc.pid
