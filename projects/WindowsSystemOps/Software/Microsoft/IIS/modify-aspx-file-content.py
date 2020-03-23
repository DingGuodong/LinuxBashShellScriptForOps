#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:modify-aspx-file-content.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/3/19
Create Time:            18:55
Description:            python modify html content by beautifulsoup4
Long Description:       
References:             https://beautiful-soup-4.readthedocs.io/en/latest/
                        https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/
Prerequisites:          []
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

from bs4 import BeautifulSoup

html_encoding = 'gbk'

wanted_html_part = r'''
<td style="width: 700px; height: 20px;font-size:13.5px; " valign="middle">
    <a href="https://example.com/dist/standalone.html?eid=xxx" target="_blank">xxx</a>
</td>
'''.strip().decode("utf-8")  # type: unicode

with open("Default.aspx") as fp:
    html_content = fp.read()

wanted_html = html_content.decode(html_encoding)  # type: unicode

# https://blog.csdn.net/adinlead/article/details/53897409
soup = BeautifulSoup(wanted_html, 'html.parser')  # do NOT use 'lxml' or will lost '.aspx' tags, but not good enough

wanted_res = soup.find('td', style="width: 700px; height: 20px;font-size:13.5px; ")
# Beautiful Soup replaces < with &lt;
# https://stackoverflow.com/questions/52040260/beautiful-soup-replaces-with-lt
wanted_res.replace_with(wanted_html_part)  # keep html tag in replace procedure
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#output-formatters
original_html_content = soup.encode(html_encoding, formatter=None)

with open("Default1.aspx", 'w') as fp:
    fp.write(original_html_content)
