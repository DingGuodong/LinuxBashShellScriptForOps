#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:sampleHttpServer
User:               Guodong
Create Date:        2016/7/30
Create Time:        14:42
 """
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse
import json
import sys
import signal
import datetime


class S(BaseHTTPRequestHandler):
    def date_time_string(self, timestamp=None):
        now = datetime.datetime.now()
        s = str(now)
        return s

    def _send_response(self, http_status_code):
        self.server_version = "WebServer/1.10.1"
        self.sys_version = ""
        self.send_response(http_status_code)

    def _set_headers(self):
        self.send_header('Content-type', 'text/html')

    def _end_headers(self):
        self.end_headers()

    @staticmethod
    def _is_json(json_data):
        try:
            json.loads(json_data)
        except ValueError:
            return False
        else:
            return True

    @staticmethod
    def _is_dict(string):
        try:
            dict(string)
        except ValueError:
            return False
        else:
            return True

    def do_GET(self):
        self._send_response(200)
        self._set_headers()
        self._end_headers()

        path = self.path
        if "?" in path:
            path, tmp = path.split('?', 1)
            qs = urlparse.parse_qs(tmp)
            print path, qs
        try:
            with open("index.html", "r") as f:
                self.wfile.write(f.read())
        except IOError:
            self.wfile.write("<html><body><h1>It works!</h1></body></html>")

    def do_HEAD(self):
        print self.headers.get('User-Agent')
        self._send_response(200)
        self._set_headers()
        self._end_headers()

    def do_POST(self):
        self._send_response(200)
        self._set_headers()
        self._end_headers()
        page_content_json_success = r'{"result":200,"msg":"Post Successfully."}'
        page_content_json_fail = r'{"result":400,"errcode":1,"msg":"Bad Request."}'
        data_string = self.rfile.read(int(self.headers['Content-Length']))
        if self._is_json(data_string):
            self.wfile.write(self.headers)
            self.wfile.write(data_string)
            return
        elif self._is_dict(data_string):
            self.wfile.write(self.headers)
            self.wfile.write(page_content_json_success)
            return
        elif isinstance(data_string, str):
            self.wfile.write(self.headers)
            self.wfile.write(data_string)
            return
        else:
            self.wfile.write(self.headers)
            self.wfile.write(page_content_json_fail)
            return


def sigterm_handler(_signo, _stack_frame):
    print "catch process signal %s, goodbye." % _signo
    sys.exit(0)


def run(server_class=HTTPServer, handler_class=S, port=80):
    httpd = None
    try:
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        print 'Starting httpd...'
        httpd.serve_forever()
    except (KeyboardInterrupt, SystemExit) as e:
        if e:  # wtf, why is this creating a new line?
            print >> sys.stderr, e
        if httpd is not None:
            httpd.socket.close()
            print "Stopping httpd..."
            sys.exit(0)
    finally:
        print "httpd stopped."


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, sigterm_handler)
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
