import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib.patches as mpatches

#Open each .txt file
fN = open('si_nd1.txt', 'r')
fS = open('si_sm1.txt', 'r')
fL = open('si_ls1.txt', 'r')

#put the data into an array
ndvi_data = np.loadtxt(fN)
sm_data = np.loadtxt(fS)
lst_data = np.loadtxt(fL)

#normalise the data using z scores
z_ndvi = stats.zscore(ndvi_data, ddof=1)
z_sm = stats.zscore(sm_data, ddof=1)
z_lst = stats.zscore(lst_data, ddof=1)
print(z_ndvi)
print('')
print(z_sm)
print('')
print(z_lst)
print('')

fig, ax = plt.subplots()

dates = []
for i in range(10,21):
    for f in range(1,13):
        #print(len(f, 2000i, sep = '.')
        month = str(f)
        year = str(i)
        date = month+"."+year
        dates.append(date)
 
        
#aesthetics
plt.style.use("seaborn-dark")
for param in ['figure.facecolor', 'axes.facecolor', 'savefig.facecolor']:
    plt.rcParams[param] = '#212946'  # bluish dark grey
for param in ['text.color', 'axes.labelcolor', 'xtick.color', 'ytick.color']:
    plt.rcParams[param] = '0.9'  # very light grey
ax.grid(color='#2A3459')  # bluish dark grey, but slightly lighter than background        

red_patch = mpatches.Patch(color=('xkcd:red'), label='LST')
green_patch = mpatches.Patch(color=('xkcd:neon green'), label='NDVI')
cyan_patch = mpatches.Patch(color=('xkcd:cyan'), label='Soil Moisture')
plt.legend(loc = 2)
plt.legend(handles=([red_patch,green_patch,cyan_patch]), loc = 'upper left')


#plot the normalised data
ax.plot(dates, z_ndvi, color = ('xkcd:cyan'))
ax.plot(dates, z_sm, color = ('xkcd:neon green'))
ax.plot(dates, z_lst, color = ('xkcd:red'))

ax.xaxis.set_major_locator(plt.MaxNLocator(12))

ax.set_ylim(-2.2,3.2)
plt.xlabel("Time (M/YY)")
plt.ylabel("Variables")
ax.set_title('Variable Comparison for the Sichuan region')



#save the figure
plt.tight_layout()
plt.savefig("Sichuan_comp", dpi = 400)