#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import sys


class MyHTTPServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>It works!</h1></body></html>")

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>got POST data!</h1></body></html>")


def run(server_class=HTTPServer, handler_class=MyHTTPServer, port=80):
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
            exit(0)


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
