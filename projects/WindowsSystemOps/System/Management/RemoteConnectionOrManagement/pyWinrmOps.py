#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyWinrmOps.py
User:               Guodong
Create Date:        2017/7/12
Create Time:        16:36
Description:
References:         http://docs.ansible.com/ansible/intro_windows.html#using-a-windows-control-machine
                    https://pypi.python.org/pypi/pywinrm/0.2.2
Dependence:
                    Windows Services:
                        服务名称: WinRM
                        显示名称: Windows Remote Management (WS-Management)
                        描述: Windows 远程管理(WinRM)服务执行 WS-Management 协议来实现远程管理。
                        WS-Management 是用于远程软件和硬件管理的标准 Web 服务协议。
                        WinRM 服务侦听网络上的 WS-Management 请求并对它们进行处理。
                        通过组策略或使用 winrm.cmd 命令行工具的侦听程序，来配置 WinRM 服务，以使其可通过网络侦听。
                        WinRM 服务提供对 WMI 数据的访问并启用事件集合。事件集合及对事件的订阅需要服务处于运行状态。
                        传输 WinRM 消息时使用 HTTP 和 HTTPS 协议。
                        WinRM 服务不依赖于 IIS ，但在同一计算机上预配置为与 IIS 共享端口。
                        WinRM 服务保留 /wsman URL 前缀。
                        若要防止与 IIS 发生冲突，管理员应确保 IIS 上承载的所有网站均不使用 /wsman URL 前缀。

 """

import winrm  # https://pypi.python.org/pypi/pywinrm/0.2.2

# Run a process on a remote host
s = winrm.Session('windows-host.example.com', auth=('john.smith', 'secret'))
r = s.run_cmd('ipconfig', ['/all'])
print(r.status_code, r.std_out, end=' ')

# Run Powershell script on remote host
ps_script = """$strComputer = $Host
Clear
$RAM = WmiObject Win32_ComputerSystem
$MB = 1048576

"Installed Memory: " + [int]($RAM.TotalPhysicalMemory /$MB) + " MB" """
r = s.run_ps(ps_script)
print(r.status_code, r.std_out, end=' ')

# Run process with low-level API with domain user, disabling HTTPS cert validation
from winrm.protocol import Protocol

p = Protocol(
    endpoint='https://windows-host:5986/wsman',
    transport='ntlm',
    username=r'somedomain\someuser',
    password='secret',
    server_cert_validation='ignore')
shell_id = p.open_shell()
command_id = p.run_command(shell_id, 'ipconfig', ['/all'])
std_out, std_err, status_code = p.get_command_output(shell_id, command_id)
p.cleanup_command(shell_id, command_id)
p.close_shell(shell_id)
