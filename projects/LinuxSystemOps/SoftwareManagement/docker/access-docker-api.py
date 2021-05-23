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
Description:            get docker info by using docker SDK

Long Description:
References:             [Develop with Docker Engine SDKs](https://docs.docker.com/engine/api/sdk/)
Prerequisites:          pip install docker
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
import docker  # pip install docker
#

# client = docker.from_env()
# client = docker.DockerClient(base_url='tcp://127.0.0.1:2375')
client = docker.DockerClient(base_url='unix://var/run/docker.sock')

docker_info = client.info()
docker_daemon_id = docker_info.get('ID')  # useful for manage license in docker container
print(docker_daemon_id)
