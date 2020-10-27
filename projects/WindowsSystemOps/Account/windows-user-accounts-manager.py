#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:windows-user-accounts-manager.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/10/27
Create Time:            15:49
Description:            disable or enable Windows user account via WinRM remote commands
Long Description:

Enable-PSRemoting -Force
set firewall policy for TCP port 5985

References:
Prerequisites:          pip install winrm
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
import json

import winrm

with open("config.json") as fp:
    config = json.load(fp)  # type: dict
    servers = config.get("self")  # type: dict


def get_ip_with_ends(num):
    """
    get full ip address with given ip num from config.json, ip num can be fourth part or full ip, such as '3' in '192.168.1.3'
    :param num: ip
    :type num: str | int
    :return: ip
    :rtype: str
    """
    if isinstance(num, int):
        num = str(num)

    if servers is not None:
        keys_list = servers.keys()
        for item in keys_list:
            if item.endswith(num):
                return item


def get_acc_psw_with_ends(num):
    """
    get full ip address, username and password with given ip num from config.json
    :param num: ip
    :type num: str | int
    :return: ip_addr, account, password
    :rtype: tuple
    """
    if isinstance(num, int):
        num = str(num)

    ip_addr = get_ip_with_ends(num)
    account = servers[ip_addr].get("account")
    password = servers[ip_addr].get("password")
    return ip_addr, account, password


def run_powershell(target, username, password, script):
    """
    run remote command with WinRM
    :param target: hostname or ip address
    :type target: str
    :param username:
    :type username: str
    :param password:
    :type password: str
    :param script: powershell commands or scripts
    :type script: str
    :return: None
    :rtype: None
    """
    shell = winrm.Session(target, auth=(username, password), transport="ntlm")
    rs = shell.run_ps(script)
    print rs.status_code, rs.std_out


def disable_account(server, name):
    """
    disable user account
    :param server:hostname or ip address
    :type server:str | int
    :param name: user account name
    :type name:str
    :return:None
    :rtype:None
    """
    ip, user, psw = get_acc_psw_with_ends(server)
    biz_name = "company."
    if biz_name not in name:
        name = biz_name + name
    script = 'NET USER {name} /ACTIVE:NO'.format(name=name)
    run_powershell(ip, user, psw, script)


def enable_account(server, name):
    """
    enable user account
    :param server:hostname or ip address
    :type server:str | int
    :param name: user account name
    :type name:str
    :return:None
    :rtype:None
    """
    ip, user, psw = get_acc_psw_with_ends(server)
    biz_name = "company."
    if biz_name not in name:
        name = biz_name + name
    script = 'NET USER {name} /ACTIVE:YES'.format(name=name)
    run_powershell(ip, user, psw, script)


if __name__ == '__main__':
    disable_account(169, 'username')
    enable_account(132, 'username')
