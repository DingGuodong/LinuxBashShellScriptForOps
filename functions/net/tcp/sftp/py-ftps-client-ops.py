#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:py-ftps-client-ops.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2019/9/17
Create Time:            17:27
Description:            use python test connection to ftp server
Long Description:
References:             FTP, FTPS and SFTP client
                        ftp://commontest:commontest@202.108.196.163:990/image
                        yum install -y lftp
                        lftp -u commontest,commontest -p 990 202.108.196.163
                        yum install -y ncftp
                        ncftp -u commontest -p commontest -P 990 202.108.196.163 /image
                        https://stackoverflow.com/questions/17204276/python-ftplib-specify-port

                        https://docs.python.org/2/library/ftplib.html

                        Tips: use Class is better than functional programming
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
import ssl
from ftplib import FTP, FTP_TLS, error_perm


def connect_ftp():
    ftp = FTP()
    # ftp.set_debuglevel(2)
    ftp.connect(host=server, port=port, timeout=10)
    ftp.login(user=username, passwd=password)
    return ftp


def connect_ftps():
    """
    FTP over TLS
    NOte:
        do NOT enable 'Require TLS session resumption on data connection when using PROT P',
        or you will get exception 'ssl.SSLEOFError: EOF occurred in violation of protocol (_ssl.c:727)'
        or server side will show '450 TLS session of data connection has not resumed or the session does not match the control connection'
    :return:
    """
    ftps = FTP_TLS()
    # ftps.set_debuglevel(2)
    ssl_version_stack = [ssl.PROTOCOL_SSLv23, ssl.PROTOCOL_SSLv3]
    tls_version_stack = [ssl.PROTOCOL_TLSv1_2, ssl.PROTOCOL_TLSv1, ssl.PROTOCOL_TLS]
    is_connected = False
    for ssl_version in ssl_version_stack + tls_version_stack:  # also can use list.extend() or list slice instead of +
        ftps.ssl_version = ssl_version
        try:
            ftps.connect(host=server, port=port)
            is_connected = True
            break
        except socket.timeout:
            continue
        except socket.error as e:
            # such as '10061', '[Errno 10061]  Connection refused.'
            print(str(e), socket.errorTab.get(int(str(e).strip()[7:-1])))
            continue
    else:
        if not is_connected:
            raise RuntimeError("No SSL/TLS supported on ftp server, does server misconfigured?")

    ftps.login(user=username, passwd=password)
    ftps.prot_p()  # 'Force PROT P to encrypt file transfers when using FTP TLS'
    return ftps


def put_file_to_ftp(ftp, src, dst):
    try:
        with open(src, 'rb') as fp:
            ftp.storbinary('STOR ' + dst, fp)
    except socket.error:
        # [ssl unwrap fails with Error 0](https://bugs.python.org/issue10808)
        # [FTP_TLS errors when use certain subcommands](https://bugs.python.org/issue31727)
        pass


def get_file_from_ftp(ftp, src, dst):
    with open(dst, 'wb') as fp:
        ftp.retrbinary('RETR ' + src, fp.write)


if __name__ == '__main__':
    server = '192.168.88.30'
    port = 990  # default port: 21
    username = 'testuser'
    password = 'testuser'
    root_path = '/'

    try:
        conn = connect_ftp()
    except error_perm as e:
        print(e)
        # 530 This server does not allow plain FTP. You have to use FTP over TLS.
        conn = connect_ftps()

    # conn.set_debuglevel(0)
    print(conn.getwelcome())
    # print(conn.pwd())
    # conn.dir()
    print(conn.retrlines("LIST"))  # conn.putcmd("LIST")
    conn.quit()
