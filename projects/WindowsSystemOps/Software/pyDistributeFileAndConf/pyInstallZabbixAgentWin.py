#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:pyInstallZabbixAgentWin.py
User:               Guodong
Create Date:        2017/6/20
Create Time:        9:28
 """
import logging
import os
from IPy import IP

ZABBIX_SERVER_CONF_SERVER_IP = '127.0.0.1,10.46.69.219'
ZABBIX_SERVER_CONF_SERVER_ACTIVE_IP = '10.46.69.219'
ZABBIX_WIN32_SERVICE_NAME = 'Zabbix Agent'

log_format = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(format=log_format)
log = logging.getLogger()
log.setLevel(logging.INFO)
log.info('Started')


def download_file(url_download_from, path_save_to):
    try:
        from requests.packages import urllib3
    except ImportError:
        import urllib3
    import os
    import sys
    import requests

    url = url_download_from if is_url_valid(url_download_from) else ""

    filename = url.split('/')[-1]

    save = os.path.join(check_path(path_save_to), filename).replace("\\", "/")

    print("Downloading '%s',\n" \
          "save '%s' to '%s'" % (url, filename, save))

    urllib3.disable_warnings()  # equal to import logging; logging.captureWarnings(capture=True)

    response = requests.request("GET", url, stream=True, data=None, headers=None)

    total_length = int(response.headers.get("Content-Length"))
    with open(save, 'wb') as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()

    if os.path.isfile(save):
        print("Done: '%s'" % save)
        print("Total Size: %d" % total_length)
        print("md5sum:", get_hash_sum(save, method="md5"))
        print("sha1sum:", get_hash_sum(save, method="sha1sum"))
        print("sha256sum:", get_hash_sum(save, method="sha256sum"))
    else:
        print("can not download", url)
        sys.exit(1)


def extract_zip(path_to_zipfile, extract_to):
    import zipfile
    extract_to = check_path(extract_to)
    log.info("Extract %s to %s" % (path_to_zipfile, extract_to))
    with zipfile.ZipFile(path_to_zipfile, 'r') as f:
        for filename in f.namelist():
            f.extract(filename, extract_to)


def get_zip_path(full_path_to_zip_file):
    (filepath, temp_filename) = os.path.split(full_path_to_zip_file)
    (filename, extension) = os.path.splitext(temp_filename)
    return os.path.join(filepath, filename).replace('\\', '/')


def config_conf(path_to_conf_file):
    import configparser

    def __add_section_to_conf():
        with open(path_to_conf_file, 'r') as original:
            data = original.read()
        with open(path_to_conf_file, 'w') as modified:
            modified.write('[DEFAULT]' + "\n" + data)  # DEFAULT is ConfigParser.DEFAULTSECT

    def __delete_section_from_conf():
        with open(path_to_conf_file, 'r') as original:
            data = original.readlines()
        with open(path_to_conf_file, 'w') as modified:
            for line in data:
                if line != '[DEFAULT]\n':
                    modified.write(line)

    ZABBIX_AGENT_CONF_HOSTNAME = get_ip_address_internal()

    __add_section_to_conf()

    zabbix_agent_conf = configparser.ConfigParser(allow_no_value=True)
    zabbix_agent_conf.read(path_to_conf_file)
    zabbix_agent_conf.set(section=configparser.DEFAULTSECT, option='logfile'.strip(), value=r'c:\zabbix_agentd.log')
    zabbix_agent_conf.set(section=configparser.DEFAULTSECT, option='server'.strip(), value=ZABBIX_SERVER_CONF_SERVER_IP)
    zabbix_agent_conf.set(section=configparser.DEFAULTSECT, option='serveractive'.strip(),
                          value=ZABBIX_SERVER_CONF_SERVER_ACTIVE_IP)
    zabbix_agent_conf.set(section=configparser.DEFAULTSECT, option='hostname'.strip(), value=ZABBIX_AGENT_CONF_HOSTNAME)
    with open(path_to_conf_file, 'wb') as f:
        zabbix_agent_conf.write(f)

    __delete_section_from_conf()


def install_service():
    import win32api
    import time
    if not os.path.exists(zabbix_install_log):
        log.info('Install zabbix service')
        try:
            win32api.ShellExecute(0, 'runas', zabbix_agent_bin_file,
                                  '--config %s --install' % zabbix_agent_conf_file, '', 0)
            time.sleep(2)  # it is not essential
            log.info('Install zabbix service finished')
            with open(zabbix_install_log, 'w') as f:
                f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + ' service installed.')
        except Exception as e:
            print(e)
            log.error('Install zabbix service failed')
            raise RuntimeError


def run_service():
    import win32api
    import time
    import win32service

    START_PENDING = win32service.SERVICE_START_PENDING or 2
    RUNNING = win32service.SERVICE_RUNNING or 4
    service_status = check_service_status(ZABBIX_WIN32_SERVICE_NAME)
    if service_status != START_PENDING or service_status != RUNNING:
        log.info('Start Zabbix Agent Service')
        try:
            win32api.ShellExecute(0, 'runas', 'sc', 'start \"%s\"' % ZABBIX_WIN32_SERVICE_NAME, '', 1)
            time.sleep(2)  # it is not essential
            log.info('Zabbix Agent service started')
        except Exception as e:
            print(e)
            raise RuntimeError
    else:
        log.info('Zabbix Agent service has already started, nothing to do')


def check_service_status(serviceName):
    import win32serviceutil
    import win32service
    import time

    UNKNOWN = 0
    STOPPED = win32service.SERVICE_STOP or 1
    START_PENDING = win32service.SERVICE_START_PENDING or 2
    STOP_PENDING = win32service.SERVICE_STOP_PENDING or 3
    RUNNING = win32service.SERVICE_RUNNING or 4

    status_code = {
        0: "UNKNOWN",
        1: "STOPPED",
        2: "START_PENDING",
        3: "STOP_PENDING",
        4: "RUNNING"
    }

    log.info('Checking Zabbix Agent Service Status')
    try:
        result = win32serviceutil.QueryServiceStatus(serviceName)[1]
        if result == START_PENDING:
            print("service %s is %s, please wait" % (serviceName, status_code[result]))
            time.sleep(2)
            return RUNNING
        elif result == STOP_PENDING:
            print("service %s is %s, please wait" % (serviceName, status_code[result]))
            time.sleep(2)
            return STOPPED
        else:
            return result if result is not None else 0
    except Exception as e:
        print(e)
        raise RuntimeError("Uncaught exception, maybe it is a 'Access Denied'")  # will not reach here


def is_iterable(source):
    if source is not None:
        try:
            iter(source)
        except TypeError:
            return False
        return True
    else:
        raise RuntimeError("argument cannot be None")


def is_url_valid(url):
    # http://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not
    from django.core.validators import URLValidator
    from django.core.exceptions import ValidationError
    val = URLValidator()
    try:
        val(url)
    except ValidationError:
        return False
    else:
        return True


def is_url_valid_u2(url):
    """
    http://validators.readthedocs.io/en/latest/
    Python has all kinds of validation tools, but every one of them requires defining a schema. I
    wanted to create a simple validation library where validating a simple value does not require
    defining a form or a schema.
    """
    import validators
    if validators.url(url):
        return True
    else:
        return False


def get_hash_sum(filename, method="md5", block_size=65536):
    import os
    import hashlib

    if not os.path.exists(filename):
        raise RuntimeError("cannot open '%s' (No such file or directory)" % filename)
    if not os.path.isfile(filename):
        raise RuntimeError("'%s' :not a regular file" % filename)

    if "md5" in method:
        checksum = hashlib.md5()
    elif "sha1" in method:
        checksum = hashlib.sha1()
    elif "sha256" in method:
        checksum = hashlib.sha256()
    else:
        raise RuntimeError("unsupported method %s" % method)

    # if os.path.exists(filename) and os.path.isfile(filename):
    with open(filename, 'rb') as f:
        buf = f.read(block_size)
        while len(buf) > 0:
            checksum.update(buf)
            buf = f.read(block_size)
        if checksum is not None:
            return checksum.hexdigest()
        else:
            return checksum


def check_path(path):
    import os
    if not os.path.exists(path):
        print('[Info] %s is not exist.' % path)
        os.makedirs(path)
        return os.path.abspath(path).replace("\\", "/")
    else:
        return os.path.abspath(path).replace("\\", "/")


def get_ip_address():
    import os
    import sys

    try:
        import netifaces
    except ImportError:
        try:
            command_to_execute = "pip install netifaces || easy_install netifaces"
            os.system(command_to_execute)
        except OSError:
            print("Can NOT install netifaces, Aborted!")
            sys.exit(1)
        import netifaces

    ip_address = list()

    for interface in netifaces.interfaces():
        try:
            ip_address.append(netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr'])
        except KeyError:
            pass
    return ip_address


def is_valid_ipv4(ip, version=4):
    try:
        result = IP(ip, ipversion=version)
    except ValueError:
        return False
    if result is not None and result != "":
        return True


def is_private_ipv4(ip, version=4):
    """
    check if the given ip address is valid and private ip
    :param ip:
    :param version:
    :return:
    """
    if is_valid_ipv4(ip, version):
        if IP(ip).iptype() == "PRIVATE":
            return True
        else:
            return False
    else:
        raise RuntimeError("Error: invalid ip address: %s" % ip)


def get_ip_address_internal():
    for ip in get_ip_address():
        if is_private_ipv4(ip):
            ip_address_internal = ip
            break
    log.warning('empty internal ip address ') if not ip_address_internal else ''
    return ip_address_internal


def get_ip_address_external():
    import os
    import sys

    try:
        import netifaces
    except ImportError:
        try:
            command_to_execute = "pip install netifaces || easy_install netifaces"
            os.system(command_to_execute)
        except OSError:
            print("Can NOT install netifaces, Aborted!")
            sys.exit(1)
        import netifaces

    routingIPAddr = '127.0.0.1'

    for interface in netifaces.interfaces():
        if interface == netifaces.gateways()['default'][netifaces.AF_INET][1]:
            try:
                routingIPAddr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
            except KeyError:
                pass
    return routingIPAddr


if __name__ == '__main__':
    zabbix_agents_url = 'http://www.zabbix.com/downloads/3.2.0/zabbix_agents_3.2.0.win.zip'
    save_to = r'C:/'

    zip_file = os.path.join(save_to, zabbix_agents_url.split('/')[-1]).replace('\\', '/')
    extract_zip_file_to = get_zip_path(zip_file)
    zabbix_agent_conf_name = 'zabbix_agentd.win.conf'
    zabbix_agent_bin_file = os.path.join(extract_zip_file_to, 'bin', 'win64', 'zabbix_agentd.exe').replace('\\', '/')
    zabbix_agent_conf_file = os.path.join(extract_zip_file_to, 'conf', zabbix_agent_conf_name).replace('\\', '/')
    zabbix_install_log = os.path.join(extract_zip_file_to, 'install.log')

    if not os.path.exists(zip_file):
        download_file(zabbix_agents_url, save_to)
    if not os.path.exists(extract_zip_file_to):
        extract_zip(zip_file, extract_zip_file_to)
    config_conf(zabbix_agent_conf_file)  # can be set more than one time
    install_service()
    run_service()
