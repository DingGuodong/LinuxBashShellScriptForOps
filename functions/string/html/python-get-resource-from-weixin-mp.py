#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:python-get-resource-from-weixin-mp.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/6/5
Create Time:            14:19
Description:            save all wanted pictures from weixin mp
Long Description:       
References:             
Prerequisites:          pip install beautifulsoup4
                        pip install requests
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
import sys

import bs4
import requests
from bs4 import BeautifulSoup


def create_file(name, content):
    """
    create file with given name and content
    :param name: filename
    :type name: str
    :param content: content
    :type content: str
    :return: None
    :rtype: None
    """
    with open(name, 'wb') as fp:
        fp.write(content)


def get_filename_ext(link):
    """
    get extension name from URL
    :param link: URL link
    :type link: str
    :return: extension name, such as '.jpeg', '.png'
    :rtype: str
    """
    # https://xxxx/640?wx_fmt=jpeg
    # https://xxxx/640?wx_fmt=png
    # https://xxxx/640?wx_fmt=jpeg&tp=webp&wxfrom=5&wx_lazy=1&wx_co=1
    pattern = re.compile(r"http.*?\?wx_fmt=(\w{3,4})")
    match = re.search(pattern, link)
    if match:
        ext = match.groups()[0]
    else:
        ext = "png"
    return "." + ext


def save_picture_from_weixin(link, index):
    """
    save picture to local
    :param link: URL link
    :type link: str
    :param index: number
    :type index: int
    :return: None
    :rtype: None
    """
    content = get_page_content(link, content=True)
    if content:
        extension = get_filename_ext(link)
        name = filename_prefix + '_' + str(index) + extension

        create_file(name, content)
    else:
        print("failed: {}".format(link))


def get_page_content(link, content=False):
    """
    get web page content
    :param link:
    :type link:
    :param content:
    :type content: str (requests.text or requests.content)
    :return: str
    :rtype: str
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/83.0.4103.61 Safari/537.36',
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;"
                  "q=0.8,application/signed-exchange;v=b3;q=0.9",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',  # en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,mt;q=0.5
    }

    try:
        response = requests.request("GET", link, headers=headers)
    except requests.exceptions.ConnectTimeout as e:
        print(url, e)
    except requests.exceptions.ReadTimeout as e:
        print(url, e)
    except requests.exceptions.SSLError as e:
        print(url, e)
    except requests.exceptions.ConnectionError as e:
        print(url, e)
    else:
        if response.ok:
            if content:
                return response.content
            else:
                return response.text

    return None


def get_wanted_resource(link):
    wanted_html = get_page_content(link)
    if not wanted_html:
        print("failed: {}".format(link))
        sys.exit(1)

    soup = BeautifulSoup(wanted_html, 'lxml')
    wanted_tag_list = soup.find_all("img", attrs={'class': 'rich_pages'})

    index = 0
    for wanted_tag in wanted_tag_list:  # type: bs4.element.Tag
        wanted_link = wanted_tag.get("data-src")
        print(wanted_link)
        save_picture_from_weixin(wanted_link, index)
        index += 1


if __name__ == '__main__':
    url = 'https://mp.weixin.qq.com/s/yJDAEoixcKONQLdGNcyyxA'
    filename_prefix = url.split("/")[-1]
    get_wanted_resource(url)
