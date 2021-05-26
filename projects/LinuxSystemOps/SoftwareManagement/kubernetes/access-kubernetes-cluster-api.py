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
References:             [使用 Kubernetes API 访问集群]
                            (https://kubernetes.io/zh/docs/tasks/administer-cluster/access-cluster-api/#python-client)
                        [使用 kubeconfig 文件组织集群访问]
                            (https://kubernetes.io/zh/docs/concepts/configuration/organize-cluster-access-kubeconfig/)
                            默认情况下，kubectl 在 $HOME/.kube 目录下查找名为 config 的文件。
                        [从 Pod 中访问 Kubernetes API]
                            (https://kubernetes.io/zh/docs/tasks/run-application/access-api-from-pod/)
                        [Shows how to load a Kubernetes config from within a cluster]
                            (https://github.com/kubernetes-client/python/blob/master/examples/in_cluster_config.py)
                        [Shows how to load a Kubernetes config from outside of the cluster]
                            (https://github.com/kubernetes-client/python/blob/master/examples/out_of_cluster_config.py)
If you get 403 errors from the API server you will have to configure RBAC to
add permission to list pods by applying the following manifest:
## cc: a prefix which short for `customer customized`
---
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: cc-nodes-pods-read
rules:
- apiGroups: [""]
  resources: ['nodes', "pods"]
  verbs: ["get", "list"]
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: cc-nodes-pods-read
subjects:
- kind: ServiceAccount
  name: default
  namespace: default
roleRef:
  kind: ClusterRole
  name: cc-nodes-pods-read
  apiGroup: rbac.authorization.k8s.io

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

# use `config.load_incluster_config()` when access kubernetes api from within a cluster
config.load_kube_config("c:\\users\\z\\desktop\\config")  # load a Kubernetes config from outside of the cluster

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
