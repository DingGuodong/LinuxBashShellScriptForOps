#!/usr/bin/env python

import json
import os
import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from subprocess import call
import re


# import logging


class GitLabAutoDeploy(BaseHTTPRequestHandler):
    CONFIG_FILEPATH = './GitLabAutoDeploy.conf.json'
    config = None
    quiet = False
    daemon = False
    branch = None
    url = None
    path = '/'

    @classmethod
    def getConfig(myClass):
        if myClass.config is None:
            try:
                configString = open(myClass.CONFIG_FILEPATH).read()
            except:
                sys.exit('Could not load ' + myClass.CONFIG_FILEPATH + ' file')

            try:
                myClass.config = json.loads(configString)
            except:
                sys.exit(myClass.CONFIG_FILEPATH + ' file is not valid json')

            for repository in myClass.config['repositories']:
                if not os.path.isdir(repository['path']):
                    try:
                        os.mkdir(repository['path'])
                    except:
                        sys.exit('Can NOT make a repository directory' + repository['path'])
                        # sys.exit('Directory ' + repository['path'] + ' not found')
                # Check for a repository with a local or a remote GIT_WORK_DIR
                if not os.path.isdir(os.path.join(repository['path'], '.git')) \
                        and not os.path.isdir(os.path.join(repository['path'], 'objects')):
                    try:
                        call(['git clone' + " " + repository['url'] + " " + repository['path']], shell=True)
                    except:
                        sys.exit('Can NOT clone repository directory into ' + os.path.isdir(repository['path']))
                        # sys.exit('Directory ' + repository['path'] + ' is not a Git repository')
        return myClass.config

    def do_GET(self):
        """ Handle GET Request"""
        if self.path == "/" or self.path == "/favicon.ico":
            self.path = "/invoke.json"
        # Prepend the file name with current dir path.
        path = os.getcwd() + self.path

        # Check if file exists there.
        if os.path.isfile(path):

            # Read the file and return its contents.
            with open(path) as fileHandle:
                # Send headers.
                self.send_header('Content-type', 'text/json')
                self.send_response(200)
                self.end_headers()
                # Send file content.
                self.wfile.write(fileHandle.read().encode())

        # Fail with 404 File Not Found error.
        else:
            # Send headers with error.
            self.send_header('Content-type', 'text/json')
            self.send_response(404, 'File Not Found')
            self.end_headers()

            # try:
            #     buf = 'It works'
            #     self.wfile.write(buf)
            # except IOError:
            #     self.send_error(400, 'Bad Request')

    def do_POST(self):
        """ Handle POST Request"""
        event = self.headers.getheader('X-Github-Event')
        if event == 'ping':
            if not self.quiet:
                print 'Ping event received'
            self.respond(204)
            return

        self.respond(204)

        urls = self.parseRequest()
        for url in urls:
            paths = self.getMatchingPaths(url)
            for path in paths:
                self.fetch(path)
                self.deploy(path)

    def validateURL(self):
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        try:
            # TODO
            # There must a bug on way
            validatedurl = re.match(regex, self.url, 0)
        except Exception:
            sys.exit('Validate URL failed!')
        return validatedurl

    def parseRequest(self):
        length = int(self.headers.getheader('content-length'))
        if length <= 0:
            sys.exit('Get content-length from headers failed!')
        body = self.rfile.read(length)
        # Debug purpose
        print 'Debug: Body is ' + body
        try:
            json.loads(body)
        except Exception:
            # do http decode
            import urllib
            body = urllib.unquote(body)
        try:
            json.loads(body)
        except Exception:
            # do remove 5 character
            body = body[5:]
        payload = json.loads(body)
        self.branch = payload['ref']
        for url in [payload['repository']['git_http_url']]:
            self.url = url
            self.validateURL()
        return [payload['repository']['git_http_url']]

    def getMatchingPaths(self, repoUrl):
        res = []
        config = self.getConfig()
        for repository in config['repositories']:
            if repository['url'] == repoUrl:
                res.append(repository['path'])
        return res

    def respond(self, code):
        self.send_response(code)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def fetch(self, path):
        if not self.quiet:
            print "\nPost push request received"
            print 'Updating ' + path
        call(['cd "' + path + '" && git fetch'], shell=True)

    def deploy(self, path):
        config = self.getConfig()
        for repository in config['repositories']:
            if repository['path'] == path:
                if 'deploy' in repository:
                    branch = None
                    if 'branch' in repository:
                        branch = repository['branch']

                    if branch is None or branch == self.branch:
                        if not self.quiet:
                            print 'Executing deploy command'
                        call(['cd "' + path + '" && ' + repository['deploy']], shell=True)

                    elif not self.quiet:
                        print 'Push to different branch (%s != %s), not deploying' % (branch, self.branch)
                break


def main():
    server = None
    try:
        for arg in sys.argv:
            if arg == '-d' or arg == '--daemon-mode':
                GitLabAutoDeploy.daemon = True
                GitLabAutoDeploy.quiet = True
            if arg == '-q' or arg == '--quiet':
                GitLabAutoDeploy.quiet = True

        if GitLabAutoDeploy.daemon:
            pid = os.fork()
            if pid != 0:
                sys.exit()
            os.setsid()

        if not GitLabAutoDeploy.quiet:
            print 'Github AutoDeploy Service v0.2 started'
        else:
            print 'Github AutoDeploy Service v 0.2 started in daemon mode'

        server = HTTPServer(('', GitLabAutoDeploy.getConfig()['port']), GitLabAutoDeploy)
        server.serve_forever()
    except (KeyboardInterrupt, SystemExit) as e:
        if e:  # wtf, why is this creating a new line?
            print >> sys.stderr, e

        if server is not None:
            server.socket.close()

        if not GitLabAutoDeploy.quiet:
            print 'Goodbye'


if __name__ == '__main__':
    main()
