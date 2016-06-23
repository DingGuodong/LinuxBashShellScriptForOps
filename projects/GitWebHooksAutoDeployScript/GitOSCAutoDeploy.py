#!/usr/bin/env python

import json
import os
import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from subprocess import call
import re


class GitOSCAutoDeploy(BaseHTTPRequestHandler):
    CONFIG_FILEPATH = './GitOSCAutoDeploy.conf.json'
    config = None
    quiet = False
    daemon = False
    branch = None
    url = None

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

    def do_POST(self):
        event = self.headers.getheader('Password')
        if event == '123.56.234.219':
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

    def validateurl(self):
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
        self.branch = payload['push_data']['ref']
        for url in [payload['push_data']['repository']['url']]:
            self.url = url
            self.validateurl()
        return [payload['push_data']['repository']['url']]

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
                GitOSCAutoDeploy.daemon = True
                GitOSCAutoDeploy.quiet = True
            if arg == '-q' or arg == '--quiet':
                GitOSCAutoDeploy.quiet = True

        if GitOSCAutoDeploy.daemon:
            pid = os.fork()
            if pid != 0:
                sys.exit()
            os.setsid()

        if not GitOSCAutoDeploy.quiet:
            print 'Github AutoDeploy Service v0.2 started'
        else:
            print 'Github AutoDeploy Service v 0.2 started in daemon mode'

        server = HTTPServer(('', GitOSCAutoDeploy.getConfig()['port']), GitOSCAutoDeploy)
        server.serve_forever()
    except (KeyboardInterrupt, SystemExit) as e:
        if e:  # wtf, why is this creating a new line?
            print >> sys.stderr, e

        if server is not None:
            server.socket.close()

        if not GitOSCAutoDeploy.quiet:
            print 'Goodbye'


if __name__ == '__main__':
    main()
