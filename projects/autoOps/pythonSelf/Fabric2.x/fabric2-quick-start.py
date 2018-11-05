#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:fabric2-quick-start.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/11/5
Create Time:            15:54
Description:            use Fabric 2 to execute SSH commands and transfer files
Long Description:       Fabric 2 is a high level SSH command execution library designed to
                        execute shell commands remotely over SSH, yielding useful Python objects in return.
                        [some scenarios]
                        1. use fabric 2 to upload scripts to hosts, then run them
                        2. do some system administration task

                        [limits]
                        1. fewer functions than Ansible, etc
                        2. config many servers with different authentication methods is really boring and tedious

References:             http://docs.fabfile.org/en/2.4/getting-started.html#run-commands-via-connections-and-run
Prerequisites:          pip install fabric==2.4.0  #  use `pip install fabric==1.14.0` to enable Fabric 1.x
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
from fabric import Connection
from fabric import SerialGroup as Group
from fabric.config import Config
from invoke import Responder
from invoke.exceptions import Exit


def disk_free(c):
    run_result = c.run('uname -s', hide=True)
    if 'Linux' in run_result.stdout:
        command = "df -h / | tail -n1 | awk '{print $5}'"
        return c.run(command, hide=True).stdout.strip()
    err = "No idea how to get disk space on {}!".format(run_result)
    raise Exit(err)


if __name__ == '__main__':
    # overriding default ssh configuration
    fabric_config = Config()
    fabric_config['load_ssh_config'] = False
    fabric_config['port'] = 22
    fabric_config['user'] = 'root'
    fabric_config['connect_kwargs'] = {
        "key_filename": "c:\Users\Guodong\.ssh\exportedkey201310171355",
    }

    # Superuser privileges via auto-response
    sudo_pass_auto_respond = Responder(
        pattern=r'\[sudo\] password:',
        response='mypassword\n',
    )

    # create connection
    cxn = Connection('192.168.88.19', config=fabric_config)

    # do tasks on host
    print cxn.run("uname -a", hide=True).stdout
    print cxn.sudo("whoami", hide=True).stdout
    cxn.run('sudo whoami', pty=True, watchers=[sudo_pass_auto_respond])
    cxn.put(__file__, "/tmp/this.py")
    cxn.run("sudo rm -f /tmp/this.py")
    # cxn.get("/tmp/this.py", "this.py")
    print disk_free(cxn)

    # config multiple servers with methods 1
    for host in ('192.168.88.19', '192.168.88.20', '192.168.88.21'):
        result = Connection(host, config=fabric_config).run('uname -s', hide=True)
        print("{}: {}".format(host, result.stdout.strip()))

    # config multiple servers, M2
    results = Group('192.168.88.19', '192.168.88.20', '192.168.88.21', config=fabric_config).run('uname -s', hide=True)
    for connection, result in results.items():
        print("{0.host}: {1.stdout}".format(connection, result))
