# http://code.activestate.com/recipes/66517/
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/65219?_ga=1.43404389.1320951527.1488780812

# IP address manipulation functions, dressed up a bit

import struct

import socket


def dottedQuadToNum(ip):
    """convert decimal dotted quad string to long integer"""
    return struct.unpack('L', socket.inet_aton(ip))[0]


def numToDottedQuad(n):
    """convert long int to dotted quad string"""
    return socket.inet_ntoa(struct.pack('L', n))


def makeMask(n):
    """return a mask of n bits as a long integer"""
    return (2 << n - 1) - 1


def ipToNetAndHost(ip, maskbits):
    """returns tuple (network, host) dotted-quad addresses given IP and mask size"""
    # (by Greg Jorgensen)

    n = dottedQuadToNum(ip)
    m = makeMask(maskbits)

    host = n & m
    net = n - host

    return numToDottedQuad(net), numToDottedQuad(host)


print(ipToNetAndHost("192.168.1.1", 24))
