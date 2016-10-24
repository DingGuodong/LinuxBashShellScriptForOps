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
        self.pid = 0
        self.pid = self.getPidInput()
        self.checkDockerServerVersion()

    def getContainerLongIdUsingDockerInspectAllContainerID(self):
        import subprocess
        result = subprocess.Popen(r"docker inspect -f '{{.State.Pid}} {{.Id}}' $(docker ps -a -q) | grep %s" % self.pid,
                                  shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)
        idList = result.stdout.read().strip().split(' ')
        if len(idList) != 0:
            return idList
        else:
            print "Container ID is NOT found for pid %s, maybe this is NOT a container pid! Now exit!" % self.pid
            pass  # sys.exit(1)

    @staticmethod
    def checkDockerServerVersion():
        versionSupported = "1.11.0"
        import subprocess
        result = subprocess.Popen("docker info", shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)

        # TODO(Guodong Ding) returncode returns bad 'NoneType'.
        # if int(result.returncode) == 0:
        #     pass
        # else:
        #     raise RuntimeError(
        #         '\'docker info\' run failed! This always means docker service is down or broken. Aborted!')

        import re
        pattern = re.compile(r'Server Version: ([0-9\.]+)')
        match = pattern.findall(result.stdout.read().strip())
        if match:
            version = match[0]
        else:
            raise RuntimeError('Unknown error. Aborted!')
        if version > versionSupported:
            print "Docker Server Version is: %s. Congratulations! This version is supported!" % version
            return True
        else:
            print "Docker Server Version is: %s. Unfortunately! This version is NOT supported!" % version
            return False

    def getPidInput(self):
        self.pid = int(raw_input('Please input pid number.'))
        if self.isLegalPid() and self.isExistedPid():
            return self.pid

    def isLegalPid(self):
        if str(self.pid).isdigit() and (int(self.pid) >= 0 or int(self.pid) <= 32768):
            return True
        else:
            raise RuntimeError('Pid input should be an integer, and should be 0~32768. Aborted!')

    def isExistedPid(self):
        if os.path.exists(os.path.join(self.proc, str(self.pid), 'cmdline')) and os.path.exists(
                os.path.join(self.proc, str(self.pid), 'status')):
            return True
        else:
            raise RuntimeError('pid is NOT exist! Aborted! ')

    def debug(self, objects):
        if not self.debugEnabled:
            return
        else:
            if objects is not None:
                print objects

    def getCurrentAllPids(self):
        return [int(name) for name in os.listdir(self.proc) if name.isdigit()]

    def getProcessStatus(self):
        status = OrderedDict()
        if self.pid in self.getCurrentAllPids():
            pidDir = os.path.join(self.proc, str(self.pid))
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

    def getCmdline(self):
        if int(self.pid) == 0:
            return None

        if self.pid in self.getCurrentAllPids():
            pidDir = os.path.join(self.proc, str(self.pid))
        else:
            print 'pid is not exist! Aborted!'
            sys.exit(1)

        if os.path.exists(pidDir):
            pass
        else:
            print 'pid is not exist! Aborted!'
            sys.exit(1)

        try:
            with open(os.path.join(pidDir, "cmdline"), 'r') as f:
                cmdline = f.read().strip().replace('\x00', ' ').strip()
                if cmdline is None or cmdline == '':
                    raise RuntimeError('cmdline is None or \'\', this always means pid is NOT exist! Aborted! ')
        except IOError:
            print 'pid is not exist! Aborted!'
            sys.exit(1)
        return str(cmdline)

    def getPPid(self):
        status = self.getProcessStatus()
        # TODO(Guodong Ding) self.getStatus won't quit right
        if len(status) == 0:
            raise KeyError("getStatus(Type: OrderedDict) returns None, this always means pid is NOT exist! Aborted!")
        return int(status['PPid'])

    def getPPidCmdline(self):
        oldPid = self.pid
        tmpPid = self.getPPid()
        self.pid = tmpPid
        result = self.getCmdline()
        self.pid = oldPid
        return result

    def getPPPid(self):
        result = int(self.getPPid())
        if result == 0:
            return result
        else:
            return int(self.getPPid())

    def getPidChain(self):
        maxPidChain = 1024
        pidChain = list()
        pidChain.append(self.pid)
        oldPid = self.pid
        for i in xrange(maxPidChain - 1):
            pidItem = self.getPPid()
            if pidItem != 0:
                pidChain.append(pidItem)
                self.pid = pidItem
            else:
                pidChain.append(0)
                break
        self.pid = oldPid
        return pidChain

    def getCmdlineChain(self):
        pidChain = self.getPidChain()
        pidCmdlineChain = OrderedDict()
        oldPid = self.pid
        for pid in pidChain:
            self.pid = pid
            pidCmdlineChain[pid] = self.getCmdline()
        self.pid = oldPid
        return pidCmdlineChain

    def isDockerRelatedProcess(self):
        string = str(self.getCmdlineChain())
        import re
        match = re.findall(r'docker', string)
        if match:
            return True
        else:
            return False

    def getContainerId(self):
        if self.isDockerRelatedProcess():
            pass
        else:
            raise RuntimeError("pid is not a docker related process's, aborted!")
        string = str(self.getCmdlineChain())
        import re
        # Docker Server Version >= 1.11 is required!
        match = re.findall(r'(?<=docker-containerd-shim )\S+', string)
        if len(match) != 0:
            return match
        elif len(self.getContainerLongIdUsingDockerInspectAllContainerID()) != 0:
            return self.getContainerLongIdUsingDockerInspectAllContainerID()[1]
        elif len(self.getContainerShortIDWithPort()) != 0:
            return self.getContainerShortIDWithPort()
        else:
            return []

    @staticmethod
    def getFDSocketInodeNumber(pid):
        inodeList = list()
        try:
            for f in os.listdir("/proc/%d/fd" % pid):
                socket = os.readlink("/proc/%d/fd/%s" % (pid, f))
                if 'socket' in socket:
                    import re
                    pattern = re.compile(r'\[(\d+)\]')
                    match = pattern.search(socket)
                    if match:
                        inodeList.append(match.groups()[0])
        except OSError:
            raise RuntimeError("Can NOT open directory \'/proc/%d/fd\'. Aborted!" % pid)

        return inodeList

    def getPortNumberWithInodeNumber(self, pid):
        inodeList = self.getFDSocketInodeNumber(pid)
        portList = list()
        try:
            with open('/proc/net/tcp', 'r') as f:
                tcp = f.read()
        except IOError:
            raise RuntimeError("Can NOT open file \'/proc/net/tcp\'")

        try:
            with open('/proc/net/tcp6', 'r') as f:
                tcp6 = f.read()
        except IOError:
            raise RuntimeError("Can NOT open file \'/proc/net/tcp6\'")

        for inodeNumber in inodeList:
            import re
            pattern = re.compile(r'.*\d+:\s\d+:(\d+).*%s.*' % inodeNumber)
            match = pattern.findall(tcp.strip())
            if match:
                portList.append(int(match[0], 16))

            match6 = pattern.findall(tcp6)
            if match6:
                portList.append(int(match6[0], 16))

        return list(set(portList))

    def getContainerShortIDWithPort(self):
        # TODO(Guodong Ding) pid should use 'docker-proxy's' pid.
        portList = self.getPortNumberWithInodeNumber(self.pid)
        import subprocess
        result = subprocess.Popen("docker ps ", shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)
        if len(portList) != 0:
            for port in portList:
                import re
                pattern = re.compile(r'([a-z0-9]+) .*%s.*' % port)
                match = pattern.findall(result.stdout.read().strip())
                if match:
                    return match[0]
        else:
            return []

    def truncateId(self):
        containerID = self.getContainerId()
        if len(containerID) != 0:
            return str(containerID[0])[:12]
        else:
            return None

    def getContainerShortID(self):
        return self.truncateId()

    def listContainer(self):
        # a python implementation for 'docker ps'
        containerId = self.getContainerShortID()
        if len(containerId) != 0:
            import subprocess
            result = subprocess.Popen("docker ps | grep %s" % containerId, shell=True, stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT)
            return result.stdout.read()
        else:
            return None

    def getContainerInfo(self):
        containerId = self.getContainerId()
        if len(containerId) != 0:
            import subprocess
            result = subprocess.Popen("docker inspect %s" % containerId[0], shell=True, stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT)
            # also can get this from /run/runc/<id>/state.json or /run/containerd/<id>/state.json
            import json
            result_string = json.dumps(result.stdout.read())
            result_object = json.loads(result_string)
            return result_object
        else:
            return None


if __name__ == '__main__':
    p = dockerContainerUtils()
    print "Pid number is: %d" % p.pid
    print "Pid number ContainerId is %s" % p.getContainerLongIdUsingDockerInspectAllContainerID()
    print "Pid number cmdline is: %s" % p.getCmdline()
    print "Parent pid number is: %s" % p.getPPid()
    print "Parent pid number cmdline is: %s" % p.getPPidCmdline()
    print "Parent parent pid number is: %s" % p.getPPPid()
    print "Pid chain is: %s" % p.getPidChain()
    print "Pid Cmdline chain is: %s" % p.getCmdlineChain()

    # TODO(Guodong Ding) pid should use 'docker-proxy's' pid.
    # print "Pid number's socket inode number is %s" % p.getFDSocketInodeNumber()
    # print "Pid number's port number is %s" % p.getPortNumberWithInodeNumber()
    # print "Pid number ContainerShortId is %s" % p.getContainerShortIDWithPort()

    print "Pid number ContainerId is %s" % p.getContainerId()
    print "Pid number short ContainerId is %s" % p.getContainerShortID()
    print "Pid number list container: %s" % p.listContainer()
    print "Pid number Container info is: %s" % p.getContainerInfo()
