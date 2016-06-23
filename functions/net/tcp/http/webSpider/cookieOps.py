#!/usr/bin/python
# -*- coding: utf-8 -*-
# Do not reinventing the wheel
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
    req = urllib2.Request(u)
    o = urllib2.build_opener(urllib2.HTTPCookieProcessor(c))
    r = o.open(req)

f = 'cookie.txt'
if os.path.exists(f) and os.path.isfile(f):
    m = hashlib.md5()
    with open(f, 'rb') as fp:
        while True:
            blk = fp.read(4096)  # 4KB per block
            if not blk:
                break
            m.update(blk)
    print m.hexdigest(), f

if c is not None:
    find = dict()
    find['wd'] = "python"
    s = "https://www.baidu.com/s"
    wd = urllib.urlencode(find)
    url = s + "?" + wd
    req = urllib2.Request(url)
    req.add_header('User-Agent',
                   "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36")
    resp = urllib2.urlopen(req)
    print req.headers
