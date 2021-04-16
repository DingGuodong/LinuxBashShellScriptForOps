#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:get-site-info.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2021/4/15
Create Time:            19:47
Description:            check if server name in nginx config can be reached
Long Description:       
References:             
Prerequisites:          pip install requests
                        pip install bs4
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
from bs4 import BeautifulSoup


def get_site_title_from_html(url):
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    #                   'Chrome/89.0.4389.114 Safari/537.36',
    #     'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,"
    #               "application/signed-exchange;v=b3;q=0.9",
    #     'Accept-Encoding': "gzip, deflate, br",
    #     'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,mt;q=0.5',
    # }

    headers = {
        'User-Agent': 'curl/7.55.1',
    }

    try:
        response = requests.request("GET", url, headers=headers, allow_redirects=True, timeout=(5, 10))
    except requests.exceptions.ConnectionError as e:
        # print((url, e))
        return False, "requests can not reached. " + str(e)
    except requests.exceptions.Timeout:
        return False, "requests timeout"
    except requests.exceptions.TooManyRedirects:
        # TODO(DingGuodong) set allow_redirects=False, then get next url from response.headers["Location"]
        return False, "too many redirects"
    except Exception as e:
        return False, str(e)

    if response.ok:
        response.encoding = 'utf-8'  # support 'utf-8' only, do not use `chardet`
        wanted_html = response.text
        soup = BeautifulSoup(wanted_html, 'html.parser')
        title = soup.find('title')
        if title is not None:
            title = title.get_text()
        else:
            title = "not found"
        return True, title
    else:
        return False, "requests fail"


def parse_data_file(filename):
    sep = ' '
    with open(filename, 'r') as fp:
        for line in fp.readlines():
            line = line.strip()
            if sep in line:
                line = line.split(sep)
            yield line


def check_site_status(hostname):
    if isinstance(hostname, list):
        # all sites use same site title when they are same group(list)
        hostname_list = list()
        requests_status_list = list()
        is_success = False
        site_title = "not found"
        for child in hostname:
            url = 'https://' + child
            is_success, site_title = get_site_title_from_html(url)
            if is_success:
                hostname_list.append(child)
            else:
                url = 'http://' + child
                is_success, site_title = get_site_title_from_html(url)
                if not is_success:
                    hostname_list.append(child + "(fail)")
                else:
                    hostname_list.append(child + '(http)')
            requests_status_list.append(is_success)
        print(" ".join(sorted(hostname_list)), "success" if all(requests_status_list) else 'fail', site_title)

    else:
        url = 'https://' + hostname
        is_success, site_title = get_site_title_from_html(url)
        if is_success:
            print(hostname, "success", site_title)
        else:
            url = 'http://' + hostname
            is_success, site_title = get_site_title_from_html(url)
            if is_success:
                print(hostname + '(http)', 'success', site_title)
            else:
                print(hostname, "fail", site_title)  # `site_title` contains the reason


if __name__ == '__main__':
    # for item in parse_data_file("web-nginx-config-server-name.txt"):
    #     check_site_status(item)

    check_site_status("github.com")
