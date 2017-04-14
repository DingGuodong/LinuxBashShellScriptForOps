#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:odbp_sendMessage.py
User:               Guodong
Create Date:        2016/8/12
Create Time:        14:49
 """

import odbp_getToken


class WeiXinSendMsgClass(object):
    def __init__(self):
        self.access_token = odbp_getToken.WeiXinTokenClass().get()
        self.to_user = ""
        self.to_party = ""
        self.to_tag = ""
        self.msg_type = "text"
        self.agent_id = 2
        self.content = ""
        self.safe = 0

        self.data = {
            "touser": self.to_user,
            "toparty": self.to_party,
            "totag": self.to_tag,
            "msgtype": self.msg_type,
            "agentid": self.agent_id,
            "text": {
                "content": self.content
            },
            "safe": self.safe
        }

    def send(self, to_user, content):
        if to_user is not None and content is not None:
            self.data['touser'] = to_user
            self.data['text']['content'] = content
        else:
            print
            raise RuntimeError
        import requests
        import json

        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send"

        querystring = {"access_token": self.access_token}

        payload = json.dumps(self.data, encoding='utf-8', ensure_ascii=False)

        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
        }

        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

        return_content = json.loads(response.content)
        if return_content["errcode"] == 0 and return_content["errmsg"] == "ok":
            print "Send successfully! %s " % return_content
        else:
            print "Send failed! %s " % return_content
