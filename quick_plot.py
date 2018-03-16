#!/usr/bin/env python

"""
Make a quick sanity plot to check we've processed things correctly
"""

import numpy as np
import sys
import os
import glob
import matplotlib.pyplot as plt

__author__  = "Martin De Kauwe"
__version__ = "1.0 (18.03.2018)"
__email__   = "mdekauwe@gmail.com"

nrows = 2160
ncols = 4320

files = glob.glob("processed/*")
fname = files[0]
data = np.fromfile(fname).reshape(nrows,ncols)
plt.imshow(data)
plt.colorbar(orientation='horizontal')
plt.show()
