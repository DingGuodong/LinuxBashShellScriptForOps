#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:json2dict2json.py
User:               Guodong
Create Date:        2016/8/26
Create Time:        14:37
 """

import json

json_string = '''
        {"login": "DingGuodong", "id": 5717062, "avatar_url": "https://avatars.githubusercontent.com/u/5717062?v=3",
        "gravatar_id": "", "url": "https://api.github.com/users/DingGuodong",
        "html_url": "https://github.com/DingGuodong",
        "followers_url": "https://api.github.com/users/DingGuodong/followers",
        "following_url": "https://api.github.com/users/DingGuodong/following{/other_user}",
        "gists_url": "https://api.github.com/users/DingGuodong/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/DingGuodong/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/DingGuodong/subscriptions",
        "organizations_url": "https://api.github.com/users/DingGuodong/orgs",
        "repos_url": "https://api.github.com/users/DingGuodong/repos",
        "events_url": "https://api.github.com/users/DingGuodong/events{/privacy}",
        "received_events_url": "https://api.github.com/users/DingGuodong/received_events", "type": "User",
        "site_admin": false, "name": "Guodong Ding", "company": null, "blog": "http://dgd2010.blog.51cto.com/",
        "location": "Qingdao,Shandong,China", "email": null, "hireable": null, "bio": "https://dingguodong.github.io/",
        "public_repos": 60, "public_gists": 0, "followers": 9, "following": 9, "created_at": "2013-10-18T09:29:33Z",
        "updated_at": "2016-08-24T02:22:30Z", "private_gists": 0, "total_private_repos": 0, "owned_private_repos": 0,
        "disk_usage": 13590, "collaborators": 0,
        "plan": {"name": "free", "space": 976562499, "collaborators": 0, "private_repos": 0}}
        '''
json_dict = {'X-XSS-Protection': '1; mode=block', 'Content-Security-Policy': "default-src 'none'",
             'Access-Control-Expose-Headers': 'ETag, Link, X-GitHub-OTP, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, X-OAuth-Scopes, X-Accepted-OAuth-Scopes, X-Poll-Interval',
             'Transfer-Encoding': 'chunked', 'Last-Modified': 'Wed, 24 Aug 2016 02:22:30 GMT',
             'Access-Control-Allow-Origin': '*', 'X-Frame-Options': 'deny', 'Status': '200 OK',
             'X-Served-By': 'a6882e5cd2513376cb9481dbcd83f3a2', 'X-GitHub-Request-Id': '3A38BA32:54A9:81AB47E:57BFE3D9',
             'ETag': 'W/"2453e886f13d1ca1f51f8268d4ce7bd5"', 'Date': 'Fri, 26 Aug 2016 06:38:17 GMT',
             'X-RateLimit-Remaining': '4993',
             'Strict-Transport-Security': 'max-age=31536000; includeSubdomains; preload',
             'Server': 'GitHub.com', 'X-GitHub-Media-Type': 'github.v3', 'X-Content-Type-Options': 'nosniff',
             'Content-Encoding': 'gzip', 'Vary': 'Accept, Authorization, Cookie, X-GitHub-OTP, Accept-Encoding',
             'X-RateLimit-Limit': '5000', 'Cache-Control': 'private, max-age=60, s-maxage=60',
             'Content-Type': 'application/json; charset=utf-8', 'X-RateLimit-Reset': '1472194721'}

json_string2dict = json.loads(json_string)
dict2json = json.dumps(json_dict, indent=4)
