#!/usr/bin/env python

"""
Figure out Australian continental LAI trend. I'm taking the maximum LAI value
per month and then plotting the spatial trend.

Need to revise this a little:
- for now I'm just fitting a linear trend: we should really seperate out the
  trend and seasonality
"""

import numpy as np
import sys
import os
import glob
import matplotlib.pyplot as plt
from scipy import stats
from mpl_toolkits.axes_grid1 import make_axes_locatable

__author__  = "Martin De Kauwe"
__version__ = "1.0 (18.03.2018)"
__email__   = "mdekauwe@gmail.com"

nrows = 2160
ncols = 4320

# Australia, roughly
row_st = 550
row_en = 953
col_st = 3500
col_en = 4020
nrowsx = row_en - row_st
ncolsx = col_en - col_st

yrs = np.arange(1982,1988)
nyrears = len(yrs)
all_yrs = np.zeros((nyrears,nrowsx,ncolsx))

yr_cnt = 0
for yr in yrs:
    yrs_data = np.zeros((24,nrowsx,ncolsx)) # two values per month
    cnt = 0

    # NB. Australian years

    # Get values from previous year ...
    for mth in ['jul', 'aug', 'sep', 'oct', 'nov', 'dec']:
        for period in ["a", "b"]:
            fn = "processed/AVHRRBUVI01.%s%s%s.abl" % (yr-1, mth, period)
            data = np.fromfile(fn).reshape(nrows,ncols)
            data = data[row_st:row_en,col_st:col_en]
            yrs_data[cnt,:,:] = np.where(data > 0.0, data, np.nan)
            cnt += 1

    for mth in ['jan', 'feb', 'mar', 'apr', 'may', 'jun']:
        for period in ["a", "b"]:
            fn = "processed/AVHRRBUVI01.%s%s%s.abl" % (yr, mth, period)
            data = np.fromfile(fn).reshape(nrows,ncols)
            data = data[row_st:row_en,col_st:col_en]
            yrs_data[cnt,:,:] = np.where(data > 0.0, data, np.nan)
            cnt += 1

    all_yrs[yr_cnt,:,:] = np.nanmax(yrs_data, axis=0)
    yr_cnt += 1


trend = np.zeros((nrowsx,ncolsx))
for row in range(nrowsx):
    for col in range(ncolsx):
        vals = all_yrs[:,row,col]
        vals = vals[~np.isnan(vals)]
        if len(vals) > 3:
            X = np.arange(len(vals))
            mask = ~np.isnan(vals)
            (slope, intercept, r_value,
             p_value, std_err) = stats.linregress(X[mask], vals[mask])
            if p_value < 0.05:
                trend[row,col] = slope
        else:
            trend[row,col] = np.nan

width  = 9.0
height = width / 1.618
fig = plt.figure(figsize=(width, height))
plt.rcParams['text.usetex'] = False
plt.rcParams['font.family'] = "sans-serif"
plt.rcParams['font.sans-serif'] = "Helvetica"
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['font.size'] = 14
plt.rcParams['legend.fontsize'] = 14
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14

ax1 = fig.add_subplot(111)
im = ax1.imshow(trend)
# create an axes on the right side of ax. The width of cax will be 5%
# of ax and the padding between cax and ax will be fixed at 0.05 inch.
divider = make_axes_locatable(ax1)
cax = divider.append_axes("right", size="5%", pad=0.05)
fig.colorbar(im, cax=cax)
plt.show()
