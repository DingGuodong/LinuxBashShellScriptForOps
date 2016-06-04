# -*- coding: utf-8 -*-
import os
import sys
import time
import sys
import pycurl

URL = "http://www.baidu.com"
c = pycurl.Curl()
c.setopt(pycurl.URL, URL)

# 连接超时时间,5秒
c.setopt(pycurl.CONNECTTIMEOUT, 5)

# 下载超时时间,5秒
c.setopt(pycurl.TIMEOUT, 5)
c.setopt(pycurl.FORBID_REUSE, 1)
c.setopt(pycurl.MAXREDIRS, 1)
c.setopt(pycurl.NOPROGRESS, 1)
c.setopt(pycurl.DNS_CACHE_TIMEOUT, 30)
index_file = open(os.path.dirname(os.path.realpath(__file__)) + "/content.txt", "wb")
c.setopt(pycurl.WRITEHEADER, index_file)
c.setopt(pycurl.WRITEDATA, index_file)
try:
    c.perform()
except Exception, e:
    print "connection error:" + str(e)
    index_file.close()
    c.close()
    sys.exit()

NAMELOOKUP_TIME = c.getinfo(c.NAMELOOKUP_TIME)
CONNECT_TIME = c.getinfo(c.CONNECT_TIME)
PRETRANSFER_TIME = c.getinfo(c.PRETRANSFER_TIME)
STARTTRANSFER_TIME = c.getinfo(c.STARTTRANSFER_TIME)
TOTAL_TIME = c.getinfo(c.TOTAL_TIME)
HTTP_CODE = c.getinfo(c.HTTP_CODE)
SIZE_DOWNLOAD = c.getinfo(c.SIZE_DOWNLOAD)
HEADER_SIZE = c.getinfo(c.HEADER_SIZE)
SPEED_DOWNLOAD = c.getinfo(c.SPEED_DOWNLOAD)

print "HTTP状态码：%s" % HTTP_CODE
print "DNS解析时间：%.2f ms" % (NAMELOOKUP_TIME * 1000)
print "建立连接时间：%.2f ms" % (CONNECT_TIME * 1000)
print "准备传输时间：%.2f ms" % (PRETRANSFER_TIME * 1000)
print "传输开始时间：%.2f ms" % (STARTTRANSFER_TIME * 1000)
print "传输结束总时间：%.2f ms" % (TOTAL_TIME * 1000)

print "下载数据包大小：%d bytes/s" % SIZE_DOWNLOAD
print "HTTP头部大小：%d byte" % HEADER_SIZE
print "平均下载速度：%d bytes/s" % SPEED_DOWNLOAD

index_file.close()
c.close()


# remove directories and their contents recursively
def remove_files_recursive(path):
    if os.path.isfile(path):
        try:
            os.remove(path)
        except OSError:
            pass
    elif os.path.isdir(path):
        for item in os.listdir(path):
            path_to_item = os.path.join(path, item)
            remove_files_recursive(path_to_item)
        try:
            os.rmdir(path)
        except OSError:
            pass


remove_files_recursive(os.path.dirname(os.path.realpath(__file__)) + "/content.txt")
