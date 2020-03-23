#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:python-get-sites.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/3/19
Create Time:            16:24
Description:            get IIS info from cmdline
Long Description:
                        # 获取网站站点基本信息
                        C:\Windows\System32\inetsrv\appcmd.exe list site "Default Web Site" /xml
                        # 获取网站物理路径
                        C:\Windows\System32\inetsrv\appcmd.exe list vdir "Default Web Site/" /xml


References:             [Getting Started with AppCmd.exe](https://docs.microsoft.com/en-us/iis/get-started/getting-started-with-iis/getting-started-with-appcmdexe)
Prerequisites:          pip install pywin32
                        pip install requests
                        pip install beautifulsoup4
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
# import win32com.client
#
# iis = win32com.client.GetObject('IIS://localhost/w3svc')
# print iis


import os
import subprocess
import xml.etree.ElementTree as ET

import requests
import shutil
from bs4 import BeautifulSoup

src_string = '''
    <td>
        src
    </td>
'''.strip()

dst_string = r'''
    <td>
        dst
    </td>
'''.strip()


def run_command(executable):
    """
    run system command by subprocess.Popen in silent
    :param executable: executable command
    :return: return_code, stdout, stderr
    """
    proc_obj = subprocess.Popen(executable, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc_obj.communicate()
    return_code = proc_obj.returncode
    return return_code, stdout, stderr


def get_list_site_xml():
    """
    appcmd list site in xml format
    :return:
    """
    appcmd_list_site_command = r'C:\Windows\System32\inetsrv\appcmd.exe list site /xml'
    return_code, stdout, stderr = run_command(appcmd_list_site_command)
    if return_code == 0:
        return stdout
    else:
        raise RuntimeError(stderr)


def get_list_vdir_root_xml(name):
    """
    appcmd list vdir in xml format
    :param name:
    :return:
    """
    appcmd_list_site_command = r'C:\Windows\System32\inetsrv\appcmd.exe list vdir "{site_name}/" /xml'.format(
        site_name=name)
    return_code, stdout, stderr = run_command(appcmd_list_site_command)
    if return_code == 0:
        return stdout
    else:
        raise RuntimeError(stderr)


def get_iis_sites_from_xml(xml_content):
    root = ET.fromstring(xml_content)
    return [site_name.get("SITE.NAME") for site_name in root.iter("SITE")]


def get_biz_site_names(sites):
    # type: (list)->list
    return [site for site in sites if site.endswith(".com")]


def get_iis_site_path_from_xml(xml_content):
    root = ET.fromstring(xml_content)
    for s in root.iter('VDIR'):
        return s.get("physicalPath")


def get_company_name_from_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Accept': "text/html, application/xhtml+xml, image/jxr, */*",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': 'zh-Hans-CN, zh-Hans; q=0.5',
    }

    try:
        response = requests.request("GET", url, headers=headers)
    except requests.exceptions.ConnectionError as e:
        print(url, e)
        return None

    if response.ok:
        wanted_html = response.text

        soup = BeautifulSoup(wanted_html, 'html.parser')

        wanted_tag_t1 = soup.find("span", attrs={'id': 'Label_UserName'})
        wanted_tag_t0 = soup.find("span", attrs={'id': 'Label_SystemName'})
        wanted_tag = wanted_tag_t1 or wanted_tag_t0

        if wanted_tag:
            sys_name = u"核心业务处理系统"
            company_name = wanted_tag.text  # type: unicode
            if sys_name in company_name:
                return company_name.strip(sys_name)
            else:
                return company_name


def backup_file(src):
    dst = src + "~"
    shutil.copy2(src, dst)


def replace_gbk_file_content(path):
    with open(path) as in_fp:
        content = in_fp.read()
    content = content.replace(src_string.decode("utf-8").encode("gbk"), dst_string.decode("utf-8").encode("gbk"))

    with open(path, 'w') as out_fp:
        out_fp.write(content)


if __name__ == '__main__':
    iis_sites_xml = get_list_site_xml()
    sites_list = get_iis_sites_from_xml(iis_sites_xml)
    biz_sites_list = get_biz_site_names(sites_list)

    for biz_site in biz_sites_list:
        biz_site_com_name = get_company_name_from_html('http://' + biz_site + '/osapcs/')

        iis_vdirs_xml = get_list_vdir_root_xml(biz_site)
        site_path = get_iis_site_path_from_xml(iis_vdirs_xml)

        default_path = os.path.join(site_path, 'osapcs/Default.aspx')
        if os.path.exists(default_path):
            with open(default_path) as fp:
                page_content = fp.read().decode("gbk").encode("utf-8")
            if src_string in page_content:
                backup_file(default_path)
                replace_gbk_file_content(default_path)
                print "OK", biz_site, biz_site_com_name, site_path, default_path
            else:
                print "Fail", biz_site, biz_site_com_name, site_path, None
        else:
            print "NotFound", biz_site, biz_site_com_name, site_path,
