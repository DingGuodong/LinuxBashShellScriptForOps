#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import cookielib
import urllib
import urllib2
import optparse


# ------------------------------------------------------------------------------
# check all cookies in cookiesDict is exist in cookieJar or not
def checkAllCookiesExist(cookieNameList, cookieJar):
    cookiesDict = {}
    for eachCookieName in cookieNameList:
        cookiesDict[eachCookieName] = False

    allCookieFound = True
    for cookie in cookieJar:
        if (cookie.name in cookiesDict):
            cookiesDict[cookie.name] = True

    for eachCookie in cookiesDict.keys():
        if (not cookiesDict[eachCookie]):
            allCookieFound = False
            break

    return allCookieFound


# ------------------------------------------------------------------------------
# just for print delimiter
def printDelimiter():
    print '-' * 80


# ------------------------------------------------------------------------------
# main function to emulate login baidu
def emulateLoginBaidu():
    print "Function: Used to demostrate how to use Python code to emulate login baidu main page: http://www.baidu.com/"
    print "Usage: emulate_login_baidu_python.py -u yourBaiduUsername -p yourBaiduPassword"
    printDelimiter()

    # parse input parameters
    parser = optparse.OptionParser()
    parser.add_option("-u", "--username", action="store", type="string", default='', dest="username",
                      help="Your Baidu Username")
    parser.add_option("-p", "--password", action="store", type="string", default='', dest="password",
                      help="Your Baidu password")
    (options, args) = parser.parse_args()
    # export all options variables, then later variables can be used
    for i in dir(options):
        exec (i + " = options." + i)

    printDelimiter()
    print "[preparation] using cookieJar & HTTPCookieProcessor to automatically handle cookies"
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)

    printDelimiter()
    print "[step1] to get cookie BAIDUID"
    baiduMainUrl = "http://www.baidu.com/"
    resp = urllib2.urlopen(baiduMainUrl)
    # respInfo = resp.info()
    # print "respInfo=",respInfo
    for index, cookie in enumerate(cj):
        print '[', index, ']', cookie

    printDelimiter()
    print "[step2] to get token value"
    getapiUrl = "https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=true"
    getapiResp = urllib2.urlopen(getapiUrl)
    # print "getapiResp=",getapiResp
    getapiRespHtml = getapiResp.read()
    # print "getapiRespHtml=",getapiRespHtml
    # bdPass.api.params.login_token='5ab690978812b0e7fbbe1bfc267b90b3'
    foundTokenVal = re.search("bdPass\.api\.params\.login_token='(?P<tokenVal>\w+)'", getapiRespHtml)
    if (foundTokenVal):
        tokenVal = foundTokenVal.group("tokenVal")
        print "tokenVal=", tokenVal

        printDelimiter()
        print "[step3] emulate login baidu"
        staticpage = "http://www.baidu.com/cache/user/html/jump.html"
        baiduMainLoginUrl = "https://passport.baidu.com/v2/api/?login"
        postDict = {
            # 'ppui_logintime': "",
            'charset': "utf-8",
            # 'codestring'    : "",
            'token': tokenVal,  # de3dbf1e8596642fa2ddf2921cd6257f
            'isPhone': "false",
            'index': "0",
            # 'u'             : "",
            # 'safeflg'       : "0",
            'staticpage': staticpage,  # http%3A%2F%2Fwww.baidu.com%2Fcache%2Fuser%2Fhtml%2Fjump.html
            'loginType': "1",
            'tpl': "mn",
            'callback': "parent.bdPass.api.login._postCallback",
            'username': username,
            'password': password,
            # 'verifycode'    : "",
            'mem_pass': "on",
        }
        postData = urllib.urlencode(postDict)
        # here will automatically encode values of parameters
        # such as:
        # encode http://www.baidu.com/cache/user/html/jump.html into http%3A%2F%2Fwww.baidu.com%2Fcache%2Fuser%2Fhtml%2Fjump.html
        # print "postData=",postData
        req = urllib2.Request(baiduMainLoginUrl, postData)
        # in most case, for do POST request, the content-type, is application/x-www-form-urlencoded
        req.add_header('Content-Type', "application/x-www-form-urlencoded")
        resp = urllib2.urlopen(req)
        # for index, cookie in enumerate(cj):
        #    print '[',index, ']',cookie
        cookiesToCheck = ['BDUSS', 'PTOKEN', 'STOKEN', 'SAVEUSERID']
        loginBaiduOK = checkAllCookiesExist(cookiesToCheck, cj)
        if (loginBaiduOK):
            print "+++ Emulate login baidu is OK, ^_^"
        else:
            print "--- Failed to emulate login baidu !"
    else:
        print "Fail to extract token value from html=", getapiRespHtml


if __name__ == "__main__":
    emulateLoginBaidu()
