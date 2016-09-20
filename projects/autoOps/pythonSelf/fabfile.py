#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-\

# Pythonic remote execution
# Refer: http://docs.fabfile.org/en/1.6/tutorial.html#conclusion
# Refer: https://github.com/dlapiduz/fabistrano/blob/master/fabistrano/deploy.py
# Refer: https://gist.github.com/mtigas/719452
# Refer: http://docs.fabfile.org/en/1.12/usage/env.html
# fab -i c:\Users\Guodong\.ssh\exportedkey201310171355 -f .\projects\autoOps\pythonSelf\fabfile.py dotask

import os
import datetime
import re
import sys
import logging
import logging.handlers
import time
import requests
import platform


def win_or_linux():
    # os.name ->(sames to) sys.builtin_module_names
    if 'posix' in sys.builtin_module_names:
        os_type = 'Linux'
    elif 'nt' in sys.builtin_module_names:
        os_type = 'Windows'
    return os_type


def is_windows():
    if "windows" in win_or_linux().lower():
        return True
    else:
        return False


def is_linux():
    if "linux" in win_or_linux().lower():
        return True
    else:
        return False


def initLoggerWithRotate():
    current_time = time.strftime("%Y%m%d%H")
    logpath = "/tmp"
    logfile = "log_fabfile_" + current_time + ".log"
    if not os.path.exists(logpath):
        os.makedirs(logpath)
    else:
        logfile = os.path.join(logpath, logfile)

    logger = logging.getLogger("fabric")
    log_formatter = logging.Formatter("%(asctime)s %(filename)s:%(lineno)d %(name)s %(levelname)s: %(message)s",
                                      "%Y-%m-%d %H:%M:%S")
    file_handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=104857600, backupCount=5)
    file_handler.setFormatter(log_formatter)
    stream_handler = logging.StreamHandler(sys.stderr)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)
    return logger


logger = initLoggerWithRotate()

os_release = platform.system()
if os_release == "Windows":
    pass
elif os_release == "Linux":
    distname = platform.linux_distribution()[0]
    if str(distname).lower() == "ubuntu":
        command_to_execute = "which pip >/dev/null 2>&1 || apt-get -y install libcurl4-openssl-dev python-pip"
        os.system(command_to_execute)
    elif str(distname).lower() == "centos":
        command_to_execute = "which pip &>/dev/null 1>&2 || yum -y install python-pip"
        os.system(command_to_execute)
else:
    print "Error => Unsupported OS type."
    logger.error("Unsupported OS type.")
    sys.exit(1)

try:
    from fabric.api import *
except ImportError:
    try:
        command_to_execute = "pip install fabric"
        os.system(command_to_execute)
    except OSError:
        sys.exit(1)
finally:
    from fabric.api import *
    from fabric.main import main
    from fabric.colors import *
    from fabric.context_managers import *
    from fabric.contrib.console import confirm

try:
    import pycurl
except ImportError:
    try:
        command_to_execute = "pip install pycurl"
        os.system(command_to_execute)
    except OSError:
        sys.exit(1)
    import pycurl

try:
    import pytz
except ImportError:
    try:
        command_to_execute = "pip install pytz"
        os.system(command_to_execute)
    except OSError:
        sys.exit(1)
    import pytz

try:
    import shutil
except ImportError:
    try:
        command_to_execute = "pip install shutil"
        os.system(command_to_execute)
    except OSError:
        sys.exit(1)
    import shutil

try:
    import certifi
except ImportError:
    try:
        command_to_execute = "pip install certifi"
        os.system(command_to_execute)
    except OSError:
        sys.exit(1)
    import certifi

env.roledefs = {
    'test': ['root@10.6.28.28:22', ],
    'nginx': ['root@10.6.28.46:22', 'root@10.6.28.27:22', ],
    'db': ['root@10.6.28.35:22', 'root@10.6.28.93:22', ],
    'sit': ['root@10.6.28.46:22', 'root@10.6.28.135:22', 'root@10.6.28.35:22', ],
    'uat': ['root@10.6.28.27:22', 'root@10.6.28.125:22', 'root@10.6.28.93:22', ],
    'all': ["10.6.28.27", "10.6.28.28", "10.6.28.35", "10.6.28.46", "10.6.28.93", "10.6.28.125", "10.6.28.135"]
}

