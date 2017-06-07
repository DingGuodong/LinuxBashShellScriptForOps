#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:webBrowserEmulator.py
User:               Guodong
Create Date:        2017/4/25
Create Time:        11:57

Original Function Idea:
    write a python script to emulate Web Browser to refresh page or something else, like refresh resume, ;)
    
 """


def open_default_browser(url):
    assert url != "", "url can not be empty"
    import webbrowser
    webbrowser.open(url)


def login_with_selenium():
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys

    browser = webdriver.Firefox()

    browser.get('http://www.yahoo.com')
    assert 'Yahoo!' in browser.title

    elem = browser.find_element_by_name('p')  # Find the search box
    elem.send_keys('seleniumhq' + Keys.RETURN)

    browser.quit()


def login():
    from splinter import Browser

    login_name = "urep_pp"
    password = "DbEhppuhJ/MvU"
    url = "http://home.51cto.com/index?reback=http://dgd2010.blog.51cto.com/"
    browser = Browser('chrome')
    browser.visit(url)
    browser.find_by_id('loginform-username').fill(login_name)
    browser.find_by_id('loginform-password').fill(password)
    browser.find_by_name('login-button').click()


if __name__ == '__main__':
    pass
