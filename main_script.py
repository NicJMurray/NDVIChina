import h5py
import mapplot
import numpy as np


### Modify the lines below ####################################################

# Set the file to read in

f = h5py.File('/lustre/ahome3/n/nm416/Desktop/code2/h5ndvi/MOD13C2.A2010001.006.2015198205120.h5', 'r')

# Set the HDF field we want to read in
h5root = f['MOD_Grid_monthly_CMG_VI/Data Fields/CMG 0.05 Deg Monthly NDVI']


# Set the box corners of our region of interest
# lower latitude, upper latitude, western longitude, eastern longitude
boxcorners = [19, 54, 70, 133]

fname = 'China_NDVI.png'
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
data /= h5root.attrs['scale_factor'] # Multiply with scale factor

# Plot and save the thing
mapplot.plot(data, boxcorners=boxcorners, fname=fname, title=title, colorbar_label='')