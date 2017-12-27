#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyRandomSort.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2017/12/26
Create Time:            17:34
Description:            random sort(shuffle) items in list
Long Description:       see also: sort -R, shuf in Linux coreutils(GNU core utilities)
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
import random


# method 1
class MyShuffle(random.Random):
    def shuffle(self, x, random_method=None):
        """x, random=random.random -> shuffle list x not in place; return x.

        Optional arg random is a 0-argument function returning a random
        float in [0.0, 1.0); by default, the standard random.random.

        """
        if isinstance(x, list):
            if random_method is None:
                random_method = self.random
            _int = int
            for i in reversed(xrange(1, len(x))):
                # pick an element in x[:i+1] with which to exchange x[i]
                j = _int(random_method() * (i + 1))
                x[i], x[j] = x[j], x[i]

            return x
        else:
            raise RuntimeError("object 'list' is required")


# method 2
def shuffle(obj_list):
    for i in reversed(xrange(1, len(obj_list))):
        # pick an element in obj_list[:i+1] with which to exchange obj_list[i]
        j = int(random.random() * (i + 1))
        obj_list[i], obj_list[j] = obj_list[j], obj_list[i]
    return obj_list


# call method 1
p = MyShuffle()
print(p.shuffle(range(10)))

# call method 2
print(shuffle(range(10)))
