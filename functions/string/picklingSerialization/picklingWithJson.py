#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:picklingWithJson.py
User:               Guodong
Create Date:        2017/6/14
Create Time:        15:30
 """
import json


class Student(object):
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score


def student2dict(student):
    return {
        'name': student.name,
        'age': student.age,
        'score': student.score
    }


s = Student('Bob', 20, 88)

class2json = json.dumps(s, indent=4, default=student2dict)

print(class2json)
