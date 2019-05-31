#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyGetLockScreenWallpaperOnWindows10.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/7/25
Create Time:            11:38
Description:            Get Lock Screen Wallpaper on Windows 10
Long Description:       
References:             
Prerequisites:          pip install shutil
Development Status:     3 - Alpha, 5 - Production/Stable
Environment:            Console
Intended Audience:      System Administrators, Developers, End Users/Desktop
License:                Freeware, Freely Distributable
Natural Language:       English, Chinese (Simplified)
Operating System:       POSIX :: Linux, Microsoft :: Windows
Programming Language:   Python :: 3

Topic:                  Utilities
 """
import os
import shutil


def get_wallpaper_path():
    # username = [os.environ.get(x) for x in ('LOGNAME', 'USER', 'LNAME', 'USERNAME') if
    #             os.environ.get(x) is not None][0]
    keyword = 'ContentDeliveryManager'
    top_dir = os.getenv('LOCALAPPDATA') + '\Packages'

    cdm_fullname = ''
    dirs_in_top_dir = os.listdir(top_dir)
    for index, item in enumerate(dirs_in_top_dir):
        if keyword in item:
            cdm_fullname = dirs_in_top_dir[index]
    wallpaper_folder = top_dir + '\\' + cdm_fullname + '\LocalState\Assets'
    if os.path.exists(wallpaper_folder):
        return wallpaper_folder
    else:
        return ""


if __name__ == '__main__':
    wallpaper_directory = get_wallpaper_path()
    wallpapers = os.listdir(wallpaper_directory)
    save_folder = os.path.dirname(os.path.realpath(__file__)) + '\wallpapers'
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    for wallpaper in wallpapers:
        wallpaper_path = os.path.join(wallpaper_directory, wallpaper)
        if os.path.getsize(wallpaper_path) < 170 * 1024:
            continue
        save_path = os.path.join(save_folder, wallpaper + '.jpg')
        shutil.copyfile(wallpaper_path, save_path)
