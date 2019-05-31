#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pySpiderSeleniumPhantomjs-demo2-douban.py
User:               Guodong
Create Date:        2017/8/10
Create Time:        18:51
Description:        
References:         
 """
import datetime
import random
import re
import time
import urllib.error
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup
from selenium import webdriver


class DoubanGroupMMSpider:
    # 豆瓣小组 请不要害羞（微信公众：haixiuzu1024）
    def __init__(self):
        self.page = 0
        self.dirName = 'DoubanGroupMM'
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap["phantomjs.page.settings.resourceTimeout"] = 1000
        cap["phantomjs.page.settings.loadImages"] = True
        # cap["phantomjs.page.settings.localToRemoteUrlAccessEnabled"] = True
        self.base_cap = cap
        self.url_refer = None
        self.driver = webdriver.PhantomJS(desired_capabilities=cap)

    def getContent(self, maxPage):
        for index in range(1, maxPage + 1):
            self.LoadPageContent(self.page)

    def LoadPageContent(self, page):
        # 获取页面内容提取
        # 记录开始时间
        begin_time = datetime.datetime.now()
        url = "https://www.douban.com/group/haixiuzu/discussion?start=" + str(page)
        self.url_refer = url
        # 豆瓣害羞小组设定每一页显示25个话题，因此下一页加25
        self.page += 25
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/60.0.3112.90 Safari/537.36"
        headers = {'User-Agent': user_agent}

        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)

        # 正则获取
        pattern_link = re.compile(
            r'<tr class="">.*?<td class="title">.*?<a href="(.*?)" title="(.*?)" class="">.*?</a>.*?</td>.*?'
            r'<td nowrap="nowrap"><a href=".*?" class="">(.*?)</a></td>.*?'
            r'<td nowrap="nowrap" class="">(\d*)</td>.*?'
            r'<td nowrap="nowrap" class="time">(.*?)</td>.*?</tr>', re.S)
        items = re.findall(pattern_link, response.read().decode('utf-8'))
        for item in items:
            post_url = item[0]
            author_name = item[2]
            post_name = item[1]
            response_count = item[3]
            commit_time = item[4]
            print('发现一名叫"{author_name}"的小组成员, '
                  '发了帖子<{post_name}>，'
                  '回应数: {response_count}, '
                  '最后回应时间为: {commit_time}'.format(author_name=author_name, post_name=post_name,
                                                  response_count=response_count,
                                                  commit_time=commit_time))
            print('<{post_name}>的详情页是: {post_url}'.format(post_name=post_name, post_url=post_url))
            print('继续获取详情页面数据...')
            time.sleep(round(0.2 + random.random(), 3))
            self.getDetailPage(post_url, author_name, begin_time)
            # break  # fetch each MM per page, for debug purpose

    def getDetailPage(self, url, author_name, begin_time):
        import requests

        headers = {
            'cache-control': "no-cache",
            'postman-token': "eafdb6c0-bbcc-de6d-a23a-ae645d03d009"
        }

        response = requests.request("GET", url, headers=headers)

        if author_name in response.text:
            print("好似获取页面正常")
            try:
                soup = BeautifulSoup(response.text, 'html.parser')
                post = soup.find('div', attrs={"class": "topic-content"}).find("p")
                images = soup.find('div', attrs={"class": "topic-figure"}).find_all("img")
                if post is not None:
                    print('"{name}"写一段这样描述的话: {post_text}'.format(name=author_name, post_text=post.get_text()))
                else:
                    print("该成员没有写任何描述")
                for image in images:
                    if image is not None:
                        print('还意外的发现了一张没有被封的照片: ', image.get("src"))
                        print('不管它长得咋样，让我们先保存它...')
                    else:
                        print("图片可能被封掉了")
            except AttributeError:
                pass
        else:
            print("好似获取页面失败了, 或者豆瓣管理员更改了页面逻辑")


def kill_process(name):
    import psutil

    ProcessNameToKill = name

    # learn from getpass.getuser()
    def getuser():
        """Get the username from the environment or password database.

        First try various environment variables, then the password
        database.  This works on Windows as long as USERNAME is set.

        """
        import os

        for username in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
            user = os.environ.get(username)
            if user:
                return user

    currentUserName = getuser()

    if ProcessNameToKill in [x.name() for x in psutil.process_iter()]:
        print(("[I] Process \"%s\" is found!" % ProcessNameToKill))
    else:
        print(("[E] Process \"%s\" is NOT running!" % ProcessNameToKill))

    for process in psutil.process_iter():
        if process.name() == ProcessNameToKill:
            try:
                # non-root user can only kill its process, but can NOT kill other users process
                if process.username().endswith(currentUserName):
                    process.kill()
                    print(("[I] Process \"%s(pid=%s)\" is killed successfully!" % (process.name(), process.pid)))
            except Exception as e:
                print(e)


if __name__ == '__main__':
    kill_process('phantomjs.exe')
    spider = DoubanGroupMMSpider()
    spider.getContent(maxPage=20)
    kill_process('phantomjs.exe')
