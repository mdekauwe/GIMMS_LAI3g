#!/usr/bin/env python

"""
Download all of the GIMMS LAI3g data ...
"""

import urllib.request
import numpy as np
import sys
import os
import io
import requests
import pandas

__author__  = "Martin De Kauwe"
__version__ = "1.0 (18.03.2018)"
__email__   = "mdekauwe@gmail.com"

save_dir_name = "data"
if not os.path.exists(save_dir_name):
    os.makedirs(save_dir_name)

url = "http://sites.bu.edu/cliveg/files/2014/08/gimms_list.txt"
s = requests.get(url).content
df = pd.read_csv(io.StringIO(s.decode('utf-8')))

for index, row in df.iterrows():
    url_f = row.values[0]
    ofile = os.path.join(save_dir_name, url_f.split('/')[-1])
    ext = ofile.split(".")[-1]
    if ext == "abl": # LAI files
        print(ofile)
        urllib.request.urlretrieve(url_f, ofile)
