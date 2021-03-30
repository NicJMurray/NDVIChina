import h5py
import mapplot
import numpy as np


### Modify the lines below ####################################################

# Set the file to read in

f = h5py.File('h5lst/MOD11C3.A2010001.006.2016035025508.h5', 'r')

# Set the HDF field we want to read in
h5root = f['MODIS_MONTHLY_0.05DEG_CMG_LST/Data Fields/LST_Day_CMG']


# Set the box corners of our region of interest
# lower latitude, upper latitude, western longitude, eastern longitude
boxcorners = [28, 40, 87, 105]

fname = 'China_LST.png'
title = '1st of July 2019 - China NDVI'
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
data *= h5root.attrs['scale_factor'] # Multiply with scale factor

# Plot and save the thing
mapplot.plot(data, boxcorners=boxcorners, fname=fname, title=title, colorbar_label='')