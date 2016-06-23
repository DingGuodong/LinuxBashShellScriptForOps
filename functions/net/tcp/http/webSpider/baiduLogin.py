#!/usr/bin/python
# -*- coding: utf-8 -*-
# Do not reinventing the wheel

# TODO
# http://developer.baidu.com/

import cookielib
import urllib2
import os
import hashlib
import urllib


def show_cookies(target):
    cookie = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    opener.open(target)
    for item in cookie:
        print 'Name = ' + item.name
        print 'Value = ' + item.value


def create_cookie_file(target):
    cookie_filename = 'cookie.txt'
    cookie = cookielib.MozillaCookieJar(cookie_filename)
    handler = urllib2.HTTPCookieProcessor(cookie)
    opener = urllib2.build_opener(handler)
    opener.open(target)
    cookie.save(ignore_discard=True, ignore_expires=True)
    return cookie


def load_cookie_file(target):
    import os
    cookie_filename = 'cookie.txt'
    if os.path.exists(cookie_filename) and os.path.isfile(cookie_filename):
        cookie = cookielib.MozillaCookieJar()
        cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
        return cookie
    else:
        return create_cookie_file(target)


u = 'http://www.baidu.com'
c = load_cookie_file(u)
if c is not None:
    values = {"userName": "", "password": "", "memberPass": ""}
    data = urllib.urlencode(values)
    url = "https://passport.baidu.com/v2/?login"
    request = urllib2.Request(url, data)
    request.add_header('User-Agent',
                       "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36")
    response = urllib2.urlopen(request)
    print response.read()
