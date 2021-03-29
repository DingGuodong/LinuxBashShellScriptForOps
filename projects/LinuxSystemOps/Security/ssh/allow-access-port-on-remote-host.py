#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:allow-access-port-on-remote-host.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2021/3/18
Create Time:            21:17
Description:            allow the public ip address of this host access a port of the remote host
Long Description:

    design thought:
    1. get public ip address of this host
    2. construct the cmd: remove old rule, add new rule
    3. execute the command on remote host via SSH protocol

Other IP APIs:
    http://ping.pe/
    https://www.ipip.net/ip.html
    https://ip138.com/
    https://ipinfo.io/
    https://ifconfig.me/
    https://httpbin.org/ip
    http://cip.cc
    https://ip.cn
    https://ident.me

References:             projects/others/aliyun/ECS/SecurityGroup/add-Internet-IP-to-aliyun-ecs-security-group.py
Prerequisites:          pip install requests
                        pip install paramiko
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

import requests

# TODO(DingGuodong) known issue: the(some) api will return IPv6 address which is not wanted.
IP_QUERY_API_S1 = "https://ifconfig.co/ip"
IP_QUERY_API_S2 = "https://api-ipv4.ip.sb/ip"


def get_public_ip_from_api(api):
    query_ip_api_url = api.strip()

    headers = {
        'Cache-Control': "no-cache",
        "User-Agent": "curl/7.55.1",
    }

    data = ""
    try:
        # Pass a (connect, read) timeout tuple, or a single float to set both timeouts to the same value
        response = requests.request("GET", query_ip_api_url, headers=headers, timeout=(10, 5))
        if response.ok:
            data = response.text.strip()
        else:
            print("API {api} status code: {code}".format(api=api, code=response.status_code))
    except Exception as _:
        del _

    return data


def get_public_ip():
    ip1, ip2 = map(get_public_ip_from_api, (IP_QUERY_API_S1, IP_QUERY_API_S2))
    ip = ip1 if ip1 != "" and ":" not in ip1 else ip2
    if ip == "":
        raise AssertionError("can NOT get IP from APIs, terminated.")
    return ip


def execute_commands_on_remote_host(host, command, **kwargs):
    import paramiko

    port = kwargs.get("port") or 22
    username = kwargs.get("username") or 'root'
    key_filename = kwargs.get("key_filename")  # os.path.expanduser(r'~/.ssh/id_rsa')
    timeout = kwargs.get("timeout") or 5

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, port=port, username=username, key_filename=key_filename, timeout=timeout)

    stdin, stdout, stderr = client.exec_command(command=command,
                                                get_pty=True)  # type: paramiko.ChannelStdinFile, list, paramiko.ChannelStderrFile
    """
    warning::   
                The server may reject this request depending on its ``AcceptEnv``
                setting; such rejections will fail silently (which is common client
                practice for this particular request type). Make sure you
                understand your server's configuration before using!
    """
    for line in stdout:
        print "Stdout: ", line,

    for line in stdout:
        print "Stderr: ", line,
    client.close()


if __name__ == '__main__':
    internet_ip = get_public_ip()
    print("Current public IP address is {}".format(internet_ip))

    # Tips: `| awk '$1=$1'` 或 `| awk 'NF--'` 去除字符串两端的（多个）空格，
    # Decrementing NF causes the values of fields past the new value to be lost,
    # and the value of $0 to  be  recomputed,  with  the  fields being separated by the value of OFS.

    command_remove_old_rule = '''firewall-cmd --permanent --zone=public ''' \
                              '''--remove-rich-rule="$(firewall-cmd --list-all | awk '/fw_temp_kw/','$1=$1')"; ''' \
                              '''firewall-cmd --reload'''

    # use `log prefix="fw_temp_kw" level="info"` as comment in firewall-cmd
    # refer: https://serverfault.com/questions/893112/migrating-from-iptables-to-firewalld-commenting-rules
    command_add_new_rule = 'firewall-cmd --permanent ' \
                           '--add-rich-rule="rule family="ipv4" source address="{ip}" ' \
                           'port protocol="tcp" port="50009" log prefix="fw_temp_kw" level="info" accept";' \
                           'firewall-cmd --reload'.format(ip=internet_ip)
    the_command = ';'.join((command_remove_old_rule, command_add_new_rule))
    # print the_command

    execute_commands_on_remote_host("47.240.129.250", the_command,
                                    port=22,
                                    username='root',
                                    key_filename=r"C:\Users\dgden\.ssh\exportedkey201310171355"
                                    )
