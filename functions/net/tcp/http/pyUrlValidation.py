#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyUrlValidation.py
User:               Guodong
Create Date:        2017/5/10
Create Time:        14:48
 """


def is_url_valid(url):
    # http://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
    from django.core.validators import URLValidator
    from django.core.exceptions import ValidationError
    val = URLValidator()
    try:
        val(url)
    except ValidationError:
        return False
    else:
        return True


def is_url_valid_u2(url):
    """
    http://validators.readthedocs.io/en/latest/
    Python has all kinds of validation tools, but every one of them requires defining a schema. I 
    wanted to create a simple validation library where validating a simple value does not require 
    defining a form or a schema.
    """
    import validators
    if validators.url(url):
        return True
    else:
        return False


print is_url_valid_u2('www.baidu.com')
print is_url_valid('https://www.baidu.com')
