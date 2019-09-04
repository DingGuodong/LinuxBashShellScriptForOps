#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:add-ssh-public-key.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/8/12
Create Time:            11:06
Description:            add an ssh key to host
Long Description:       Fabric 2 is a high level SSH command execution library designed to
                        execute shell commands remotely over SSH, yielding useful Python objects in return.
                        [some scenarios]
                        1. use fabric 2 to upload scripts to hosts, then run them
                        2. do some system administration task

                        [limits]
                        1. fewer functions than Ansible, etc
                        2. config many servers with different authentication methods is really boring and tedious

References:             http://docs.fabfile.org/en/2.5/getting-started.html#run-commands-via-connections-and-run
Prerequisites:          pip install fabric==2.5.0  #  use `pip install fabric==1.14.1` to enable Fabric 1.x
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
from fabric.config import Config
from invoke import Responder
from invoke.exceptions import Exit
from paramiko.ssh_exception import AuthenticationException

# name, ip, port, username, password, is_sudo, tag, description
hosts_ssh_config = '''
ecs1,192.168.88.18,22,username,password,true,dev,dev machine 1
ecs2,192.168.88.19,22,username,password,true,dev,dev machine 2
ecs3,192.168.88.20,22,username,password,true,dev,dev machine 3
'''

# ssh public key
ssh_public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDR' \
                 '/h48IUPlp8ho4MpW3ez49eN4OyB5U9gs4TlhTPHyf1F3nZvoWXveBtIYpFnr' \
                 '/FnuiKK26hrJwNlDE1J66BK1IbJrgHbYEhYLbT5dT9a0cXvrhn' \
                 '/3pifQIKiaakC8XLvpGKafw2gW8T2pi6MeFmEToSU1OM59FysbqX' \
                 '/blNBKRqqjadRUgS9dA4ZJL6IAvCngFUEJgWSVVe5oSYvJmtmRquYCISdMXQJB' \
                 '/uQwLqmcV2fbVoHI4zvfxjFVoQWRvtb2jddbd2US562IG' \
                 '/5Wv1vnzY4kBRkkulcHLie8NG/Yh6fBt+R0K0XKWDvrcFF7nm6sZOmg8BSX+g6dUfsPxN9r'

for host in hosts_ssh_config.strip().split("\n"):
    # get host config from 'hosts_ssh_config'
    name, ip, port, username, password, is_sudo, tag, description = host.strip().split(",")

    # connection config
    fabric_config = Config()
    fabric_config['load_ssh_config'] = False
    fabric_config['port'] = int(port)
    fabric_config['user'] = username
    fabric_config['connect_kwargs'] = {
        'password': password,
        "key_filename": r"C:\Users\dgden\.ssh\ebt-linux-centos-ssh-root-key.pem",
    }

    # Superuser privileges via auto-response
    sudo_pass_auto_respond = Responder(
        pattern=r'\[sudo\] password:',
        response=password + '\n',
    )

    # create ssh connection
    cxn = Connection(ip, config=fabric_config)

    # add an ssh key to host
    try:
        run_result = cxn.run('cat ~/.ssh/authorized_keys', hide=True)
        if run_result.failed:
            cxn.run('mkdir -p ~/.ssh', hide=True)
            cxn.run('echo %s >> ~/.ssh/authorized_keys' % ssh_public_key, hide=True)
            cxn.run('chmod 700 ~/.ssh', hide=True)
            cxn.run('chmod 400 ~/.ssh/authorized_keys', hide=True)
        else:
            if ssh_public_key not in run_result.stdout:
                cxn.run('cp ~/.ssh/authorized_keys ~/.ssh/authorized_keys$(date +%Y%m%d%H%M%S)~', hide=True)
                cxn.run('echo %s >> ~/.ssh/authorized_keys' % ssh_public_key, hide=True)
            else:
                print("ssh key already added.")
    except AuthenticationException as e:
        raise Exit(e)
