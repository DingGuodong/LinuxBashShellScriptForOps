#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:get-value-from-json-with-jsonpath.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/11/1
Create Time:            9:40
Description:            use jsonpath to get wanted resource from json string object
Long Description:       
References:             
Prerequisites:          pip2.7 install jsonpath
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

import json

import jsonpath

test_json_str = """
{
    "PageNumber": 1,
    "TotalCount": 1,
    "PageSize": 10,
    "RegionId": "cn-hangzhou",
    "RequestId": "C435DD12-35E1-XXXX-XXXX-107C2873E91D",
    "SecurityGroups": {
        "SecurityGroup": [
            {
                "CreationTime": "2016-10-27T01:49:17Z",
                "Tags": {
                    "Tag": []
                },
                "SecurityGroupId": "sg-SecurityGroupId",
                "SecurityGroupName": "SecurityGroupName",
                "Description": "Description",
                "ResourceGroupId": "",
                "SecurityGroupType": "normal",
                "VpcId": ""
            }
        ]
    }
}
"""

wanted_res_1 = jsonpath.jsonpath(json.loads(test_json_str), "$.SecurityGroups.SecurityGroup[0].SecurityGroupId")

wanted_res_2 = jsonpath.jsonpath(json.loads(test_json_str),
                                 '$.SecurityGroups.SecurityGroup[?(@.Description=="Description")].SecurityGroupId')

wanted_res_3 = jsonpath.jsonpath(json.loads(test_json_str), "$.SecurityGroups.SecurityGroup[*].SecurityGroupId")
