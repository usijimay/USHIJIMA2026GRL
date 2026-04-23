import os
import numpy as np
import sys
import pygrib
import netCDF4
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)
import config.config as cf
import io_interface.io_interface.nc_write as ncw


def read_JRA55_UP(ybgn, yend, km = 37, kr = [], level = [], fbase = cf.datadir()+'/obs/WindProfile/JRA55/Monthly/anl_p125_ugrd.'):
    
    lon = np.arange(0,360,1.25)
    lat = np.arange(-90,91.25,1.25)
    if np.size(kr) == 0:
        kr = np.arange(km).astype(int)
    if np.size(level) == 0:
        level = JRAL(km)[kr]
    else:
        kr = np.where(np.isin(JRAL(km),level))[0]
    
    kr = km-kr    

    for year in range(ybgn, yend+1):
        for mon in range(1,13):
            grbf = pygrib.open(fbase+str(year)+str(mon).zfill(2))            
            for k in kr:
                var0 = grbf.message(k).data()[0][::-1]
                if k == kr[0]:
                    vark = var0[np.newaxis]
                else:
                    vark = np.ma.vstack((vark, var0[np.newaxis]))
            if mon == 1:
                varm = vark[np.newaxis]
            else:
                varm = np.ma.vstack((varm, vark[np.newaxis]))
        if year == ybgn:
            var = varm[np.newaxis]
        else:
            var = np.ma.vstack((var, varm[np.newaxis]))
            
    if np.size(kr) == 1:        
        return lon, lat, var[:,:,0]
    else:
        return lon, lat, level, var


def read_JRA55_UP_CLM(ybgn, yend, km = 37, kr = [], level = [], fbase = cf.datadir()+'/obs/WindProfile/JRA55/MONCLM/anl_p125_ugrd.'):

    fnamec = fbase+str(ybgn)+str(yend)
    varname = 'ua'
    if os.path.isfile(fnamec):
        nc = netCDF4.Dataset(fnamec, 'r')
        lon  = nc.variables['lon'][:]
        lat  = nc.variables['lat'][:]
        lev  = nc.variables['depth'][:]
        varM = nc.variables[varname][:]
    else:
        if np.size(kr) == 1:
            lon, lat, var = read_JRA55_UP(ybgn, yend, km = km, kr = kr, level = level, fbase = fbase.replace('MONCLM', 'Monthly'))
        else:
            lon, lat, lev, var = read_JRA55_UP(ybgn, yend, km = km, kr = kr, level = level, fbase = fbase.replace('MONCLM', 'Monthly'))
        varM = np.mean(var, axis=0)
        fdir = os.path.dirname(fnamec)
        if os.path.isdir(fdir) == False:
            os.makedirs(fdir)

        if np.size(kr) == 1:
            ncw.write_woa1x1_3d(fnamec, np.arange(12), lon, lat, varM, varname)
        else:
            ncw.write_woa1x1_4d(fnamec, np.arange(12), lev, lon, lat, varM, varname)            
            
    if np.size(kr) == 1:        
        return lon, lat, varM
    else:
        return lon, lat, lev, varM

    
def JRAL(nlev):
    if nlev == 37:
        level = np.array([1000, 975, 950, 925, 900, 875, 850, 825, 800, 775, 750, 700, 650, 600, 550, 500, 450, 400, 350, 300, 250, 225, 200, 175, 150, 125, 100, 70, 50, 30, 20, 10, 7, 5, 3, 2, 1])

        
    return level

        
