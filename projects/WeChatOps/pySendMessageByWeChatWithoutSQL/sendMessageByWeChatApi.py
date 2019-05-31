#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:sendMessageByWeChatApi.py
User:               Guodong
Create Date:        2017/9/25
Create Time:        19:00
Description:        Refactoring WeChat Message Sender by Python without SQL database
                    SQL is not required, using filesystem  persistent storage as database,
                    data are stored in  pickled objects, fetch data as access a python dict rather than a SQL database.
                    So far, I did not find the limits about message count can be sent on wechat official website.
References:
                    [微信公众平台-企业号开发者中心-接口文档](http://qydev.weixin.qq.com/wiki/index.php?title=%E9%A6%96%E9%A1%B5)
                    [发送接口说明](http://qydev.weixin.qq.com/wiki/index.php?title=%E5%8F%91%E9%80%81%E6%8E%A5%E5%8F%A3%E8%AF%B4%E6%98%8E)

Prerequisites:      [shelve, json,]
 """
import datetime
import json
import os
import shelve

import requests


class WeChatMessageSender(object):
    def __init__(self, cid, secret):
        self.corpid = cid
        self.corpsecret = secret

        self.database = 'wechat.db'

        self.requested_time = None

        self.valid_data = self.load_data()
        self.access_token = self.valid_data['access_token']

        self.message_data = dict()

    def get_token(self):
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"

        querystring = {
            "corpid": self.corpid,
            "corpsecret": self.corpsecret
        }

        headers = {
            'cache-control': "no-cache",
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        self.requested_time = datetime.datetime.now()

        response_data = response.text

        if response_data:
            return response_data
        else:
            return None

    def parse_token(self):
        data_type_json = self.get_token()
        if data_type_json != "" and data_type_json is not None:
            data_type_dict = json.loads(data_type_json)

            if data_type_dict['errcode'] == 0 or data_type_dict['errmsg'] == 'ok':
                return data_type_dict
            else:
                return None

    def retrieve_data(self):
        persistent_object = shelve.open(self.database)
        data = self.parse_token()
        if data is not None:
            persistent_object['access_token'] = data['access_token']
            persistent_object['expires_in'] = data['expires_in']
            persistent_object['requested_time'] = self.requested_time
            expire_time = self.requested_time + datetime.timedelta(seconds=data['expires_in'])
            persistent_object['expires_on'] = str(expire_time)
            persistent_object['is_expired'] = False

        self.valid_data = dict(persistent_object)
        persistent_object.close()

    def validate_data(self):
        if not os.path.exists(self.database):
            self.retrieve_data()

        persistent_object = shelve.open(self.database)
        data = dict(persistent_object)
        persistent_object.close()

        expire_time = datetime.datetime.strptime(data['expires_on'], '%Y-%m-%d %H:%M:%S.%f')
        now_time = datetime.datetime.now()
        if now_time > expire_time:
            self.retrieve_data()

    def load_data(self):
        self.validate_data()

        persistent_object = shelve.open(self.database)
        data = dict(persistent_object)
        persistent_object.close()
        return data

    def get_access_token(self):
        # test purpose
        return self.valid_data

    def reset_data(self):
        # test purpose for further use
        if os.path.exists(self.database):
            os.remove(self.database)
        self.get_access_token()

    def sender_config(self, content, to_user="", to_party="", to_tag="", msg_type="text", agent_id=1, safe=1):
        # parameters instruction see this URL as follows.
        # http://qydev.weixin.qq.com/wiki/index.php?title=%E6%B6%88%E6%81%AF%E7%B1%BB%E5%9E%8B%E5%8F%8A%E6%95%B0%E6%8D%AE%E6%A0%BC%E5%BC%8F
        self.message_data['touser'] = to_user
        self.message_data['toparty'] = to_party
        self.message_data['totag'] = to_tag
        self.message_data['msgtype'] = msg_type
        self.message_data['agentid'] = agent_id
        self.message_data['text'] = dict()
        self.message_data['text']['content'] = content
        self.message_data['safe'] = safe

    def send(self):
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send"

        querystring = {"access_token": self.access_token}

        payload = json.dumps(self.message_data, encoding='utf-8', ensure_ascii=False)

        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
        }

        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
        print(response.text)


if __name__ == '__main__':
    CorpID = 'your corp id'
    Secret = 'your secret for your corp id'
    w = WeChatMessageSender(CorpID, Secret)
    w.sender_config("message body to send.", to_user='username in your corp\'s app', agent_id=2)
    w.send()
