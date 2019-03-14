#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:python-backup-mysql-and-files.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/2/18
Create Time:            15:16
Description:            backup mysql database and app files to remote host
Long Description:       
References:             
Prerequisites:          pip install paramiko
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
import os
import tarfile
import time
from subprocess import call

import paramiko

backup_config = {
    "user": "root",
    "password": "=kZ0W0e7KkdA",
    "host": "127.0.0.1",
    "port": "3306",
    "database": "suitecrm",
    "now": time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())),
    "app_dir": "/opt/ebt/apps/suitecrm",
    "backup_dir": "/opt/ebt/data/backup/apps/suitecrm",
    "save_copies": 10,
    "save_days": 10,
    "storage": {
        "host": {
            "user": "root",
            "password": "",
            "public_key": "/root/.ssh/id_rsa",
            "ip": "10.46.68.233",
            "ssh_port": "22",
            "target": "/data"
        },
        "s3": {},
        "oss": {},
    }
}


def prepare():
    # make sure dir exists
    backup_dir = backup_config.get("backup_dir")
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)


def compress_files(name, path):
    """
    compress files or directory using tar in python
    :param name: tgz filename, the name can be a full path of name
    :param path: path to file or directory
    :return:
    """
    with tarfile.open(name, "w:gz") as tar:
        tar.add(path, arcname=os.path.basename(path))


def put_file_over_ssh(src, dst):
    """
    Upload file to remote host using SSH
    sample sftp, scp with paramiko
    :param src:
    :param dst:
    :return:
    """
    host_config = backup_config.get("storage").get("host")
    hostname = host_config.get("ip")
    port = int(host_config.get("ssh_port")) or paramiko.config.SSH_PORT
    username = host_config.get("user")
    public_key = host_config.get("public_key")
    timeout = 5

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname, port=port, username=username, key_filename=public_key, timeout=timeout)

    sftp_client = ssh_client.open_sftp()
    sftp_client.put(src, dst)

    sftp_client.close()
    ssh_client.close()


def backup_mysql():
    """
    Backup MySQL database using `mysqldump`

    mysqldump -u root --password="=kZ0W0e7KkdA" -h 127.0.0.1 -P 3306 \
        --force --routines --events --triggers --single-transaction --databases \
        suitecrm > backup_suitecrm_201902181645.sql
    mysqldump -u root -p"=kZ0W0e7KkdA" -h 127.0.0.1 -P 3306 \
        -f -R -E --triggers --single-transaction -B \
        suitecrm > backup_suitecrm_201902181645.sql

    :return:
    """
    cli = """mysqldump -u {user} -p"{password}" -h {host} -P {port} \
        -f -R -E --triggers --single-transaction -B \
        {database} > {backup_dir}/backup_{database}_{now}.sql 2>/dev/null""".format(**backup_config)
    call(cli, shell=True)

    sql_name = "{backup_dir}/backup_{database}_{now}.sql".format(**backup_config)
    tgz_name = sql_name + ".tar.gz"
    compress_files(tgz_name, sql_name)


def backup_files():
    """
    packaging app files
    :return:
    """
    app_dir = os.path.abspath(backup_config.get("app_dir"))
    if os.path.islink(app_dir):
        app_dir = os.readlink(app_dir)

    tgz_name = "{backup_dir}/backup_app_{database}_{now}.tar.gz".format(**backup_config)

    compress_files(tgz_name, app_dir)


def scp_files():
    """
    Remote Backup: send backups to remote host
    :return:
    """
    target = backup_config.get("storage").get("host").get("target")
    part1_db = "{backup_dir}/backup_{database}_{now}.sql.tar.gz".format(**backup_config)
    part2_apps = "{backup_dir}/backup_app_{database}_{now}.tar.gz".format(**backup_config)

    for item in [part1_db, part2_apps]:
        if os.path.exists(item):
            put_file_over_ssh(item, os.path.join(target, os.path.basename(item)))


def cleanup():
    """
    remove old backups, only keep backups not older than x days and count less than x.
    :return:
    """
    backup_dir = backup_config.get("backup_dir")
    save_copies = backup_config.get("save_copies")
    save_days = backup_config.get("save_days")

    if len(os.listdir(backup_dir)) > save_copies * 3:
        for top, dirs, nondirs in os.walk(backup_dir, followlinks=True):
            for item in nondirs:
                fpath = os.path.abspath(os.path.join(top, item))
                st_ctime = os.stat(fpath).st_ctime
                if time.time() - st_ctime > save_days * 86400:
                    os.remove(fpath)


if __name__ == '__main__':
    prepare()

    backup_mysql()
    backup_files()
    scp_files()

    cleanup()
