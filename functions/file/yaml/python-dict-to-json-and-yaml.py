#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:html-form-multilevel-drop-down-list-data-structure-level-4.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/12/18
Create Time:            9:31
Description:            create nested drop down menu of parent child data
Long Description:       
References:
    - [create nested drop down menu of parent child data]
        (https://stackoverflow.com/questions/58145046/create-nested-drop-down-menu-of-parent-child-data)

Prerequisites:          []
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
import os
import sys

import yaml

try:
    from io import StringIO
except ImportError:
    try:
        import cStringIO as StringIO
    except ImportError:
        import StringIO

biz_dict = {
    "root": "top here",
    "data": {
        "level1_name1": {
            "id": 1,
            "parent_id": None,
            "value": "value",
            "sub_data": {
                "level2_name1": {
                    "id": 11,
                    "parent_id": 1,
                    "value": "value",
                    "sub_data": {
                        "level3_name1": {
                            "id": 111,
                            "parent_id": 11,
                            "value": "value",
                            "sub_data": {}
                        }
                    }
                }
            },
            "extra": "limits, etc"
        },
        "level1_name2": {
            "id": 2,
            "parent_id": None,
            "value": "value",
            "sub_data": {
                "level2_name1": {
                    "id": 21,
                    "parent_id": 2,
                    "value": "value",
                    "sub_data": {}
                },
                "level2_name2": {
                    "id": 22,
                    "parent_id": 2,
                    "value": "value",
                    "data": {}
                }
            },
            "extra": "limits, etc"
        }
    },
    "description": ""
}

biz_json = json.dumps(biz_dict, indent=4)

# dump yaml content to sys.stdout
yaml.safe_dump(biz_dict, sys.stdout, default_flow_style=False)

yaml_file_path = "the_yaml.yaml"

# dump yaml content to file
with open(yaml_file_path, 'w') as fp:
    yaml.safe_dump(biz_dict, fp, default_flow_style=False)

# load yaml content to python dict
with open(yaml_file_path, 'r') as fp:
    yaml_dict = yaml.safe_load(fp)
    print(yaml_dict)

if os.path.exists(yaml_file_path):
    os.remove(yaml_file_path)
