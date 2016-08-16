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
import odbp_database
import datetime
import time
import sys


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
        limit = None
        date = None
        try:
            limit = odbp_database.sqlite3_get_limits()
        except odbp_database.sqlite3.Error:
            pass

        if limit is not None:
            date = limit[0][1]
            day_in_database = time.strftime("%d", time.strptime(date, "%Y-%m-%d %H:%M:%S"))
            day_in_local = time.strftime("%d", time.localtime(time.time()))
            if day_in_database < day_in_local:
                used = 600
                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            else:
                used = limit[0][0]
                date = limit[0][1]

            if used > 600:
                print "reached to limit, please try again tomorrow!"
            else:
                pass
        else:
            print "Get limit from database failed! result is %s" % limit

        if to_user is not None and content is not None:
            self.data['touser'] = to_user
            self.data['text']['content'] = content
        else:
            print "parameters wrong!"
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
            try:
                limit = odbp_database.sqlite3_get_limits()
            except odbp_database.sqlite3.Error as e:
                print e
                sys.exit(1)
            else:
                if limit is not None:
                    odbp_database.sqlite3_update_limit(limit[0][0] + 1, date)
                    print "The limit used times is %s." % (limit[0][0] + 1)
                else:
                    odbp_database.sqlite3_set_limit(600, 1, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        else:
            print "Send failed! %s " % return_content
