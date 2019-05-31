#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:pyUseMapImprovePerformance.py
Version:                0.0.1
Author:                 Guodong
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2018/1/11
Create Time:            10:32
Description:            use map as parallel executor to improve performance
Long Description:       
References:             https://yq.aliyun.com/articles/337746?spm=5176.100238.spm-cont-list.121.4b8421e547hM0C
Prerequisites:          Pillow
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
from multiprocessing import Pool

try:
    # PIL is only 32-bit available on 64-bit Windows System.
    # We can INSTALL this packages by copy it from "Anaconda2" or use 'Pillow' to replace 'PIL'.
    # Pillow is the friendly PIL fork by Alex Clark and Contributors.
    # PIL is the Python Imaging Library by Fredrik Lundh and Contributors.
    # Note: Pillow is used in Django as well.
    from PIL import Image
except ImportError:
    import Image

SIZE = (75, 75)
SAVE_DIRECTORY = 'thumbs'


def get_image_paths(folder):
    return [os.path.join(folder, f) for f in os.listdir(folder) if 'jpeg' in f.lower() or 'jpg' in f.lower()]


def create_thumbnail(filename):
    im = Image.open(filename)
    im.thumbnail(SIZE, Image.ANTIALIAS)
    base, fname = os.path.split(filename)
    save_path = os.path.join(base, SAVE_DIRECTORY, fname)
    im.save(save_path)


def example_another():
    import urllib.request, urllib.error, urllib.parse
    from multiprocessing.dummy import Pool as ThreadPool

    urls = [
        'http://www.python.org',
        'http://www.python.org/about/',
        'http://www.onlamp.com/pub/a/python/2003/04/17/metaclasses.html',
        'http://www.python.org/doc/',
        'http://www.python.org/download/',
        'http://www.python.org/getit/',
        'http://www.python.org/community/',
        'https://wiki.python.org/moin/',
        'http://planet.python.org/',
        'https://wiki.python.org/moin/LocalUserGroups',
        'http://www.python.org/psf/',
        'http://docs.python.org/devguide/',
        'http://www.python.org/community/awards/'
        # etc..
    ]
    # Make the Pool of workers
    thread_pool = ThreadPool(4)
    # Open the urls in their own threads
    # and return the results
    results = thread_pool.map(urllib.request.urlopen, urls)
    # close the pool and wait for the work to finish
    thread_pool.close()
    thread_pool.join()

    print(results)


if __name__ == '__main__':
    original_images_folder = os.path.abspath(str(r"D:\Users\Chris\Pictures\iPhone\DCIM\100APPLE"))
    save_dirs = os.path.join(original_images_folder, SAVE_DIRECTORY)
    if not os.path.exists(save_dirs):
        os.mkdir(save_dirs)
    images = get_image_paths(original_images_folder)
    print("{count} images files are going to be processed ...".format(count=len(images)))
    pool = Pool()
    pool.map(create_thumbnail, images)
    pool.close()
    pool.join()
