#!/usr/bin/env python3
# -*- coding:utf-8 -*-
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
Description:            template of preinstallation task for fabric 2
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
Todo:                   support dry-run, such as show direct commands which can be executed on Linux System
 """
from fabric import Connection
from fabric.config import Config
from invoke import Responder
from invoke.exceptions import Exit
from paramiko.ssh_exception import AuthenticationException

# name, ip, port, username, password, is_sudo, tag, description
hosts_ssh_config = '''
ecs3,192.168.88.14,22,ebt,ebt,true,k8s,k8s node 3
ecs1,192.168.88.15,22,ebt,ebt,true,k8s,k8s node 1
ecs2,192.168.88.16,22,ebt,ebt,true,k8s,k8s node 2
'''

# ssh public key
ssh_public_key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDR' \
                 '/h48IUPlp8ho4MpW3ez49eN4OyB5U9gs4TlhTPHyf1F3nZvoWXveBtIYpFnr' \
                 '/FnuiKK26hrJwNlDE1J66BK1IbJrgHbYEhYLbT5dT9a0cXvrhn' \
                 '/3pifQIKiaakC8XLvpGKafw2gW8T2pi6MeFmEToSU1OM59FysbqX' \
                 '/blNBKRqqjadRUgS9dA4ZJL6IAvCngFUEJgWSVVe5oSYvJmtmRquYCISdMXQJB' \
                 '/uQwLqmcV2fbVoHI4zvfxjFVoQWRvtb2jddbd2US562IG' \
                 '/5Wv1vnzY4kBRkkulcHLie8NG/Yh6fBt+R0K0XKWDvrcFF7nm6sZOmg8BSX+g6dUfsPxN9r'


def add_ssh_key():
    """
    add an ssh key to host
    :return: None
    """
    try:
        run_result = cxn.run('cat ~/.ssh/authorized_keys', hide=True, warn=True)
        if run_result.failed:
            cxn.run('mkdir -p ~/.ssh', hide=True)
            cxn.run('echo %s >> ~/.ssh/authorized_keys' % ssh_public_key, hide=True)
        else:
            if ssh_public_key not in run_result.stdout:
                cxn.run('cp ~/.ssh/authorized_keys ~/.ssh/authorized_keys$(date +%Y%m%d%H%M%S)~', hide=True)
                cxn.run('echo %s >> ~/.ssh/authorized_keys' % ssh_public_key, hide=True)
            else:
                print("ssh key already added.")
    except AuthenticationException as e:
        raise Exit(e)


def show_system_dist_and_version():
    """
    To determine the distribution and version of Linux installed
    :return:
    """
    run_result = cxn.sudo('lsb_release -idrc && cat /proc/version', hide=True)
    print(run_result.stdout)


def is_apt():
    """
    :return:
    """
    run_result = cxn.run('command -v apt', hide=True)
    if run_result.ok:
        return True
    else:
        return False


def is_yum():
    run_result = cxn.run('command -v yum', hide=True)
    if run_result.ok:
        return True
    else:
        return False


def install_packages_base():
    """
    facter -> collect and display facts about the system
    :return:
    """
    if is_apt():
        cxn.sudo(
            'apt update && apt install -y '
            'apt-transport-https ca-certificates openssl libssl-dev curl bash-completion '
            'ruby facter '
            'ntp ntp-doc '
            'bash-completion command-not-found '
            'net-tools iputils-ping dnsutils',
            hide=True, warn=True, pty=True, watchers=[sudo_pass_auto_respond])
    elif is_yum():
        cxn.sudo(
            'yum install -y epel-release && yum makecache fast',
            hide=True, warn=True, pty=True, watchers=[sudo_pass_auto_respond])
        cxn.sudo(
            'yum install -y ca-certificates openssl openssl-devel curl rpm gnupg2 nss bash-completion '
            'facter ruby-json '
            'ntp ntpdate ntp-doc '
            'bash-completion PackageKit-command-not-found '
            'net-tools iputils bind-utils '
            'yum-plugin-fastestmirror',
            hide=True, warn=True, pty=True, watchers=[sudo_pass_auto_respond])
    else:
        raise Exit("install_packages_base failed.")


def get_system_info_from_facter():
    """
    facter - Gather system information, Collect and display facts about the system.
    :return: str in json
    """
    run_result = cxn.sudo('facter --json', hide=True, warn=True)
    if run_result.ok:
        return run_result.stdout
    else:
        return None


def get_system_product_uuid():
    """
    https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/#verify-the-mac-address-and-product-uuid-are-unique-for-every-node

    /sys/class/dmi/id/product_uuid:
        The main board product UUID, as set by the board manufacturer and encoded in the BIOS DMI information.
        It may be used to identify a mainboard and only the mainboard.
        It changes when the user replaces the main board. Also,
        often enough BIOS manufacturers write bogus serials into it.
        In addition, it is x86-specific. Access for unprivileged users is forbidden.
        Hence it is of little general use.

    Other info:
        /sys/class/dmi/id/board_serial:
            /Service Tag/Serial Number/

    :return:
    """
    run_result = cxn.sudo("cat /sys/class/dmi/id/product_uuid", hide=True, warn=True)
    if run_result.ok:
        return run_result.stdout
    else:
        return None


def configuring_kernel_parameters():
    kernel_parameters = """
