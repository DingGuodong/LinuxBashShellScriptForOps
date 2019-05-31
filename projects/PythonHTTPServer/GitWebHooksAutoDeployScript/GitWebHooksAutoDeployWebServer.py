#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:GitWebHooksAutoDeployWebServer.py
User:               Guodong
Create Date:        2016/9/5
Create Time:        10:23
 """
import json
import os
import sys
import logging
import logging.handlers
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import signal


def initLoggerWithRotate(logPath="/var/log", logName=None):
    current_time = time.strftime("%Y%m%d%H")
    if logName is not None:
        logPath = os.path.join(logPath, logName)
        logFilename = logName + "_" + current_time + ".log"
    else:
        logName = "default"
        logFilename = logName + ".log"

    if not os.path.exists(logPath):
        os.makedirs(logPath)
        logFilename = os.path.join(logPath, logFilename)
    else:
        logFilename = os.path.join(logPath, logFilename)

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


myLogger = initLoggerWithRotate("/var/log", "git_webhooks")
myLogger.setLevel(logging.INFO)


class GitAutoDeploy(BaseHTTPRequestHandler):
    class WebServer(BaseHTTPRequestHandler):

        def _send_response(self, http_status_code):
            self.server_version = "WebServer/1.10.1"
            self.sys_version = ""
            self.send_response(http_status_code)

        def _set_headers(self):
            self.send_header('Content-type', 'text/html')

        def _end_headers(self):
            self.end_headers()

        def do_GET(self):
            self._send_response(200)
            self._set_headers()
            self._end_headers()

            path = self.path
            if "?" in path:
                path, tmp = path.split('?', 1)
                qs = urllib.parse.parse_qs(tmp)
                print(path, qs)
            try:
                with open("index.html", "r") as f:
                    self.wfile.write(f.read())
            except IOError:
                self.wfile.write("<html><body><h1>It works!</h1></body></html>")
                myLogger.info(
                    self.headers.getheader('Host') + " " + self.headers.getheader(
                        'User-Agent') + " " + self.command + " " + self.path)

        def do_HEAD(self):
            self._send_response(200)
            self._set_headers()
            self._end_headers()
            myLogger.info(
                self.headers.getheader('Host') + " " + self.headers.getheader(
                    'User-Agent') + " " + self.command + " " + self.path)

        def do_POST(self):
            event = self.headers.getheader('X-Github-Event')
            if event == 'ping':
                myLogger.info(
                    self.headers.getheader('Host') + " " + self.headers.getheader(
                        'User-Agent') + " " + self.command + " " + self.path)
                myLogger.info('Ping event received')
                self.send_response(204)  # HTTP Status Code Definitions:
                # https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
                return
            if event != 'push':
                myLogger.info('Unhandled event received')
                self.send_response(204)
                return

            if self.headers.getheader('content-type') == "application/json":
                self.send_response(200)
                length = int(self.headers.getheader('content-length'))
                body = self.rfile.read(length)
                payload = json.loads(body)
                myLogger.info(
                    self.headers.getheader('Host') + " " + self.headers.getheader(
                        'User-Agent') + " " + self.command + " " + self.path)
                myLogger.info(payload)
            elif self.headers.getheader('content-type') == "application/x-www-form-urlencoded":
                self.send_response(200)
                length = int(self.headers.getheader('content-length'))
                body = self.rfile.read(length)
                myLogger.info(
                    self.headers.getheader('Host') + " " + self.headers.getheader(
                        'User-Agent') + " " + self.command + " " + self.path)
                myLogger.info(urllib.parse.parse_qs(body))
            else:
                self.send_response(200)
                myLogger.info(
                    self.headers.getheader('Host') + " " + self.headers.getheader(
                        'User-Agent') + " " + self.command + " " + self.path)
                myLogger.info("Unhandled Request: bad content type.")

    class ParsePayloads(object):
        # TODO(Guodong Ding) continue here
        def __init__(self):
            pass

        def parseRequest(self):
            pass


def sigterm_handler(_signo, _stack_frame):
    print("catch process signal %s, goodbye." % _signo)
    sys.exit(0)


def run(server_class=HTTPServer, handler_class=GitAutoDeploy.WebServer, port=80):
    httpd = None
    try:
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        print('Starting httpd...')
        httpd.serve_forever()
    except (KeyboardInterrupt, SystemExit) as e:
        if e:  # wtf, why is this creating a new line?
            print(e, file=sys.stderr)
        if httpd is not None:
            httpd.socket.close()
            print("Stopping httpd...")
            sys.exit(0)
    finally:
        print("httpd stopped.")


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, sigterm_handler)
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
