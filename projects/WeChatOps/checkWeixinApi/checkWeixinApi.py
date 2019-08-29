#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:checkWeixinApi.py
User:               Guodong
Create Date:        2017/1/18
Create Time:        17:11
 """
from gevent import monkey

monkey.patch_all()

hosts = [
    'https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info',  # 公众平台接口通用域名
    'https://qyapi.weixin.qq.com/cgi-bin/menu/get',  # 企业号域名
    'https://login.weixin.qq.com/',  # 微信网页版
    'https://wx2.qq.com/',  # 微信网页版
    'http://weixin.qq.com/'  # 微信首页
]


def request_http(url):
    print('GET: %s' % url)
    import requests

    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/51.0.2704.106 Safari/537.36",
        'cache-control': "no-cache",
    }

    response = requests.request("GET", url, headers=headers)

    print(len(response.text), "retrieved from %s " % url)
    gevent.sleep(0.5)
    print(response.headers, "from %s " % url)


if __name__ == '__main__':
    import gevent

    gevent.joinall([gevent.spawn(request_http, host) for host in hosts])
