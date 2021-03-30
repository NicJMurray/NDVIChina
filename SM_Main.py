#comment these out whilst unused

import matplotlib.pyplot as plt
#import mapplot
import numpy as np
import netCDF4 as nc

 
 
### Modify the lines below ####################################################
 
# Set the file to read in
 
import os

#create empty array to store file names 
name = []
#empty array for averages later
monthlyAverage = []
monthlystd = []
#full directory path (use pwd in terminal once cd into correct location)
#make sure this file contains ALL 120 NDVI files in h5
directory = r'/lustre/ahome3/n/nm416/Desktop/code2/sm'
#each filename ending in .h5 in this directory is added to name array
for filename in os.listdir(directory):
    if filename.endswith(".nc"):
        name.append(os.path.join('sm/'+filename))
    else:
        continue

#print entire name array to verify the correct files included
#testing reasons - can comment out once sure it's working
#print(name)
name = sorted(name)

#print(fn[11])
#print(tit[11])
 
for i in range(132):
    
    f = nc.Dataset(name[i], 'r')

    # Set the HDF field we want to read in
    sm = f['sm']
    
    # Set the box corners of our region of interest
    # lower latitude, upper latitude, western longitude, eastern longitude
    boxcorners = [24.02, 26.091, 116.15, 117.78]




    
    fname = 'gansusm.png'
    title = 'Month: 01, Year: 2009'
    colorbar_label=''
    
    
    ### Don't touch the script from here on! ######################################
    ###############################################################################
    
    ### Calculate which parts of the big array we actually want to grab ###########
    lat_n, lon_n = sm.shape[1:]
    
    north_lat = int((-lat_n / 180.0) * boxcorners[0] + lat_n / 2.0)
    south_lat = int((-lat_n / 180.0) * boxcorners[1] + lat_n / 2.0)
    west_lon = int((lon_n / 360.0) * boxcorners[2] + lon_n / 2.0)
    east_lon = int((lon_n / 360.0) * boxcorners[3] + lon_n / 2.0)
    
    ###############################################################################
    
    # Replace fill values by NaN's
    data = np.array(sm[0, south_lat:north_lat,
                           west_lon:east_lon]).astype(float)
    
    data[np.where(data == sm._FillValue)] = np.nan
    #find the average value per month
    aV = np.nanmean(data)

    #add these average values into array created earlier
    monthlyAverage.append(aV)
    sd = np.nanstd(data)
    monthlystd.append(sd)


#Print the monthly average array
#print(monthlyAverage)
avgMonth = []
monthlyDev = []
for i in range(12):
    months = monthlyAverage[i::12]
    avg = np.mean(months)
    avgMonth.append(avg)
    monthlyDev.append(months - avg)
    i += 1

#print('Average month:', avgMonth)

dev2 = []
for i in range(11):    
    lst2 = [item[i] for item in monthlyDev]
    dev2.append(lst2)
#print(monthlyDev)
monthlyDev = np.concatenate(dev2)
#print('Dev:', monthlyDev)

#Create list of dates
dates = []

for i in range(10,21):
    for f in range(1,13):
        #print(len(f, 2000i, sep = '.')
        month = str(f)
        year = str(i)
        date = month+"."+year
        dates.append(date)

fig, ax = plt.subplots()

plt.tight_layout()

x = dates
y = monthlyAverage


ax.xaxis.set_major_locator(plt.MaxNLocator(12))
#ax.set_xticklabels(dates, rotation = 90)


# Plot some data on the axes.
ax.errorbar(x,y, yerr = monthlystd, fmt = '-', capsize = 3, color = ('xkcd:cyan'), 
            ecolor = 'grey', linewidth=2.5, elinewidth=1)


ax.plot(dates,monthlyAverage, color = ('xkcd:cyan'))  # Plot some data on the axes.
ax.xaxis.set_major_locator(plt.MaxNLocator(12))
ax.set_ylim(0.10,0.4)
plt.xlabel("Time (M/YY)")
plt.ylabel("Soil moisture m3/m3")
ax.set_title('Soil Moisture Monthly Avg: 2010-2021 Fujian (With Standard Dev)')

#ax.axhline(y=0, color = 'orange', linestyle = 'solid')

plt.style.use("seaborn-dark")
for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
    plt.rcParams[param] = '#212946'  # bluish dark grey
for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
    plt.rcParams[param] = '0.9'  # very light grey
ax.grid(color='#2A3459')  # bluish dark grey, but slightly lighter than background


plt.tight_layout()
plt.savefig("Fujian_sstd", dpi = 400)



