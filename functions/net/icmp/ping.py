#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:ping.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/10/18
Create Time:            11:35
Description:            A pure python ping implementation using raw socket
Long Description:       update: fix timeout not work really

                        A pure python ping implementation using raw socket.


                        Note that ICMP messages can only be sent from processes running as root.


                        Derived from ping.c distributed in Linux's netkit. That code is
                        copyright (c) 1989 by The Regents of the University of California.
                        That code is in turn derived from code written by Mike Muuss of the
                        US Army Ballistic Research Laboratory in December, 1983 and
                        placed in the public domain. They have my thanks.

                        Bugs are naturally mine. I'd be glad to hear about them. There are
                        certainly word - size dependenceies here.

                        Copyright (c) Matthew Dixon Cowles, <http://www.visi.com/~mdc/>.
                        Distributable under the terms of the GNU General Public License
                        version 2. Provided with no warranties of any sort.

                        Original Version from Matthew Dixon Cowles:
                          -> ftp://ftp.visi.com/users/mdc/ping.py

                        Rewrite by Jens Diemer:
                          -> http://www.python-forum.de/post-69122.html#69122


                        Revision history
                        ~~~~~~~~~~~~~~~~

                        March 11, 2010
                        changes by Samuel Stauffer:
                        - replaced time.clock with default_timer which is set to
                          time.clock on windows and time.time on other systems.

                        May 30, 2007
                        little rewrite by Jens Diemer:
                         -  change socket asterisk import to a normal import
                         -  replace time.time() with time.clock()
                         -  delete "return None" (or change to "return" only)
                         -  in checksum() rename "str" to "source_string"

                        November 22, 1997
                        Initial hack. Doesn't do much, but rather than try to guess
                        what features I (or others) will want in the future, I've only
                        put in what I need now.

                        December 16, 1997
                        For some reason, the checksum bytes are in the wrong order when
                        this is run under Solaris 2.X for SPARC but it works right under
                        Linux x86. Since I don't know just what's wrong, I'll swap the
                        bytes always and then do an htons().

                        December 4, 2000
                        Changed the struct.pack() calls to pack the checksum and ID as
                        unsigned. My thanks to Jerome Poincheval for the fix.

                        Januari 27, 2015
                        Changed receive response to not accept ICMP request messages.
                        It was possible to receive the very request that was sent.

                        Last commit info:
                        ~~~~~~~~~~~~~~~~~
                        $LastChangedDate: $
                        $Rev: $
                        $Author: $
References:             https://raw.githubusercontent.com/samuel/python-ping/master/ping.py
Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3
Topic:                  Utilities
 """

import os
import select
import struct
import sys

import socket
import time

if sys.platform == "win32":
    # On Windows, the best timer is time.clock()
    default_timer = time.clock
else:
    # On most other platforms the best timer is time.time()
    default_timer = time.time

# From /usr/include/linux/icmp.h; your milage may vary.
ICMP_ECHO_REQUEST = 8  # Seems to be the same on Solaris.


def checksum(source_string):
    """
    I'm not too confident that this is right but testing seems
    to suggest that it gives the same answers as in_cksum in ping.c
    :param source_string: bytes
    :return:
    """
    sum_ = 0
    countTo = (len(source_string) / 2) * 2
    count = 0
    while count < countTo:
        thisVal = source_string[count + 1] * 256 + source_string[count]
        sum_ = sum_ + thisVal
        sum_ = sum_ & 0xffffffff  # Necessary?
        count = count + 2

    if countTo < len(source_string):
        sum_ = sum_ + source_string[len(source_string) - 1]
        sum_ = sum_ & 0xffffffff  # Necessary?

    sum_ = (sum_ >> 16) + (sum_ & 0xffff)
    sum_ = sum_ + (sum_ >> 16)
    answer = ~sum_
    answer = answer & 0xffff

    # Swap bytes. Bugger me if I know why.
    answer = answer >> 8 | (answer << 8 & 0xff00)

    return answer


def receive_one_ping(my_socket, ID, timeout):
    """
    receive the ping from the socket.
    """
    timeLeft = timeout
    while True:
        startedSelect = default_timer()
        whatReady = select.select([my_socket], [], [], timeLeft)
        howLongInSelect = (default_timer() - startedSelect)
        if whatReady[0] is []:  # Timeout
            return

        timeReceived = default_timer()
        try:
            recPacket, addr = my_socket.recvfrom(1024)
        except socket.timeout:  # make sure timeout works
            return
        icmpHeader = recPacket[20:28]
        type_, code, checksum_, packetID, sequence = struct.unpack(
            "bbHHh", icmpHeader
        )
        # Filters out the echo request itself.
        # This can be tested by pinging 127.0.0.1
        # You'll see your own request
        if type_ != 8 and packetID == ID:
            bytesInDouble = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
            return timeReceived - timeSent

        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return


def send_one_ping(my_socket, dest_addr, ID):
    """
    Send one ping to the given >dest_addr<.
    """
    dest_addr = socket.gethostbyname(dest_addr)

    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    my_checksum = 0

    # Make a dummy heder with a 0 checksum.
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, ID, 1)
    bytesInDouble = struct.calcsize("d")
    data = (192 - bytesInDouble) * "Q"
    data = struct.pack("d", default_timer()) + data.encode("utf-8")

    # Calculate the checksum on the data and the dummy header.
    my_checksum = checksum(header + data)

    # Now that we have the right checksum, we put that in. It's just easier
    # to make up a new header than to stuff it into the dummy.
    header = struct.pack(
        "bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), ID, 1
    )
    packet = header + data
    my_socket.sendto(packet, (dest_addr, 1))  # Don't know about the 1


def do_one(dest_addr, timeout):
    """
    Returns either the delay (in seconds) or none on timeout.
    """
    socket.setdefaulttimeout(timeout)
    icmp = socket.getprotobyname("icmp")
    try:
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    except socket.timeout:
        return
    except socket.error as e:
        # Operation not permitted
        msg = str(e) + " - Note that ICMP messages can only be sent from processes running as root."
        raise socket.error(msg)

    my_ID = os.getpid() & 0xFFFF

    send_one_ping(my_socket, dest_addr, my_ID)
    delay = receive_one_ping(my_socket, my_ID, timeout)

    my_socket.close()
    return delay


def verbose_ping(dest_addr, timeout=2, count=4):
    """
    Send >count< ping to >dest_addr< with the given >timeout< and display
    the result.
    """
    for i in range(count):
        print("ping %s..." % dest_addr, )
        try:
            delay = do_one(dest_addr, timeout)
        except socket.gaierror as e:
            print("failed. (socket error: '%s')" % str(e))
            break

        if delay is None:
            print("failed. (timeout within %ssec.)" % timeout)
        else:
            delay = delay * 1000
            print("get ping in %0.4fms" % delay)


if __name__ == '__main__':
    verbose_ping("www.python.org")
    verbose_ping("heise.de")
    verbose_ping("google.com")
    verbose_ping("a-test-url-that-is-not-available.com")
    verbose_ping("192.168.1.1")
    verbose_ping("192.168.88.1", timeout=1, count=4)
