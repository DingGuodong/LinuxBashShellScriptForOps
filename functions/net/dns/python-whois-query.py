#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:python-whois-query.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2021/4/19
Create Time:            20:41
Description:            python query whois info of domain name.
Long Description:       
References:             https://pypi.org/project/python-whois/
Prerequisites:          pip install python-whois  # `whois` command is required
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

import pytz
import whois


def to_string(name):
    """
    :param name:
    :type name: list|str|set
    :return:
    :rtype:
    """
    if isinstance(name, list):
        return ", ".join([str(x) for x in name])
    else:
        return str(name)


def to_string_lower_and_uniq(name):
    """
    :param name:
    :type name: str|list
    :return:
    :rtype: str
    """
    if isinstance(name, list):
        return ", ".join(list(set([str(x).lower() for x in name])))
    else:
        return str(name)


def utc_to_timezone(datetime_utc, timezone='Asia/Shanghai'):
    return datetime_utc.replace(
        tzinfo=pytz.timezone('UTC')).astimezone(
        pytz.timezone(timezone))


def datetime_to_string(datetime_obj, fmt="%Y-%m-%d %H:%M:%S"):
    return datetime_obj.strftime(fmt)


def utc_to_string(datetime_utc, fmt="%Y-%m-%d %H:%M:%S"):
    return datetime_to_string(utc_to_timezone(datetime_utc), fmt)


def _get_whois_info(domain_name):
    try:
        parsed_whois_info = whois.whois(domain_name)
    except whois.parser.PywhoisError as e:
        error_message = str(e)
        if error_message.startswith("No match for"):
            error_message = error_message.split(os.linesep)[0]
        return False, error_message
    return True, parsed_whois_info


def get_whois_info(domain_name):
    is_success, parsed_info = _get_whois_info(domain_name)
    if not is_success:
        raise whois.parser.PywhoisError(parsed_info)

    domain_name = to_string_lower_and_uniq(parsed_info.get('domain_name'))
    registrar = parsed_info.get('registrar')
    created_date_utc = parsed_info.get('creation_date')  # "1999-10-11T11:05:17Z", "%Y-%m-%dT%H:%M:%S.%fZ"
    email = parsed_info.get('emails')

    organization = parsed_info.get('org')
    print(" | ".join([to_string(x) for x in [domain_name, registrar, created_date_utc, email, organization]]))


if __name__ == '__main__':
    get_whois_info("baidu.com")
