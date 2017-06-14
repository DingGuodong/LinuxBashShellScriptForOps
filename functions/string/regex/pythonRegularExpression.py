#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-

import re

reg = r'ab?'
pattern = re.compile(reg)
string = 'abb'
search = pattern.search(string)
if search:
    print search.group()
else:
    print None
