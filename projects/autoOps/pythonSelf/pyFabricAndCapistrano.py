#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyFabricAndCapistrano.py
User:               Guodong
Create Date:        2017/9/12
Create Time:        13:48
Description:        
References:         https://github.com/dlapiduz/fabistrano
Prerequisites:      []
 """
import functools
from fabric.api import run, env, sudo, put, task

# TODO(Guodong Ding) NO QA
env.timeout = 6000


def dir_exists(path):
    # return run('[ -d %s ] && echo 1 || echo 0' % path) == '1'
    pass


def with_defaults(func):
    """A decorator that sets all defaults for a task."""

    @functools.wraps(func)
    def decorated(*args, **kwargs):
        env.setdefault('use_sudo', True)
        env.setdefault('git_branch', 'master')
        env.setdefault('python_bin', 'python')
        env.setdefault('remote_owner', 'www-data')
        env.setdefault('remote_group', 'www-data')
        env.setdefault('pip_install_command', 'pip install -r requirements.txt')

        env.setdefault('domain_path', "%(base_dir)s/%(app_name)s" %
                       {'base_dir': env.base_dir,
                        'app_name': env.app_name})
        env.setdefault('current_path', "%(domain_path)s/current" %
                       {'domain_path': env.domain_path})
        env.setdefault('releases_path', "%(domain_path)s/releases" %
                       {'domain_path': env.domain_path})
        env.setdefault('shared_path', "%(domain_path)s/shared" %
                       {'domain_path': env.domain_path})
        if not 'releases' not in env:
            if dir_exists(env.releases_path):
                env.releases = sorted(run('ls -x %(releases_path)s' % {'releases_path': env.releases_path}).split())

                if len(env.releases) >= 1:
                    env.current_revision = env.releases[-1]
                    env.current_release = "%(releases_path)s/%(current_revision)s" % \
                                          {'releases_path': env.releases_path,
                                           'current_revision': env.current_revision}
                if len(env.releases) > 1:
                    env.previous_revision = env.releases[-2]
                    env.previous_release = "%(releases_path)s/%(previous_revision)s" % \
                                           {'releases_path': env.releases_path,
                                            'previous_revision': env.previous_revision}
        return func(*args, **kwargs)

    return decorated


def sudo_run(*args, **kwargs):
    if env.use_sudo:
        sudo(*args, **kwargs)
    else:
        run(*args, **kwargs)


@task
@with_defaults
def restart():
    """Restarts your application"""
    try:
        run("touch %(current_release)s/%(wsgi_path)s" %
            {'current_release': env.current_release,
             'wsgi_path': env.wsgi_path})
    except AttributeError:
        try:
            sudo_run(env.restart_cmd)
        except AttributeError:
            pass


@with_defaults
def permissions():
    """Make the release group-writable"""
    sudo_run("chown -R %(user)s:%(group)s %(domain_path)s" %
             {'domain_path': env.domain_path,
              'user': env.remote_owner,
              'group': env.remote_group})
    sudo_run("chmod -R g+w %(domain_path)s" % {'domain_path': env.domain_path})


@task
@with_defaults
def setup():
    """Prepares one or more servers for deployment"""
    sudo_run("mkdir -p %(domain_path)s/{releases,shared}" % {'domain_path': env.domain_path})
    sudo_run("mkdir -p %(shared_path)s/{system,log}" % {'shared_path': env.shared_path})
    permissions()


@with_defaults
def checkout():
    """Checkout code to the remote servers"""
    from time import time
    env.current_release = "%(releases_path)s/%(time).0f" % {'releases_path': env.releases_path, 'time': time()}
    run("cd %(releases_path)s; git clone -b %(git_branch)s -q %(git_clone)s %(current_release)s" %
        {'releases_path': env.releases_path,
         'git_clone': env.git_clone,
         'current_release': env.current_release,
         'git_branch': env.git_branch})


@task
def update():
    """Copies your project and updates environment and symlink"""
    update_code()
    update_env()
    symlink()
    set_current()
    permissions()


@task
def update_code():
    """Copies your project to the remote servers"""
    checkout()
    permissions()


@with_defaults
def symlink():
    """Updates the symlink to the most recently deployed version"""
    run("ln -nfs %(shared_path)s/log %(current_release)s/log" % {'shared_path': env.shared_path,
                                                                 'current_release': env.current_release})


@with_defaults
def set_current():
    """Sets the current directory to the new release"""
    run("ln -nfs %(current_release)s %(current_path)s" % {'current_release': env.current_release,
                                                          'current_path': env.current_path})


@with_defaults
def update_env():
    """Update servers environment on the remote servers"""
    sudo_run("cd %(current_release)s; %(pip_install_command)s" % {'current_release': env.current_release,
                                                                  'pip_install_command': env.pip_install_command})
    permissions()


@task
@with_defaults
def cleanup():
    """Clean up old releases"""
    if len(env.releases) > 3:
        directories = env.releases
        directories.reverse()
        del directories[:3]
        env.directories = ' '.join(
            ["%(releases_path)s/%(release)s" % {'releases_path': env.releases_path, 'release': release} for release in
             directories])
        run("rm -rf %(directories)s" % {'directories': env.directories})


@with_defaults
def rollback_code():
    """Rolls back to the previously deployed version"""
    if len(env.releases) >= 2:
        env.current_release = env.releases[-1]
        env.previous_revision = env.releases[-2]
        env.current_release = "%(releases_path)s/%(current_revision)s" % {'releases_path': env.releases_path,
                                                                          'current_revision': env.current_revision}
        env.previous_release = "%(releases_path)s/%(previous_revision)s" % {'releases_path': env.releases_path,
                                                                            'previous_revision': env.previous_revision}
        run("rm %(current_path)s; ln -s %(previous_release)s %(current_path)s && rm -rf %(current_release)s" % {
            'current_release': env.current_release, 'previous_release': env.previous_release,
            'current_path': env.current_path})


@task
def rollback():
    """Rolls back to a previous version and restarts"""
    rollback_code()
    restart()


@task(default=True)
def deploy():
    """Deploys your project. This calls both `update' and `restart'"""
    update()
    restart()
