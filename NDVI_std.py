#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 16:32:04 2021

@author: nm416
"""

#comment these out whilst unused
import h5py
#import mapplot
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
 
 
### Modify the lines below ####################################################
 
# Set the file to read in
 
import os

#empty array for dates
dates = []
#looping over years then months, connecting those as strings and appending
#to dates
for i in range(10,21):
    for f in range(1,13):
        month = str(f)
        year = str(0+i)
        date = month+"."+year
#        date = f,2000+i,sep="."
        #print(date)
        dates.append(date)
#        print ("Month",f,2000+i)
#print for testing
#print (dates)


#create empty array to store file names 
name = []
#empty array for averages later
monthlyAverage = []
monthlystd = []
#full directory path (use pwd in terminal once cd into correct location)
#make sure this file contains ALL 120 NDVI files in h5
directory = r'/lustre/ahome3/n/nm416/Desktop/code2/h5ndvi'
#each filename ending in .h5 in this directory is added to name array
for filename in os.listdir(directory):
    if filename.endswith(".h5"):
        name.append(os.path.join('h5ndvi/'+filename))
    else:
        continue

#print entire name array to verify the correct files included
#testing reasons - can comment out once sure it's working
print(name)
#sort name array into alphabetical order
name = sorted(name)
#check it put it into date order
print(name)


for i in range(132):
    
    f = h5py.File(name[i], 'r')
 
    # Set the HDF field we want to read in
    h5root = f['MOD_Grid_monthly_CMG_VI/Data Fields/CMG 0.05 Deg Monthly NDVI']
 
 
    # Set the box corners of our region of interest
    # lower latitude, upper latitude, western longitude, eastern longitude
    boxcorners = [34.47, 40.75, 111.15, 114.13]




 
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
    
    #find the average value per month
    aV = np.nanmean(data)
    #print the average for each month (testing, comment out when sure)
    print(aV)
    print(name[i])
    print(dates[i])
    #add these average values into array created earlier
    monthlyAverage.append(aV)
    
    sd = np.nanstd(data)
    monthlystd.append(sd)


#print the monthly average array
#print(monthlyAverage)

x = dates
y = monthlyAverage
    
fig, ax = plt.subplots()  # Create a figure containing a single axes.
# Plot some data on the axes.
ax.errorbar(x,y, yerr = monthlystd, fmt = '-', capsize = 3, color = ('xkcd:neon green'), 
            ecolor = 'grey', linewidth=2.5, elinewidth=1)


ax.set_xlabel('Time (M/YY)')
ax.set_ylabel('NDVI')
ax.set_title('NDVI Monthly Avg: 2010-2021 Shanxi (With Standard Dev)')
ax.set_ylim(0,1)
plt.setp(ax.get_xticklabels(), rotation = 45)
ax.xaxis.set_major_locator(ticker.MaxNLocator(12))
ax.xaxis.set_minor_locator(ticker.MaxNLocator(150))

#ax.set_facecolor('xkcd:forest green')
#fig.patch.set_facecolor('xkcd:mint green')
plt.style.use("seaborn-dark")
for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
    plt.rcParams[param] = '#212946'  # bluish dark grey
for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
    plt.rcParams[param] = '0.9'  # very light grey
ax.grid(color='#2A3459')  # bluish dark grey, but slightly lighter than background


plt.tight_layout()
plt.savefig("Shanxi_NDVI", dpi = 400)

