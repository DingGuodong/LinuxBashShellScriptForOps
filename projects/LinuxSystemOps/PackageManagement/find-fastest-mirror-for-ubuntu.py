#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:find-fastest-mirror-for-ubuntu.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/8/24
Create Time:            16:42
Description:            select the fastest apt mirror on Ubuntu Linux
Long Description:
current fastest apt mirror on Ubuntu Linux in China Mainland is: http://mirrors.aliyun.com/ubuntu/
```
sed -i 's@http://cn.archive.ubuntu.com/ubuntu/@http://mirrors.aliyun.com/ubuntu/@g' /etc/apt/sources.list
```
References:             [How to select the fastest apt mirror on Ubuntu Linux](https://linuxconfig.org/how-to-select-the-fastest-apt-mirror-on-ubuntu-linux)
Prerequisites:          pip install requests ping
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
import ping
import requests


def get_mirrors_list():
    url = 'http://mirrors.ubuntu.com/mirrors.txt'
    resp = requests.get(url)
    if resp.ok:
        mirrors_list = resp.text
        return mirrors_list.strip().split("\n")


def get_domain_name_from_url(url):
    # type: (str) -> str
    # https://stackoverflow.com/questions/9626535/get-domain-name-from-url
    # https://docs.python.org/2/library/urlparse.html
    from urlparse import urlparse
    parsed_uri = urlparse(url)
    # domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    domain_name = "{uri.netloc}".format(uri=parsed_uri)
    return domain_name


def ping_icmp_net_latency(dest_addr):
    percent, max_rtt, avrg_rtt = ping.quiet_ping(dest_addr)
    return percent, max_rtt, avrg_rtt


def get_fastest_mirror_host():
    fastest_mirror = None
    mirror_list = get_mirrors_list()
    for mirror in mirror_list:
        domain = get_domain_name_from_url(mirror)
        percent, max_rtt, avrg_rtt = ping_icmp_net_latency(domain)
        if percent == 0:
            print(mirror, percent, max_rtt, avrg_rtt)
            if fastest_mirror is None:
                fastest_mirror = mirror, percent, max_rtt, avrg_rtt
            else:
                if fastest_mirror[3] > avrg_rtt:
                    fastest_mirror = mirror, percent, max_rtt, avrg_rtt
    return mirror_list, fastest_mirror


def get_fastest_mirror_url():
    mirror_list, fastest_mirror = get_fastest_mirror_host()
    for mirror in mirror_list:
        if fastest_mirror[0] in mirror:
            return mirror


if __name__ == '__main__':
    fastest_mirror_url = get_fastest_mirror_url()
    print("fastest apt mirror on Ubuntu Linux is: {}".format(fastest_mirror_url))

    print('sudo cp /etc/apt/sources.list /etc/apt/sources.list$(date +%Y%m%d$H%M%S)~')
    print('''grep -oP '(?<=://)(.*)(?=.archive)' /etc/apt/sources.list| head -n1''')
    print(r"sudo sed -i -e 's/http:\/\/cn.archive/mirror:\/\/mirrors/' "
          r"-e 's/\/ubuntu\//\/mirrors.txt/' /etc/apt/sources.list")

    print(r"sed -i 's@http://cn.archive.ubuntu.com/ubuntu/@{}@g' /etc/apt/sources.list".format(fastest_mirror_url))
