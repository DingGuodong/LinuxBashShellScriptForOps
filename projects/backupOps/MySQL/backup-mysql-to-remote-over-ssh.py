#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:backup-mysql-to-remote-over-ssh.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/3/13
Create Time:            19:45
Description:            backup entire MySQL database to remote host
Long Description:       TODO(Guodong) logger support and time or performance measure
References:             
Prerequisites:          pip install python-dateutil paramiko
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3

Topic:                  Utilities
 """

import datetime
import os
import subprocess
import tarfile
import time
from subprocess import call

import paramiko
from dateutil.relativedelta import relativedelta

DEBUG = True

backup_config = {
    "user": "root",
    "password": "=kZ0W0e7KkdA",
    "host": "127.0.0.1",
    "port": "3306",
    "databases": [],
    "database": "",
    "now": time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())),
    "backup_dir": "/opt/ebt/data/backup/mysql",
    "save_copies": 2,  # 2 recommends
    "save_days": 3,  # recommends 2 days at least
    "storage": {
        "host": {
            "user": "root",
            "password": "",
            "public_key": "/root/.ssh/id_rsa",
            "ip": "10.46.68.233",
            "ssh_port": "22",
            "target": "/data/backup"  # 'host' and 'port'(known as instance name) will auto join into 'target' path
        },
        "s3": {},  # NotImplemented
        "oss": {},  # NotImplemented
    }
}


def to_unicode_or_bust(obj, encoding='utf-8'):
    """
    convert non-unicode object to unicode object
    :param obj: str object or unicode
    :param encoding:
    :return:
    """
    if isinstance(obj, str):
        if not isinstance(obj, str):
            obj = str(obj, encoding)

    return obj


def to_str_or_bust(obj, encoding='utf-8'):
    """
    convert unicode object to str object
    :param obj: unicode object or str
    :param encoding:
    :return:
    """
    if isinstance(obj, str):
        if isinstance(obj, str):
            obj = obj.encode(encoding)

    return obj


def run_command(executable):
    proc_obj = subprocess.Popen(executable, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc_obj.communicate()
    return_code = proc_obj.returncode
    return return_code, stdout, stderr


def run_command_over_ssh(executable):
    """
    execute command on remote host over SSH
    :param executable:
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

    # running commands on the remote machine
    ssh_client.exec_command(executable)

    ssh_client.close()


def get_databases():
    """
    get names of database
    :return:
    """
    command = """mysql -u {user} -p"{password}" -h {host} -P {port} \
            --show-warnings=FALSE  --table=FALSE -e "show databases;" """.format(**backup_config)
    resp = run_command(command)
    return resp


def prepare():
    """
    complete backup_config
    :return: None
    """
    # get and fill in databases list
    return_code, stdout, stderr = get_databases()
    if return_code == 0:
        backup_config["databases"] = stdout.strip().split(os.linesep)[1:]
    else:
        raise RuntimeError(stderr)

    # assign backup_dir
    backup_config["backup_dir"] = os.path.join(backup_config.get("backup_dir"),
                                               "_".join((backup_config.get("host"), backup_config.get("port"))))

    # make sure dir exists
    backup_dir = backup_config.get("backup_dir")
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # make sure remote dir exists
    backup_instance_name = "_".join((backup_config.get("host"), backup_config.get("port")))
    target = backup_config.get("storage").get("host").get("target")
    target = os.path.join(target, backup_instance_name)
    backup_config["storage"]["host"]["target"] = target
    run_command_over_ssh("mkdir -p %s" % target)


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


def backup_one_database():
    """
    Backup one MySQL database using `mysqldump` and compress it into tgz

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
        {database} > {backup_dir}/backup_{database}_{now}.sql 2>&1""".format(**backup_config)
    call(cli, shell=True)

    sql_name = "{backup_dir}/backup_{database}_{now}.sql".format(**backup_config)
    tgz_name = sql_name + ".tar.gz"
    compress_files(tgz_name, sql_name)

    if os.path.exists(sql_name):
        os.remove(sql_name)


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


def backup_databases():
    """
    backup each database to remote host
    :return:
    """
    databases = backup_config.get("databases")
    for database in databases:
        backup_config["database"] = database

        if DEBUG:
            print("backup database for \'{database}\'...".format(**backup_config))
        backup_one_database()

        if DEBUG:
            print("scp backup file for \'{database}\'...".format(**backup_config))
        scp_files()

        if DEBUG:
            print("Succeed: backup database for \'{database}\' finished.".format(**backup_config))


def cleanup():
    """
    remove old backups, only keep backups not older than x days and count less than x.
    :return:
    """
    backup_dir = backup_config.get("backup_dir")
    save_copies = backup_config.get("save_copies")
    save_days = backup_config.get("save_days")

    if len(os.listdir(backup_dir)) > save_copies * len(backup_config.get("databases")):
        for top, dirs, nondirs in os.walk(backup_dir, followlinks=True):
            for item in nondirs:
                fpath = os.path.abspath(os.path.join(top, item))
                st_ctime = os.stat(fpath).st_ctime
                if time.time() - st_ctime > save_days * 86400:
                    os.remove(fpath)


def clean_old_backups(path, ext="bak", days=30):
    """
    clean old backups with given directory, return counts of files deleted
    :param path: backup directory
    :param ext: extension of backup file
    :param days: days of backup saves
    :return:
    """
    path = to_unicode_or_bust(path)
    if not os.path.exists(path):
        raise RuntimeError("Error: cannot access \'%s\': No such file or directory" % path)

    timestamp_before_save_days = time.mktime((datetime.datetime.today() + relativedelta(days=-days)).timetuple())

    count_removed = 0
    for top, dirs, nondirs in os.walk(path):
        for filename in nondirs:
            if filename.endswith(ext):
                filepath = os.path.join(top, filename)
                if os.path.getmtime(filepath) < timestamp_before_save_days:
                    count_removed += 1
                    os.remove(filepath)

    return count_removed


def main():
    prepare()
    backup_databases()
    cleanup()


if __name__ == '__main__':
    main()
