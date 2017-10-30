#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:remove_old_error_log.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/10/30
Create Time:            11:38
Description:            
Long Description:       
References:             
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
import re


def sort_files_by_ctime_with_extension(path=None, type_extension=None):
    if not os.path.exists(path):
        raise RuntimeError('No such file or directory.')

    if isinstance(type_extension, (list, tuple)):
        file_extension_iterable = type_extension
    elif isinstance(type_extension, str):
        file_extension_iterable = (type_extension,)
    else:
        raise RuntimeError('Bad file extension name.')

    working_directory = path
    sorted_files = list()

    all_files_with_date_dict = dict()
    for top, dirs, nondirs in os.walk(working_directory):
        if len(nondirs) != 0:
            for filename in nondirs:
                full_path_to_filename = os.path.join(top, filename)
                if full_path_to_filename.endswith(tuple(file_extension_iterable)):
                    all_files_with_date_dict[full_path_to_filename] = os.path.getctime(full_path_to_filename)

    for item in sorted(all_files_with_date_dict.items(), cmp=lambda x, y: cmp(x[1], y[1]), reverse=True):
        sorted_files.append(item[0])

    return sorted_files


def sort_files_by_ctime_with_regex_match(path=None, regex=None):
    if not os.path.exists(path):
        raise RuntimeError('No such file or directory.')

    def is_match_regex(string, regex_expression):
        pattern = re.compile(regex_expression)
        is_matched = pattern.search(string)
        if is_matched:
            return True
        else:
            return False

    working_directory = path
    sorted_files = list()

    all_files_with_date_dict = dict()
    for top, dirs, nondirs in os.walk(working_directory):
        if len(nondirs) != 0:
            for filename in nondirs:
                full_path_to_filename = os.path.join(top, filename)
                if is_match_regex(full_path_to_filename, regex):
                    all_files_with_date_dict[full_path_to_filename] = os.path.getctime(full_path_to_filename)

    for item in sorted(all_files_with_date_dict.items(), cmp=lambda x, y: cmp(x[1], y[1]), reverse=True):
        sorted_files.append(item[0])

    return sorted_files


def find_filter(files=None, keywords=None, excludes=None):
    if isinstance(files, (list, tuple)):
        files_iterable = files
    elif isinstance(files, str):
        files_iterable = (files,)
    else:
        raise RuntimeError('Bad parameter.')

    if isinstance(keywords, (list, tuple)):
        keywords_iterable = keywords
    elif isinstance(keywords, str):
        keywords_iterable = (keywords,)
    else:
        raise RuntimeError('Bad parameter.')

    if isinstance(excludes, (list, tuple)):
        excludes_iterable = excludes
    elif isinstance(excludes, str):
        excludes_iterable = (excludes,)
    else:
        raise RuntimeError('Bad parameter.')

    filtered_dict = dict()

    for keyword in keywords_iterable:
        for filename in files_iterable:
            if keyword in filename and os.path.basename(filename) not in excludes_iterable:
                filtered_dict.setdefault(keyword, []).append(filename)

    return filtered_dict


if __name__ == '__main__':
    save_number = 10
    log_path_to_clean = '/opt/ebt/logs/agent-stats/'
    trash_dir = os.path.join(log_path_to_clean, 'to_delete')
    regex_match_rule = '[0-9]{2,4}-[0-9]{1,2}-[0-9]{1,2}'  # such as 2017-10-30
    keywords_to_match = ('error', 'request')
    files_to_ignore = ('agent-stats.gc.log', 'agent-stats.log', 'error.log ', 'request.log')

    sort_files = sort_files_by_ctime_with_regex_match(path=log_path_to_clean, regex=regex_match_rule)
    all_matched_files = find_filter(files=sort_files, keywords=keywords_to_match, excludes=files_to_ignore)

    files_to_delete = list()

    for key, value in all_matched_files.iteritems():
        if len(value) <= save_number:
            pass
        else:
            files_to_delete += value[save_number:]

    if not os.path.exists(trash_dir):
        os.makedirs(trash_dir)

    for file_to_delete in files_to_delete:
        os.rename(file_to_delete, os.path.join(trash_dir, os.path.basename(file_to_delete)))
