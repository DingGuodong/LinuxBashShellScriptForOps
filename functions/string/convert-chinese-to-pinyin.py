#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:convert-chinese-to-pinyin.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2021/3/16
Create Time:            14:30
Description:            Convert Chinese characters to Pinyin
Long Description:       
References:             
Prerequisites:          pip install pypinyin
                        pip install jieba
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
import jieba
from pypinyin import lazy_pinyin

# company_type_set = {
#     u"股份有限公司",
#     u"有限责任公司"
#     u"有限公司",
# }

company_type_list = [u"公司", u"有限", u"责任", u"股份"]
biz_type_list = [u"保险代理", u"保险经纪", u"保险", ]


def remove_company_type(company_name):
    for company_type in company_type_list:
        company_name = company_name.replace(company_type, u"")
    return company_name


def remove_biz_type(company_name):
    for biz_type in biz_type_list:
        company_name = company_name.replace(biz_type, u"")
    return company_name


def get_company_name_and_brief(company_name):
    jieba_list = list(jieba.cut(company_name))

    if 2 >= len(jieba_list) >= 1:
        company_name_brief = jieba_list[0]
    elif 3 >= len(jieba_list) >= 2:
        company_name_brief = u"".join(jieba_list[0:1])
    elif 5 >= len(jieba_list) >= 3:
        company_name_brief = u"".join(jieba_list[0:2])
    else:
        company_name_brief = u"".join(jieba_list[0:3])

    company_name_brief = remove_biz_type(company_name_brief)

    print company_name.encode("utf-8"), company_name_brief.encode("utf-8"), "".join(lazy_pinyin(company_name_brief))


if __name__ == '__main__':
    company_name_list = [
        u"山东大有保险代理股份有限公司",  # test case
        u"升宏保险代理有限公司",
        u"安信联合保险经纪有限公司",
        u"重庆恒蕴汽车保险代理有限公司",
        u"黑龙江善邦保险代理有限公司",
        u"国泰家和保险代理有限公司",  # "和"
        u"北京易才宏业保险经纪有限公司"
    ]
    for com_name in company_name_list:
        get_company_name_and_brief(com_name)
