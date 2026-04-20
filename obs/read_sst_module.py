import os
import re
import numpy as np
import netCDF4
import calendar
import pandas as pd

def read_input4MIPs(ybgn, yend, filename = '', varname = 'tos', dtype = 'nc', lonname = 'lon', latname = 'lat', cann = False, camip = False, dirbase =  ""):    
    
    if camip:
        if filename == '':
            if varname == 'tos':
                filename = dirbase + '/SST/input4MIPs/model/sst_TL159_CMIP6AMIP_YYYY.dat'
            elif 'ic' in varname:
                filename = dirbase + '/SST/input4MIPs/model/ice_TL159_CMIP6AMIP_YYYY.dat'
        
        RES = 'TL159'
        dlon = 1.125    
        lon = np.arange(0., 360., dlon)
        dblat = os.environ['HOME']+'/anl_esm/anlpy/remap_tools/remap_tools/'
        flat = open(dblat+RES+'_lat.txt', 'r')   
        rls = flat.readlines()            
        flat.close()
        lat = np.array([])
        for rl in rls:
            lat = np.concatenate([lat,np.array(re.split(" +", rl)[1:-1]).astype(np.float)])
        
        im = np.size(lon); jm = np.size(lat)
        for year in range(ybgn, yend+1):
            var0 = np.fromfile(filename.replace('YYYY', str(year)), '>f').reshape(1,12,jm,im)
            if year == ybgn:
                var = var0.copy()
            else:
                var = np.vstack((var, var0))
        var = var[:,:,::-1]

    else:    
        if filename == '':
            filename = dirbase + '/SST/input4MIPs/tos_input4MIPs_SSTsAndSeaIce_CMIP_PCMDI-AMIP-1-1-0_gs1x1_187001-201512.nc'

        lon, lat, var = read_nc(filename, varname = varname, lonname = lonname, latname = latname)
        var = var[12*(ybgn-1870):12*(yend+1-1870)].reshape(-1,12,180,360)

        if cann:
            var = np.average(var, axis=1, weights = calendar.mdays[1:])

    return lon, lat, var


def read_nc(filename, varname = 'tos', lonname = 'lon', latname = 'lat'):
    
    nc = netCDF4.Dataset(filename, 'r')
    # lon = nc.variables['lon'][:]
    # lat = nc.variables['lat'][:]
    
    lon = nc.variables[lonname][:]
    lat = nc.variables[latname][:]    
    var = nc.variables[varname][:]        
    
    return lon, lat, var

