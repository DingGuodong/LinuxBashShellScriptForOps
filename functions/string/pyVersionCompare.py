#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyVersionCompare.py
User:               Guodong
Create Date:        2017/9/5
Create Time:        11:08
Description:        a function for software version compare
References:         https://segmentfault.com/q/1010000000331434
 """

nginx_url = r'http://nginx.org/download/nginx-1.12.1.tar.gz'
tengine_url = r'http://tengine.taobao.org/download/tengine-2.2.0.tar.gz'


def get_version_from_text(text):
    result = ""
    if text != "":
        import re
        pattern = re.compile(r'(\d+(\.\d+)*)')
        match = pattern.search(text)
        if match:
            result = match.group()
    return result


def compare_version(version_left="", version_right=""):
    """
    get latest version in version_lest and version right, using  "from distutils.version import LooseVersion".
    Refers: https://segmentfault.com/q/1010000000331434

    :param version_left:
    :param version_right:
    :return latest version in version_lest and version right:
    """
    from distutils.version import LooseVersion as version

    # https://codegolf.stackexchange.com/questions/49778/how-can-i-use-cmpa-b-with-python3
    res = (version(version_left) > version(version_right)) - (version(version_left) < version(version_right))
    if res > 0:
        return version_left
    elif res < 0:
        return version_right
    else:
        return version_left


def compare_version_degraded(version_left="", version_right=""):
    if validate_version(version_left) and validate_version(version_right):
        pass
    else:
        raise RuntimeError("bad parameter, version is not passed validation.")


def validate_version(version):
    import re
    pattern = re.compile(r'(\d+(\.\d+)*)')
    match = pattern.search(version)
    if match:
        return True
    else:
        return False


if __name__ == '__main__':
    print(compare_version("3.4.1", "2.3.2"))
