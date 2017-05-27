#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pySshConnectTryAllTheTime.py
User:               Guodong
Create Date:        2017/5/23
Create Time:        20:47
 """


def try_ssh_to_server():
    import paramiko
    import time

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("121.199.6.40", port=22, username="root",
                   key_filename="C:\Users\Guodong\.ssh\ebt-linux-centos-ssh-root-key.pem", timeout=5)
    print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    stdin, stdout, stderr = client.exec_command("uname -a")
    for line in stdout:
        print line,
    client.close()


if __name__ == '__main__':
    import time

    keep_running_flag = True
    times = 1
    while keep_running_flag:
        print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), times
        try:
            try_ssh_to_server()
        except Exception:
            time.sleep(10)
            times += 1
            pass
        else:
            keep_running_flag = False
