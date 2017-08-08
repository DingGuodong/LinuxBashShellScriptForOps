#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:matlab_plot_demo_3.py
User:               Guodong
Create Date:        2017/8/7
Create Time:        19:54
Description:
References:         《Python编程 : 从入门到实践》 作者：[美] Eric Matthes 第15章 生成数据
 """
import matplotlib.pyplot as plt

input_values = [1, 2, 3, 4, 5]
squares = [1, 4, 9, 16, 25]
plt.plot(input_values, squares, linewidth=1, color='g')
plt.title("Square Numbers", fontsize=24)
plt.xlabel("Value", fontsize=14)
plt.ylabel("Square of Value", fontsize=14)
plt.tick_params(axis='both', labelsize=14)
plt.show()
