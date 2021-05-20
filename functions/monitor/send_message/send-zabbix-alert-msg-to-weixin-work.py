#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:sendMessageByWeChatWorkApi.py
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
                    update@202104
                    [企业微信发送应用消息](https://work.weixin.qq.com/api/doc/90000/90135/90236)
Prerequisites:      [six, shelve, json, requests]
 """
import datetime
import json
import os
import shelve
import sys

import requests
import six


class WeChatMessageSender(object):
    def __init__(self, cid, secret):
        self.corpid = cid
        self.corpsecret = secret

        # please set this value into abs path, such as `/usr/lib/zabbix/alertscripts/wechat.db` when using zabbix.
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
        """

        :param content:
                        text: 消息内容，最长不超过2048个字节，注意：主页型应用推送的文本消息在微信端最多只显示20个字（包含中英文）
        :type content:
        :param to_user: 成员名称使用该成员在企业微信中的账号名（并非显示名称），账号名可以在企业微信后台查到
                        成员ID列表（消息接收者，多个接收者用‘|’分隔，最多支持1000个）。
                        特殊情况：指定为@all，则向关注该企业应用的全部成员发送
        :type to_user: str
        :param to_party:部门ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为@all时忽略本参数
        :type to_party:
        :param to_tag:标签ID列表，多个接收者用‘|’分隔，最多支持100个。当touser为@all时忽略本参数
        :type to_tag:
        :param msg_type:消息类型，此时固定为：text （支持消息型应用跟主页型应用）, 支持news, file, voice
        :type msg_type:
        :param agent_id:企业应用的id，整型。可在应用的设置页面查看
        :type agent_id:
        :param safe: 表示是否是保密消息，0表示否，1表示是，默认0
        :type safe:
        :return:
        :rtype:
        """
        # parameters instruction see this URL as follows.
        # http://qydev.weixin.qq.com/wiki/index.php?title=%E6%B6%88%E6%81%AF%E7%B1%BB%E5%9E%8B%E5%8F%8A%E6%95%B0%E6%8D%AE%E6%A0%BC%E5%BC%8F
        self.message_data['touser'] = to_user
        self.message_data['toparty'] = to_party
        self.message_data['totag'] = to_tag
        self.message_data['msgtype'] = msg_type
        self.message_data['agentid'] = agent_id
        if msg_type == "text":
            self.message_data['text'] = dict()
            self.message_data['text']['content'] = content
        elif msg_type == "markdown":  # qa failed, ui not support
            self.message_data['markdown'] = dict()
            self.message_data['markdown']['content'] = content
        self.message_data['safe'] = safe

    def send(self, debug=False):
        """
        该方法不同于企业微信机器人，此方法是将信息通过企业微信管理后台中"应用管理"中创建的"应用"，
        发送给该应用中的成员，成员名称使用该成员在企业微信中的账号名（并非显示名称），账号名可以在企业微信后台查到
        :return:
        :rtype:
        """
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send"

        if debug:
            querystring = {
                "access_token": self.access_token,
                "debug": "1"
            }
        else:
            querystring = {"access_token": self.access_token}

        if six.PY2:
            payload = json.dumps(self.message_data, encoding='utf-8', ensure_ascii=False)
        else:
            payload = json.dumps(self.message_data, ensure_ascii=False)

        headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
        }

        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
        print(response.text)


def usage():
    print("""
    Function: send markdown message to somebody using wechat work API
    Usage: python %s <username> <subject> <message body>
    Zabbix setting: 'Administration' -> 'Media types' 
                    https://hostname/zabbix.php?action=mediatype.edit&mediatypeid=4
                    Script parameters: {ALERT.SENDTO} {ALERT.SUBJECT} {ALERT.MESSAGE}
    Example: python %s "username" "Test email from Python" "Python rules them all!"
""" % (__file__, sys.argv[0]))
    sys.exit(0)


if __name__ == '__main__':
    # [企业微信管理后台](https://work.weixin.qq.com/wework_admin/)
    CorpID = 'your corp id'  # 企业ID，可通过企业微信后台"我的企业"|"企业ID"查看
    Secret = 'app secret'  # 企业微信中自建企业应用的Secret
    AgentID = 1000010  # 企业微信中自建企业应用的AgentId
    # ToUser = 'DingGuodong'  # 企业微信企业成员的账号名（非显示名）

    argv_length = len(sys.argv)
    if not (argv_length == 1 or argv_length == 4):
        print("bad call")
    if argv_length == 1:
        subject = "Test Message"
        message = "Test message sent by Python over Wechat Work"
        to_user = 'DingGuodong'  # if there are more than one phone number to at, use space spilt them
        # at_all = False
    else:
        to_user = sys.argv[1]
        subject = sys.argv[2]
        message = sys.argv[3]
        if subject == "":
            subject = "empty subject."
        if message == "":
            message = "empty message."

    basic_msg_template = """
### {subject}
{message}
""".format(subject=subject, message=message).strip()

    w = WeChatMessageSender(CorpID, Secret)
    w.sender_config(basic_msg_template, to_user=to_user, agent_id=AgentID, msg_type="markdown", safe=0)
    w.send()
