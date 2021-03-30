#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 16:32:04 2021

@author: nm416
"""

import h5py
import numpy as np
import matplotlib.pyplot as plt
 
 
# Set the file to read in
 
import os
dates = []  #empty array for dates
#looping over the months and creating a date array
for i in range(10,21):
    for f in range(1,13):
        month = str(f)
        year = str(0+i)
        date = month+"."+year
        dates.append(date)



#file names
name = []
#averages
monthlyAverage = []
#using the correct directiory and adding every file ending in .h5 to the array
directory = r'/lustre/ahome3/n/nm416/Desktop/code2/h5ndvi'
for filename in os.listdir(directory):
    if filename.endswith(".h5"):
        name.append(os.path.join('h5ndvi/'+filename))
    else:
        continue


name = sorted(name)


for i in range(132):
    
    f = h5py.File(name[i], 'r')
    # Set the HDF field we want to read in
    h5root = f['MOD_Grid_monthly_CMG_VI/Data Fields/CMG 0.05 Deg Monthly NDVI']
    # Set the box corners of our region of interest
    # lower latitude, upper latitude, western longitude, eastern longitude
    boxcorners = [26.93, 29.736, 100.78, 103]

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
    
    #find the average value per month
    aV = np.nanmean(data)
    monthlyAverage.append(aV)


fig, ax = plt.subplots()  # Create a figure containing a single axes.

plt.tight_layout()
ax.plot(dates,monthlyAverage, color = ('xkcd:emerald'), marker = '.')  # Plot time series
ax.xaxis.set_major_locator(plt.MaxNLocator(12))
ax.set_ylim(0,1)
plt.xlabel("Month and Year")
plt.ylabel("NDVI")
plt.title("NDVI of the Sichuan Province from 2010 to 2021")

#aesthetics
plt.style.use("seaborn-dark")
for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
    plt.rcParams[param] = '#212946'  # bluish dark grey
for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
    plt.rcParams[param] = '0.9'  # very light grey
ax.grid(color='#2A3459')  # bluish dark grey, but slightly lighter than background

#save file
plt.tight_layout()
plt.savefig("Sichuan_NDVI", dpi = 400)

