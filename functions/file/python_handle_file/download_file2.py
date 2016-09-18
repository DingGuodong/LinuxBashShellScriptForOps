#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:download_file2.py
User:               Guodong
Create Date:        2016/9/14
Create Time:        9:40
 """
import requests
import progressbar
import requests.packages.urllib3

requests.packages.urllib3.disable_warnings()

url = "https://raw.githubusercontent.com/racaljk/hosts/master/hosts"

response = requests.request("GET", url, stream=True, data=None, headers=None)

save_path = "/tmp/hosts"

total_length = int(response.headers.get("Content-Length"))
with open(save_path, 'wb') as f:
    # widgets = ['Processed: ', progressbar.Counter(), ' lines (', progressbar.Timer(), ')']
    # pbar = progressbar.ProgressBar(widgets=widgets)
    # for chunk in pbar((i for i in response.iter_content(chunk_size=1))):
    #     if chunk:
    #         f.write(chunk)
    #         f.flush()

    widgets = ['Progress: ', progressbar.Percentage(), ' ',
               progressbar.Bar(marker='#', left='[', right=']'),
               ' ', progressbar.ETA(), ' ', progressbar.FileTransferSpeed()]
    pbar = progressbar.ProgressBar(widgets=widgets, maxval=total_length).start()
    for chunk in response.iter_content(chunk_size=1):
        if chunk:
            f.write(chunk)
            f.flush()
        pbar.update(len(chunk) + 1)
    pbar.finish()
