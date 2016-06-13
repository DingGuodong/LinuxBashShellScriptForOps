#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
import dns.resolver
import time

dnsDict = {"Australia - Melbourne": "168.1.79.238",
           "Australia - Sydney": "54.66.128.66",
           "Brazil": "54.94.226.225",
           "Canada SmartDNSCanada - Montreal": "169.54.78.85",
           "Canada FlagCanada - Toronto": "169.53.182.120",
           "Germany": "54.93.173.153",
           "India SmartDNSIndia": "169.38.73.5",
           "Ireland": "54.229.171.243",
           "Israel": "195.28.181.161",
           "Italy SmartDNSItaly": "95.141.39.236",
           "Japan FlagJapan": "54.64.107.105",
           "Mexico Smart DNS ProxyMexico": "169.57.10.21",
           "Netherlands FlagNetherlands": "46.166.189.68",
           "New Zealand Smart DNSNew Zealand": "223.165.64.97",
           "Singapore": "54.255.130.140",
           "South Africa SmartDNS 1South Africa 1": "154.70.152.42",
           "South Africa SmartDNSSouth Africa 2": "129.232.164.26",
           "Spain FlagSpain": "192.162.27.100",
           "Sweden FlagSweden": "46.246.29.69",
           "Switzerland SmartDNSSwitzerland": "81.17.17.170",
           "Turkey": "188.132.234.170",
           "US East - N. Virginia": "23.21.43.50",
           "US Center - Dallas": "169.53.235.135",
           "US West - Los Angeles": "54.183.15.10"}

domain = "github.com"
responseDict = {}
for key, value in dnsDict.items():
    dnsServer = value
    startTime = time.time()
    try:
        print "Start a query using %s ..." % key
        query = dns.resolver.Resolver()
        query.nameservers = [str(value)]
        query.timeout = 1.0
        query.lifetime = 3.0
        query.query(domain, 'A')
    except Exception:
        pass
    endTime = time.time()
    elapsedTime = (endTime - startTime)
    responseDict.setdefault(key, elapsedTime)

responseSortDict = sorted(responseDict.iteritems(), key=lambda t: t[1], reverse=False)

title = ["SmartDNS Position", "IP Address", "Response Time"]
print "%-40s %-30s %s" % (title[0], title[1], title[2])
for key, value in responseSortDict:
    print "%-40s %-30s %s" % (key, dnsDict.get(key), value)
