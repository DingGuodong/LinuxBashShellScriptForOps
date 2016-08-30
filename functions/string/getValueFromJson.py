#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:getValueFromJson.py
User:               Guodong
Create Date:        2016/8/30
Create Time:        15:05
 """
import json

json_example = '''
[
  {
    "NetworkSettings": {
      "Networks": {
        "bridge": {
          "MacAddress": "02:42:ac:11:00:04",
          "GlobalIPv6PrefixLen": 0,
          "GlobalIPv6Address": "",
          "IPv6Gateway": "",
          "IPAMConfig": null,
          "Links": null,
          "Aliases": null,
          "NetworkID": "6ea210e0bbfe3b2fd2faf556164211f97f50bd3aacffdf5fa6355333f77e109b",
          "EndpointID": "ace1bae319843a73d704e62d3cfc11b3ac5152bfcaabb525321a0315d4c54ec3",
          "Gateway": "172.17.0.1",
          "IPAddress": "172.17.0.4",
          "IPPrefixLen": 16
        }
      },
      "MacAddress": "02:42:ac:11:00:04",
      "SecondaryIPAddresses": null,
      "SandboxKey": "/var/run/docker/netns/3859a4134ebc",
      "Ports": {
        "80/tcp": null,
        "443/tcp": null,
        "10107/tcp": [
          {
            "HostPort": "10107",
            "HostIp": "0.0.0.0"
          }
        ]
      },
      "LinkLocalIPv6PrefixLen": 0,
      "LinkLocalIPv6Address": "",
      "HairpinMode": false,
      "SandboxID": "3859a4134ebcd46f1f1a983c097fe811dd1f44112970bd4fd18e4127e43b8963",
      "Bridge": "",
      "SecondaryIPv6Addresses": null,
      "EndpointID": "ace1bae319843a73d704e62d3cfc11b3ac5152bfcaabb525321a0315d4c54ec3",
      "Gateway": "172.17.0.1",
      "GlobalIPv6Address": "",
      "GlobalIPv6PrefixLen": 0,
      "IPAddress": "172.17.0.4",
      "IPPrefixLen": 16,
      "IPv6Gateway": ""
    },
    "Config": {
      "StopSignal": "SIGTERM",
      "Labels": {},
      "OnBuild": null,
      "Tty": true,
      "ExposedPorts": {
        "80/tcp": {},
        "443/tcp": {},
        "10107/tcp": {}
      },
      "AttachStderr": false,
      "AttachStdout": false,
      "AttachStdin": false,
      "User": "",
      "Domainname": "",
      "Hostname": "my_app",
      "OpenStdin": true,
      "StdinOnce": false,
      "Env": [
        "PATH=/usr/local/jdk1.8.0_91/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
        "NGINX_VERSION=1.10.1-1~jessie",
        "JAVA_HOME=/usr/local/jdk1.8.0_91",
        "JRE_HOME=/usr/local/jdk1.8.0_91/jre",
        "CLASSPATH=.:/usr/local/jdk1.8.0_91/lib:/usr/local/jdk1.8.0_91/jre/lib"
      ],
      "Cmd": [
        "nginx",
        "-g",
        "daemon off;"
      ],
      "Image": "jdk8-nginx:latest",
      "Volumes": null,
      "WorkingDir": "",
      "Entrypoint": null
    },
    "Mounts": [
      {
        "Propagation": "rprivate",
        "RW": true,
        "Mode": "",
        "Destination": "/data/html",
        "Source": "/data/docker/my_app/my_app-web"
      },
      {
        "Propagation": "rprivate",
        "RW": true,
        "Mode": "",
        "Destination": "/data/vert",
        "Source": "/data/docker/my_app/my_app-backend"
      },
      {
        "Propagation": "rprivate",
        "RW": true,
        "Mode": "",
        "Destination": "/etc/localtime",
        "Source": "/etc/localtime"
      },
      {
        "Propagation": "rprivate",
        "RW": true,
        "Mode": "",
        "Destination": "/etc/nginx/conf.d/http_proxy_10107.conf",
        "Source": "/data/docker/my_app/nginx/conf/http_proxy_10107.conf"
      }
    ],
    "GraphDriver": {
      "Data": null,
      "Name": "aufs"
    },
    "HostConfig": {
      "Ulimits": null,
      "PidsLimit": 0,
      "OomKillDisable": false,
      "MemorySwappiness": -1,
      "MemorySwap": 0,
      "MemoryReservation": 0,
      "Memory": 0,
      "KernelMemory": 0,
      "Devices": [],
      "CpusetMems": "",
      "CpusetCpus": "",
      "CpuQuota": 0,
      "CpuPeriod": 0,
      "BlkioDeviceWriteIOps": null,
      "BlkioDeviceReadIOps": null,
      "BlkioDeviceWriteBps": null,
      "IpcMode": "",
      "GroupAdd": null,
      "ExtraHosts": null,
      "DnsSearch": [],
      "DnsOptions": [],
      "Dns": [
        "8.8.4.4",
        "114.114.114.114"
      ],
      "CapDrop": null,
      "CapAdd": null,
      "Binds": [
        "/etc/localtime:/etc/localtime",
        "/data/docker/my_app/nginx/conf/http_proxy_10107.conf:/etc/nginx/conf.d/http_proxy_10107.conf",
        "/data/docker/my_app/my_app-web:/data/html",
        "/data/docker/my_app/my_app-backend:/data/vert"
      ],
      "ContainerIDFile": "",
      "LogConfig": {
        "Config": {},
        "Type": "json-file"
      },
      "NetworkMode": "default",
      "PortBindings": {
        "10107/tcp": [
          {
            "HostPort": "10107",
            "HostIp": ""
          }
        ]
      },
      "RestartPolicy": {
        "MaximumRetryCount": 0,
        "Name": "always"
      },
      "VolumeDriver": "",
      "VolumesFrom": null,
      "Links": null,
      "OomScoreAdj": 0,
      "PidMode": "",
      "Privileged": false,
      "PublishAllPorts": false,
      "ReadonlyRootfs": false,
      "SecurityOpt": null,
      "UTSMode": "",
      "ShmSize": 67108864,
      "ConsoleSize": [
        0,
        0
      ],
      "Isolation": "",
      "CpuShares": 0,
      "CgroupParent": "",
      "BlkioWeight": 0,
      "BlkioWeightDevice": null,
      "BlkioDeviceReadBps": null
    },
    "ExecIDs": null,
    "HostnamePath": "/var/lib/docker/containers/040ea22f33c20d70de3339eeb8b8414c07fbd5740de3dd39cebb32375595f256/hostname",
    "ResolvConfPath": "/var/lib/docker/containers/040ea22f33c20d70de3339eeb8b8414c07fbd5740de3dd39cebb32375595f256/resolv.conf",
    "Image": "sha256:d27af5eeb1ba0d042e883496c180a6b8bec646dbf6d306aea02179faed447ecc",
    "State": {
      "FinishedAt": "2016-08-15T08:25:10.183190679Z",
      "StartedAt": "2016-08-15T08:26:41.262617964Z",
      "Error": "",
      "Status": "running",
      "Running": true,
      "Paused": false,
      "Restarting": false,
      "OOMKilled": false,
      "Dead": false,
      "Pid": 3197,
      "ExitCode": 0
    },
    "Args": [
      "-g",
      "daemon off;"
    ],
    "Path": "nginx",
    "Created": "2016-06-15T02:14:51.040944197Z",
    "Id": "040ea22f33c20d70de3339eeb8b8414c07fbd5740de3dd39cebb32375595f256",
    "HostsPath": "/var/lib/docker/containers/040ea22f33c20d70de3339eeb8b8414c07fbd5740de3dd39cebb32375595f256/hosts",
    "LogPath": "/var/lib/docker/containers/040ea22f33c20d70de3339eeb8b8414c07fbd5740de3dd39cebb32375595f256/040ea22f33c20d70de3339eeb8b8414c07fbd5740de3dd39cebb32375595f256-json.log",
    "Name": "/my_app",
    "RestartCount": 0,
    "Driver": "aufs",
    "MountLabel": "",
    "ProcessLabel": "",
    "AppArmorProfile": ""
  }
]
'''

json_object = json.loads(json_example)  # type is a list
print json_object[0]["Mounts"]
for i in json_object[0]["Mounts"]:
    print i["Destination"]
