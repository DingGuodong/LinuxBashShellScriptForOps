#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:TestGit.py
User:               Guodong
Create Date:        2016/8/24
Create Time:        9:40
 """
import getpass
import re
import sys

from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *

config = {
    "deploy_to": '/var/www/my_app_name',
    "scm": 'git',
    "repo_url": 'https://github.com/DingGuodong/GoogleHostsFileForLinux.git',
    "branch": 'master',
    "log_level": 'debug',
    "keep_releases": 10
}

env.roledefs = {
    'test': ['root@10.6.28.28:22', ],
    'nginx': ['root@10.6.28.46:22', 'root@10.6.28.27:22', ],
    'db': ['root@10.6.28.35:22', 'root@10.6.28.93:22', ],
    'sit': ['root@10.6.28.46:22', 'root@10.6.28.135:22', 'root@10.6.28.35:22', ],
    'uat': ['root@10.6.28.27:22', 'root@10.6.28.125:22', 'root@10.6.28.93:22', ],
    'all': ["10.6.28.27", "10.6.28.28", "10.6.28.35", "10.6.28.46", "10.6.28.93", "10.6.28.125", "10.6.28.135"]
}

env.user = "root"
env.hosts = ["10.6.28.27", "10.6.28.28", "10.6.28.35", "10.6.28.46", "10.6.28.93", "10.6.28.125", "10.6.28.135"]


def win_or_linux():
    # os.name ->(sames to) sys.builtin_module_names
    if 'posix' in sys.builtin_module_names:
        os_type = 'Linux'
    elif 'nt' in sys.builtin_module_names:
        os_type = 'Windows'
    return os_type


def is_windows():
    if "windows" in win_or_linux().lower():
        return True
    else:
        return False


def is_linux():
    if "linux" in win_or_linux().lower():
        return True
    else:
        return False


class Capistrano(object):
    class SCM(object):
        class Git(object):
            def __init__(self):
                self.repo_url = None
                self.name = None
                self.branch = None
                self.repo_path = None
                self.user = None

            def set(self, repo_url, branch=None, repo_path=None):
                if repo_url is None:
                    abort("You must specify a repository to clone.")
                else:
                    self.repo_url = repo_url
                if branch is None:
                    self.branch = "master"
                else:
                    self.branch = branch

                pattern = re.compile(r"(\w+)(?=\.git$)")
                match = pattern.search(repo_url)
                if match:
                    paths = match.group()
                else:
                    paths = None
                if repo_path is not None and not os.path.exists(repo_path):
                    try:
                        os.mkdir(repo_path)
                    except IOError:
                        repo_path = os.path.join(os.path.dirname(__file__), paths)
                elif repo_path is None:
                    repo_path = ""
                self.repo_path = os.path.abspath(repo_path)

            def clone(self):
                local("git clone --branch %s %s %s" % (self.branch, self.repo_url, self.repo_path))

            def check(self):
                with lcd(self.repo_path):
                    return local("git ls-remote --heads %s" % self.repo_url, capture=True)

            def pull(self):
                with lcd(self.repo_path):
                    if os.path.exists(os.path.join(self.repo_path, ".git")):
                        local("git pull origin %s" % self.branch)
                    else:
                        self.clone()
                        self.pull()

            def update(self):
                pass

            def status(self):
                with lcd(self.repo_path):
                    local("git status")

            def branch(self):
                with lcd(self.repo_path):
                    local("git rev-parse --abbrev-ref HEAD", capture=True)

            def long_id(self):
                with lcd(self.repo_path):
                    return local("git rev-parse HEAD", capture=True)

            def short_id(self):
                with lcd(self.repo_path):
                    return local("git rev-parse --short HEAD", capture=True)

            def fetch_revision(self):
                with lcd(self.repo_path):
                    return local("git rev-list --max-count=1 %s" % self.branch, capture=True)

            def user(self):
                if is_linux():
                    self.user = "%s(%s)" % (os.getlogin(), os.getuid())
                if is_windows():
                    import getpass
                    self.user = getpass.getuser()

    class DSL(object):
        class Paths(object):
            def __init__(self):
                self.deploy_to = config['deploy_to']
                self.current = None

            # TODO(Guodong Ding) fetch 'deploy_to' from config file or dict
            def deploy_path(self):
                return os.path.abspath(self.deploy_to)

            def current_path(self):
                current_directory = "current"
                return os.path.join(self.deploy_path(), current_directory)

            def releases_path(self):
                return os.path.join(self.deploy_path(), "releases")

            def set_release_path(self):
                import datetime
                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                self.current = os.path.join(self.releases_path(), timestamp)
                return os.path.join(self.releases_path(), timestamp)

            def shared_path(self):
                return os.path.join(self.deploy_path(), "shared")

            def repo_path(self):
                return os.path.join(self.deploy_path(), "repo")

            def revision_log(self):
                return os.path.join(self.deploy_path(), "revisions.log")

            def __paths(self):
                return self.releases_path(), self.repo_path(), self.shared_path()

            def makepaths(self):
                for directory in self.__paths():
                    if not os.path.exists(directory):
                        os.makedirs(directory)

            def make_release_dirs(self):
                os.makedirs(self.set_release_path())

            def make_current(self):
                if is_linux():
                    if os.path.exists(self.current_path()) and os.path.islink(self.current_path()):
                        os.unlink(self.current_path())
                    os.symlink(self.current, self.current_path())
                if is_windows():
                    if os.path.exists(self.current_path()):
                        import shutil
                        shutil.rmtree(self.current_path())
                    try:
                        local("ln -sd %s %s" % (self.current, self.current_path()))
                    except Exception as _:
                        del _
                        raise NotImplementedError

            def update_revision_log(self, branch=None, sid=None, release=None, by=None):
                print(blue("Log details of the deploy"))
                with open(self.revision_log(), 'a') as f:
                    f.write("Branch %s (at %s) deployed as release %s by %s\n" % (branch, sid, release, by))

            def cleanup(self):
                keep_releases = config['keep_releases']
                releases = local("ls -xtr %s" % self.releases_path(), capture=True).split()
                # print releases[-keep_releases:]
                if len(releases) > keep_releases:
                    for release in releases[0:(len(releases) - keep_releases)]:
                        local("rm -rf %s" % os.path.join(self.releases_path(), release))

            @staticmethod
            def __get_file_last_line(inputfile):
                filesize = os.path.getsize(inputfile)
                blocksize = 1024
                with open(inputfile, 'rb') as f:
                    last_line = ""
                    if filesize > blocksize:
                        maxseekpoint = (filesize // blocksize)
                        f.seek((maxseekpoint - 1) * blocksize)
                    elif filesize:
                        f.seek(0, 0)
                    lines = f.readlines()
                    if lines:
                        lineno = 1
                        while last_line == "":
                            last_line = lines[-lineno].strip()
                            lineno += 1
                    return last_line

            def rollback(self):
                print(blue("Revert to previous release timestamp"))
                revision_log_message = self.__get_file_last_line(self.revision_log())
                last_release = None
                import re
                s = re.compile(r"release (.*) by")
                match = s.search(revision_log_message)
                if match:
                    last_release = match.groups()[0]
                else:
                    abort("Can NOT found rollback release in revision log files, %s." % self.revision_log())
                if os.path.exists(last_release):
                    print(yellow("Symlink previous release to current"))
                else:
                    abort("Can NOT found rollback release on filesystem.")
                if is_linux():
                    if os.path.exists(self.current_path()) and os.path.islink(self.current_path()):
                        os.unlink(self.current_path())
                    os.symlink(last_release, self.current_path())
                if is_windows():
                    if os.path.exists(self.current_path()):
                        import shutil
                        shutil.rmtree(self.current_path())
                    try:
                        local("ln -sd %s %s" % (last_release, self.current_path()))
                    except Exception as _:
                        del _
                        raise NotImplementedError

    class Application(object):
        class Deploy(object):
            def __init__(self):
                self.P = Capistrano.DSL.Paths()
                self.G = Capistrano.SCM.Git()

            def deploy(self):
                # TODO(Guodong Ding): core job here, this is a deploy demo
                with lcd(self.P.current_path()):
                    try:
                        src = os.path.join(self.P.repo_path(), "replaceLocalHostsFileAgainstGfw.sh")
                        local_path = os.path.join(self.P.current_path(), "hosts")
                        remote_path = "/tmp/replaceLocalHostsFileAgainstGfw.sh"
                        with open(src, 'r') as f:
                            content = f.read()
                        with open(local_path, "w") as f:
                            f.write(content)
                        if os.path.getsize(local_path):
                            print(red("upload files to remote hosts"))
                            put(local_path, remote_path)
                            run("chmod +x %s" % remote_path)
                            run("ls -al %s" % remote_path)
                            print(red("deploy test demo successfully!"))
                    except IOError:
                        raise NotImplementedError

            def run(self):
                print(blue("Do deploy procedure."))
                self.P.makepaths()
                self.G.set(config["repo_url"], repo_path=self.P.repo_path())
                self.G.pull()

                self.P.make_release_dirs()
                self.P.make_current()
                self.deploy()
                self.P.update_revision_log(self.G.branch, self.G.short_id(), self.P.current, getpass.getuser())
                self.P.cleanup()
                print(green("Deploy successfully!"))


@roles("test")
def test_deploy():
    c = Capistrano.Application.Deploy()
    c.run()


def terminal_debug(defName):
    command = r"fab -i c:\Users\Guodong\.ssh\exportedkey201310171355\
                -f %s \
                %s" % (__file__, defName)
    os.system(command)
    sys.exit(0)


if __name__ == '__main__':
    if len(sys.argv) == 1 and is_windows():
        terminal_debug("test_deploy")

    sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    print(red("Please use 'fab -f %s'" % " ".join(str(x) for x in sys.argv[0:])))
    sys.exit(1)
