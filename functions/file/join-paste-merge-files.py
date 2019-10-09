#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:join-paste-merge-files.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/10/9
Create Time:            9:33
Description:            deep understanding buffering and flush in file
Long Description:       文件合并，合并文件，paste, merge lines of files
References:             https://docs.python.org/2/library/functions.html?highlight=open#open
                        https://docs.python.org/2/library/stdtypes.html#bltin-file-objects
                        [python读写文件write和flush](https://blog.csdn.net/fenfeiqinjian/article/details/49444973)
Tips: 需要注意的是：由于缓冲，字符串可能实际上没有出现在该写入的文件中，直到调用flush()或close()方法被调用.
一般的文件流操作都包含缓冲机制，write方法并不直接将数据写入文件，而是先写入内存中特定的缓冲区。
flush方法是用来刷新缓冲区的，即将缓冲区中的数据立刻写入文件，同时清空缓冲区。
正常情况下缓冲区满时，操作系统会自动将缓冲数据写入到文件中。
至于close方法，原理是内部先调用flush方法来刷新缓冲区，再执行关闭操作，这样即使缓冲区数据未满也能保证数据的完整性。
如果进程意外退出或正常退出时而未执行文件的close方法，缓冲区中的内容将会丢失。

Tips: 在使用循环将多个部分顺序写入文件时，一般程序员会忽略缓冲的影响，
要么关闭缓冲（bufferring，可能影响性能），要么执行刷新（flush）操作。

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
import codecs
import os

wanted_files_list = filter(lambda x: x.endswith('.csv'), os.listdir("."))

# 1. Apply to Python2.7, Python3.x has better open()
with codecs.open('joined_files_1.csv', 'wb', encoding='utf-8') as out:
    for filename in wanted_files_list:
        with codecs.open(filename, 'rb', encoding='utf-8') as inf:
            content = inf.read()  # type: unicode
            if content.endswith("\r\n"):
                out.write(content)
            else:
                out.write(content + '\r\n')
            out.flush()  # must fp.flush()

            # Note flush() does not necessarily write the file’s data to disk.
            # Use flush() followed by os.fsync() to ensure this behavior.
            # Force write of file with filedescriptor fd to disk.
            # to ensure that all internal buffers associated with f are written to disk.
            # https://docs.python.org/2/library/stdtypes.html#file.flush
            # https://docs.python.org/2/library/os.html#os.fsync
            os.fsync(out.fileno())


# 2. following code has same result
with open('joined_files_2.csv', 'wb') as out:
    for filename in wanted_files_list:
        with open(filename, 'rb') as inf:
            content = inf.read()  # type: str
            if content.endswith("\r\n"):
                out.write(content)
            else:
                out.write(content + '\r\n')
            out.flush()  # must fp.flush()

            # Note flush() does not necessarily write the file’s data to disk.
            # Use flush() followed by os.fsync() to ensure this behavior.
            # Force write of file with filedescriptor fd to disk.
            # to ensure that all internal buffers associated with f are written to disk.
            # https://docs.python.org/2/library/stdtypes.html#file.flush
            # https://docs.python.org/2/library/os.html#os.fsync
            os.fsync(out.fileno())


# 3. following code has same result too
with open('joined_files_3.csv', 'wb', buffering=0) as out:  # buffering = 0, does NOT need fp.flush()
    for filename in wanted_files_list:
        with open(filename, 'rb', buffering=0) as inf:
            content = inf.read()  # type: str
            if content.endswith("\r\n"):
                out.write(content)
            else:
                out.write(content + '\r\n')
