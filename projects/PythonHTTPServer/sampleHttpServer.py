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
import codecs
import datetime
import json
import locale
import os
import signal
import socket
import sys
import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


def get_system_encoding():
    """
    The encoding of the default system locale but falls back to the given
    fallback encoding if the encoding is unsupported by python or could
    not be determined.  See tickets #10335 and #5846
    """
    try:
        encoding = locale.getdefaultlocale()[1] or 'ascii'
        codecs.lookup(encoding)
    except Exception as _:
        del _
        encoding = 'ascii'
    return encoding


DEFAULT_LOCALE_ENCODING = get_system_encoding()

hostname = socket.gethostname()


def usage():
    print("""Help message:
    Function: A sample http server writen with Python, using it to test if the port can be reached.
    Usage: %s [<tcp port>]
        port options is optional, default is 80.
    Example:
        python %s
        python %s 80

""") % (__file__, sys.argv[0], sys.argv[0])
    sys.exit(0)


def RegexURLResolver(regex, string):
    import re
    p = re.compile(str(regex), re.IGNORECASE)
    match = p.match(str(string))
    if match:
        return True
    else:
        return False


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

        if RegexURLResolver(r'^/\?', path):
            path, tmp = path.split('?', 1)
            qs = urlparse.parse_qs(tmp)
            print path, qs
            for key, value in qs.items():
                print key, value[0]
                self.wfile.write("<html><body><h1>%s:%s</h1></body></html>" % (key, value[0]))
            self.finish()
        if RegexURLResolver(r'^/$', path):
            try:
                with open("index.html", "r") as f:
                    self.wfile.write(f.read())
            except IOError:
                self.wfile.write("<html><body><h1>It works! on host: %s.</h1></body></html>" % hostname)
                self.finish()
        elif RegexURLResolver(r'^/admin/$', path):
            self.wfile.write(
                "<html><body><h1>It works! on host: %s, request is: %s.</h1></body></html>" % (hostname, path))
            self.finish()
        else:
            self.wfile.write(self.responses[404])
            self.finish()

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
        quit_command = 'CTRL-BREAK' if sys.platform == 'win32' else 'CONTROL-C'
        print 'Starting httpd server at http://%s:%s' % (hostname, port)
        # TODO(GuodongDing): Add bind address support, 'print' can using 'sys.stdout.write()' with a python 'dict'
        print 'Server %s (bind-address): \'*\'; port: %s' % (hostname, port)
        print '%s: ready for connections.' % os.path.basename(__file__)
        print 'Quit the server with %s.' % quit_command
        print sys.version
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
        print "%s: Shutdown complete" % os.path.basename(__file__)
        sys.exit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, sigterm_handler)
    from sys import argv

    if len(argv) == 2 and argv[1].isdigit():
        run(port=int(argv[1]))
    if len(argv) == 1:
        run()
    else:
        print "Bad usage: %s" % argv
        usage()
