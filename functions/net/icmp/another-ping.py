#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:another-ping.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/10/18
Create Time:            18:07
Description:            
Long Description:       
References:             https://github.com/certator/pyping
                        https://github.com/samuel/python-ping

                        https://github.com/certator/pyping/network/members

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

import os
import select
import signal
import socket
import struct
import sys
import time

import six

if sys.platform.startswith("win32"):
    # On Windows, the best timer is time.clock()
    default_timer = time.clock
else:
    # On most other platforms the best timer is time.time()
    default_timer = time.time

# ICMP parameters
ICMP_ECHOREPLY = 0  # Echo reply (per RFC792)
ICMP_ECHO = 8  # Echo request (per RFC792)
ICMP_MAX_RECV = 2048  # Max size of incoming buffer

MAX_SLEEP = 1000


def calculate_checksum(source_string):
    """
    A port of the functionality of in_cksum() from ping.c
    Ideally this would act on the string as a series of 16-bit ints (host
    packed), but this works.
    Network data is big-endian, hosts are typically little-endian
    """
    countTo = (int(len(source_string) / 2)) * 2
    sum = 0
    count = 0

    # Handle bytes in pairs (decoding as short ints)
    loByte = 0
    hiByte = 0
    while count < countTo:
        if sys.byteorder == "little":
            loByte = source_string[count]
            hiByte = source_string[count + 1]
        else:
            loByte = source_string[count + 1]
            hiByte = source_string[count]
        if not six.PY3:
            loByte = ord(loByte)
            hiByte = ord(hiByte)
        sum = sum + (hiByte * 256 + loByte)
        count += 2

    # Handle last byte if applicable (odd-number of bytes)
    # Endianness should be irrelevant in this case
    if countTo < len(source_string):  # Check for odd length
        loByte = source_string[len(source_string) - 1]
        if not six.PY3:
            loByte = ord(loByte)
        sum += loByte

    sum &= 0xffffffff  # Truncate sum to 32 bits (a variance from ping.c, which
    # uses signed ints, but overflow is unlikely in ping)

    sum = (sum >> 16) + (sum & 0xffff)  # Add high 16 bits to low 16 bits
    sum += (sum >> 16)  # Add carry from above (if any)
    answer = ~sum & 0xffff  # Invert and truncate to 16 bits
    answer = socket.htons(answer)

    return answer


def is_valid_ip4_address(addr):
    """
    see also IPy.parseAddress()
        Parse a string and return the corresponding IP address (as integer)
        and a guess of the IP version.

    :param addr:
    :return:
    """
    parts = addr.split(".")
    if not len(parts) == 4:
        return False
    for part in parts:
        try:
            number = int(part)
        except ValueError:
            return False
        if number > 255 or number < 0:
            return False
    return True


def to_ip(addr):
    if is_valid_ip4_address(addr):
        return addr
    try:
        socket.gethostbyname(addr)
    except socket.gaierror:
        print("ping: unknown host %s" % addr)  # Win32: 'Ping 请求找不到主机 %s。请检查该名称，然后重试。'
        sys.exit(2)
    return socket.gethostbyname(addr)


class Response(object):
    def __init__(self):
        self.max_rtt = None
        self.min_rtt = None
        self.avg_rtt = None
        self.packet_lost = None
        self.ret_code = None
        self.output = []

        self.packet_size = None
        self.timeout = None
        self.destination = None
        self.destination_ip = None


