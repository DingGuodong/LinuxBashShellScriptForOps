# -*- coding: utf-8 -*-

import urlparse
import urllib
import urllib2
import sys
import re


def is_valid_url(p_url):
    import re
    regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    # return url is not None and regex.search(url)
    if p_url is None:
        print "url parameter is missing."
        exit(1)
    elif p_url is not None and regex.search(p_url):
        return p_url
    else:
        print "url is invalid."
        exit(1)


def get_html_charset(p_html):
    regex_html_meta_content_charset = '<meta[ ]+.*charset=([a-zA-Z]+-?[0-9]+-?[0-9]?)["\'][ ]?/>'
    regex = re.compile(regex_html_meta_content_charset, re.IGNORECASE)
    charset = regex.search(p_html)
    if charset is None:
        charset = "utf-8"
    return charset

url = "http://blog.csdn.net/"
req_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) \
    Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'gzip',
    'Connection': 'close',
    'Referer': None
}
req_timeout = 5
req = urllib2.Request(url, None, req_header)
resp = urllib2.urlopen(req, None, req_timeout)
html = resp.read()
print html

encoding_of_system = sys.getfilesystemencoding()
# encoding_of_system = sys.getdefaultencoding()

# urlAddress = "http://dgd2010.blog.51cto.com/"
# urlAddress = "http://blog.csdn.net/zhoudaxia/article/details/23176731"
urlAddress = "http://daily.zhihu.com/"
validUrlAddress = is_valid_url(urlAddress)
print urlparse.urlparse(validUrlAddress)

url_file_object = urllib.urlopen(validUrlAddress)
print "Open URL is ", url_file_object.geturl()
url_file_object_list = url_file_object.readlines()

if isinstance(url_file_object_list, list):
    print "It is a list"

for html in url_file_object_list:
    encoding_of_html_body = get_html_charset(html)

for html in url_file_object_list:
    print html
    try:
        html.decode(encoding_of_html_body)
    except Exception as e:
        print "debug trace: \n\t", e
        exit(0)
    print html.decode(encoding_of_html_body).encode(encoding_of_system)
