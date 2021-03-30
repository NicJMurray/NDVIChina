#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 14:51:04 2021

@author: nm416
"""


import h5py
import mapplot
import numpy as np


### Modify the lines below ####################################################

# Set the file to read in

import os

name = []
directory = r'/lustre/ahome3/n/nm416/Desktop/code2/h5ndvi'
for filename in os.listdir(directory):
    if filename.endswith(".h5"):
        name.append(os.path.join('NDVI/'+filename))
    else:
        continue

fn = ['China_NDVI_0719.png', 'China_NDVI_0819.png', 'China_NDVI_0919.png'
         , 'China_NDVI_1019.png', 'China_NDVI_1119.png', 'China_NDVI_1219.png', 
         'China_NDVI_0120.png', 'China_NDVI_0220.png', 'China_NDVI_0320.png'
         , 'China_NDVI_0420.png', 'China_NDVI_0520.png', 'China_NDVI_0620.png',
         'China_NDVI_0720.png']

tit = ['1st of July 2019 - NDVI', '1st of August 2019 - NDVI', '1st of September 2019 - NDVI', 
       '1st of October 2019 - NDVI', '1st of November 2019 - NDVI', '1st of December 2019 - NDVI', 
       '1st of January 2020 - NDVI', '1st of February 2020 - NDVI', '1st of March 2020 - NDVI', 
       '1st of April 2020 - NDVI', '1st of May 2020 - NDVI', '1st of June 2020 - NDVI', 
       '1st of July 2020']


for i in range(13):
    
    f = h5py.File(name[i], 'r')

    # Set the HDF field we want to read in
    h5root = f['MOD_Grid_monthly_CMG_VI/Data Fields/CMG 0.05 Deg Monthly NDVI']


    # Set the box corners of our region of interest
    # lower latitude, upper latitude, western longitude, eastern longitude
    boxcorners = [19, 54, 70, 133]

    fname = fn[i]
    title = tit[i]
    colorbar_label=''


### Don't touch the script from here on! ######################################
###############################################################################

### Calculate which parts of the big array we actually want to grab ###########
    lat_n, lon_n = h5root.shape

    north_lat = int((-lat_n / 180.0) * boxcorners[0] + lat_n / 2.0)
    south_lat = int((-lat_n / 180.0) * boxcorners[1] + lat_n / 2.0)
    west_lon = int((lon_n / 360.0) * boxcorners[2] + lon_n / 2.0)
    east_lon = int((lon_n / 360.0) * boxcorners[3] + lon_n / 2.0)

###############################################################################

# Replace fill values by NaN's
    data = np.array(h5root[south_lat:north_lat,
                       west_lon:east_lon]).astype(float)

    data[np.where(data == h5root.fillvalue)] = np.nan
    data /= h5root.attrs['scale_factor'] # Multiply with scale factor

# Plot and save the thing
    mapplot.plot(data, boxcorners=boxcorners, fname=fname, title=title, colorbar_label='')