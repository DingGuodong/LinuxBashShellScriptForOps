#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:ssh-execute-commands-on-remote-host.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2021/3/19
Create Time:            11:27
Description:            
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


def execute_commands_on_remote_host(host, command, **kwargs):
    """
    execute commands on remote host via SSH protocol

    :param host: hostname or ip address
    :type host: str
    :param command: commands
    :type command: str
    :param kwargs:
        port: ssh port, type: int
        username: username, type: str
        key_filename: the path of ssh private key file, type: str
        timeout: timeout, type: int
        NOTE: we always recommend that using ssh key auth instead using a weak password
    :type kwargs:
    :return:
    :rtype:
    """
    import paramiko

    port = kwargs.get("port") or 22
    username = kwargs.get("username") or 'root'
    key_filename = kwargs.get("key_filename")  # os.path.expanduser(r'~/.ssh/id_rsa')
    timeout = kwargs.get("timeout") or 5

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, port=port, username=username, key_filename=key_filename, timeout=timeout)

    stdin, stdout, stderr = client.exec_command(command=command,
                                                get_pty=True)  # type: paramiko.ChannelStdinFile, list, paramiko.ChannelStderrFile
    """
    warning::   
                The server may reject this request depending on its ``AcceptEnv``
                setting; such rejections will fail silently (which is common client
                practice for this particular request type). Make sure you
                understand your server's configuration before using!
    """
    for line in stdout:
        print("Stdout: ", line,)

    for line in stdout:
        print("Stderr: ", line,)
    client.close()


if __name__ == '__main__':
    execute_commands_on_remote_host("47.240.129.250", 'uname -a',
                                    port=22,
                                    username='root',
                                    key_filename=r"C:\Users\dgden\.ssh\exportedkey201310171355"
                                    )