class Ping(object):
    def __init__(self, destination, timeout=1000, packet_size=55, own_id=None, quiet_output=True, udp=False, bind=None):
        self.quiet_output = quiet_output
        if quiet_output:
            self.response = Response()
            self.response.destination = destination
            self.response.timeout = timeout
            self.response.packet_size = packet_size

        self.destination = destination
        self.timeout = timeout
        self.packet_size = packet_size
        self.udp = udp
        self.bind = bind

        if own_id is None:
            self.own_id = os.getpid() & 0xFFFF
        else:
            self.own_id = own_id

        try:
            # FIXME: Use destination only for display this line here? see: https://github.com/jedie/python-ping/issues/3
            self.dest_ip = to_ip(self.destination)
            if quiet_output:
                self.response.destination_ip = self.dest_ip
        except socket.gaierror as e:
            self.print_unknown_host(e)
        else:
            self.print_start()

        self.seq_number = 0
        self.send_count = 0
        self.receive_count = 0
        self.min_time = 999999999
        self.max_time = 0.0
        self.total_time = 0.0

    # --------------------------------------------------------------------------

    def print_start(self):
        msg = "\nPYTHON-PING %s (%s): %d data bytes of data." % (self.destination, self.dest_ip, self.packet_size)
        if self.quiet_output:
            self.response.output.append(msg)
        else:
            print(msg)

    def print_unknown_host(self, e):
        msg = "\nPYTHON-PING: Unknown host: %s (%s)\n" % (self.destination, e.args[1])
        if self.quiet_output:
            self.response.output.append(msg)
            self.response.ret_code = 1
        else:
            print(msg)

        raise Exception("unknown_host")

    # sys.exit(-1)

    def print_success(self, delay, ip, packet_size, ip_header, icmp_header):
        msg = ""
        if ip == self.destination:
            from_info = ip
        else:
            from_info = "%s (%s)" % (self.destination, ip)

            msg = "%d bytes from %s: icmp_seq=%d ttl=%d time=%.1f ms" % (
                packet_size, from_info, icmp_header["seq_number"], ip_header["ttl"], delay)

        if self.quiet_output:
            self.response.output.append(msg)
            self.response.ret_code = 0
        else:
            print(msg)

    # print("IP header: %r" % ip_header)
    # print("ICMP header: %r" % icmp_header)

    def print_failed(self):
        msg = "Request timed out."

        if self.quiet_output:
            self.response.output.append(msg)
            self.response.ret_code = 1
        else:
            print(msg)

    def print_exit(self):
        msg = "\n--- %s PYTHON PING statistics ---" % self.destination

        if self.quiet_output:
            self.response.output.append(msg)
        else:
            print(msg)

        lost_count = self.send_count - self.receive_count
        # print("%i packets lost" % lost_count)
        lost_rate = float(lost_count) / self.send_count * 100.0

        msg = "%d packets transmitted, %d packets received, %0.1f%% packet loss" % (
            self.send_count, self.receive_count, lost_rate)

        if self.quiet_output:
            self.response.output.append(msg)
            self.response.packet_lost = lost_count
        else:
            print(msg)

        if self.receive_count > 0:
            msg = "round-trip (ms)  min/avg/max = %0.3f/%0.3f/%0.3f" % (
                self.min_time, self.total_time / self.receive_count, self.max_time)
            if self.quiet_output:
                self.response.min_rtt = '%.3f' % self.min_time
                self.response.avg_rtt = '%.3f' % (self.total_time / self.receive_count)
                self.response.max_rtt = '%.3f' % self.max_time
                self.response.output.append(msg)
            else:
                print(msg)

        if self.quiet_output:
            self.response.output.append('\n')
        else:
            print('')

    # --------------------------------------------------------------------------

    def signal_handler(self, signum, frame):
        """
        Handle print_exit via signals
        """
        self.print_exit()
        msg = "\n(Terminated with signal %d)\n" % signum

        if self.quiet_output:
            self.response.output.append(msg)
            self.response.ret_code = 0
        else:
            print(msg)

        sys.exit(0)

    def setup_signal_handler(self):
        signal.signal(signal.SIGINT, self.signal_handler)  # Handle Ctrl-C
        if hasattr(signal, "SIGBREAK"):
            # Handle Ctrl-Break e.g. under Windows
            signal.signal(signal.SIGBREAK, self.signal_handler)

    # --------------------------------------------------------------------------

    def header2dict(self, names, struct_format, data):
        """ unpack the raw received IP and ICMP header informations to a dict """
        unpacked_data = struct.unpack(struct_format, data)
        return dict(zip(names, unpacked_data))

    # --------------------------------------------------------------------------

    def run(self, count=None, deadline=None):
        """
        send and receive pings in a loop. Stop if count or until deadline.
        """
        if not self.quiet_output:
            self.setup_signal_handler()

        while True:
            delay = self.do()

            self.seq_number += 1
            if count and self.seq_number >= count:
                break
            if deadline and self.total_time >= deadline:
                break

            if delay is None:
                delay = 0

            # Pause for the remainder of the MAX_SLEEP period (if applicable)
            if MAX_SLEEP > delay:
                time.sleep((MAX_SLEEP - delay) / 1000.0)

        self.print_exit()
        if self.quiet_output:
            return self.response

    def do(self):
        """
        Send one ICMP ECHO_REQUEST and receive the response until self.timeout
        """
        try:  # One could use UDP here, but it's obscure
            if self.udp:
                current_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.getprotobyname("icmp"))
            else:
                current_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))

            # Bind the socket to a source address
            if self.bind:
                current_socket.bind((self.bind, 0))  # Port number is irrelevant for ICMP

        except socket.error as exc:
            if exc.errno == 1:
                # Operation not permitted - Add more information to traceback
                etype, evalue, etb = sys.exc_info()
                evalue = etype(
                    "%s - Note that ICMP messages can only be send from processes running as root." % evalue
                )
                six.reraise(etype, evalue, etb)
            raise  # raise the original error

        send_time = self.send_one_ping(current_socket)
        if send_time is None:
            return
        self.send_count += 1

        receive_time, packet_size, ip, ip_header, icmp_header = self.receive_one_ping(current_socket)
        current_socket.close()

        if receive_time:
            self.receive_count += 1
            delay = (receive_time - send_time) * 1000.0
            self.total_time += delay
            if self.min_time > delay:
                self.min_time = delay
            if self.max_time < delay:
                self.max_time = delay

            self.print_success(delay, ip, packet_size, ip_header, icmp_header)
            return delay
        else:
            self.print_failed()

    def send_one_ping(self, current_socket):
        """
        Send one ICMP ECHO_REQUEST
        """
        # Header is type (8), code (8), checksum (16), id (16), sequence (16)
        checksum = 0

        # Make a dummy header with a 0 checksum.
        header = struct.pack(
            "!BBHHH", ICMP_ECHO, 0, checksum, self.own_id, self.seq_number
        )

        padBytes = []
        startVal = 0x42
        for i in range(startVal, startVal + self.packet_size):
            padBytes += [(i & 0xff)]  # Keep chars in the 0-255 range
        data = bytes(padBytes)

        # Calculate the checksum on the data and the dummy header.
        checksum = calculate_checksum(header + data)  # Checksum is in network order

        # Now that we have the right checksum, we put that in. It's just easier
        # to make up a new header than to stuff it into the dummy.
        header = struct.pack(
            "!BBHHH", ICMP_ECHO, 0, checksum, self.own_id, self.seq_number
        )

        packet = header + data

        send_time = default_timer()

        try:
            current_socket.sendto(packet, (self.destination, 1))  # Port number is irrelevant for ICMP
        except socket.error as e:
            self.response.output.append("General failure (%s)" % (e.args[1]))
            current_socket.close()
            return

        return send_time

    def receive_one_ping(self, current_socket):
        """
        Receive the ping from the socket. timeout = in ms
        """
        timeout = self.timeout / 1000.0

        while True:  # Loop while waiting for packet or timeout
            select_start = default_timer()
            inputready, outputready, exceptready = select.select([current_socket], [], [], timeout)
            select_duration = (default_timer() - select_start)
            if inputready is []:  # timeout
                return None, 0, 0, 0, 0

            packet_data, address = current_socket.recvfrom(ICMP_MAX_RECV)

            icmp_header = self.header2dict(
                names=[
                    "type", "code", "checksum",
                    "packet_id", "seq_number"
                ],
                struct_format="!BBHHH",
                data=packet_data[20:28]
            )

            receive_time = default_timer()

            if icmp_header["packet_id"] == self.own_id:  # Our packet
                ip_header = self.header2dict(
                    names=[
                        "version", "type", "length",
                        "id", "flags", "ttl", "protocol",
                        "checksum", "src_ip", "dest_ip"
                    ],
                    struct_format="!BBHHHBBHII",
                    data=packet_data[:20]
                )
                packet_size = len(packet_data) - 28
                ip = socket.inet_ntoa(struct.pack("!I", ip_header["src_ip"]))
                # XXX: Why not ip = address[0] ???
                return receive_time, packet_size, ip, ip_header, icmp_header

            timeout = timeout - select_duration
            if timeout <= 0:
                return None, 0, 0, 0, 0


def ping(hostname, timeout=1000, count=4, packet_size=56, *args, **kwargs):
    p = Ping(hostname, timeout, packet_size, *args, **kwargs)
    return p.run(count)


if __name__ == '__main__':
    ping('www.python.org', quiet_output=False)
