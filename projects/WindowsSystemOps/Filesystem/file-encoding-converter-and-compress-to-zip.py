#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:file-encoding-converter-and-compress-to-zip.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/6/10
Create Time:            15:09
Description:            convert file encoding utf-16 to utf-8 then zip it
Long Description:       file encoding converter, compress files using zip
References:             [UTF-8, UTF-16, UTF-32 & BOM](https://unicode.org/faq/utf_bom.html)
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
import os
import zipfile

import chardet
import datetime


def is_file_encoding_with_utf8_or_utf16(path, encoding='utf-8'):
    """
    usage:
        is_file_encoding_with_utf8_or_utf16("test_utf8.csv", 'utf-8') -> True
        is_file_encoding_with_utf8_or_utf16("test_utf8.csv", 'utf-16') -> False
        is_file_encoding_with_utf8_or_utf16("test_utf16.csv", 'utf-16') -> True
        is_file_encoding_with_utf8_or_utf16("test_utf16.csv", 'utf-8') -> False
    :param path: file's path
    :type path: str
    :param encoding: 'utf-8' or 'utf-16'
    :type encoding: str
    :return: boolean
    :rtype:  bool
    """
    encoding = encoding.lower()
    if encoding not in ['utf-8', 'utf-16']:
        raise ValueError("bad encoding, only 'utf-8' or 'utf-16' is allowed.")

    if os.path.exists(path):
        with open(path, 'r') as fp:
            content = fp.read()

        try:
            _ = content.decode(encoding)
        except UnicodeDecodeError:
            rlc = False  # low credibility
        else:
            rlc = True

        encoding_from_chardet_raw = chardet.detect(content).get("encoding")
        if encoding_from_chardet_raw:
            encoding_from_chardet = encoding_from_chardet_raw.lower()
            try:
                _ = content.decode(encoding_from_chardet)
            except UnicodeDecodeError:
                rmc = False  # medium credibility
            else:
                rmc = True
        else:
            rmc = False
            encoding_from_chardet = ""

        if rmc and (encoding in encoding_from_chardet):
            return True  # high credibility
        elif rmc and (encoding not in encoding_from_chardet):
            return False  # high credibility
        elif not rmc and (encoding in encoding_from_chardet):
            return False  # high credibility
        elif rlc:
            return True
        else:
            return False

    else:
        return False


def convert_file_from_utf16_to_utf8(path):
    if not is_file_encoding_with_utf8_or_utf16(path, 'utf-8'):
        with open(path, 'rb') as fp1:
            content = fp1.read()
        with open(path, 'wb') as fp2:
            # # source: Little-endian UTF-16 Unicode text, with CRLF, CR line terminators
            # # output: UTF-8 Unicode (with BOM) text, with CRLF line terminators
            # fp2.write(content.decode("utf-16le").encode("utf-8"))

            # source: Little-endian UTF-16 Unicode text, with CRLF, CR line terminators
            # output: UTF-8 Unicode text, with CRLF line terminators
            fp2.write(content.decode("utf-16").encode("utf-8"))


def zip_compress(name, files, arc, keep_name=True):
    """
    compress files using zip
    :param name: zip file name, such as 'x.zip'
    :type name: str
    :param files: files to compress
    :type files: str or list
    :param arc: a absolute path, the top path of files
    :type arc: str
    :param keep_name: whether keep the parent directory name of files
    :type keep_name: bool
    :return: None
    :rtype: None
    """
    if isinstance(files, str):
        files_list = [files]
    elif isinstance(files, list):
        files_list = files
    else:
        raise RuntimeError

    with zipfile.ZipFile(name, 'w', compression=zipfile.ZIP_DEFLATED) as fp:
        for origin_file in files_list:
            if keep_name:
                parent = os.path.basename(arc)
                cur_arc = origin_file.replace(arc, "").strip(os.sep)
                archive_name = os.sep.join((parent, cur_arc))
            else:
                archive_name = origin_file.replace(arc, "")
            fp.write(origin_file, arcname=archive_name)


def compress_src_directory_to_dst(save_name, source):
    if os.path.isdir(source):
        # put all files wanted into a list obj
        wanted_files_list = list()
        for top, dirs, nondirs in os.walk(source_path):
            # WARNING: some empty folder which has no file will not add zip
            for filename in nondirs:
                cur_file = os.path.join(top, filename)
                convert_file_from_utf16_to_utf8(cur_file)
                wanted_files_list.append(cur_file)

        if wanted_files_list:
            zip_compress(save_name, wanted_files_list, arc=source, keep_name=False)


if __name__ == '__main__':
    # source data path
    source_path = r"D:\WWW\DingLvAnHou\Databakup"

    # generate save as name
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    base_name = os.path.basename(source_path)
    save_as_filename = base_name + today + ".zip"
    save_as_path = r"D:\WWW\DingLvAnHou\DataBak"
    save_as_zip = os.path.join(save_as_path, save_as_filename)

    # compress source data
    compress_src_directory_to_dst(save_as_zip, source_path)
