#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pySshConnectParallel.py
User:               Guodong
Create Date:        2017/8/8
Create Time:        13:36
Description:        save data into persistent object in multi-threading
References:         
 """
import threading
import shelve  # Manage shelves of pickled objects
import os


def remote_exec(hostname, command):
    import paramiko
    try:
        lock.acquire(5)  # same as time.sleep(5) until task finished, in fact it's better to not use threading here
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port=22, username="root",
                       key_filename=r"C:\Users\Guodong\.ssh\ebt-linux-centos-ssh-root-key.pem", timeout=5)
        stdin, stdout, stderr = client.exec_command(command)
        # print "Hostname: {hostname}, Out: {out}".format(hostname=hostname, out=list(stdout))
        persistent_object[hostname] = list(stdout)  # save data into persistent object in this threading
        lock.release()
    except Exception as e:
        print('ssh failed', e)


if __name__ == '__main__':
    ip_list = ['10.46.68.233', '10.47.49.161', '10.46.69.219']
    command_to_exec = 'ls -a'
    tmp_db = "__tmp.db"
    persistent_object = shelve.open(tmp_db)
    lock = threading.Lock()
    for thread in [threading.Thread(target=remote_exec, args=(ip, command_to_exec), ) for ip in ip_list]:
        thread.setDaemon(True)
        thread.start()
    thread.join()

    for host in ip_list:
        # print persistent_object[host]
        for item in persistent_object[host]:  # fetch data from persistent object
            print(item, end=' ')
    persistent_object.close()
    os.remove(tmp_db)
