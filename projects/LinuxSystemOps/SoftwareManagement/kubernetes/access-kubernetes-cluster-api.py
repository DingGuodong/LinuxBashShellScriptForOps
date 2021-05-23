#!/usr/bin/python
# encoding: utf-8
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:access-docker-api.py
Version:                0.0.1
Author:                 DingGuodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2021/5/23
Create Time:            19:57
Description:            get kubernetes cluster info by using kubernetes SDK

Long Description:
References:             [使用 Kubernetes API 访问集群](https://kubernetes.io/zh/docs/tasks/administer-cluster/access-cluster-api/#python-client)
Prerequisites:          pip install kubernetes
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
from kubernetes import client, config

config.load_kube_config("c:\\users\\z\\desktop\\config")

v1 = client.CoreV1Api()

ret = v1.list_node()
for item in ret.items:
    if item.metadata.labels.get("kubernetes.io/role") == 'worker':
        print(item.status.node_info.machine_id, item.status.node_info.system_uuid)
    else:
        # 单节点master: kubernetes.io/role label 未标记为master
        print(item)
        print(item.status.node_info.machine_id, item.status.node_info.system_uuid)

ret = v1.list_namespaced_pod(namespace='default')
print(ret)
