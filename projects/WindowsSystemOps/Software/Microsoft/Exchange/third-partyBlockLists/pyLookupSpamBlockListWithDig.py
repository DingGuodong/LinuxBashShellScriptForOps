#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyLookupSpamBlockListWithDig.py
User:               Guodong
Create Date:        2017/8/31
Create Time:        11:06
Description:        check if IP is in Spamhaus Block List,
                    using gevent( a coroutine -based Python networking library) and dig(a dns/bind utils)
References:         https://gist.github.com/danielpunkass/4287421
 """

from gevent import monkey

monkey.patch_all()
import gevent


class SpamHausChecker(object):
    """spam checker using spamhaus"""

    def __init__(self):
        self.in_block_list = False
        self.block_list_name = list()
        self.block_list = (
            ".zen.spamhaus.org",
            ".sbl.spamhaus.org",
            ".xbl.spamhaus.org",
            ".pbl.spamhaus.org",
        )

    def is_spam(self, ip):
        query = self.__build_spamhaus_zone(ip)
        return self.__query_spamhaus(query) != ""

    def is_not_spam(self, ip):
        query = self.__build_spamhaus_zone(ip)
        return self.__query_spamhaus(query) == ""

    def real_is_spam(self, ip):
        gevent.joinall(
            [gevent.spawn(self.__query_spamhaus_all_zone, query) for query in self.__build_spamhaus_zones(ip)])

        if self.in_block_list:
            return True
        else:
            return False

    def __build_spamhaus_zones(self, ip):
        ip_segments = ip.split(".")
        ip_segments.reverse()
        return [".".join(ip_segments) + zone for zone in self.block_list]

    @staticmethod
    def __build_spamhaus_zone(ip):
        ip_segments = ip.split(".")
        ip_segments.reverse()
        return ".".join(ip_segments) + ".zen.spamhaus.org"

    @staticmethod
    def __query_spamhaus(query):
        import subprocess
        # command list:
        # dig +short -t TXT 98.14.129.124.zen.spamhaus.org
        # dig +short -t TXT 90.14.129.124.zen.spamhaus.org
        # dig +short -t TXT 98.14.129.124.sbl.spamhaus.org
        # dig +short -t TXT 98.14.129.124.xbl.spamhaus.org
        # dig +short -t TXT 98.14.129.124.pbl.spamhaus.org
        proc_obj = subprocess.Popen("dig +short -t TXT {name}".format(name=query), shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
        stdout, stderr = proc_obj.communicate()
        return_code = proc_obj.returncode
        if return_code == 0:
            return stdout
        else:
            return stderr

    def __query_spamhaus_all_zone(self, query):
        import subprocess
        command = "dig +short -t TXT {name}".format(name=query)
        proc_obj = subprocess.Popen(command, shell=True,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
        stdout, stderr = proc_obj.communicate()
        return_code = proc_obj.returncode
        if return_code == 0:
            if stdout != "":
                self.block_list_name.append(query)
                self.in_block_list = True
        else:
            raise IOError("Run command \"{command}\" failed, return code is {return_code}, output is {stdout}".format(
                command=command, return_code=return_code, stdout=(stdout, stderr)))


if __name__ == '__main__':
    q = SpamHausChecker()
    print(q.is_spam("124.129.14.90"))
    print(q.is_not_spam("124.129.14.90"))

    print(q.is_spam("58.56.175.254"))
    print(q.is_not_spam("58.56.175.254"))

    print(q.real_is_spam('124.129.14.90'))
    print(q.real_is_spam('58.56.175.254'))
