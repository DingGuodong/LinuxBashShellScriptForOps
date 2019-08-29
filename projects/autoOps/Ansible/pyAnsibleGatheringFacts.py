#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyAnsibleGatheringFacts.py
User:               Guodong
Create Date:        2017/8/24
Create Time:        17:35
Description:        gathering facts using Ansible on localhost or remote hosts
References:         from ansible.module_utils import facts
Prerequisite:       1.sudo with no password
                    2.ssh trust
                    3.python-pip installed
 """
import json
import os
import re
import stat
import subprocess
import sys


def check_ansible_env():
    if not is_linux():
        print("Linux Supported Only. Aborted!")
        sys.exit(1)

    if not is_privilege:
        print("Please run this script as a admin user with sudo privilege or run as root.")
        sys.exit(1)

    if not is_ansible_installed():
        install_ansible()

    if not is_inventory_set():
        set_inventory()


def is_linux():
    if "posix" in os.name.lower() or "linux" in sys.platform.lower():
        return True
    else:
        return False


def is_privilege():
    return is_sudo()


def is_sudo():
    try:
        with open("/root/.bashrc", 'w+') as f:
            f.readline()
            return True
    except IOError:
        return False


def is_ansible_installed():
    path = get_bin_path("ansible", opt_dirs=(os.path.join(os.path.expanduser('~'), '.local/bin'),))
    if path is not None:
        if os.path.exists(path):
            return True
        else:
            return False
    else:
        return False


def install_ansible():
    run_command("pip install ansible")


def set_inventory(inventory_file="/etc/ansible/hosts"):
    basedir = os.path.dirname(inventory_file)
    content = """[localhost]
127.0.0.1 ansible_user=root ansible_ssh_private_key_file=/etc/ssh/ssh_host_rsa_key ansible_ssh_common_args="-oStrictHostKeyChecking=no"
"""
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    if not os.path.exists(inventory_file):
        try:
            with open(inventory_file, 'w') as f:
                f.write(content)
        except IOError as e:
            print(e)
            print("Permission denied, is sudo or root?")
            sys.exit(1)
    else:
        with open(inventory_file, 'r') as original:
            data = original.read()
        if "localhost" not in data or "127.0.0.1" not in data:
            try:
                with open(inventory_file, 'w') as f:
                    f.write(content)
            except IOError as e:
                print(e)
                print("Permission denied, is sudo or root?")
                sys.exit(1)


def is_inventory_set(inventory_file="/etc/ansible/hosts"):
    try:
        with open(inventory_file, 'r') as original:
            data = original.read()
        if "localhost" not in data or "127.0.0.1" not in data:
            return False
        else:
            return True
    except IOError:
        return False


def gather_facts():
    ansible_bin_path = get_bin_path("ansible", opt_dirs=(os.path.join(os.path.expanduser('~'), '.local/bin'),))
    proc_obj = subprocess.Popen("{ansible} localhost  -m setup".format(ansible=ansible_bin_path), shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
    stdout, stderr = proc_obj.communicate()
    return_code = proc_obj.returncode
    if return_code == 0:
        return stdout
    else:
        return stderr


def facts_to_json():
    facts = gather_facts()
    if facts is not None:
        facts_json_string = re.sub("^127.*=>\s+", "", facts)
        return facts_json_string
    else:
        return ""


def facts_to_dict():
    facts = gather_facts()
    if facts is not None:
        facts_json_string = re.sub("^127.*=>\s+", "", facts)
        facts_dict = json.loads(facts_json_string)
        return facts_dict
    else:
        return {}


def sample_data():
    raw_data = facts_to_dict()
    if raw_data is not None:
        # for key in raw_data.keys():
        #     print key
        thin_data = raw_data
        for key in thin_data['ansible_facts'].keys():
            if '_veth' in key \
                    or '_docker0' in key \
                    or '_lo' in key \
                    or '_all_ipv6_addresses' in key \
                    or '_devices' in key \
                    or '_mounts' in key \
                    or '_device_links' in key:
                thin_data['ansible_facts'].pop(key, None)

        # for key in thin_data['ansible_facts'].keys():
        #     print key

        return json.dumps(thin_data['ansible_facts'], indent=4)
    else:
        return ""


def run_command(executable, use_sudo=True):
    if not executable or not isinstance(executable, (str, unicode)):
        print("parameter error, str type is required, but got type \'parameter_type\'.".format(
            parameter_type=type(executable)))
        sys.exit(1)
    if use_sudo:
        executable = "sudo /bin/bash -c \"" + executable + "\""

    if sys.platform == "linux2":
        print("Run local command \'{command}\' on Linux...".format(command=executable))

        proc_obj = subprocess.Popen(executable, shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
        stdout, stderr = proc_obj.communicate()
        return_code = proc_obj.returncode
        if return_code == 0:
            print("Run local command \'{command}\' successfully!".format(command=executable))
            print(stdout)
        else:
            print("Run local command \'{command}\' failed! " \
                  "return code is: {return_code}".format(command=executable,
                                                         return_code=return_code if return_code is not None else 1))
            print(stdout, stderr)
    else:
        print("Linux Supported Only. Aborted!")
        sys.exit(1)


def get_bin_path(arg, required=False, opt_dirs=None):
    """
    find system executable in PATH.
    Optional arguments:
       - required:  if executable is not found and required is true
       - opt_dirs:  optional list of directories to search in addition to PATH
    if found return full path; otherwise return None
    """
    sbin_paths = ['/sbin', '/usr/sbin', '/usr/local/sbin']
    paths = []

    # https://stackoverflow.com/questions/9039191/mutable-default-method-arguments-in-python
    # https://stackoverflow.com/questions/1132941/least-astonishment-and-the-mutable-default-argument
    if not opt_dirs:
        opt_dirs = []

    for d in opt_dirs:
        if d is not None and os.path.exists(d):
            paths.append(d)
    paths += os.environ.get('PATH', '').split(os.pathsep)
    bin_path = None
    # mangle PATH to include /sbin dirs
    for p in sbin_paths:
        if p not in paths and os.path.exists(p):
            paths.append(p)
    for d in paths:
        if not d:
            continue
        path = os.path.join(d, arg)
        if os.path.exists(path) and not os.path.isdir(path) and is_executable(path):
            bin_path = path
            break
    if required and bin_path is None:
        print('Failed to find required executable %s in paths: %s' % (arg, os.pathsep.join(paths)))
    return bin_path


def is_executable(path):
    """is the given path executable?

    Limitations:
    * Does not account for FSACLs.
    * Most times we really want to know "Can the current user execute this
      file"  This function does not tell us that, only if an execute bit is set.
    """
    # These are all bitfields so first bitwise-or all the permissions we're
    # looking for, then bitwise-and with the file's mode to determine if any
    # execute bits are set.
    return (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH) & os.stat(path)[stat.ST_MODE]


if __name__ == '__main__':
    check_ansible_env()
    print(sample_data())
