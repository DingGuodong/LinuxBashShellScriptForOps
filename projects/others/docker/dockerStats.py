#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# fork and modify something from http://dl528888.blog.51cto.com/2382721/1660844

import os
import json
import sys
import subprocess
import time

try:
    from docker import Client
except ImportError:
    try:
        command_to_execute = "pip install docker-py"
        os.system(command_to_execute)
    except OSError:
        exit(1)
    finally:
        from docker import Client


def check_container_stats(container_name, collect_item):
    stats = client.stats(container=container_name)
    old_result = json.loads(stats.next())
    new_result = json.loads(stats.next())
    client.close()
    result = None
    if collect_item == 'cpu_total_usage':
        result = new_result['cpu_stats']['cpu_usage']['total_usage'] - old_result['cpu_stats']['cpu_usage'][
            'total_usage']
    elif collect_item == 'cpu_system_usage':
        result = new_result['cpu_stats']['system_cpu_usage'] - old_result['cpu_stats']['system_cpu_usage']
    elif collect_item == 'cpu_percent':
        cpu_total_usage = new_result['cpu_stats']['cpu_usage']['total_usage'] - old_result['cpu_stats']['cpu_usage'][
            'total_usage']
        cpu_system_usage = new_result['cpu_stats']['system_cpu_usage'] - old_result['cpu_stats']['system_cpu_usage']
        cpu_num = len(old_result['cpu_stats']['cpu_usage']['percpu_usage'])
        result = round((float(cpu_total_usage) / float(cpu_system_usage)) * cpu_num * 100.0, 2)
    elif collect_item == 'mem_usage':
        result = new_result['memory_stats']['usage']
    elif collect_item == 'mem_limit':
        result = new_result['memory_stats']['limit']
    elif collect_item == 'mem_percent':
        mem_usage = new_result['memory_stats']['usage']
        mem_limit = new_result['memory_stats']['limit']
        result = round(float(mem_usage) / float(mem_limit) * 100.0, 2)
    # network_rx_packets=new_result['network']['rx_packets']
    # network_tx_packets=new_result['network']['tx_packets']
    elif collect_item == 'network_rx_bytes':
        network_check_command = """docker exec %s awk '/eth0/ {print "{\\"rx\\":"$2",\\"tx\\":"$10"}"}' /proc/net/dev""" \
                                % container_name
        network_old_result = eval(
            ((subprocess.Popen(network_check_command, shell=True, stdout=subprocess.PIPE)).stdout.readlines()[0]).strip(
                '\n'))
        time.sleep(1)
        network_new_result = eval(
            ((subprocess.Popen(network_check_command, shell=True, stdout=subprocess.PIPE)).stdout.readlines()[0]).strip(
                '\n'))
        result = int(network_new_result['rx']) - int(network_old_result['rx'])
    elif collect_item == 'network_tx_bytes':
        network_check_command = """docker exec %s awk '/eth0/ {print "{\\"rx\\":"$2",\\"tx\\":"$10"}"}' /proc/net/dev""" \
                                % container_name
        network_old_result = eval(
            ((subprocess.Popen(network_check_command, shell=True, stdout=subprocess.PIPE)).stdout.readlines()[0]).strip(
                '\n'))
        time.sleep(1)
        network_new_result = eval(
            ((subprocess.Popen(network_check_command, shell=True, stdout=subprocess.PIPE)).stdout.readlines()[0]).strip(
                '\n'))
        result = int(network_new_result['tx']) - int(network_old_result['tx'])
    return result


if __name__ == "__main__":
    client = Client(base_url='unix:///var/run/docker.sock')
    container = None
    item = None
    if sys.argv[1] is not None and sys.argv[2] is not None:
        container = sys.argv[1]
        item = sys.argv[2]
    else:
        exit(1)
    print(check_container_stats(container, item))
