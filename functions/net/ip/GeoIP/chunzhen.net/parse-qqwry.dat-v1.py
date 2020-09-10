#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:parse-qqwry.dat-v1.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/9/9
Create Time:            17:26
Description:            parse qqwry.dat data file
Long Description:       
References:             https://github.com/animalize/qqwry-python3
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
# coding=utf-8
#
# for Python 3.0+
# 来自 https://pypi.python.org/pypi/qqwry-py3
# 版本：2020-06-25
#
# 用法
# ============
# from qqwry import QQwry
# q = QQwry()
# q.load_file('qqwry.dat')
# result = q.lookup('8.8.8.8')
#
#
# 解释q.load_file(filename, load_index=False)函数
# --------------
# 加载qqwry.dat文件。成功返回True，失败返回False。
#
# 参数filename可以是qqwry.dat的文件名（str类型），也可以是bytes类型的文件内容。
#
# 当参数load_index=False时（默认参数）：
# 程序行为：把整个文件读入内存，从中搜索
# 加载速度：很快，0.004 秒
# 进程内存：较少，16.9 MB
# 查询速度：较慢，5.3 万次/秒
# 使用建议：适合桌面程序、大中小型网站
#
# 当参数load_index=True时：
# 程序行为：把整个文件读入内存。额外加载索引，把索引读入更快的数据结构
# 加载速度：★★★非常慢，因为要额外加载索引，0.78 秒★★★
# 进程内存：较多，22.0 MB
# 查询速度：较快，18.0 万次/秒
# 使用建议：仅适合高负载服务器
#
# （以上是在i3 3.6GHz, Win10, Python 3.6.2 64bit，qqwry.dat 8.86MB时的数据）
#
#
# 解释q.lookup('8.8.8.8')函数
# --------------
# 找到则返回一个含有两个字符串的元组，如：('国家', '省份')
# 没有找到结果，则返回一个None
#
#
# 解释q.clear()函数
# --------------
# 清空已加载的qqwry.dat
# 再次调用load_file时不必执行q.clear()
#
#
# 解释q.is_loaded()函数
# --------------
# q对象是否已加载数据，返回True或False
#
#
# 解释q.get_last_one()函数
# --------------
# 返回最后一条数据，最后一条通常为数据的版本号
# 没有数据则返回一个None

import array
import bisect
import logging
import socket
import struct

__all__ = ('QQwry',)

logger = logging.getLogger(__name__)


def int3(data, offset):
    return data[offset] + (data[offset + 1] << 8) + \
           (data[offset + 2] << 16)


def int4(data, offset):
    return data[offset] + (data[offset + 1] << 8) + \
           (data[offset + 2] << 16) + (data[offset + 3] << 24)


