import sys
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
import matplotlib.path as mpath
import cmocean.cm as cmo    
    
def ax_setgrd(ax, projection_type='PlateCarree', xlim = [0., 359.9], ylim = [-90., 90.], lon_interval = 60, lat_interval = 30, lw_ax = 1.):

    gl = ax.gridlines(crs=ccrs.PlateCarree(), linewidth = lw_ax, color = 'k')

    if (xlim[0]<1.)*(xlim[1]>359.):
        gl.xlocator = mticker.FixedLocator(np.arange(-360,360.1,lon_interval))
    else:
        xticks = np.arange(xlim[0], xlim[1], lon_interval)
        xticks[xticks>180] = xticks[xticks>180]-360.                              
        gl.xlocator = mticker.FixedLocator(xticks)
        
    yticks = np.arange(ylim[0], ylim[1]+0.1, lat_interval)
    gl.ylocator = mticker.FixedLocator(yticks)

    ax.set_extent([xlim[0], xlim[1], ylim[0], ylim[1]], crs = ccrs.PlateCarree())
    ax = ctp_set_boundary_ax(ax, projection_type)

    return ax

def imcf(ax, lon, lat, var, level = [0], vr=[-999,-999,21], rt = 10, extend = 'both', cmap = 'jet', ERR = -9.99e33, vticklabel = ['']):

    data_crs = ccrs.PlateCarree()
    if np.size(level) == 1:
        vtick = np.linspace(vr[0],vr[1],round(vr[2])) 
        image = ax.contourf(lon, lat, var, np.linspace(vr[0], vr[1], (round(vr[2])-1)*rt+1), extend = extend, cmap = cmap, transform = data_crs)
        vticklabel = ['']
    else:
        vartmp = np.zeros_like(var)
        nls = np.size(level)
        levtmp = np.arange(nls)
        vartmp[var<level[0]] = -0.5
        for nl in range(nls-1):
            vartmp[(level[nl]<=var)*(var<level[nl+1])] = nl+0.5
        vartmp[level[-1]<var] = nls - 0.5
        if 'MaskedArray' in str(type(var)):            
            vartmp[var.mask] = np.nan

        vtick = levtmp
        if np.size(vticklabel) == 1:
            vticklabel = level
        
        image = ax.contourf(lon, lat, vartmp, levtmp, extend = extend, cmap = cmap, transform = data_crs)

    return ax, image, vtick, vticklabel
        
def imc(ax, lon, lat, var, levels = [0.,], lfmt = '%1.1f', lfontsize = 11, lwidth = 1.0, cntcol = 'k'):

    data_crs = ccrs.PlateCarree()
    ll = ax.contour(lon, lat, var, levels = levels, colors = cntcol, transform = data_crs, linewidths = lwidth)
    ll.clabel(fmt=lfmt, fontsize=lfontsize)

    return ax, ll


def ctp_set_boundary_ax(ax, projection_type):
    if (projection_type == 'Orthographic') or \
       (projection_type == 'NorthPolarStereo') or \
       projection_type == 'SouthPolarStereo' :
        
        theta = np.linspace(0, 2*np.pi, 100)
        center, radius = [0.5, 0.5], 0.5
        verts = np.vstack([np.sin(theta), np.cos(theta)]).T
        circle = mpath.Path(verts * radius + center)        

        ax.set_boundary(circle, transform=ax.transAxes)

    return ax


