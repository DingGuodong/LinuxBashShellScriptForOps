#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
# Refer: http://docs.fabfile.org/en/1.6/tutorial.html#conclusion
# Refer: https://github.com/dlapiduz/fabistrano/blob/master/fabistrano/deploy.py
# Refer: https://gist.github.com/mtigas/719452
# fab -f .\projects\autoOps\pythonSelf\fabfile.py dotask -i c:\Users\Guodong\.ssh\exportedkey201310171355

import os
import datetime
import re
import sys
import logging
import time
import socket
import requests
import platform

current_time = time.strftime("%Y%m%d")
logpath = "/tmp"
logfile = "log_fabfile_" + current_time + ".log"
try:
    os.makedirs(logpath)
except OSError:
    pass

if os.path.exists(logpath):
    logfile = logpath + "/" + logfile
else:
    logfile = "log_fabfile_" + current_time + ".log"

formatter = "%(asctime)s %(filename)s:%(lineno)d %(levelname)s: %(message)s"
logging.basicConfig(filename=logfile, level=logging.INFO, format=formatter)

logging.info("Started.")

os_release = platform.system()
if os_release == "Windows":
    pass
elif os_release == "Linux":
    distname = platform.linux_distribution()[0]
    if str(distname).lower() == "ubuntu":
        command_to_execute = "apt-get -y install libcurl4-openssl-dev python-pip"
        os.system(command_to_execute)
    elif str(distname).lower() == "centos":
        command_to_execute = "yum -y install python-pip"
        os.system(command_to_execute)
else:
    print "Error => Unsupported OS type."
    logging.error("Unsupported OS type.")
    sys.exit(1)

try:
    from fabric.api import *
except ImportError:
    try:
        command_to_execute = "pip install fabric"
        os.system(command_to_execute)
    except OSError:
        exit(1)
finally:
    from fabric.api import *
    from fabric.main import main
    from fabric.colors import *

try:
    import pycurl
except ImportError:
    try:
        command_to_execute = "pip install pycurl"
        os.system(command_to_execute)
    except OSError:
        sys.exit(1)
finally:
    import pycurl

try:
    import pytz
except ImportError:
    try:
        command_to_execute = "pip install pytz"
        os.system(command_to_execute)
    except OSError:
        sys.exit(1)
finally:
    import pytz

try:
    import shutil
except ImportError:
    try:
        command_to_execute = "pip install shutil"
        os.system(command_to_execute)
    except OSError:
        sys.exit(1)
finally:
    import shutil

try:
    import certifi
except ImportError:
    try:
        command_to_execute = "pip install certifi"
        os.system(command_to_execute)
    except OSError:
        sys.exit(1)
finally:
    import certifi

env.roledefs = {
    'testEnvironment': ['root@10.6.28.28:22', ],
    'productionEnvironment': ['root@10.6.28.28:22', ],
}

env.git_address = ''
env.basedir = '/root/www'
env.capistrano_ds_lock = env.basedir + '/.capistrano_ds_lock'


def sudo_run(*args, **kwargs):
    if env.use_sudo:
        sudo(*args, **kwargs)
    else:
        run(*args, **kwargs)


def check_var_is_absent(var):
    if var is None or var == "":
        print var + " is None or empty, please check and fix it!"
        sys.exit(1)


def check_runtime_dependencies():
    check_var_is_absent(env.basedir)
    pass


def backup_file(path, extension='~'):
    backup_filename = path + '.' + extension

    if os.path.islink(path):
        src = os.readlink(path)
    else:
        src = path

    shutil.copy2(src, backup_filename)

    return backup_filename


def rollback_file(path, extension='~'):
    if os.path.islink(path):
        src = os.readlink(path)
    else:
        src = path
    if os.path.exists(src + extension):
        shutil.copy2(src + extension, src)
    return src


@roles('testEnvironment')
def check_network_connectivity():
    internet_hostname = "www.aliyun.com"
    ping = 'ping -c4 ' + internet_hostname
    result_code = None
    try:
        run(ping)
    except Exception:
        result_code = 1
    if result_code is not None:
        print red("Error   => connect to Internet failed!")
        logging.error("connect to Internet failed!")
    else:
        print green("Success => connect to Internet successfully!")


def check_name_resolve():
    internet_hostname = "www.aliyun.com"
    nslookup = 'nslookup ' + internet_hostname
    result_code = None
    try:
        run(nslookup)
    except Exception:
        result_code = 1
    if result_code is not None:
        print red("Error   => name resolve to Internet failed!")
        logging.error("name resolve to Internet failed!")
    else:
        print green("Success => name resolve to Internet successfully!")


def set_dns_resolver():
    pass


@roles('testEnvironment')
def set_hosts_file(hosts="/etc/hosts"):
    if not os.path.exists(hosts):
        if not os.path.exists(os.path.dirname(hosts)):
            os.makedirs(os.path.dirname(hosts))

    with open(hosts, "w") as f:
        hosts_url = "https://raw.githubusercontent.com/racaljk/hosts/master/hosts"
        conn = requests.head(hosts_url)
        if conn.status_code != 200:
            hosts_url = "https://coding.net/u/scaffrey/p/hosts/git/raw/master/hosts"
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, hosts_url)
        curl.setopt(pycurl.CAINFO, certifi.where())
        curl.setopt(pycurl.WRITEDATA, f)
        curl.perform()
        curl.close()
    # TODO(Guodong Ding) Ubuntu Linux not passed here, but CentOS passed!
    hostname = socket.gethostname()
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except Exception:
        ip = None
    with open(hosts, "a") as f:
        if ip is not None:
            appended_content = "\n" + "127.0.0.1 " + hostname + "\n" + ip + " " + hostname + "\n"
        else:
            appended_content = "\n" + "127.0.0.1 " + hostname + "\n"
        f.write(appended_content)


def set_capistrano_directory_structure_over_fabric():
    print blue("setting capistrano directory structure ...")
    capistrano_release = env.basedir + '/release'
    capistrano_repository = env.basedir + '/repository'
    capistrano_share = env.basedir + '/share'
    capistrano_backup = env.basedir + '/backup'
    if os.path.exists(env.capistrano_ds_lock):
        pass
    else:
        if not os.path.exists(capistrano_release):
            os.makedirs(capistrano_release)
        if not os.path.exists(capistrano_repository):
            os.makedirs(capistrano_repository)
        if not os.path.exists(capistrano_share):
            os.makedirs(capistrano_share)
        if not os.path.exists(capistrano_backup):
            os.makedirs(capistrano_backup)

        with open(env.capistrano_ds_lock, 'w') as f:
            if os.path.exists("/etc/timezone"):
                tz = file("/etc/timezone").read().strip()
                if tz == 'Asia/Chongqing' or tz == 'Asia/Shanghai':
                    content = datetime.datetime.now(tz=pytz.timezone(tz))
                else:
                    content = datetime.datetime.now(tz=pytz.timezone('Asia/Shanghai'))
            else:
                content = datetime.datetime.now()
            f.write(str(content))
    print green("setting capistrano directory structure successfully!")


def set_capistrano_directory_structure_local():
    local(set_capistrano_directory_structure_over_fabric())


def git_clone_local():
    code_dir = env.basedir + '/repository'
    git_clone = "git clone " + env.git_address + " " + code_dir
    local(git_clone)


if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    print "Please use 'fab -f %s'" % sys.argv[0:]
    sys.exit(1)
