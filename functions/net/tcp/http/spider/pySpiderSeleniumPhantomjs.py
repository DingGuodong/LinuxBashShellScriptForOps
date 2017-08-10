#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pySpiderSeleniumPhantomjs.py
User:               Guodong
Create Date:        2017/8/9
Create Time:        15:44
Description:        use selenium and phantomjs fetch Taobao MM pictures
                    Improvements: fix some bugs or improvement in old refs
References:         http://www.jianshu.com/p/3d84afc43d42
                    http://cuiqingcai.com/1001.html

 """
import urllib2
import re
import os
import datetime
from selenium import webdriver


class TaobaoMMSpider:
    def __init__(self):
        self.page = 1
        self.dirName = 'TaobaoMM'
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap["phantomjs.page.settings.resourceTimeout"] = 1000
        cap["phantomjs.page.settings.loadImages"] = True
        # cap["phantomjs.page.settings.localToRemoteUrlAccessEnabled"] = True
        self.driver = webdriver.PhantomJS(desired_capabilities=cap)

    def getContent(self, maxPage):
        for index in range(1, maxPage + 1):
            self.LoadPageContent(index)

    def LoadPageContent(self, page):
        # 获取页面内容提取
        # 记录开始时间
        begin_time = datetime.datetime.now()
        url = "https://mm.taobao.com/json/request_top_list.htm?page=" + str(page)
        self.page += 1

        USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)' \
                     ' Chrome/44.0.2403.130 Safari/537.36'
        headers = {'User-Agent': USER_AGENT}

        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)

        # 正则获取
        pattern_link = re.compile(r'<div.*?class="pic-word">.*?<img src="(.*?)".*?'
                                  r'<a.*?class="lady-name".*?href="(.*?)".*?>(.*?)</a>.*?'
                                  r'<em>.*?<strong>(.*?)</strong>.*?'
                                  r'<span>(.*?)</span>', re.S)
        items = re.findall(pattern_link, response.read().decode('gbk'))

        for item in items:
            # 头像，个人详情，名字，年龄，地区
            print u'发现一位MM 名字叫{name} 年龄{age} 坐标{location}'.format(name=item[2], age=item[3], location=item[4])
            print u'{name}的个人主页是 {website}'.format(name=item[2], website=item[1])
            print u'继续获取详情页面数据...'
            # 详情页面
            detailPage = item[1]
            name = item[2]
            self.getDetailPage(detailPage, name, begin_time)
            break  # fetch each MM per page, for debug purpose

    def getDetailPage(self, url, name, begin_time):
        url = 'https:' + url
        self.driver.get(url)
        base_msg = self.driver.find_elements_by_xpath('//div[@class="mm-p-info mm-p-base-info"]/ul/li')
        brief = ''
        for item in base_msg:
            text = item.text.replace(u'　', ' ')
            print text
            brief += text + '\n'

        icon_url = self.driver.find_element_by_xpath('//div[@class="mm-p-model-info-left-top"]//img')
        icon_url = icon_url.get_attribute('src')

        save_dir = self.dirName + '/' + name
        self.mkdir(save_dir)

        # 保存头像
        try:
            self.saveIcon(icon_url, save_dir, name)
        except Exception, e:
            print u'保存头像失败 %s' % e.message

        # 开始跳转相册列表
        images_url = self.driver.find_element_by_xpath('//ul[@class="mm-p-menu"]//a')
        images_url = images_url.get_attribute('href')
        try:
            self.getAllImage(images_url, name)
        except Exception, e:
            print u'获取所有相册异常 %s' % e.message

        end_time = datetime.datetime.now()
        # 保存个人信息 以及耗时
        try:
            self.saveBrief(brief, save_dir, name, end_time - begin_time)
        except Exception, e:
            print u'保存个人信息失败 %s' % e.message

    def getAllImage(self, images_url, name):
        # 获取所有图片
        self.driver.get(images_url)
        # 只获取第一个相册，获取第二个相册的xpath是'//*[@id="J_HerPanel"]/div/div[1]/div/h4/a'
        photos = self.driver.find_element_by_xpath('//*[@id="J_HerPanel"]/div/div[1]/div/h4/a')
        photos_url = photos.get_attribute('href')

        # 进入相册页面获取相册内容，第2张照片是'//*[@id="J_Photo_fall"]/div[2]/div/div[1]/a/img'
        self.driver.get(photos_url)
        # 获取10张照片
        images_all = list()
        for page in range(1, 10):
            images_all += self.driver.find_elements_by_xpath(
                "//*[@id=\"J_Photo_fall\"]/div[{page}]/div/div[1]/a/img".format(page=page))
        self.saveImages(images_all, name)

    def saveImages(self, images, name):
        index = 1
        print u'%s 的相册有%s张照片, 尝试全部下载....' % (name, len(images))

        for imageUrl in images:
            splitPath = imageUrl.get_attribute('src').split('.')
            fTail = splitPath.pop()
            if len(fTail) > 3:
                fTail = "jpg"
            fileName = self.dirName + '/' + name + '/' + name + str(index) + "." + fTail
            print u'下载照片地址%s ' % fileName

            self.saveImage(imageUrl.get_attribute('src'), fileName)
            index += 1

    def saveIcon(self, url, save_dir, name):
        print u'头像地址%s %s ' % (url, name)

        splitPath = url.split('.')
        fTail = splitPath.pop()
        fileName = save_dir + '/' + name + '.' + fTail
        print fileName
        self.saveImage(url, fileName)

    @staticmethod
    def saveImage(imageUrl, fileName):
        # 写入图片
        print imageUrl
        u = urllib2.urlopen(imageUrl)
        data = u.read()
        f = open(fileName, 'wb')
        f.write(data)
        f.close()

    @staticmethod
    def saveBrief(content, save_dir, name, speed_time):
        # 保存个人信息
        speed_time = u'当前MM耗时 ' + str(speed_time)
        content = content + '\n' + speed_time
        fileName = save_dir + '/' + name + '.txt'
        f = open(fileName, 'w+')
        print u'正在获取%s的个人信息保存到%s' % (name, fileName)
        f.write(content.encode('utf-8'))

    @staticmethod
    def mkdir(path):
        # 创建目录
        path = path.strip()
        print u'创建目录%s' % path
        if os.path.exists(path):
            return False
        else:
            os.makedirs(path)
            return True


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
        print "[I] Process \"%s\" is found!" % ProcessNameToKill
    else:
        print "[E] Process \"%s\" is NOT running!" % ProcessNameToKill

    for process in psutil.process_iter():
        if process.name() == ProcessNameToKill:
            try:
                # non-root user can only kill its process, but can NOT kill other users process
                if process.username().endswith(currentUserName):
                    process.kill()
                    print "[I] Process \"%s(pid=%s)\" is killed successfully!" % (process.name(), process.pid)
            except Exception as e:
                print e


if __name__ == '__main__':
    kill_process('phantomjs.exe')
    spider = TaobaoMMSpider()
    spider.getContent(maxPage=2)
    kill_process('phantomjs.exe')
