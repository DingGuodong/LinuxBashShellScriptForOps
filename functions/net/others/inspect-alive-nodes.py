#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:inspect-alive-nodes.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/12/27
Create Time:            17:27
Description:            inspect if node is alive using icmp and tcp
Long Description:       
References:             
Prerequisites:          pip install ping || sudo -H pip install ping
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
from __future__ import print_function

import re
from multiprocessing.pool import ThreadPool, Pool

import ipaddress
import ping
import requests
import socket
from typing import Generator

try:
    from queue import Queue  # Windows test passed
except ImportError:
    try:
        from Queue import Queue  # Linux test passed
    except ImportError:
        from multiprocessing import Queue  # others


def get_hosts_from_network(address):
    # type: (unicode) -> Generator
    """
    :param address: such as '192.168.0.0/24', '192.168.0.1/24'
    :return: generator
    """
    net_obj = ipaddress.ip_network(address, strict=False)  # allow given a host ip address, such as '10.0.0.1/8'
    return net_obj.hosts()


def is_port_can_be_connected(ip, port):
    port = int(port)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        return_code = s.connect_ex((ip, port))
        s.close()
        if return_code == 0:
            return True
    except socket.error:
        return False


def is_node_alive_with_port_opened_thread(payload):
    ip, port, queue = payload
    if is_port_can_be_connected(ip, port):
        queue.put((ip, port))


def is_node_alive_with_port_opened(ip):
    # https://nmap.org/book/nmap-services.html
    # http://www.iana.org/assignments/port-numbers
    # awk '! /^unknow/&&/tcp/ {print+$2}' /usr/share/nmap/nmap-services
    queue = Queue()
    pool = ThreadPool(200)
    pool.map(is_node_alive_with_port_opened_thread, [(ip, port, queue) for port in range(1, 65535)])
    pool.close()
    pool.join()
    for _ in range(queue.qsize()):
        print(queue.get())


def is_node_alive_with_icmp_ping(ip):
    percent_lost, mrtt, artt = ping.quiet_ping(ip, timeout=1, count=1, psize=64)
    if percent_lost == 0:
        return True
    else:
        return False


def is_node_alive_with_icmp_ping_thread(payload):
    ip, queue = payload
    if is_node_alive_with_icmp_ping(ip):
        queue.put(ip)


def get_nodes_alive_using_ping(nodes):
    queue = Queue()
    pool = ThreadPool(254)
    pool.map(is_node_alive_with_icmp_ping_thread, [(str(node), queue) for node in nodes])
    pool.close()
    pool.join()
    nodes_alive_list = list()
    for _ in range(queue.qsize()):
        host = queue.get()
        print(host)
        nodes_alive_list.append(host)
    return nodes_alive_list


def get_title_from_html(text):
    """
    also can use 'lxml' or 'BeautifulSoup'
    :param text:
    :type text: str
    :return:
    :rtype: str
    """
    pattern = re.compile('<title>(.*?)</title>')
    match = pattern.search(text)
    if match:
        groups_tuple = match.groups()
        return groups_tuple[0]
    else:
        return text


def request_ip_port_80(ip):
    """
    request a url with redirect
    :return:
    """
    url = 'http://{}/'.format(ip)

    try:
        response = requests.request('GET', url, allow_redirects=True, timeout=(2.0, 2.0))  # Defaults to ``True``.
    except requests.exceptions.ConnectTimeout:
        print("{} : {}".format(ip, "connect timeout"))
        return False
    except requests.exceptions.ReadTimeout:
        print("{} : {}".format(ip, "read timeout"))
        return False
    except requests.exceptions.SSLError:
        print("{} : {}".format(ip, "ssl error"))
        return False
    except requests.exceptions.ConnectionError:
        print("{} : {}".format(ip, "connection failed"))
        return False

    if response.ok:
        # response.content type: bytes
        print("{} : {}".format(ip, get_title_from_html(str(response.content))))
        # print("{} : {}".format(ip, get_title_from_html(response.content.decode("utf-8").encode("utf-8"))))
        # response.text    type: unicode
        print("{} : {}".format(ip, get_title_from_html(str(response.text.encode(response.encoding)))))
        return True
    else:
        return False


if __name__ == '__main__':
    given_network = u'192.168.88.0/24'  # must be unicode
    hosts = get_hosts_from_network(given_network)
    alive_nodes_list = get_nodes_alive_using_ping(hosts)

    process_pool = Pool(2)
    process_pool.map(request_ip_port_80, alive_nodes_list)

    is_node_alive_with_port_opened('192.168.88.19')
