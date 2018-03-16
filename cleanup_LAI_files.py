#!/usr/bin/env python

"""
Clean up the LAI files: turn into LAI units, screen bad data and rotate, write
to a new file.
"""

import numpy as np
import sys
import os
import glob
import tarfile

__author__  = "Martin De Kauwe"
__version__ = "1.0 (18.03.2018)"
__email__   = "mdekauwe@gmail.com"

nrows = 2160
ncols = 4320

odir = "processed"
if not os.path.exists(odir):
    os.makedirs(odir)

for fname in glob.glob("data/*"):
    data = np.fromfile(fname, dtype=np.uint8).reshape(ncols, nrows)
    data = np.where(np.logical_or(data < 0, data > 70), np.nan, data)
    data *= 0.1
    data = np.rot90(data)

    ofname = os.path.basename(fname)
    data.tofile(os.path.join(odir, ofname))
