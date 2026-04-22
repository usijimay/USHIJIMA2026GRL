import os
import netCDF4

def main(expid, fbase, varname, nd, ybgn, yend, idirbase = '/data38/theme-C/usijimay/TSE-C/AMIP/', odirbase = '/data38/theme-C/usijimay/TSE-C/AMIP/'):
    odir = odirbase + expid  + '/d_analy_a/'+str(ybgn)+'-'+str(yend)+'/'
    if os.path.isdir(odir) == False:
        os.makedirs(odir)    

    ofile = odir+fbase+str(ybgn)+'-'+str(yend)

    if nd == 2:
        lon, lat, var = em2.ReadData2DY(expid, fbase, varname, ybgn, yend, dirbase = idirbase)
        ncw.write_woa1x1_3d(ofile, np.arange(12), lon, lat, np.mean(var, axis=0), varname)       
    elif nd == 3:
        lon, lat, lev, var = em3.ReadData3DY(expid, fbase, varname, ybgn, yend, dirbase = idirbase)            
        ncw.write_woa1x1_4d(ofile, np.arange(12), lev, lon, lat, np.mean(var, axis=0), varname)           
    
def ReadData3DClm(expid, fbase, varname, ybgn, yend, cann = False, dirbase = '/data38/theme-C/usijimay/TSE-C/AMIP/', dirbase0 = '/data38/theme-C/usijimay/TSE-C/AMIP/'):     

    fname = dirbase + expid + '/d_analy_a/'+str(ybgn)+'-'+str(yend)+'/'+fbase+str(ybgn)+'-'+str(yend)
    if os.path.isfile(fname) == False:
        main(expid, fbase, varname, 3, ybgn, yend, idirbase = dirbase0, odirbase = dirbase)

    nc = netCDF4.Dataset(fname, 'r')
    lon = nc.variables['lon'][:]
    lat = nc.variables['lat'][:]
    lev = nc.variables['depth'][:]    
    var = nc.variables[varname][:]    

    return lon, lat, lev, var

def ReadData2DClm(expid, fbase, varname, ybgn, yend, cann = False, dirbase = '/data38/theme-C/usijimay/TSE-C/AMIP/', dirbase0 = '/data38/theme-C/usijimay/TSE-C/AMIP/'):     

    fname = dirbase + expid + '/d_analy_a/'+str(ybgn)+'-'+str(yend)+'/'+fbase+str(ybgn)+'-'+str(yend)
    if os.path.isfile(fname) == False:
        main(expid, fbase, varname, 2, ybgn, yend, idirbase = dirbase0, odirbase = dirbase)

    nc = netCDF4.Dataset(fname, 'r')
    lon = nc.variables['lon'][:]
    lat = nc.variables['lat'][:]
    var = nc.variables[varname][:]    

    return lon, lat, var



if __name__ == '__main__':
    for expid in expids:
        main(expid, fbase, varname, nd, ybgn, yend)    

