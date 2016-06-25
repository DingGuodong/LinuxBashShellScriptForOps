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
    import pytz
except ImportError:
    try:
        command_to_execute = "pip install pytz"
        os.system(command_to_execute)
    except OSError:
        exit(1)
finally:
    import pytz

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


def check_runtime_dependencies():
    pass


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
    else:
        print green("Success => name resolve to Internet successfully!")


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


def git_clone():
    code_dir = env.basedir + '/repository'
    local()


if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    print "Please use 'fab -f %s'" % sys.argv[0:]
    sys.exit(1)
