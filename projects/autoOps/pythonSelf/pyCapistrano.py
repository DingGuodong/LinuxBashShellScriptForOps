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
from fabric.api import *
from fabric.main import main
from fabric.colors import *
from fabric.context_managers import *
from fabric.contrib.console import confirm
import os
import sys
import re
import getpass


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

    def user(self):
        if is_linux():
            self.user = "%s(%s)" % (os.getlogin(), os.getuid())
        if is_windows():
            import getpass
            self.user = getpass.getuser()


config = {
    "deploy_to": '/var/www/my_app_name',
    "scm": 'git',
    "repo_url": 'https://github.com/DingGuodong/GoogleHostsFileForLinux.git',
    "branch": 'master',
    "log_level": 'debug',
    "keep_releases": 10
}


class Capistrano(object):
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

            def paths(self):
                return self.releases_path(), self.repo_path(), self.shared_path()

            def makepaths(self):
                for directory in self.paths():
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
                    except Exception:
                        raise NotImplementedError

            def update_revision_log(self, branch=None, sid=None, release=None, by=None):
                with open(self.revision_log(), 'a') as f:
                    f.write("Branch %s (at %s) deployed as release %s by %s\n" % (branch, sid, release, by))

            def cleanup(self):
                keep_releases = config['keep_releases']
                releases = local("ls -xtr %s" % self.releases_path(), capture=True).split()
                # print releases[-keep_releases:]
                if len(releases) > keep_releases:
                    for release in releases[0:(len(releases) - keep_releases)]:
                        local("rm -rf %s" % os.path.join(self.releases_path(), release))


c = Capistrano.DSL.Paths()
c.makepaths()

g = Git()
g.set("https://github.com/DingGuodong/GoogleHostsFileForLinux.git", repo_path=c.repo_path())
g.pull()

c.make_release_dirs()
c.make_current()
c.update_revision_log(g.branch, g.short_id(), c.current, getpass.getuser())
c.cleanup()
