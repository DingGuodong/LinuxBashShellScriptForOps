# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:ping-url-etc.py
Version:                0.0.1
Author:                 guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/09/03
Create Time:            10:57:19
Description:            ping a url as ping a ip or domain name
Long Description:       
Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 2.6
Programming Language:   Python :: 2.7
Topic:                  Utilities
TODO(Guodong): using `pyinstaller` to pack this script into ONE executable file(such as p.exe)
Update:                 add arguments supports
"""
import os
import sys

import six


def get_domain_name_from_url(url):
    # https://stackoverflow.com/questions/9626535/get-domain-name-from-url
    # https://docs.python.org/3/library/urllib.parse.html
    # https://docs.python.org/2/library/urlparse.html
    if six.PY3:
        from urllib.parse import urlparse
    else:
        from urlparse import urlparse

    parsed_uri = urlparse(url)
    # domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    domain_name = "{uri.netloc}".format(uri=parsed_uri)
    if domain_name != "":
        return domain_name
    else:
        # return original url, usually as parsed_uri.path
        return url


def run_ping(destination, option=""):
    command = "ping.exe {} {}".format(option, destination)
    try:
        os.system(command)
    except KeyboardInterrupt:
        sys.exit(0)


def find_max_len_item(the_list):
    """
    find the max length string in the list
    :param the_list: A list of strings
    :type the_list: list
    :return: a string in the list
    :rtype: str
    """
    return max(the_list, key=len)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("USAGE: {} option destination".format(sys.argv[0]))
        exit(1)

    host = sys.argv[1]
    if host.startswith("http"):
        host = get_domain_name_from_url(host).split(":")[0]
        run_ping(host, " ".join(sys.argv[2:]))
    else:
        host = find_max_len_item(sys.argv[1:])

        cur_option = sys.argv[1:]
        cur_option.remove(host)
        host = get_domain_name_from_url(host).split(":")[0]
        run_ping(host, " ".join(cur_option))
