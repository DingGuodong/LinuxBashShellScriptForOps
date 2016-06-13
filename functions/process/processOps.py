#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
import psutil

process_names = [proc.name() for proc in psutil.process_iter()]
print process_names

print "==> memory info"
mem = psutil.virtual_memory()
print mem.total
print mem.used
print mem.free  # mem.available
print mem.percent

print "==> swap info"
swap = psutil.swap_memory()
print swap.total
print swap.used
print swap.free
print swap.percent
print swap.sin
print swap.sout

print "==> cpu info"
print psutil.cpu_count(logical=False)
print psutil.cpu_count()
print psutil.cpu_percent()
print psutil.cpu_times(percpu=True)

print "==> user info"
user = psutil.users()
print user