# Best Practices and Tuning Recommendations
# http://docs.oracle.com/cd/B28359_01/install.111/b32002/pre_install.htm#LADBI246
# https://www.ibm.com/support/knowledgecenter/en/linuxonibm/liaag/wkvm/wkvm_c_tune_tcpip.htm
fs.aio-max-nr = 1048576
fs.file-max = 6815744
kernel.core_uses_pid = 1
kernel.hung_task_timeout_secs = 0
kernel.msgmax = 65536
kernel.msgmnb = 65536
kernel.sem = 250 32000 100 128
kernel.shmall = 4294967295
kernel.shmmax = 68719476736
kernel.shmmni = 4096
kernel.sysrq = 0
net.core.netdev_max_backlog = 262144
net.core.rmem_default = 8388608
net.core.rmem_max = 16777216
net.core.somaxconn = 262144
net.core.wmem_default = 8388608
net.core.wmem_max = 16777216
net.ipv4.conf.default.accept_source_route = 0
net.ipv4.conf.default.rp_filter = 1
net.ipv4.ip_forward = 0
net.ipv4.ip_local_port_range = 9000 65500
net.ipv4.tcp_fin_timeout = 1
net.ipv4.tcp_keepalive_time = 1200
net.ipv4.tcp_max_orphans = 3276800
net.ipv4.tcp_max_syn_backlog = 262144
net.ipv4.tcp_max_tw_buckets = 6000
net.ipv4.tcp_mem = 94500000 915000000 927000000
net.ipv4.tcp_rmem = 4096 87380 4194304
net.ipv4.tcp_wmem = 4096 16384 4194304
net.ipv4.tcp_sack = 1
net.ipv4.tcp_synack_retries = 5
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_syn_retries = 5
net.ipv4.tcp_timestamps = 0
net.ipv4.tcp_tw_recycle = 1
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_window_scaling = 1
vm.swappiness = 10
"""
    cxn.run('sudo cp /etc/sysctl.conf /etc/sysctl.conf$(date +%Y%m%d%H%M%S)~', pty=True,
            watchers=[sudo_pass_auto_respond])
    cxn.run("echo -e '{}' | sudo tee /etc/sysctl.conf".format(kernel_parameters), hide=True, pty=True,
            watchers=[sudo_pass_auto_respond])


def add_security_limits(domain, type_, item, value):
    """
    design as '/etc/security/limits.conf', see the file '/etc/security/limits.conf' for more infomation
    :param domain: username or a group name, with @group syntax or the wildcard * for default entry
    :param type_: soft or hard
    :param item: nofile, nproc, stack, etc
    :param value:
    :return:

    """

    cxn.run(
        'echo "{domain} {type_} {item} {value}" | sudo tee -a /etc/security/limits.d/90-user.conf'.format(
            domain=domain,
            type_=type_,
            item=item,
            value=value),
        warn=True,
        pty=True, watchers=[sudo_pass_auto_respond])

    print("set security limits '{domain} {type_} {item} {value}' success.".format(
        domain=domain,
        type_=type_,
        item=item,
        value=value))


def set_security_limits():
    """
    nofile - max number of open files, 1024, 65536
    nproc - max number of processes, 2047, 16384
    stack - max stack size (KB), 10240, 32768
    """
    text_of_limits = """
{username} soft nofile 1024
{username} hard nofile 65536
{username} soft nproc 2047
{username} hard nproc 16384
{username} soft stack 10240
{username} hard stack 32768
    """.format(username=username)

    security_limits_file = '/etc/security/limits.d/90-user.conf'
    do_uniq_file_content = False
    if is_remote_file_exist(security_limits_file):
        tee_option = '-a'
        print("WARN: file {filename} is exists, some line maybe repetitive.".format(filename=security_limits_file))
        do_uniq_file_content = True
    else:
        tee_option = ''

    cxn.run("echo -e '{text}' | sudo tee {option} {filename}".format(text=text_of_limits,
                                                                     option=tee_option, filename=security_limits_file),
            hide=True, pty=True,
            watchers=[sudo_pass_auto_respond])

    if do_uniq_file_content:
        print("WARN: file {filename} maybe resorted.".format(filename=security_limits_file))
        if is_apt():  # sort (GNU coreutils) 8.25
            cxn.run("sort -u {filename} | tee {filename}".format(filename=security_limits_file))
        elif is_yum():  # sort (GNU coreutils) 8.4
            cxn.run("sort -u {filename} -o {filename}".format(filename=security_limits_file))


def performance_tuning():
    set_security_limits()
    configuring_kernel_parameters()


def create_user(user, passwd, is_super=False):
    print("creating user with a password.")
    run_result = cxn.run('sudo useradd {user}'.format(user=user), warn=True, pty=True,
                         watchers=[sudo_pass_auto_respond])
    if run_result.ok:
        print("user created.")
    elif "useradd: user '{}' already exists".format(user) in run_result.stdout:
        print("useradd: user '{}' already exists".format(user))
    else:
        raise Exit("useradd user failed.")

    run_result = cxn.run('echo "{user}:{password}" | sudo chpasswd'.format(user=user, password=passwd),
                         pty=True,
                         warn=True,
                         watchers=[sudo_pass_auto_respond])
    if run_result.failed:
        raise Exit("passwd user failed.")
    else:
        print("passwd user success.")

    if is_super:
        cxn.run('echo "{username} ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/{username}'.format(username=user),
                warn=True,
                pty=True, watchers=[sudo_pass_auto_respond])
        cxn.run('sudo chmod 0440 /etc/sudoers.d/{username}'.format(username=user),
                warn=True,
                pty=True, watchers=[sudo_pass_auto_respond])
        print("enable sudo success.")


def is_remote_file_exist(path):
    if cxn.sudo('test -e {}'.format(path), warn=True).failed:
        return False
    else:
        return True


def upload_file(src, dst):
    try:
        cxn.put(src, dst)
    except IOError as e:
        if "Permission denied" in e:
            tmp_dst = "/tmp/" + (src.split("/")[-1] if "/" in src else src.split("\\")[-1])
            cxn.put(src, tmp_dst)
            cxn.sudo("mv {tmp_dst} {dst}".format(tmp_dst=tmp_dst, dst=dst), pty=True,
                     watchers=[mv_answer_yes_auto_respond])


def append_text_to_file(text, path):
    cxn.run('cp {path} {path}$(date +%Y%m%d%H%M%S)~'.format(path=path))
    cxn.run("echo -e '{}' | tee -a /etc/profile".format(text))


def override_text_to_file(text, path):
    cxn.run('cp {path} {path}$(date +%Y%m%d%H%M%S)~'.format(path=path))
    cxn.run("echo -e '{}' | tee /etc/profile".format(text))


def create_directory(path):
    if cxn.run('test -d {}'.format(path), warn=True).failed:
        cxn.run('mkdir -p {}'.format(path))


def create_biz_directories():
    """
    biz is stand for business
    e.g: /opt/<company abbr>/<sub-biz abbr>/{data, log}
    :return:
    """
    pass


if __name__ == '__main__':
    for host in hosts_ssh_config.strip().split("\n"):
        # get host config from 'hosts_ssh_config'
        name, ip, port, username, password, is_sudo, tag, description = host.strip().split(",")  # type: (str,)

        # connection config
        fabric_config = Config()
        fabric_config['load_ssh_config'] = False
        fabric_config['port'] = int(port)
        fabric_config['user'] = username
        fabric_config['sudo'] = {'password': password}
        fabric_config['connect_kwargs'] = {
            'password': password,
            "key_filename": r"C:\Users\dgden\.ssh\ebt-linux-centos-ssh-root-key.pem",
        }

        # Superuser privileges via auto-response
        sudo_pass_auto_respond = Responder(
            pattern=r'\[sudo\] password:',
            response=password + '\n',
        )
        sudo_pass_auto_respond_for_user = Responder(
            pattern=r'\[sudo\] password for {user}:'.format(user=username),
            response=password + '\n',
        )

        # Superuser privileges via auto-response
        mv_answer_yes_auto_respond = Responder(
            pattern=r'mv: replace',
            response='y\n',
        )

        # create ssh connection
        cxn = Connection(ip, config=fabric_config)

        show_system_dist_and_version()

        add_ssh_key()

        performance_tuning()

        install_packages_base()

        wanted_username = 'user'
        wanted_password = 'password'
        create_user(wanted_username, wanted_password, is_super=False)
