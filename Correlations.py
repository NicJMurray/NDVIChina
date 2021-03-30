import numpy as np
from numpy import cov
from scipy.stats import pearsonr
from scipy.stats import spearmanr
import matplotlib.pyplot as plt

#Open each text file
fN = open('si_nd.txt', 'r')
fS = open('si_sm.txt', 'r')
fL = open('si_ls.txt', 'r')

#put the data into an array
ndvi_data = np.loadtxt(fN)
sm_data = np.loadtxt(fS)
lst_data = np.loadtxt(fL)

#Find the mean of each variable
nAv = np.mean(ndvi_data)
sAv = np.mean(sm_data)
lAv = np.mean(lst_data)

#Find the standard deviations of each variable
nstd = np.std(ndvi_data)
smstd = np.std(sm_data)
lstd = np.std(lst_data)

covariance = cov(ndvi_data, sm_data)
print(covariance)

#Find the Pearsons Correlation
corr, _ = pearsonr(ndvi_data, sm_data)
print('Pearsons correlation NDVI and SM: %.3f' % corr)
corr, _ = pearsonr(ndvi_data, lst_data)
print('Pearsons correlation NDVI and LST: %.3f' % corr)
corr, _ = pearsonr(lst_data, sm_data)
print('Pearsons correlation LST and SM: %.3f' % corr)

#Find the Spearmans Correlation
corr, _ = spearmanr(ndvi_data, sm_data)
print('Spearmans correlation NDVI and SM: %.3f' % corr)
corr, _ = spearmanr(ndvi_data, lst_data)
print('Spearmans correlation NDVI and LST: %.3f' % corr)
corr, _ = spearmanr(lst_data, sm_data)
print('Spearmans correlation LST and SM: %.3f' % corr)

b = pearsonr(ndvi_data, sm_data)
print('R and P value', b)


fig, ax = plt.subplots()
ax.scatter(ndvi_data, sm_data, color = ('xkcd:cyan'))
ax.set_xlabel('NDVI')
ax.set_ylabel('Soil moisture')
ax.set_title('Soil Moisture and NDVI Monthly Deviation correlation plot [Sichuan]')
ax.grid(color='#2A3459')
plt.savefig("Sichuan_smcor", dpi = 400)

fig, ax = plt.subplots()
ax.scatter(ndvi_data, lst_data, color = ('xkcd:rust'))
ax.set_xlabel('NDVI')
ax.set_ylabel('LST')
ax.set_title('LST and NDVI Monthly Deviation Correlation Plot [Sichuan]')
ax.grid(color='#2A3459')
plt.savefig("Sichuan_lstcor", dpi = 400)


