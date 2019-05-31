#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:genSerializedUniqueNumber.py
User:               Guodong
Create Date:        2017/3/15
Create Time:        11:59

8 bit pure and serial number generator same as GUID, UUID Generator
 """
from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import time
import os
import logging
import logging.handlers


def initLoggerWithRotate(logPath="/var/log", logName=None, singleLogFile=True):
    current_time = time.strftime("%Y%m%d%H")
    logRootPath = logPath  # logRootPath known as logTopPath
    if logName is not None and not singleLogFile:
        logFullPath = os.path.join(logRootPath, logName)
        logFilename = logName + "_" + current_time + ".log"
    elif logName is not None and singleLogFile:
        logFullPath = os.path.join(logRootPath, logName)
        logFilename = logName + ".log"
    else:
        logFullPath = logRootPath
        logName = "default"
        logFilename = logName + ".log"

    if not os.path.exists(logFullPath):
        os.makedirs(logFullPath)
        logFilename = os.path.join(logFullPath, logFilename)
    else:
        logFilename = os.path.join(logFullPath, logFilename)

    logger = logging.getLogger(logName)
    log_formatter = logging.Formatter("%(asctime)s %(filename)s:%(lineno)d %(name)s %(levelname)s: %(message)s",
                                      "%Y-%m-%d %H:%M:%S")
    file_handler = logging.handlers.RotatingFileHandler(logFilename, maxBytes=104857600, backupCount=5)
    file_handler.setFormatter(log_formatter)
    stream_handler = logging.StreamHandler(sys.stderr)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)
    return logger


log_path = "/var/log"
log_name = "." + os.path.splitext(os.path.basename(__file__))[0]
log = initLoggerWithRotate(logPath="/var/log", logName=log_name, singleLogFile=True)
log.setLevel(logging.INFO)

persistent_storage_filesystem = 'genSerializedUniqueNumber.db'


def read_from_filesystem_storage():
    try:
        with open(persistent_storage_filesystem, 'r') as f:
            number = f.read()
            if number != "":
                return number
            else:
                return False
    except IOError:
        with open(persistent_storage_filesystem, 'w') as f:
            f.write("1")
            return False


def write_into_filesystem_storage(number):
    with open(persistent_storage_filesystem, 'w') as f:
        f.write(str(number))


def exec_8_bit_serial_number_generator():
    number_init = int(read_from_filesystem_storage()) or 0
    number_wanted = '{:0>8}'.format(str(number_init))
    number_init += 1
    write_into_filesystem_storage(number_init)
    return number_wanted


class simpleHTTPServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        if "favicon.ico" in self.path:
            pass
        else:
            number_wanted = exec_8_bit_serial_number_generator()
            self._set_headers()
            self.wfile.write(number_wanted)

    def do_HEAD(self):
        pass

    def do_PUT(self):
        pass

    def do_DELETE(self):
        pass

    def do_POST(self):
        pass


def run(server_class=HTTPServer, handler_class=simpleHTTPServer, port=80):
    hostname = "192.168.1.67"
    httpd = None
    try:
        server_address = (hostname, port)
        httpd = server_class(server_address, handler_class)
        quit_command = 'CTRL-BREAK' if sys.platform == 'win32' else 'CONTROL-C'
        print('Starting httpd server at http://%s:%s' % (hostname, port))
        print('Server %s (bind-address): \'*\'; port: %s' % (hostname, port))
        print('Quit the server with %s.' % quit_command)
        print(sys.version)
        httpd.serve_forever()
    except (KeyboardInterrupt, SystemExit) as e:
        if e:
            print(e, file=sys.stderr)
        if httpd is not None:
            httpd.socket.close()
            print("Stopping httpd...")
            exit(0)
    finally:
        print("httpd stopped.")
        sys.exit(0)


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
