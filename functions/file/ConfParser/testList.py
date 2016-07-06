#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
import ConfigParser

old_list = [1, 2, 3, [4, 5, 6]]
new_list1 = old_list[:]
new_list2 = old_list
print id(old_list)
print id(new_list1)
print id(new_list2)

print id(old_list[0])
print id(new_list1[0])
print id(new_list2[0])

print id(old_list[3])
print id(new_list1[3])
print id(new_list2[3])

print old_list
old_list.pop()
print old_list
print new_list1
print new_list2
