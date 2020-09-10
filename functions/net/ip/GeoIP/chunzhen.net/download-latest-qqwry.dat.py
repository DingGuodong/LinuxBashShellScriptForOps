#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:download-latest-qqwry.dat.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/9/10
Create Time:            11:05
Description:            download latest qqwry.dat from chunzhen.net
Long Description:       
References:

`innoextract` is a tool for extracting data from an Inno Setup installer
 Inno Setup is a tool to create installers for Microsoft Windows applications.
 Inno Extracts allows one to extract such installers under non-windows systems
 without running the actual installer using wine.

Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3
Topic:                  Utilities
 """
import os
import shutil
import sys

import requests

mswindows = (sys.platform == "win32")

qqwry_download_url = 'http://update.cz88.net/soft/setup.zip'

windows_download_url = 'https://constexpr.org/innoextract/files/' \
                       'innoextract-1.9/innoextract-1.9-windows.zip'  # may not latest version

linux_binary_download_url = 'https://constexpr.org/innoextract/files/innoextract-1.9-linux.tar.xz'

ubuntu_install_cli = 'sudo apt install innoextract -y'
centos_install_cli = 'sudo yum install innoextract -y'  # epel is required,test passed on CentOS7, failed on CentOS6


def extract_zip(path_to_zipfile, extract_to="."):
    import zipfile
    with zipfile.ZipFile(path_to_zipfile, 'r') as f:
        for filename in f.namelist():
            f.extract(filename, extract_to)


def get_file_content(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/77.0.3865.90 Safari/537.36",
        'Accept': "*/*",
        'Accept-Language': "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6,mt;q=0.5",
        'cache-control': "no-cache",
        'Connection': "close"
    }

    try:
        response = requests.request('GET', url, headers=headers, allow_redirects=True, timeout=(10.0, 10.0))
        if response.ok:
            return response.content  # type: bytes
        else:
            return b''

    except requests.exceptions.ConnectTimeout:
        print("{} : {}".format(url, "connect timeout"))
    except requests.exceptions.ReadTimeout:
        print("{} : {}".format(url, "read timeout"))
    except requests.exceptions.SSLError:
        print("{} : {}".format(url, "ssl error"))
    except requests.exceptions.ConnectionError:
        print("{} : {}".format(url, "connection failed"))

    return b''


def download_file_to_curdir(url):
    filename = url.split("/")[-1]
    content = get_file_content(url)
    if content != b'':
        with open(filename, 'wb') as fp:
            fp.write(content)
    else:
        raise IOError("download failed, try again later or choose other solution")


def download_then_extract_zip(url):
    download_file_to_curdir(url)
    filename = url.split("/")[-1]
    extract_zip(filename)


def prepare_qqwry():
    temp_work_dir = "tmp"
    if not os.path.exists(temp_work_dir):
        os.mkdir(temp_work_dir)
    os.chdir(temp_work_dir)

    if mswindows:
        download_then_extract_zip(windows_download_url)
        download_then_extract_zip(qqwry_download_url)

        os.system("innoextract.exe setup.exe")
        shutil.copy(r"app\qqwry.dat", "..")
        os.chdir("..")
        # shutil.rmtree(temp_work_dir)  # can NOT remove unidentifiable Chinese code
        os.system("rmdir /S /Q {}".format(temp_work_dir))
    else:
        download_file_to_curdir(qqwry_download_url)
        filename = qqwry_download_url.split("/")[-1]
        extract_zip(filename)
        os.system("||".join([ubuntu_install_cli, centos_install_cli]))

        os.system("innoextract setup.exe")  # innoextract version may be too old
        if not os.path.exists("app"):
            download_file_to_curdir(linux_binary_download_url)
            filename = linux_binary_download_url.split("/")[-1]
            os.system("tar Jxf {}".format(filename))
            os.system("./innoextract-*-linux/innoextract setup.exe")

        shutil.copy(r"app/qqwry.dat", "..")
        os.chdir("..")
        # shutil.rmtree(temp_work_dir)  # can NOT remove unidentifiable Chinese code
        os.system("rm -rf {}".format(temp_work_dir))

    if os.path.exists("qqwry.dat"):
        print("download successfully.")
    else:
        print("some error occurs.")


if __name__ == '__main__':
    prepare_qqwry()
