#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:service-starter.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/2/11
Create Time:            8:57
Description:            start all business services after system reboot
                        批量启动服务器中指定目录里的服务，找到服务后直接调用其启动脚本
Long Description:       “服务”是指业务服务，如开发的java、node等，不涉及公共或基础服务，如nginx、MySQL等作为基础服务
                        1. 同一个服务可能在部署目录中存在多个版本，需要确定当前运行版本，默认取创建时间最新的版本作为当前运行版本
                        2. 在部署目录中的公共或基础服务属于应该排除或区分的服务
                        3. 逐一启动服务并间隔1s，通过/etc/rc.local发起，可能会有一定的延迟：延迟时间=服务数量*(avg启动时间+1s)
                        4. 使用日志记录启动错误失败的服务和错误日志
References:             [Linux command to find the which are the jars loaded by the jvm](https://stackoverflow.com/questions/2776780/linux-command-to-find-the-which-are-the-jars-loaded-by-the-jvm)
                        [Find where java class is loaded from](https://stackoverflow.com/questions/227486/find-where-java-class-is-loaded-from)
                        [How to get the path of running java program [duplicate]](https://stackoverflow.com/questions/17540942/how-to-get-the-path-of-running-java-program)
                        ```bash
                        # 查找服务名为“dataexchange”的java服务的cwd目录，cwd目录实际上就是当前服务的目录
                        # 示例输出：/opt/ebt/apps/dataexchange.3615022eb66aeb97b93093a288c9e9fb85d0f89d
                        lsof -p $(ps -ef|awk '/[d]ataexchange/{print $2}') | awk '$4=="cwd"{print $NF}'
                        # 注意：使用jps时需要使用运行java服务的账户运行
                        lsof -p $(su - ebt -c "jps -l" | awk '/dataexchange/{print $1}') | awk '$4=="cwd"{print $NF}'
                        ```
Prerequisites:          []
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 2.6
Programming Language:   Python :: 2.7
Topic:                  Utilities
 """
import logging
import os
import subprocess
import time
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

DEBUG = False

JAVA_PACKAGE_NAME_FOR_MAIN_CLASS_LIST = [  # not used, get by `jps -l` or `ps -ef | grep [A]pplication`
    "com.ebt.datres.Application",
    "com.ebt.datres.TouchApplication",
    "com.ebt.platform.dataexchange.Application",
    "com.ebt.service.agentmanagement.Application",
    "com.ebt.service.canal2kafka.Application",
    "com.ebt.service.cashier.Application",
    "com.ebt.service.cloud.Application",
    "com.ebt.service.customer.Application",
    "com.ebt.service.erisk.Application",
    "com.ebt.service.erp.Application",
    "com.ebt.service.file.Application",
    "com.ebt.service.market.Application",
    "com.ebt.service.osap.java.Application",
    "com.ebt.service.pms.Application",
    "com.ebt.service.policy.Application",
    "com.ebt.service.proposal.Application",
    "com.ebt.service.sms.Application",
    "com.ebt.service.user.Application"
]

OPT_EBT_APPS_EXCLUDED_LIST = [
    'app-files',
    'kafka',
    'nginx-conf',
    'zookeeper',
    'mycat',
    'canal',
    'node',
    'python'
]

POST_DEPLOY_SCRIPTS_PATH_LIST = [
    'scripts/post_deploy.sh',  # java, ebtdatres
    'deploy/post_deploy.sh',  # node, zyj-mobile
]

logger = logging.getLogger('mylog')


def set_file_logger(filename, name="mylog", level=logging.INFO, format_string=None):
    global logger
    if not format_string:
        format_string = "%(asctime)s %(name)s %(levelname)s %(thread)d : %(message)s"
    logger = logging.getLogger(name)
    logger.setLevel(level)
    file_handler = logging.FileHandler(filename)
    file_handler.setLevel(level)
    formatter = logging.Formatter(format_string, datefmt=None)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def set_file_logger_date(filename, name="mylog", saves=10, level=logging.INFO, format_string=None):
    global logger
    if not format_string:
        format_string = "%(asctime)s %(name)s %(levelname)s %(thread)d : %(message)s"
    logger = logging.getLogger(name)
    logger.setLevel(level)
    file_handler = TimedRotatingFileHandler(filename, when='d', backupCount=saves, )
    file_handler.setLevel(level)
    formatter = logging.Formatter(format_string, datefmt=None)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def set_file_logger_size(filename, name="mylog", max_size=1024 * 1024 * 2, saves=10, level=logging.INFO,
                         format_string=None):
    global logger
    if not format_string:
        format_string = "%(asctime)s %(name)s %(levelname)s %(thread)d : %(message)s"
    logger = logging.getLogger(name)
    logger.setLevel(level)
    file_handler = RotatingFileHandler(filename, maxBytes=max_size, backupCount=saves)
    file_handler.setLevel(level)
    formatter = logging.Formatter(format_string, datefmt=None)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def set_stream_logger(name='mylog', level=logging.DEBUG, format_string=None):
    """
    stream logger for debug purpose
    """
    global logger
    if not format_string:
        format_string = "%(asctime)s %(name)s %(levelname)s %(pathname)s:%(lineno)d " \
                        "%(process)d %(thread)d : %(message)s"  # see logging.__init__.Formatter()
    logger = logging.getLogger(name)
    logger.setLevel(level)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    formatter = logging.Formatter(format_string, datefmt=None)  # the ISO8601 date format, 2018-12-11 15:01:17,290
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)


def debug_msg(msg, *args, **kwargs):
    # TODO(DingGuodong): a good debug function wanted
    # no qa
    if DEBUG:
        print("debug: {msg}".format(msg=msg))
        print("args: {args}".format(args=str(args)))
        print("kwargs: {kwargs}".format(kwargs=str(kwargs)))


def debug_msg_with_logging(msg, *args, **kwargs):
    """
    脚本调试函数，输出日志行到标准输出
    :param msg: str, 需要打印日志的普通字符串
    :param args: 需要打印日志的list、tuple等
    :param kwargs: 需要打印日志的字典
    :return:
    """
    if DEBUG:
        set_stream_logger('ssd', logging.INFO)  # service_starter_debug
        logger.debug(msg, *args, **kwargs)


def console_log_msg(msg, level="error", *args, **kwargs):
    """
    记录日志到指定的文件并按照日期切割
    :param msg: str, 需要打印日志的普通字符串
    :param level: str, 打印日志的级别，可以定error、warn、debug、info等其他
    :param args: 需要打印日志的list、tuple等
    :param kwargs: 需要打印日志的字典
    :return:
    """
    set_file_logger_date(self_script_output_log_path, name="ssc")  # service_starter_common
    if level == "error":
        logger.error(msg, *args, **kwargs)
    elif level == "warn":
        logger.warn(msg, *args, **kwargs)
    elif level == "debug":
        logger.debug(msg, *args, **kwargs)
    else:
        logger.info(msg, *args, **kwargs)


def sort_app_paths_by_ctime(apps_list):
    """
    :param apps_list: 未经过排序的服务列表
    :return: list 返回按照文件或目录创建时间顺序的列表，按照时间从旧到新排列
    """
    return sorted(apps_list, key=lambda x: os.path.getctime(x))


def find_current_app(path, app_package_name):
    """
    find current version, find running version
    依照app_package_name找到含有app_package_name的所有路径，找到时间最新的路径作为当前运行路径
    :param path: 服务部署根目录，部署服务的根目录
    :param app_package_name: 服务包名，服务名
    :return:
    """
    current_apps_list = []
    for top, dirs, nondirs in os.walk(path):
        for directory in dirs:
            if directory.startswith(app_package_name):
                current_apps_list.append(os.path.join(top, directory))
        break
    uniq_app = sort_app_paths_by_ctime(current_apps_list)[-1]
    return uniq_app


def find_all_apps(path):
    """
    按照提供的path找到path下所有符合条件的服务
    :param path: 服务部署根目录，部署服务的根目录
    :return:
    """
    if os.path.exists(path):
        os.chdir(path)
    else:
        raise IOError("No such file or directory")

    apps_path_list = []
    for top, dirs, nondirs in os.walk(path):
        apps_path_list = [os.path.join(top, directory) for directory in dirs]
        break

    apps_path_string = " ".join(apps_path_list)
    # debug_msg_with_logging(apps_path_string)
    uniq_apps_path_list = []
    uniq_apps_name_list = []
    for app_path in apps_path_list:
        app_package_name = os.path.basename(app_path).split(".")[0]
        if app_package_name in OPT_EBT_APPS_EXCLUDED_LIST:
            continue
        apps_count = apps_path_string.count(app_package_name)  # not best, may be an issue

        if apps_count > 1 and app_package_name not in uniq_apps_name_list:
            current_app = find_current_app(path, app_package_name)
            uniq_apps_path_list.append(current_app)
        elif apps_count > 1 and app_package_name in uniq_apps_name_list:
            # debug_msg_with_logging(app_package_name)
            pass
        else:
            if app_package_name not in OPT_EBT_APPS_EXCLUDED_LIST:
                uniq_apps_path_list.append(app_path)

        uniq_apps_name_list.append(app_package_name)

    uniq_apps_path_list = list(set(uniq_apps_path_list))

    return uniq_apps_path_list


def run_command(executable):
    """
    run system command by subprocess.Popen in silent
    :param executable: executable command
    :return: return_code, stdout, stderr
    """
    proc_obj = subprocess.Popen(executable, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc_obj.communicate()
    return_code = proc_obj.returncode
    return return_code, stdout, stderr


def call_service_start_script(app_path):
    """
    根据找到的服务的目录app_path，找到其中的启动脚本，并运行它
    :param app_path: 服务路径
    :return:
    """
    real_script_path = None
    for script_path in POST_DEPLOY_SCRIPTS_PATH_LIST:
        script_full_path = os.path.join(app_path, script_path)
        if os.path.exists(script_full_path):
            real_script_path = script_full_path
    if real_script_path is not None:
        print("INFO: found script path: ".format(path=real_script_path))
        return_code, stdout, stderr = run_command("su - ebt -c \"/bin/bash {path}\"".format(path=real_script_path))
        if return_code != 0:
            print("ERROR: script execute failed: {path}".format(path=real_script_path))
            console_log_msg("script execute failed: {path}".format(path=real_script_path))
            console_log_msg(stdout)
            console_log_msg(stderr)
            console_log_msg("\n" * 10)
        else:
            print("SUCCESS: script execute succeed: {path}".format(path=real_script_path))
    else:
        print("WARNING: script path not found: {path}".format(path=app_path))
        console_log_msg("WARNING: script path not found: {path}".format(path=app_path), level="warn")

    time.sleep(1)  # no qa when put self into /etc/rc.local


if __name__ == '__main__':
    # override default setting
    DEBUG = True  # enable debug
    opt_ebt_apps_path = r'/opt/ebt/apps'  # set service deploy directory
    self_script_output_log_path = r"/opt/ebt/logs/service_starter.log"  # set script logging file

    wanted_apps_path_list = find_all_apps(opt_ebt_apps_path)
    for wanted_app_path in wanted_apps_path_list:
        print("INFO: found path: ".format(path=wanted_app_path))
        call_service_start_script(wanted_app_path)
