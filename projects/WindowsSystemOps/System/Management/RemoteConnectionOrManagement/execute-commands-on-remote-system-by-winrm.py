#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:execute-commands-on-remote-system-by-winrm.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/12/11
Create Time:            9:01
Description:            Run the commands on remote server 使用Python在远程服务器上执行命令行
Long Description:       令人兴奋的是，pywinrm支持Linux, Mac OS X or Windows
                        与使用PowerShell执行远程命令相似，目标机器需要开启WinRM服务，而本地不强制需要开启
References:             [diyan/pywinrm](https://github.com/diyan/pywinrm)
Prerequisites:          pip install pywinrm
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
import winrm

# Run a process on a remote host
# https://github.com/diyan/pywinrm/#valid-transport-options
# ntlm: Will use NTLM authentication for both domain and local accounts.

# https://github.com/diyan/pywinrm/#run-a-process-on-a-remote-host
# NOTE: pywinrm will try and guess the correct endpoint url from the following formats:
# windows-host -> http://windows-host:5985/wsman
# windows-host:1111 -> http://windows-host:1111/wsman
s = winrm.Session('windows-host', auth=('username', 'password'), transport="ntlm")
r = s.run_cmd('ipconfig', ['/all'])
print r.status_code, r.std_out,

# Run Powershell script on remote host
ps_script = """$strComputer = $Host
Clear
$RAM = WmiObject Win32_ComputerSystem
$MB = 1048576

"Installed Memory: " + [int]($RAM.TotalPhysicalMemory /$MB) + " MB" """
r = s.run_ps(ps_script)
print r.status_code, r.std_out,

