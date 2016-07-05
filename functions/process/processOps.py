#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
import psutil

print "==> process info"
proc_dict = dict()
for proc in psutil.process_iter():
    try:
        proc_dict[proc.pid] = {'pid': proc.pid, 'name': proc.name()}
    except StopIteration:
        pass

# process_names = [proc.name() for proc in psutil.process_iter()]
# process_pid = [proc.pid for proc in psutil.process_iter()]

for key in proc_dict:
    print proc_dict[key]['pid'], proc_dict[key]['name']

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

scputimes_dict = dict()
for scputimes_tuple in psutil.cpu_times(percpu=True):
    scputimes_dict['user'] = scputimes_tuple[0]
    scputimes_dict['system'] = scputimes_tuple[1]
    scputimes_dict['idle'] = scputimes_tuple[2]
    scputimes_dict['interrupt'] = scputimes_tuple[3]
    scputimes_dict['dpc'] = scputimes_tuple[4]
    print scputimes_dict

print "==> user info"
user = psutil.users()
print user
