#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
import psutil

process_names = [proc.name() for proc in psutil.process_iter()]
print process_names

print psutil.virtual_memory()

print psutil.cpu_percent()
