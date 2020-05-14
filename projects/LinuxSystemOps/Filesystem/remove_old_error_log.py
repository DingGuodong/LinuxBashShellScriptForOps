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
Description:            python remove old logs with a given directory
Long Description:       
References:             
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
import re
import sys


def sort_files_by_ctime_with_extension(path=None, type_extension=None, excludes=None):
    if not os.path.exists(path):
        raise RuntimeError('No such file or directory.')

    if isinstance(excludes, (list, tuple)):
        excludes_iterable = excludes
    elif isinstance(excludes, str):
        excludes_iterable = (excludes,)
    else:
        raise RuntimeError('Bad parameter.')

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
        if len(nondirs) != 0 and not top.endswith(excludes_iterable):
            for filename in nondirs:
                full_path_to_filename = os.path.join(top, filename)
                if full_path_to_filename.endswith(tuple(file_extension_iterable)):
                    all_files_with_date_dict[full_path_to_filename] = os.path.getctime(full_path_to_filename)

    for item in sorted(list(all_files_with_date_dict.items()), key=lambda x: x[1], reverse=True):
        sorted_files.append(item[0])

    return sorted_files


def sort_files_by_ctime_with_regex_match(path=None, regex=None, excludes=None):
    if not os.path.exists(path):
        raise RuntimeError('No such file or directory.')

    if isinstance(excludes, (list, tuple)):
        excludes_iterable = excludes
    elif isinstance(excludes, str):
        excludes_iterable = (excludes,)
    else:
        raise RuntimeError('Bad parameter.')

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
        if len(nondirs) != 0 and not top.endswith(excludes_iterable):
            for filename in nondirs:
                full_path_to_filename = os.path.join(top, filename)
                if is_match_regex(full_path_to_filename, regex):
                    all_files_with_date_dict[full_path_to_filename] = os.path.getctime(full_path_to_filename)

    for item in sorted(list(all_files_with_date_dict.items()), key=lambda x: x[1], reverse=True):
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


def get_disk_usage(path):
    import subprocess
    command = "du -sh %s" % path
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    (stdout, stderr) = p.communicate()
    if p.returncode != 0:
        print("encountered an error (return code %s) while executing '%s'" % (p.returncode, command))
        if stdout is not None:
            print("Standard output:", stdout)
        if stderr is not None:
            print("Standard error:", stderr)
        return ""
    else:
        return stdout


if __name__ == '__main__':
    save_number = 30  # each type log file save 30.
    regex_match_rule = r'\d{2,4}-\d{1,2}-\d{1,2}'  # such as 2017-10-30, 18-01-02
    keywords_to_match = ('error', 'request')
    trash_dir_name = 'to_delete'
    apps_log_root_path = os.path.abspath('/opt/ebt/logs/')

    print("Cleaning old logs in path: {path}".format(path=apps_log_root_path))
    for app_log_path in [os.path.join(apps_log_root_path, log_path) for log_path in os.listdir(apps_log_root_path)]:
        if os.path.isfile(app_log_path):
            continue
        app_service_name = os.path.basename(app_log_path)
        print(r"\---+ Processing {app}'s old logs, path: {path}".format(app=app_service_name, path=app_log_path))
        trash_dir = os.path.join(app_log_path, trash_dir_name)
        files_to_ignore = ('%s.gc.log' % app_service_name, '%s.log' % app_service_name, 'error.log ', 'request.log')

        # skip scan trash dir
        dirs_to_ignore = (trash_dir_name,)

        sort_files = sort_files_by_ctime_with_regex_match(path=app_log_path, regex=regex_match_rule,
                                                          excludes=dirs_to_ignore)
        all_matched_files = find_filter(files=sort_files, keywords=keywords_to_match, excludes=files_to_ignore)

        files_to_delete = list()

        if not os.path.exists(trash_dir):
            os.makedirs(trash_dir)

        for key, value in all_matched_files.items():
            if len(value) <= save_number:
                print("log type \"{type}\" files are in good state, skip".format(type=key))
                pass
            else:
                print("{number} log files with type \"{type}\" are going to be processed".format(
                    number=len(value) - save_number, type=key))
                files_to_delete += value[save_number:]  # or use list(set(list_obj)) to make sure each member is unique

        # do os.rename() after collection(get files to delete) finished
        for file_to_delete in files_to_delete:
            try:
                if os.path.exists(file_to_delete):
                    # os.rename() is equal to GNU 'mv' and  shutil.move()
                    os.rename(file_to_delete, os.path.join(trash_dir, os.path.basename(file_to_delete)))
                else:
                    print('WARNING: file not exist, No such file or directory, {file}'.format(
                        file=file_to_delete))
            except OSError as e:  # for debug purpose, in case of Permission issue
                print('ERROR: OSError is raised.')
                print(e)
                print(e.args)
                # DeprecationWarning: BaseException.message has been deprecated as of Python 2.6
                # print(e.message)
                print(file_to_delete)
                print(os.path.join(trash_dir, os.path.basename(file_to_delete)))
                sys.exit(1)

    print("OK! Cleaning old logs in path: {path}, Finished!".format(path=apps_log_root_path))
    print("Next Todo: use the command as follows to clean old log files:\n")
    print("find /opt/ebt/logs/ -type d  -name to_delete | xargs -i rm -r {}")
