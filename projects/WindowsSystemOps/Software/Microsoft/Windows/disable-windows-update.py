#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:disable-windows-update.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/12/30
Create Time:            17:56
Description:            disable Windows Update Service
Long Description:       
References:             
Prerequisites:          pip install psutil
                        pip install wmi
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
import psutil
import time
import wmi


def stop_update_process():
    # core windows update services are "wuauserv" and "TrustedInstaller"
    # another windows services will released by Microsoft in the future.
    # such as 'WaaSMedicSvc', 'sedsvc'
    windows_update_services_list = [
        "wuauserv",
        "TrustedInstaller"
    ]

    for service_name in windows_update_services_list:
        pid = psutil.win_service_get(name=service_name).pid()
        if pid > 0:  # not None
            psutil.Process(pid=pid).terminate()


def get_wmi_instance(computer, user, password):
    try:
        #
        # Using wmi module before 1.0rc3
        #
        connection = wmi.connect_server(server=computer, user=user, password=password)
        instance = wmi.WMI(wmi=connection)
        return instance
    except Exception:
        #
        # Using wmi module at least 1.0rc3
        #
        instance = wmi.WMI(computer=computer, user=user, password=password)
        return instance


def disable_update_service():
    # https://stackoverflow.com/questions/25395175/how-to-disable-a-windows-service-with-python/65557206#65557206
    # sc config <service name> start=disabled
    # Set-Service -Name <service name> -StartupType Disabled
    # https://docs.microsoft.com/en-us/windows/win32/cimwin32prov/win32-service
    # https://docs.microsoft.com/en-us/windows/win32/cimwin32prov/changestartmode-method-in-class-win32-service

    # wmi error code:	-2147023169	PRC_S_Call_Failed_DNE 远程过程调用失败且未执行。
    c = wmi.WMI()
    time.sleep(0.5)

    windows_update_services_list = [
        "wuauserv",
        "TrustedInstaller"
    ]

    for service_name in windows_update_services_list:
        service = c.Win32_Service(Name=service_name)[0]
        service.ChangeStartMode(StartMode="Disabled")


def change_filename():
    # NO QA. change filename of 'C:\WINDOWS\servicing\TrustedInstaller.exe'
    pass


def disable_task():
    # prevent the task scheduler from starting the windows update services
    # name: 'Scheduled Start'
    # path: '\Microsoft\Windows\WindowsUpdate'
    pass


def set_gpo():
    # disable windows update using GPO

    # 指定 Intranet Microsoft 更新服务位置
    # https://docs.microsoft.com/zh-cn/windows/deployment/update/waas-wu-settings#specify-intranet-microsoft-update-service-location
    # GP English name: Specify intranet Microsoft update service location
    # GP name: CorpWuURL
    # GP element: CorpWUURL_Name
    # GP path: Windows Components/Windows Update
    # GP ADMX file name: WindowsUpdate.admx
    pass


def set_registry():
    # disable windows update using registry

    # Windows Registry Editor Version 5.00
    #
    # [HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate]
    # "WUServer"="http://windowsupdate.aliyun-inc.com"
    # "WUStatusServer"="http://windowsupdate.aliyun-inc.com"
    #
    # [HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Microsoft\Windows\WindowsUpdate\AU]
    # "NoAutoUpdate"=dword:00000000
    # "AUOptions"=dword:00000002
    # "ScheduledInstallDay"=dword:00000000
    # "ScheduledInstallTime"=dword:00000003
    # "UseWUServer"=dword:00000001
    # "AutoInstallMinorUpdates"=dword:00000000
    pass


def set_firewall():
    # block access windows update server
    # WindowsUpdateUrls:
    # "stats.microsoft.com,download.microsoft.com,update.microsoft.com,windowsupdate.microsoft.com,windowsupdate.com,download.windowsupdate.com,ntservicepack.microsoft.com,wustat.windows.com"
    pass


if __name__ == '__main__':
    stop_update_process()
    disable_update_service()