class QQwry(object):
    def __init__(self):
        self.idx1 = None
        self.idx2 = None
        self.idxo = None

        self.data = None
        self.index_begin = -1
        self.index_end = -1
        self.index_count = -1

        self.__fun = None

    def clear(self):
        self.idx1 = None
        self.idx2 = None
        self.idxo = None

        self.data = None
        self.index_begin = -1
        self.index_end = -1
        self.index_count = -1

        self.__fun = None

    def load_file(self, filename, load_index=False):
        self.clear()

        if type(filename) == bytes:
            self.data = buffer_ = filename
            filename = 'memory data'
        elif type(filename) == str:
            # read file
            try:
                with open(filename, 'br') as f:
                    self.data = buffer_ = f.read()
            except Exception as e:
                logger.error('%s open failed：%s' % (filename, str(e)))
                self.clear()
                return False

            if self.data is None:
                logger.error('%s load failed' % filename)
                self.clear()
                return False
        else:
            self.clear()
            return False

        if len(buffer_) < 8:
            logger.error('%s load failed, file only %d bytes' %
                         (filename, len(buffer_))
                         )
            self.clear()
            return False

            # index range
        index_begin = int4(buffer_, 0)
        index_end = int4(buffer_, 4)
        if index_begin > index_end or \
                (index_end - index_begin) % 7 != 0 or \
                index_end + 7 > len(buffer_):
            logger.error('%s index error' % filename)
            self.clear()
            return False

        self.index_begin = index_begin
        self.index_end = index_end
        self.index_count = (index_end - index_begin) // 7 + 1

        if not load_index:
            logger.info('%s %s bytes, %d segments. without index.' %
                        (filename, format(len(buffer_), ','), self.index_count)
                        )
            self.__fun = self.__raw_search
            return True

        # load index
        self.idx1 = array.array('L')
        self.idx2 = array.array('L')
        self.idxo = array.array('L')

        try:
            for i in range(self.index_count):
                ip_begin = int4(buffer_, index_begin + i * 7)
                offset = int3(buffer_, index_begin + i * 7 + 4)

                # load ip_end
                ip_end = int4(buffer_, offset)

                self.idx1.append(ip_begin)
                self.idx2.append(ip_end)
                self.idxo.append(offset + 4)
        except Exception:
            logger.error('%s load index error' % filename)
            self.clear()
            return False

        logger.info('%s %s bytes, %d segments. with index.' %
                    (filename, format(len(buffer_), ','), len(self.idx1))
                    )
        self.__fun = self.__index_search
        return True

    def __get_addr(self, offset):
        # mode 0x01, full jump
        mode = self.data[offset]
        if mode == 1:
            offset = int3(self.data, offset + 1)
            mode = self.data[offset]

        # country
        if mode == 2:
            off1 = int3(self.data, offset + 1)
            c = self.data[off1:self.data.index(b'\x00', off1)]
            offset += 4
        else:
            c = self.data[offset:self.data.index(b'\x00', offset)]
            offset += len(c) + 1

        # province
        if self.data[offset] == 2:
            offset = int3(self.data, offset + 1)
        p = self.data[offset:self.data.index(b'\x00', offset)]

        return c.decode('gb18030', errors='replace'), p.decode('gb18030', errors='replace')

    def lookup(self, ip_str):
        try:
            ip = struct.unpack(">I", socket.inet_aton(ip_str))[0]
            return self.__fun(ip)
        except Exception:
            return None

    def __raw_search(self, ip):
        left = 0
        right = self.index_count

        while right - left > 1:
            m = (left + right) // 2
            offset = self.index_begin + m * 7
            new_ip = int4(self.data, offset)

            if ip < new_ip:
                right = m
            else:
                left = m

        offset = self.index_begin + 7 * left
        ip_begin = int4(self.data, offset)

        offset = int3(self.data, offset + 4)
        ip_end = int4(self.data, offset)

        if ip_begin <= ip <= ip_end:
            return self.__get_addr(offset + 4)
        else:
            return None

    def __index_search(self, ip):
        posi = bisect.bisect_right(self.idx1, ip) - 1

        if posi >= 0 and self.idx1[posi] <= ip <= self.idx2[posi]:
            return self.__get_addr(self.idxo[posi])
        else:
            return None

    def is_loaded(self):
        return self.__fun is not None

    def get_last_one(self):
        try:
            offset = int3(self.data, self.index_end + 4)
            return self.__get_addr(offset + 4)
        except Exception:
            return None


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        fn = 'qqwry.dat'
        q = QQwry()
        q.load_file(fn)
        print(q.get_last_one())

        for cur_ip_str in sys.argv[1:]:
            s = q.lookup(cur_ip_str)
            print('%s\n%s' % (cur_ip_str, s))
    elif len(sys.argv) == 1:
        cur_ip_str = "114.114.114.114"
        fn = 'qqwry.dat'
        q = QQwry()
        q.load_file(fn)
        print(q.get_last_one())
        s = q.lookup(cur_ip_str)
        print('%s\n%s' % (cur_ip_str, s))
    else:
        print('请以查询ip作为参数运行')