env.user = "root"
env.hosts = ["10.6.28.27", "10.6.28.28", "10.6.28.35", "10.6.28.46", "10.6.28.93", "10.6.28.125", "10.6.28.135"]
env.command_timeout = 15
env.connection_attempts = 2


def show_uname():
    try:
        out = run("uname -a")
    except KeyboardInterrupt:
        logger.warning("We catch 'Ctrl + C' pressed, task canceled!")
        sys.exit(1)
    if out.return_code == 0:
        logger.info("task finished successfully on " + env.host + " .")
    else:
        logger.error("task finished failed on " + env.host + " .")


# Call method: ping:www.qq.com
def ping(host):
    if host is not None:
        try:
            out = run("ping -c1 " + host + " >/dev/null 2>&1")
        except KeyboardInterrupt:
            logger.warning("We catch 'Ctrl + C' pressed, task canceled!")
            sys.exit(1)
        if out.return_code == 0:
            logger.info("task ping finished successfully on " + env.host + " .")
        else:
            logger.error("task ping finished failed on " + env.host + " .")


def showDiskUsage():
    try:
        run("df -h")
    except KeyboardInterrupt:
        logger.warning("We catch 'Ctrl + C' pressed, task canceled!")
        sys.exit(1)


def setNameServer(server=None):
    nameServerList = ""
    if isinstance(server, list) and len(server) >= 1:
        for host in server:
            nameServerList += ("namserver %s\n" % host)
    else:
        nameServerList = "nameserver 182.254.116.116\n"

    print("Executing on %(host)s as %(user)s" % env)
    try:
        out = run('test -f /etc/resolv.conf && echo "%s" > /etc/resolv.conf' % nameServerList.strip('\n'))
    except KeyboardInterrupt:
        logger.warning("We catch 'Ctrl + C' pressed, task canceled!")
        sys.exit(1)
    if out.return_code == 0:
        logger.info("task finished successfully on " + env.host + " .")
        run('test -f /etc/resolv.conf && cat /etc/resolv.conf')
    else:
        logger.error("task finished failed on " + env.host + " .")
        abort("task finished failed on " + env.host + " .")


def checkWeChatApi():
    qy_api = "qyapi.weixin.qq.com"
    api = "api.weixin.qq.com"
    ping(qy_api)
    ping(api)


def showUptime():
    run("uptime")


def putSelf():
    try:
        put(__file__, '/tmp/fabric.py')
    except Exception as e:
        logger.error("task putSelf failed! msg: %s" % e)
        abort("task putSelf failed! msg: %s" % e)


def sudo_run(*args, **kwargs):
    if env.use_sudo is not None:
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
        logger.error("connect to Internet failed!")
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
        logger.error("name resolve to Internet failed!")
    else:
        print green("Success => name resolve to Internet successfully!")


def set_dns_resolver():
    serverList = ['182.254.116.116', '202.106.196.115', '202.106.0.20']
    setNameServer(serverList)


def set_hosts_file(hosts="/etc/hosts"):
    import socket
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

    hostname = socket.gethostname()  # socket.getfqdn()
    print hostname
    try:
        ip = socket.gethostbyname(socket.gethostname())  # TODO(Guodong Ding) Ubuntu not passed here, but CentOS passed!
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


def git_clone_local():
    code_dir = env.basedir + '/repository'
    git_clone = "git clone " + env.git_address + " " + code_dir
    local(git_clone)


def terminal_debug(defName):
    command = "fab -i c:\Users\Guodong\.ssh\exportedkey201310171355\
                -f C:/Users/Guodong/PycharmProjects/LinuxBashShellScriptForOps/projects/autoOps/pythonSelf/fabfile.py \
                %s" % defName
    os.system(command)


if __name__ == '__main__':
    if len(sys.argv) == 1 and is_windows():
        logger.info("Started.")
        terminal_debug("showUptime")
        terminal_debug("showDiskUsage")
        sys.exit(0)

    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    print red("Please use 'fab -f %s'" % " ".join(str(x) for x in sys.argv[0:]))
    logger.error("Syntax error. Exit now.")
    sys.exit(1)
