#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 17:00:52 2021

@author: nm416
"""

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
yearlyAverage = []

#full directory path (use pwd in terminal once cd into correct location)
#make sure this file contains ALL 120 NDVI files in h5
directory = r'/lustre/ahome3/n/nm416/Desktop/code2/h5ndvi'
#each filename ending in .h5 in this directory is added to name array
for filename in os.listdir(directory):
    if filename.endswith(".h5"):
        name.append(os.path.join('h5ndvi/'+filename))
    else:
        continue


name = sorted(name)

 
for i in range(130):
    
    f = h5py.File(name[i], 'r')
 
    # Set the HDF field we want to read in
    h5root = f['MOD_Grid_monthly_CMG_VI/Data Fields/CMG 0.05 Deg Monthly NDVI']
 
 
    # Set the box corners of our region of interest
    # lower latitude, upper latitude, western longitude, eastern longitude
    boxcorners = [-19.230, -12.646, -42.312, -38.128]
    
 
 
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
    #print(aV)
    #print(name[i])
    #print(dates[i])
    #add these average values into array created earlier
    monthlyAverage.append(aV)


#print the monthly average array
#print('Monthly Average:',monthlyAverage)

#Calculate the average LST over 10yrs    
aV2 = np.mean(monthlyAverage)
print('10yr Average:', aV2) 

#Find the average value for each year 
list1 = [monthlyAverage]
b = np.mean(np.array(list1).reshape(-1, 13), axis=1)
print('Year average:', b) 


#Creat x-axis of years 2010-2019 
x = np.linspace(2010,2021,10)
#print(x)

 
fig, ax = plt.subplots()  # Create a figure containing a single axes.
# Plot some data on the axes.
ax.plot(x, b, color = 'darkgreen')
#Add a line to show the 10yr average
plt.axhline(y=aV2, color='blue', linestyle='--')


ax.set_title('NDVI Yearly Average: 2010-2019, East Coast')
ax.set_xlabel('Years')
ax.set_ylabel('NDVI')
plt.setp(ax.get_xticklabels(), rotation = 45)
ax.xaxis.set_major_locator(ticker.MaxNLocator(13))
