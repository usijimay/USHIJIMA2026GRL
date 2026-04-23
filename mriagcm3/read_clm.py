import os
import sys
import netCDF4
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)
import config.config as cf    
    
def ReadData3DClm(expid, fbase, varname, ybgn, yend, cann = False, dirbase = cf.datadir()+'/TSE-C/AMIP/', dirbase0 = cf.datadir()+'/TSE-C/AMIP/'):     

    fname = dirbase + expid + '/d_analy_a/'+str(ybgn)+'-'+str(yend)+'/'+fbase+str(ybgn)+'-'+str(yend)

    nc = netCDF4.Dataset(fname, 'r')
    lon = nc.variables['lon'][:]
    lat = nc.variables['lat'][:]
    lev = nc.variables['depth'][:]    
    var = nc.variables[varname][:]    

    return lon, lat, lev, var

def ReadData2DClm(expid, fbase, varname, ybgn, yend, cann = False, dirbase = cf.datadir()+'/TSE-C/AMIP/', dirbase0 = cf.datadir()+'/TSE-C/AMIP/'):     

    fname = dirbase + expid + '/d_analy_a/'+str(ybgn)+'-'+str(yend)+'/'+fbase+str(ybgn)+'-'+str(yend)

    nc = netCDF4.Dataset(fname, 'r')
    lon = nc.variables['lon'][:]
    lat = nc.variables['lat'][:]
    var = nc.variables[varname][:]    

    return lon, lat, var

