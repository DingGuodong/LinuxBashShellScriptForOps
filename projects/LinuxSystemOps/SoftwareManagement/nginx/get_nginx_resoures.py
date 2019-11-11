#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:get_nginx_resoures.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/8/6
Create Time:            13:57
Description:            retrieve, fetch, find latest version of packages(Nginx/OpenSSL/PCRE/Zlib)'s URL
                        render "nginx-install-update.sh", replace old versions with latest versions

Long Description:
References:             
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
 """

import re
from multiprocessing import Pool
from urlparse import urlparse, urlunsplit

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/54.0.2840.99 Safari/537.36',
}


def fn_timer(func):
    from functools import wraps

    @wraps(func)
    def function_timer(*args, **kwargs):
        import time
        time_begin = time.time()
        result = func(*args, **kwargs)
        time_end = time.time()
        print "Total time running {function_name}: {time_spent} seconds".format(function_name=func.func_name,
                                                                                time_spent=(time_end - time_begin))

        return result

    return function_timer


def confirm(question, default=True):
    """
    Ask user a yes/no question and return their response as True or False.

    :parameter question:
    ``question`` should be a simple, grammatically complete question such as
    "Do you wish to continue?", and will have a string similar to " [Y/n] "
    appended automatically. This function will *not* append a question mark for
    you.
    The prompt string, if given,is printed without a trailing newline before reading.

    :parameter default:
    By default, when the user presses Enter without typing anything, "yes" is
    assumed. This can be changed by specifying ``default=False``.

    :return True or False
    """
    # Set up suffix
    if default:
        suffix = "Y/n"
    else:
        suffix = "y/N"
    # Loop till we get something we like
    while True:
        response = raw_input("%s [%s] " % (question, suffix)).lower()
        # Default
        if not response:
            return default
        # Yes
        if response in ['y', 'yes']:
            return True
        # No
        if response in ['n', 'no']:
            return False
        # Didn't get empty, yes or no, so complain and loop
        print("I didn't understand you. Please specify '(y)es' or '(n)o'.")


def get_nginx_url():
    downloads_page_url = 'https://nginx.org/en/download.html'  # type: str
    scheme = urlparse(downloads_page_url).scheme
    netloc = urlparse(downloads_page_url).netloc
    base_url = urlunsplit((scheme, netloc, '', '', ''))

    file_url_list = list()

    content = requests.get(downloads_page_url, headers=headers)
    Soup = BeautifulSoup(content.text, 'lxml')
    available_version = Soup.find('div', id="content").find_all("a")
    for link in available_version:
        pattern = re.compile(r'.*\.tar\.gz$')
        match = pattern.search(link.get("href"))
        if match:
            file_url_list.append(base_url + match.group())

    print file_url_list[1]  # 0 is Mainline version, 1 is Stable version
    return file_url_list[1]


def get_openssl_url():
    downloads_page_url = 'https://www.openssl.org/source/'  # type: str
    file_url_list = list()
    latest_version = ""
    file_url = ""

    content = requests.get(downloads_page_url, headers=headers)
    Soup = BeautifulSoup(content.text, 'lxml')
    available_version = Soup.find('div', class_="entry-content").find_all('a')

    for link in available_version:
        pattern = re.compile(r'.*\.tar\.gz$')
        match = pattern.search(link.get("href"))
        if match:
            file_url_list.append(downloads_page_url + match.group())

    latest_version_mass = Soup.find('div', class_="entry-content").find_all('p')
    pattern = re.compile(r'The latest stable version is the (.*) series\.')
    match = pattern.search(str(latest_version_mass))
    if match:
        latest_version = match.groups()[0]

    number = 0
    for number, item in enumerate(file_url_list):
        if latest_version != "" and latest_version in file_url_list[number]:
            file_url = file_url_list[number]
            break
    if file_url == "":
        file_url = file_url_list[number]
        print file_url
    else:
        print file_url

    return file_url


def get_pcre_url():
    downloads_page_url = 'https://ftp.pcre.org/pub/pcre/'
    file_url_list = list()

    content = requests.get(downloads_page_url, headers=headers)
    Soup = BeautifulSoup(content.text, 'lxml')
    available_version = Soup.find_all('a')

    for link in available_version:
        pattern = re.compile(r'pcre-.*\.tar\.gz$')
        match = pattern.search(link.get("href"))
        if match:
            file_url_list.append(downloads_page_url + match.group())

    print file_url_list[-1]  # latest version
    return file_url_list[-1]


def get_zlib_url():
    downloads_page_url = 'http://zlib.net/'
    file_url_list = list()

    content = requests.get(downloads_page_url, headers=headers)
    Soup = BeautifulSoup(content.text, 'lxml')
    available_version = Soup.find_all('a')

    for link in available_version:
        pattern = re.compile(r'zlib-.*\.tar\.gz$')
        match = pattern.search(link.get("href"))
        if match:
            file_url_list.append(downloads_page_url + match.group())

    print file_url_list[0]
    return file_url_list[0]


def get_version_from_url(url):
    if str(url).endswith(".tar.gz"):
        return str(url).strip().split("/")[-1].replace(".tar.gz", "")


def instantiate(x):
    return x()


def render_file(versions):
    """
    render "nginx-install-update.sh", replace old versions with latest versions
    :param versions: tuple or list which has 4 items
    :return:
    """
    nginx_ver, openssl_ver, pcre_ver, zlib_ver = ('',) * 4
    if len(versions) == 4:
        nginx_ver, openssl_ver, pcre_ver, zlib_ver = versions
    else:
        exit(1)

    # Tips: "\\n" == r"\n" == r'\n',"\n" == '\n', so using '\n' when you need line separator
    # TODO(Guodong) use os.linesep to replace "\n"
    pattern_nginx_ver = re.compile(r'(.*NGINX_SOURCE_LATEST_VERSION=")(.*?)("\n.*)')
    pattern_openssl_ver = re.compile(r'(.*OPENSSL_SOURCE_LATEST_VERSION=")(.*?)("\n.*)')
    pattern_pcre_ver = re.compile(r'(.*PCRE_SOURCE_LATEST_VERSION=")(.*?)("\n.*)')
    pattern_zlib_ver = re.compile(r'(.*ZLIB_SOURCE_LATEST_VERSION=")(.*?)("\n.*)')

    with open("nginx-install-update.sh", 'r') as fp_origin:
        content = fp_origin.read()
        print content.split("\n")[27:31]
        # print pattern_nginx_ver.search(content).group(2)
        content = re.sub(pattern_nginx_ver, r'\1%s\3' % nginx_ver, content)
        content = pattern_openssl_ver.sub(r"\1%s\3" % openssl_ver, content)
        content = pattern_pcre_ver.sub(r"\1%s\3" % pcre_ver, content)
        content = pattern_zlib_ver.sub(r"\1%s\3" % zlib_ver, content)
        print content.split("\n")[27:31]

    with open("nginx-install-update.sh", 'w') as fp_modified:
        fp_modified.write(content)


if __name__ == '__main__':
    p = Pool(4)
    res_list = p.map(instantiate, [get_nginx_url, get_openssl_url, get_pcre_url, get_zlib_url])
    print res_list
    for res in res_list:
        print get_version_from_url(res)

    if confirm("It is ok?"):
        res_list = [get_version_from_url(res) for res in res_list]
        render_file(res_list)
    else:
        exit(1)
