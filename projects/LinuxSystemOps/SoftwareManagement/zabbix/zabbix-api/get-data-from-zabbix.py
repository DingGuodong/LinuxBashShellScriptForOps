#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:get-data-from-zabbix-u1.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/6/3
Create Time:            10:01
Description:            access data using Zabbix API
Long Description:       Zabbix API allows you to programmatically retrieve and modify the configuration of Zabbix and provides access to historical data. It is widely used to:
                            - Create new applications to work with Zabbix;
                            - Integrate Zabbix with third party software;
                            - Automate routine tasks.

References:             [Zabbix API libraries](https://zabbix.org/wiki/Docs/api/libraries#Python)
                        [Zabbix module for Python](https://github.com/adubkov/py-zabbix)
                        [Zabbix Manual|API](https://www.zabbix.com/documentation/4.0/manual/api)
                        [API Method reference](https://www.zabbix.com/documentation/4.0/manual/api/reference)
Prerequisites:          pip install py-zabbix
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
from pyzabbix.api import ZabbixAPI


def get_free_memory():
    """
    :return: free memory of Linux or Windows
    :rtype: float
    """
    # https://www.zabbix.com/documentation/4.0/manual/api/reference/item/get
    mem_free = zapi.item.get(
        hostids=host_id,
        output=["lastvalue"],
        search={"key_": "vm.memory.size[free]"}  # Windows
    )
    if len(mem_free) != 0:
        mem_free_last = mem_free[0].get('lastvalue')
    else:
        mem_free = zapi.item.get(
            hostids=host_id,
            output=["lastvalue"],
            search={"key_": "vm.memory.size[available]"},  # Linux
        )

        if len(mem_free) != 0:
            mem_free_last = mem_free[0].get('lastvalue')
        else:  # host is enabled but has no item
            return 0.0
    return float(mem_free_last)


def others_defs():
    # Get API Version
    # To simplify API versioning, since Zabbix 2.0.4, the version of the API matches the version of Zabbix itself.
    print(zapi.api_version())  # zapi.apiinfo.version()
    print(zapi.do_request('apiinfo.version'))
    # Get item id with a item name
    print(zapi.get_id("item", item='Free memory'))


if __name__ == '__main__':
    ZABBIX_URL = 'https://localhost/zabbix'
    ZABBIX_USER = 'username'
    ZABBIX_PASSWORD = 'password'

    # Create ZabbixAPI class instance
    with ZabbixAPI(url=ZABBIX_URL, user=ZABBIX_USER, password=ZABBIX_PASSWORD) as zapi:

        # zapi.host.get(output=["host"]) --> zapi.do_request("host.get", params={"output":['host']})
        # Impl: pyzabbix.api.ZabbixAPI.__getattr__()
        # https://www.zabbix.com/documentation/4.0/manual/api/reference/host/get
        host_list = zapi.host.get(
            output=["host"],  # output="extend",
            selectInterfaces=["ip"],  # not mandatory
            status=0,
        )

        for host in host_list:  # type: dict
            print(host)
            host_name = host.get("host")
            host_id = host.get("hostid")
            print(host_name, get_free_memory())
            break
