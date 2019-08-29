#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:get-value-from-json-in-pythonic-way.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/7/25
Create Time:            16:43
Description:            use JMESPath to get a value from json
Long Description:       such as get a very deep value from the json returned by aliyun API
References:             [JMESPath Tutorial](http://jmespath.org/tutorial.html)
                        [JMESPath Examples](http://jmespath.org/examples.html)
Prerequisites:          pip install jmespath
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

import jmespath

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

target_json_dict = json.loads(test_json_str, encoding='utf-8')

wanted_value = jmespath.search("SecurityGroups.SecurityGroup[*].SecurityGroupId | [0]", target_json_dict)
print(wanted_value)

print(jmespath.search("SecurityGroups.SecurityGroup[0].SecurityGroupId", target_json_dict))

print(jmespath.search("SecurityGroups.SecurityGroup[*].SecurityGroupId", target_json_dict))

print(jmespath.search("SecurityGroups.SecurityGroup[?Description=='Description'] | [0]", target_json_dict))

print(jmespath.search("SecurityGroups.SecurityGroup[?Description=='Description'] | [0].SecurityGroupId",
                      target_json_dict))
