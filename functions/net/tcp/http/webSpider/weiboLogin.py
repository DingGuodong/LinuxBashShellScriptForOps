#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
# refer to https://github.com/yoyzhou/weibo_login

import os
import urllib
import urllib2
import cookielib
import base64
import re
import hashlib
import json
import rsa
import binascii


def get_prelogin_status(username):
    """
    Perform prelogin action, get prelogin status, including servertime, nonce, rsakv, etc.
    :param username:
    """
    # prelogin_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&client=ssologin.js(v1.4.5)'
    prelogin_url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=' + get_user(
        username) + '&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.11)'
    data = urllib2.urlopen(prelogin_url).read()
    p = re.compile('\((.*)\)')

    try:
        json_data = p.search(data).group(1)
        data = json.loads(json_data)
        servertime = str(data['servertime'])
        nonce = data['nonce']
        rsakv = data['rsakv']
        return servertime, nonce, rsakv
    except:
        print 'Getting prelogin status met error!'
        return None


def login(username, pwd, cookie_file):
    """
        Login with use name, password and cookies.
        (1) If cookie file exists then try to load cookies;
        (2) If no cookies found then do login
        :param username:
        :param pwd:
        :param cookie_file:
    """
    cookie_jar = None
    # If cookie file exists then try to load cookies
    if os.path.exists(cookie_file):
        try:
            cookie_jar = cookielib.LWPCookieJar(cookie_file)
            cookie_jar.load(ignore_discard=True, ignore_expires=True)
            loaded = 1
        except cookielib.LoadError:
            loaded = 0
            print 'Loading cookies error'

        # install loaded cookies for urllib2
        if loaded:
            cookie_support = urllib2.HTTPCookieProcessor(cookie_jar)
            opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
            urllib2.install_opener(opener)
            print 'Loading cookies success'
            return 1
        else:
            return do_login(username, pwd, cookie_file)

    else:  # If no cookies found
        return do_login(username, pwd, cookie_file)


def do_login(username, pwd, cookie_file):
    """"
    Perform login action with use name, password and saving cookies.
    @param username: login user name
    @param pwd: login password
    @param cookie_file: file name where to save cookies when login succeeded 
    """
    # POST data per LOGIN WEIBO, these fields can be captured using httpfox extension in FIrefox
    login_data = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'userticket': '1',
        'pagerefer': '',
        'vsnf': '1',
        'su': '',
        'service': 'miniblog',
        'servertime': '',
        'nonce': '',
        'pwencode': 'rsa2',
        'rsakv': '',
        'sp': '',
        'encoding': 'UTF-8',
        'prelt': '45',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
    }

    cookie_jar2 = cookielib.LWPCookieJar()
    cookie_support2 = urllib2.HTTPCookieProcessor(cookie_jar2)
    opener2 = urllib2.build_opener(cookie_support2, urllib2.HTTPHandler)
    urllib2.install_opener(opener2)
    login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.11)'
    try:
        servertime, nonce, rsakv = get_prelogin_status(username)
    except:
        return

    # Fill POST data
    print 'starting to set login_data'
    login_data['servertime'] = servertime
    login_data['nonce'] = nonce
    login_data['su'] = get_user(username)
    login_data['sp'] = get_pwd_rsa(pwd, servertime, nonce)
    login_data['rsakv'] = rsakv
    login_data = urllib.urlencode(login_data)
    http_headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0'}
    req_login = urllib2.Request(
        url=login_url,
        data=login_data,
        headers=http_headers
    )
    result = urllib2.urlopen(req_login)
    text = result.read()
    p = re.compile('location\.replace\(\'(.*?)\'\)')
    # 在使用httpfox登录调试时，我获取的返回参数  location.replace('http://weibo.com 这里使用的是单引号 原来的正则中匹配的是双引号# 导致没有login_url得到 单引号本身在re中无需转义
    # p = re.compile('location\.replace\(\B'(.*?)'\B\)') 经调试 这样子是错误的 re中非的使用\'才能表达单引号
    try:
        # Search login redirection URL
        login_url = p.search(text).group(1)
        data = urllib2.urlopen(login_url).read()
        # Verify login feedback, check whether result is TRUE
        patt_feedback = 'feedBackUrlCallBack\((.*)\)'
        p = re.compile(patt_feedback, re.MULTILINE)

        feedback = p.search(data).group(1)
        feedback_json = json.loads(feedback)
        if feedback_json['result']:
            cookie_jar2.save(cookie_file, ignore_discard=True, ignore_expires=True)
            return 1
        else:
            return 0
    except:
        return 0


def get_pwd_wsse(pwd, servertime, nonce):
    """
    Get wsse encrypted password
    :param pwd:
    :param servertime:
    :param nonce:
    :return:
    """
    pwd1 = hashlib.sha1(pwd).hexdigest()
    pwd2 = hashlib.sha1(pwd1).hexdigest()
    pwd3_ = pwd2 + servertime + nonce
    pwd3 = hashlib.sha1(pwd3_).hexdigest()
    return pwd3


def get_pwd_rsa(pwd, servertime, nonce):
    """
    Get rsa2 encrypted password, using RSA module from https://pypi.python.org/pypi/rsa/3.1.1, documents can be accessed at
    http://stuvel.eu/files/python-rsa-doc/index.html
    :param pwd:
    :param servertime:
    :param nonce:
    :return:
    """
    # n, n parameter of RSA public key, which is published by WEIBO.COM
    # hardcoded here but you can also find it from values return from prelogin status above
    weibo_rsa_n = 'EB2A38568661887FA180BDDB5CABD5F21C7BFD59C090CB2D245A87AC253062882729293E5506350508E7F9AA3BB77F4333231490F915F6D63C55FE2F08A49B353F444AD3993CACC02DB784ABBB8E42A9B1BBFFFB38BE18D78E87A0E41B9B8F73A928EE0CCEE1F6739884B9777E4FE9E88A1BBE495927AC4A799B3181D6442443'

    # e, exponent parameter of RSA public key, WEIBO uses 0x10001, which is 65537 in Decimal
    weibo_rsa_e = 65537
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(pwd)

    # construct WEIBO RSA Publickey using n and e above, note that n is a hex string
    key = rsa.PublicKey(int(weibo_rsa_n, 16), weibo_rsa_e)

    # get encrypted password
    crypto_pwd = rsa.encrypt(message, key)
    # turn back encrypted password binaries to hex string
    return binascii.b2a_hex(crypto_pwd)


def get_user(username):
    """
    :param username:
    :return:
    """
    username_ = urllib.quote(username)
    username = base64.encodestring(username_)[:-1]
    return username


if __name__ == '__main__':

    weibo_username = ''
    weibo_password = ''
    weibo_login_cookies_filename = 'weibo_login_cookies.dat'

    if login(weibo_username, weibo_password, weibo_login_cookies_filename):
        print 'Login WEIBO succeeded'
        test_page = urllib2.urlopen('http://weibo.com/ppnet?is_all=1').read()
        print test_page
    else:
        print 'Login WEIBO failed'
