# -*- coding: utf-8 -*-
import json

# https://code.visualstudio.com/docs/editor/userdefinedsnippets
vscode_used_defined_snippets_text = r'''
#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by Visual Studio Code.
File Name:              LinuxBashShellScriptForOps: .py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            $CURRENT_MONTH_NAME_SHORT/$CURRENT_DATE/$CURRENT_YEAR_SHORT
Create Time:            $CURRENT_HOUR:$CURRENT_MINUTE
Description:            
Long Description:       
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
 '''

python_json_dict = {"body": vscode_used_defined_snippets_text.strip().split("\n")}

print(json.dumps(python_json_dict, indent=4))
