#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyCheckWebsitesStatus.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/12/29
Create Time:            16:42
Description:            check websites status
Long Description:       https://www.githubstatus.com/api/v2/status.json
                        {
                          "page": {
                            "id": "kctbh9vrtdwd",
                            "name": "GitHub",
                            "url": "https://www.githubstatus.com",
                            "time_zone": "Etc/UTC",
                            "updated_at": "2018-12-29T08:52:34.841Z"
                          },
                          "status": {
                            "indicator": "none",
                            "description": "All Systems Operational"
                          }
                        }
References:             
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
import socket
import threading

import dns.resolver
import requests


def main(url):
    if not check_website_status(url):
        print "%s down" % url


def check_website_status(url):
    return is_url_can_get(parse_url(url))


def is_url_can_get(url):
    try:
        resp = requests.get(url)
        if resp.ok:
            return True
        else:
            return False
    except requests.RequestException:
        return False


def parse_url(url="www.githubstatus.com", ssl=False):
    if url.startswith('http'):
        return url
    elif ssl:
        return 'https://' + url
    else:
        return 'http://' + url


def query_dns_rr(qname, rdtype="A", nameserver="8.8.8.8", debug=False):
    if 'http' in qname:
        qname = get_domain_name_from_url(qname)

    resolver = dns.resolver.Resolver()
    resolver.timeout = 3  # does it really works?
    resolver.nameservers = [nameserver]  # default_nameserver = resolver.nameservers
    resolver.cache = False
    answer = None
    try:
        answer = resolver.query(qname, rdtype).response.answer
    except dns.resolver.NoAnswer as e:
        if debug:
            print(e)
        pass
    except dns.resolver.NXDOMAIN as e:
        if debug:
            print(e)
        pass
    except dns.exception.Timeout as e:
        if debug:
            print(e)
        pass
    except dns.resolver.NoNameservers as e:
        if debug:
            print(e)
        pass

    records = []
    if answer:
        for record in answer[-1]:
            records.append(str(record))
        return records
    else:
        return records


def get_domain_name_from_url(url):
    # https://stackoverflow.com/questions/9626535/get-domain-name-from-url
    # https://docs.python.org/2/library/urlparse.html
    from urlparse import urlparse
    parsed_uri = urlparse(url)
    # domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    domain_name = "{uri.netloc}".format(uri=parsed_uri)
    return domain_name


if __name__ == '__main__':
    socket.setdefaulttimeout(3)  # does it really works?

    sites_list = []
    sites_string = """
www.microsoft.com
www.redhat.com
http://www.qq.com
https://github.com
any_else_site_not_exists
    """
    for site in sites_string.split('\n'):
        if site.strip() != '':
            sites_list.append(site.strip())
    print sites_list

    for site in sites_list:
        res = query_dns_rr(site)
        if len(res) != 0:
            print "%s %s" % (site, res[0])
        else:
            print "%s %s" % (site, "not available")

    threading_pool = list()
    for site in sites_list:
        threading_pool.append(threading.Thread(target=main, args=(site,)))

    for thread in threading_pool:
        thread.setDaemon(True)
        thread.start()

    thread.join()
