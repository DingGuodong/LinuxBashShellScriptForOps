#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:getDockerContainerInfoWithPidNumber.py
User:               Guodong
Create Date:        2016/10/18
Create Time:        10:25
 """
import os
import sys
from collections import OrderedDict


class dockerContainerUtils(object):
    def __init__(self):
        processInformationPseudoFileSystem = "/proc"
        self.proc = processInformationPseudoFileSystem
        self.debugEnabled = True

    def debug(self, objects):
        if not self.debugEnabled:
            return
        else:
            if objects is not None:
                print objects

    def getPids(self):
        return [int(name) for name in os.listdir(self.proc) if name.isdigit()]

    def getStatus(self, pid):
        status = OrderedDict()
        if pid in self.getPids():
            pidDir = os.path.join(self.proc, str(pid))
        if os.path.exists(pidDir):
            pass
        else:
            print 'pid is not exist!'
            sys.exit(1)
        try:
            with open(os.path.join(pidDir, "status"), 'r') as f:
                content = f.read().strip().split("\n")
                for item in content:
                    kv = item.replace('\t', ' ').split(":")
                    status[kv[0].strip()] = kv[1].strip()
        except IOError:
            print 'pid is not exist!'
            sys.exit(1)
        return dict(status)

    def getCmdline(self, pid):
        if int(pid) == 0:
            return None

        if pid in self.getPids():
            pidDir = os.path.join(self.proc, str(pid))
        else:
            print 'pid is not exist!'
            sys.exit(1)

        if os.path.exists(pidDir):
            pass
        else:
            print 'pid is not exist!'
            sys.exit(1)

        try:
            with open(os.path.join(pidDir, "cmdline"), 'r') as f:
                cmdline = f.read().strip().replace('\x00', ' ').strip()
                if cmdline is None or cmdline == '':
                    raise RuntimeError('cmdline is None or \'\'')
        except IOError:
            print 'pid is not exist!'
            sys.exit(1)
        return str(cmdline)

    def getPPid(self, pid):
        status = self.getStatus(pid)
        # TODO(Guodong Ding) self.getStatus(pid) won't quit right
        if len(status) == 0:
            raise KeyError("getStatus(Type: OrderedDict) returns None, this always means pid is NOT exist!")
        return int(status['PPid'])

    def getPPidCmdline(self, pid):
        return self.getCmdline(self.getPPid(pid))

    def getPPPid(self, pid):
        result = int(self.getPPid(pid))
        if result == 0:
            return result
        else:
            return int(self.getPPid(result))

    def getPidChain(self, pid):
        maxPidChain = 1024
        pidChain = list()
        pidChain.append(pid)
        for i in xrange(maxPidChain - 1):
            pidItem = self.getPPid(pid)
            if pidItem != 0:
                pidChain.append(pidItem)
                pid = pidItem
            else:
                pidChain.append(0)
                break

        return pidChain

    def getCmdlineChain(self, pid):
        pidChain = self.getPidChain(pid)
        pidCmdlineChain = OrderedDict()
        for pid in pidChain:
            pidCmdlineChain[pid] = self.getCmdline(pid)
        return pidCmdlineChain

    def isDockerRelatedProcess(self, pid):
        string = str(self.getCmdlineChain(pid))
        import re
        match = re.findall(r'docker', string)
        if match:
            return True
        else:
            return False

    def getContainerId(self, pid):
        if self.isDockerRelatedProcess(pid):
            pass
        else:
            raise RuntimeError("pid is not a docker related process's, aborted!")
        string = str(self.getCmdlineChain(pid))
        import re
        match = re.findall(r'(?<=docker-containerd-shim )\S+', string)
        if len(match) != 0:
            return match
        else:
            return None

    def getContainerInfo(self, pid):
        containerId = self.getContainerId(pid)
        if len(containerId):
            import subprocess
            result = subprocess.Popen("docker inspect %s" % containerId[0], shell=True, stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT)
            import json
            result_string = json.dumps(result.stdout.read())
            result_object = json.loads(result_string)
            return result_object
        else:
            return None


if __name__ == '__main__':
    pidNumber = int(raw_input('Please input pid number.'))
    p = dockerContainerUtils()
    print "Pid number is: %d" % pidNumber
    print "Pid number cmdline is: %s" % p.getCmdline(pidNumber)
    print "Parent pid number is: %s" % p.getPPid(pidNumber)
    print "Parent pid number cmdline is: %s" % p.getPPidCmdline(pidNumber)
    print "Parent parent pid number is: %s" % p.getPPPid(pidNumber)
    print "Pid chain is: %s" % p.getPidChain(pidNumber)
    print "Pid Cmdline chain is: %s" % p.getCmdlineChain(pidNumber)
    print "Pid number ContainerId is %s" % p.getContainerId(pidNumber)
    print "Pid number Container info is %s" % p.getContainerInfo(pidNumber)
