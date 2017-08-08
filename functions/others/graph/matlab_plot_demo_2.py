#!/usr/bin/python
# encoding: utf-8
# -*- coding: utf8 -*-
"""
Created by PyCharm.
File:               LinuxBashShellScriptForOps:matlab_plot_demo_2.py
User:               Guodong
Create Date:        2017/8/7
Create Time:        19:51
Description:
References:         https://matplotlib.org/examples/pylab_examples/load_converter.html
 """
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import matplotlib.dates as mdates
from matplotlib.dates import bytespdate2num

datafile = cbook.get_sample_data('msft.csv', asfileobj=False)
print('loading', datafile)

dates, closes = np.loadtxt(datafile, delimiter=',',
                           converters={0: bytespdate2num('%d-%b-%y')},
                           skiprows=1, usecols=(0, 2), unpack=True)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot_date(dates, closes, '-')
fig.autofmt_xdate()
plt.show()
