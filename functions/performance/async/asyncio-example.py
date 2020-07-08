#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:asyncio-example.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/7/8
Create Time:            11:19
Description:            asyncio example
Long Description:       
References:             [python 的协程和异步](https://zhuanlan.zhihu.com/p/42406700)
Prerequisites:          pip3 install aiohttp
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
import asyncio

import aiohttp


async def get_response(arg):
    print(arg[0])
    async with aiohttp.ClientSession() as session:
        async with session.get(arg[1]) as resp:
            print(arg[0], resp.status)


if __name__ == '__main__':
    urls = [
        ('A', 'https://movie.douban.com/top250'),
        ('B', 'https://movie.douban.com/top250?start=25&filter='),
        ('C', 'https://movie.douban.com/top250?start=50&filter=')
    ]

    tasks = [
        asyncio.ensure_future(get_response(urls[0])),
        asyncio.ensure_future(get_response(urls[1])),
        asyncio.ensure_future(get_response(urls[2]))
    ]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
