import numpy as np
import numpy.ma as ma
import matplotlib as mpl
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

#mpl.use('AGG')

from matplotlib import pyplot as plt
from matplotlib import ticker as mticker


def plot(data, boxcorners, fname='default.png', title='no title set', cmap=plt.cm.hot, vmin='None',vmax='None', colorbar_label='', extend='neither'):

    if vmin == 'None':
        vmin=np.nanmin(data)
    if vmax == 'None':
        vmax=np.nanmax(data)

    xn = np.linspace(boxcorners[2], boxcorners[3], data.shape[1])
    yn = np.linspace(boxcorners[1], boxcorners[0], data.shape[0])
    xg, yg = np.meshgrid(xn, yn)
    
    fig = plt.figure()
    ax = plt.axes(projection=ccrs.PlateCarree())

    #ax.coastlines('50m',linewidth=0.3) # Use this for higher resolution
    ax.coastlines(linewidth=0.3)
 
    plt.title(title,fontsize=20)
    plt.subplots_adjust(left=None, bottom=0.18, right=None, top=0.85, wspace=None, hspace=None)

    gl = ax.gridlines(crs=ccrs.PlateCarree(),linewidth=0.5,draw_labels=True,color='gray',alpha=0.5,linestyle='--')
    gl.xlabels_top = False
    gl.xlocator = mticker.FixedLocator(np.arange(0., 360.1, 20.)-180)
    gl.ylocator = mticker.FixedLocator(np.arange(-90., 90.1, 10.))
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER
    gl.xlabel_style = {'size':10,'color':'gray'}
    gl.ylabel_style = {'size':10,'color':'gray'}

   
    ax.set_extent([boxcorners[2], boxcorners[3], boxcorners[0], boxcorners[1]])

    ax.background_patch.set_facecolor('silver')

    plt.pcolormesh(xg, yg, ma.masked_where(np.isnan(data), data),transform=ccrs.PlateCarree(), vmin=vmin, vmax=vmax,cmap=cmap)

    # Colour bar
    axc = fig.add_axes([0.2, 0.1, 0.6, 0.025]) 	
    mpl.rc('font', size=14)
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)

    cb = mpl.colorbar.ColorbarBase(axc, norm=norm, orientation='horizontal',cmap=cmap,extend=extend)
    cb.set_label(colorbar_label,fontsize=14)
    
    
    plt.savefig(fname, bbox_inches='tight', dpi=300)
    plt.clf()
    plt.close()
