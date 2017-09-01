#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:checkIfInBlockLists.py
User:               Guodong
Create Date:        2017/8/9
Create Time:        11:39
Description:        check if domain name or ip in block lists
References:         
 """
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys


def bl_urlbl(domain):
    url = "https://admin.uribl.com/"

    querystring = {"section": "lookup"}

    payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n" \
              "Content-Disposition: form-data; name=\"domains\"\r\n\r\n{domains}\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n" \
              "Content-Disposition: form-data; name=\"section\"\r\n\r\nlookup\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\n" \
              "Content-Disposition: form-data; name=\"method\"\r\n\r\n\r\n" \
              "------WebKitFormBoundary7MA4YWxkTrZu0gW--".format(domains=domain)
    headers = {
        'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
        'referer': "https://admin.uribl.com/?section=lookup",
        'cache-control': "no-cache",
        'postman-token': "f4a0f3d0-6589-af06-f1cb-a4648600afdf"
    }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

    soup = BeautifulSoup(response.text, 'lxml')
    lookup_results = soup.find('table', class_="lookup_form").find_all('span')
    for item in lookup_results:
        if item['title'] != '':
            return item['title']


def bl_spamhaus(domain):
    # https://www.spamhaus.org/query/ip/124.129.14.90, need JavaScript support
    # This lookup tool is for manual (non-automated) lookups only.
    # Any perceived use of automated tools to access this web lookup system will
    # result in firewalling or other countermeasures.

    # http://selenium-python.readthedocs.io/
    # http://selenium-python.readthedocs.io/installation.html#drivers

    # Python pip egg: spam-blocklists
    # from spam.spamhaus import SpamHausChecker
    pass


class PythonOrgSearch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("http://www.python.org")
        self.assertIn("Python", driver.title)
        elem = driver.find_element_by_name("q")
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)
        assert "No results found." not in driver.page_source

    def tearDown(self):
        self.driver.close()


class SpamhausOrgSearch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get("https://www.spamhaus.org/lookup/")
        self.assertIn("Blocklist Removal Center", driver.title)
        elem = driver.find_element_by_name("ip")
        elem.send_keys("124.129.14.90")
        elem.send_keys(Keys.RETURN)
        assert "Please turn JavaScript on and reload the page." not in driver.page_source

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
