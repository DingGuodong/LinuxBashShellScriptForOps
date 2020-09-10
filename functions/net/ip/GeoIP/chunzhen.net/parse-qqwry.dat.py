#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:parse-qqwry.dat.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/9/9
Create Time:            10:16
Description:            parse qqwry.dat data file
Long Description:       
References:             [C/C++/Python写的纯真IP数据库访问例程](http://blog.chinaunix.net/uid-20758462-id-1876988.html)
                        [Python读取纯真IP数据库](https://blog.51cto.com/qicheng0211/1589442)
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
import struct


class ChunZhenIPLocator(object):
    def __init__(self, ip_db_file):
        self.cur_start_ip = 0
        self.cur_end_ip_offset = 0
        self.cur_end_ip = 0

        self.ipdb = open(ip_db_file, "rb")
        db_header = self.ipdb.read(8)
        (self.first_index, self.last_index) = struct.unpack('II', db_header)
        self.index_count = int((self.last_index - self.first_index) / 7) + 1
        print("当前IP数据库版本：{version}，记录总数: {count} 条".format(version=self.get_version(), count=self.index_count))

    def get_version(self):
        s = self.get_ip_addr(0xffffff00)
        return s.decode("utf-8")

    def get_area_addr(self, offset=0):
        if offset:
            self.ipdb.seek(offset)
        db_header = self.ipdb.read(1)
        (byte,) = struct.unpack('B', db_header)
        if byte == 0x01 or byte == 0x02:
            p = self.get_long3()
            if p:
                return self.get_string(p)
            else:
                return ""
        else:
            self.ipdb.seek(-1, 1)
            return self.get_string(offset)

    def get_addr(self, offset):
        self.ipdb.seek(offset + 4)
        db_header = self.ipdb.read(1)
        (byte,) = struct.unpack('B', db_header)
        if byte == 0x01:
            country_offset = self.get_long3()
            self.ipdb.seek(country_offset)
            db_header = self.ipdb.read(1)
            (b,) = struct.unpack('B', db_header)
            if b == 0x02:
                country_addr = self.get_string(self.get_long3())
                self.ipdb.seek(country_offset + 4)
            else:
                country_addr = self.get_string(country_offset)
            area_addr = self.get_area_addr()
        elif byte == 0x02:
            country_addr = self.get_string(self.get_long3())
            area_addr = self.get_area_addr(offset + 8)
        else:
            country_addr = self.get_string(offset + 4)
            area_addr = self.get_area_addr()
        return country_addr + b" " + area_addr

    def dump(self, first, last):
        if last > self.index_count:
            last = self.index_count
        for index in range(first, last):
            offset = self.first_index + index * 7
            self.ipdb.seek(offset)
            buf = self.ipdb.read(7)
            (ip, of1, of2) = struct.unpack("IHB", buf)
            address = self.get_addr(of1 + (of2 << 16))
            # 把GBK转为utf-8
            address = address.decode("gbk").encode("utf-8")
            print("%d\t%s\t%s" % (index, self.ip2str(ip), address))

    def set_ip_range(self, index):
        offset = self.first_index + index * 7
        self.ipdb.seek(offset)
        buf = self.ipdb.read(7)
        (self.cur_start_ip, of1, of2) = struct.unpack("IHB", buf)
        self.cur_end_ip_offset = of1 + (of2 << 16)
        self.ipdb.seek(self.cur_end_ip_offset)
        buf = self.ipdb.read(4)
        (self.cur_end_ip,) = struct.unpack("I", buf)

    def get_ip_addr(self, ip):
        left = 0
        right = self.index_count - 1
        while left < right - 1:
            middle = int((left + right) / 2)
            self.set_ip_range(middle)
            if ip == self.cur_start_ip:
                left = middle
                break
            if ip > self.cur_start_ip:
                left = middle
            else:
                right = middle
        self.set_ip_range(left)
        # version information,255.255.255.X,ugly but useful
        if ip & 0xffffff00 == 0xffffff00:
            self.set_ip_range(right)
        if self.cur_start_ip <= ip <= self.cur_end_ip:
            address = self.get_addr(self.cur_end_ip_offset)
            # 把GBK转为utf-8
            address = address.decode("gbk").encode("utf-8")
        else:
            address = "未找到该IP的地址"
        return address

    def get_ip_range(self, ip):
        self.get_ip_addr(ip)
        ip_range = self.ip2str(self.cur_start_ip) + ' - ' + self.ip2str(self.cur_end_ip)
        return ip_range

    def get_string(self, offset=0):
        if offset:
            self.ipdb.seek(offset)
        string = b""
        ch = self.ipdb.read(1)
        (byte,) = struct.unpack('B', ch)
        while byte != 0:
            string = string + ch
            ch = self.ipdb.read(1)
            (byte,) = struct.unpack('B', ch)
        return string

    @staticmethod
    def ip2str(ip):
        return str(ip >> 24) + '.' + str((ip >> 16) & 0xff) + '.' + str((ip >> 8) & 0xff) + '.' + str(ip & 0xff)

    @staticmethod
    def str2ip(s):
        (ip,) = struct.unpack('I', socket.inet_aton(s))
        return ((ip >> 24) & 0xff) | ((ip & 0xff) << 24) | ((ip >> 8) & 0xff00) | ((ip & 0xff00) << 8)

    def get_long3(self, offset=0):
        if offset:
            self.ipdb.seek(offset)
        string = self.ipdb.read(3)
        (a, b) = struct.unpack('HB', string)
        return (b << 16) + a


# Demo
def main():
    import sys
    ip_locator = ChunZhenIPLocator("qqwry.dat")

    if len(sys.argv) == 1:
        ip = "114.114.114.114"
    elif len(sys.argv) != 2:
        print('Usage: python {} <IP>'.format(sys.argv[0]))
        return
    else:
        ip = sys.argv[1]
    address = ip_locator.get_ip_addr(ip_locator.str2ip(ip))
    cur_range = ip_locator.get_ip_range(ip_locator.str2ip(ip))
    print("此IP %s 属于 %s\n所在网段: %s" % (ip, address.decode("utf-8"), cur_range))


if __name__ == "__main__":
    main()
