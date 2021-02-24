#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:parse-redis.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2021/2/24
Create Time:            11:54
Description:            Convert the type of obj or sub item in obj returned by django_redis from bytes to str or bust
Long Description:

背景：django_redis client 的 `mgetall()` 方法默认返回的字典中的键值的类型均为bytes，无法正常序列化为json

各位大佬，我有个问题想咨询一下，通过django_redis模块获取redis中的一个字典d，得到的字典d的键值都为bytes类型，我想知道有没有比较好的办法将这个字典d序列化为json，但尽可能保存字典d中值的类型。
比如字典d原始数据为：

 {b'id': b'1', b'username': b'admin', b'name': b'DingGuodong', b'avatar': b'http://127.0.0.1:8769/media/avatar/default.png', b'email': b'uberurey_ups@163.com', b'permissions': b'["admin"]', b'department': b'', b'mobile': b'18353271212'}

我想序列化后为：

 {
        "id": "1",
        "username": "admin",
        "name": "DingGuodong",
        "avatar": "http://127.0.0.1:8769/media/avatar/default.png",
        "email": "u****@163.com",
        "permissions": ["admin"],
        "department": "",
        "mobile": "1*********2",
        "use_cache": "True"
    }
请问有没有现成的轮子可用？

References:             https://linmingjie.cn/index.php/archives/26/
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
Notes：
1. 除了可以使用此文件中的 ParsedRedis 类外，还可以直接使用 parse_redis 函数
2. 值得注意的是 django_redis 的 HMSET 并不能接收所有可能的某个字典，比如
"""
from django_redis import get_redis_connection


def list_liked_str2list(value):
    """
    Convert a list-like string to a list or leave it unchanged
    :param value:
    :type value: bytes
    :return:
    :rtype: str, list
    """
    if value.startswith(b'[') and value.endswith(b']'):
        parsed_value_list = value.strip(b'[').strip(b']').split(b",")
        return [list_liked_str2list(item) for item in parsed_value_list]
    else:
        # do decode at last
        return value.decode('utf-8').strip("'").strip('"')


def parse_redis(obj):
    """
    Convert the type of obj or sub item in obj to str or bust
    :param obj:
    :type obj:
    :return:
    :rtype:
    """
    if isinstance(obj, dict):
        # return {x.decode('utf-8'): obj[x].decode('utf-8') for x in obj}
        parsed_dict = {}
        for key, value in obj.items():  # type:bytes
            parsed_dict.update({key.decode('utf-8'): list_liked_str2list(value)})

        return parsed_dict
    elif isinstance(obj, bytes):
        return obj.decode('utf-8')
    elif isinstance(obj, set):
        return set(x.decode('utf-8') for x in obj)
    elif isinstance(obj, list):
        return [x.decode('utf-8') for x in obj]
    else:
        return obj


def parse_redis_u1(obj):
    import ast
    if isinstance(obj, dict):
        parsed_dict = {}
        for key, value in obj.items():
            key = key.decode("utf-8")
            value = value.decode("utf-8")
            if value.startswith('[') and value.endswith(']'):
                value = ast.literal_eval(value)
            parsed_dict[key] = value

        return parsed_dict
    elif isinstance(obj, bytes):
        return obj.decode('utf-8')
    elif isinstance(obj, set):
        return set(x.decode('utf-8') for x in obj)
    elif isinstance(obj, list):
        return [x.decode('utf-8') for x in obj]
    else:
        return obj


def parse_redis_u2(obj):
    import json
    if isinstance(obj, dict):
        parsed_dict = {}
        for key, value in obj.items():
            key = key.decode("utf-8")
            value = value.decode("utf-8")
            if value.startswith('[') and value.endswith(']'):
                value = json.loads(value)
            parsed_dict[key] = value

        return parsed_dict
    elif isinstance(obj, bytes):
        return obj.decode('utf-8')
    elif isinstance(obj, set):
        return set(x.decode('utf-8') for x in obj)
    elif isinstance(obj, list):
        return [x.decode('utf-8') for x in obj]
    else:
        return obj


def to_container(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return parse_redis(result)

    return wrapper


class ParsedRedis(object):
    def __init__(self, conf='default'):
        self.conn = get_redis_connection(conf)

    def __getattr__(self, func):
        return to_container(getattr(self.conn, func))
