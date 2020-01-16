#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created by PyCharm.
File Name:              LinuxBashShellScriptForOps:genterate-a-word-cloud.py
Version:                0.0.1
Author:                 dgden
Author Email:           dgdenterprise@gmail.com
URL:                    https://github.com/DingGuodong/LinuxBashShellScriptForOps
Download URL:           https://github.com/DingGuodong/LinuxBashShellScriptForOps/tarball/master
Create Date:            2020/1/13
Create Time:            9:38
Description:            Generate a Word cloud(Tag Cloud)
Long Description:       【标签云 (Tag cloud)】标签云或文字云是关键词的视觉化描述，用于汇总用户生成的标签或一个网站的文字内容。
                        标签一般是独立的词汇，常常按字母顺序排列，其重要程度又能通过改变字体大小或颜色来表现，
                        所以标签云可以灵活地依照字序或热门程度来检索一个标签。 -- 《维基百科》
References:             [如何用Python做中文词云？](https://zhuanlan.zhihu.com/p/28954970)
Prerequisites:          pip install jieba
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
import time

import PIL.Image as image
import jieba
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud


def generate_word_cloud(path):
    """
    Generate a Word cloud
    :param path: the path to text file
    :return: WordCloud
    """
    with open(path) as f:
        text = f.read()

    text = " ".join(jieba.cut(text))

    wordcloud = WordCloud(
        font_path="simhei.ttf",
        max_words=1000,
    ).generate(text)

    now = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

    wordcloud.to_file("_".join((path, now)) + ".png")
    return wordcloud


def generate_word_cloud_with_mask(path, mask=None):
    """
    Generate a Word cloud
    If mask is not None, width and height will be ignored and the shape of mask will be used instead.
    :param path: the path to text file
    :param mask: the path to mask file
    :return: WordCloud
    """
    with open(path) as f:
        text = f.read()

    text = " ".join(jieba.cut(text))

    mask = np.array(image.open(mask))

    wordcloud = WordCloud(
        font_path="simhei.ttf",  # "C:\Windows\Fonts\simhei.ttf"
        max_words=1000,
        mask=mask,
        background_color='white',
    ).generate(text)

    now = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))

    wordcloud.to_file("_".join((path, now)) + "masked.png")
    return wordcloud


def display_image(wordcloud):
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    plt.close()


if __name__ == '__main__':

    filename_list = [
        ('daily-report-2017.txt', '2017.PNG'),
        ('daily-report-2018.txt', '2018.PNG'),
        ('daily-report-2019.txt', '2019.PNG'),
    ]

    for filename, picture in filename_list:
        display_image(generate_word_cloud_with_mask(filename, picture))
