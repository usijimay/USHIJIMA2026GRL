import os
import re
import numpy as np
import netCDF4
import calendar
import pandas as pd
# import dirbaseobs as dbo
# BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# import config.config as cf


# def read_sst(ybgn, yend, dataname, dsrv = 'CLIM', res = 'mon1x1', filename = '', varname = '', dtype = 'nc', lonname = 'lon', latname = 'lat', cann = False):
    
#     if ('COBE' in dataname.upper()) * ('SST2' in dataname.upper()):
#         lon, lat, vary = read_COBESST2(ybgn, yend, filename = filename, dsrv = dsrv, varname = varname, dtype = dtype, cann = cann)
#     elif ('ERSST' in dataname.upper()) * ('5' in dataname):
#         if varname == '':
#             varname = 'sst'
#         lon, lat, vary = read_ERSST5(ybgn, yend, filename = filename, varname = varname, dtype = dtype, cann = cann)
#     elif ('HADISST' in dataname.upper()):
#         if varname == '':
#             varname = 'sst'
#         lon, lat, vary = read_HadISST(ybgn, yend, filename = filename, varname = varname, dtype = dtype, cann = cann)
#     elif ('INPUT4MIPS' in dataname.upper()):
#         if varname == '':
#             varname = 'tos'
#         lon, lat, vary = read_input4MIPs(ybgn, yend, filename = filename, varname = varname, dtype = dtype, cann = cann)
#     elif ('HADSST4' in dataname.upper()):
#         if varname == '':
#             varname = 'tos'
#         lon, lat, vary = read_HadSST4(ybgn, yend, filename = filename, varname = varname, dtype = dtype, cann = cann)
#     elif 'ICOADS' in dataname.upper():
#         if varname == '':
#             varname = 'sst'
#         lon, lat, vary = read_ICOADS(ybgn, yend, filename = filename, varname = varname, dtype = dtype, cann = cann)
#     elif ('MGD' in dataname.upper()) * ('SST' in dataname.upper()):
#         lon, lat, vary = read_MGDSST(ybgn, yend, res = res, filename = filename, cann = cann)

#     return lon, lat, vary

        
# def read_sst_clim(ybgn, yend, dataname, dsrv = 'CLIM', res = 'mon1x1', filename = '', varname = '', dtype = 'nc', lonname = 'lon', latname = 'lat', cann = False):
    
#     lon, lat, var = read_sst(ybgn, yend, dataname, dsrv = dsrv, res = res, filename = filename, varname = varname, dtype = dtype, cann = cann)

#     return lon, lat, np.mean(var, axis=0)


# def read_sst_gm(ybgn, yend, dataname = 'COBE-SST2', dsrv = '', res = '', fbase = '', cann = False):
    
#     if fbase == '':
#         if dsrv == 'CLIM':
#             srvname = '_CLIMSRV'
#         elif dsrv == 'JMA':
#             srvname = '_JMANEARGOOS'
#         else:
#             srvname = ''
#         dirbase =  dbo.DirbaseDefault()
#         fbase = dirbase+'/SST/'+dataname+srvname+'/global_mean/sstgm.'


#     for year in range(ybgn, yend+1):
#         var = np.fromfile(fbase+str(year), '<f')
            
#         if year == ybgn:
#             vary = var[np.newaxis]
#         else:
#             vary = np.vstack((vary, var[np.newaxis]))

#     if cann:
#         vary = np.average(vary, axis=1, weights = calendar.mdays[1:])

#     return vary


# # def read_COBESST2(ybgn, yend, filename = '/nas/personal/usijimay/obs/SST/COBESST2_CLIMSRV/netCDF/cobe-sst2.YYYY.nc', varname = 'WTMP_surface', dtype = 'nc'):
# def read_COBESST2(ybgn, yend, dsrv = 'CLIM', filename = '', varname = '', dtype = 'nc', lonname = 'lon', latname = 'lat', cann = False):
    
#     if filename == '':
#         dirbase =  dbo.DirbaseDefault()
#         if varname == '':
#             varname = 'tos'
#         lonname = 'lon'
#         latname = 'lat'

#         if dsrv == 'CLIM':
#             if (varname == '')*(dtype == 'nc_old'):
#                 filename = dirbase + '/SST/COBESST2_CLIMSRV/netCDF_old/cobe-sst2.YYYY.nc'
#                 if varname == '':
#                     varname = 'WTMP_surface'
#                 lonname = 'longitude'
#                 latname = 'latitude'
#             else:
#                 filename = dirbase + '/SST/COBESST2_CLIMSRV/netCDF/cobe-sst2.YYYY.nc'
#         elif dsrv == 'JMA':
#             filename = dirbase + '/SST/COBESST2_JMANEARGOOS/netCDF/cobe-sst2.YYYY.nc'   

#     for year in range(ybgn, yend+1):
#         if dtype == 'nc':
#             lon, lat, var = read_nc(filename.replace('YYYY', str(year)), varname = varname, lonname = lonname, latname = latname)

#         if cann:
#             var = np.average(var, axis=0, weights = calendar.mdays[1:])
#         if year == ybgn:
#             vary = var[np.newaxis]
#         else:
#             vary = np.ma.vstack((vary, var[np.newaxis]))

#     return lon, lat, vary


# # def read_COBESST2_clim(ybgn, yend, filename = '/nas/personal/usijimay/obs/SST/COBESST2_CLIMSRV/netCDF/cobe-sst2.YYYY.nc', varname = 'WTMP_surface', dtype = 'nc'):
# def read_COBESST2_clim(ybgn, yend, dsrv = 'CLIM', filename = '', varname = '', dtype = 'nc', cann = False):
    
#     lon, lat, vary = read_COBESST2(ybgn, yend, filename = filename, varname = varname, dtype = dtype, cann = cann)

#     return lon, lat, np.mean(vary, axis=0)

# # def read_COBESST2_GM(ybgn, yend, fbase = '/nas/personal/usijimay/obs/SST/COBESST2_CLIMSRV/global_mean/cobe-sst2.'):
# def read_COBESST2_GM(ybgn, yend, fbase = '', cann = False):

#     if fbase == '':
#         dirbase =  dbo.DirbaseDefault()
#         fbase = dirbase + '/SST/COBESST2_CLIMSRV/global_mean/cobe-glb.'

#     for year in range(ybgn, yend+1):
#         # if os.path.isdir(fbase+str(year)) == False:
#         #     sys.exit(make global mean data)

#         var = np.fromfile(fbase+str(year), '<f')
#         if cann:
#             var = np.average(var, axis=0, weights = calendar.mdays[1:])
            
#         if year == ybgn:
#             vary = var[np.newaxis]
#         else:
#             vary = np.vstack((vary, var[np.newaxis]))

#     return vary

# # def read_COBESST2_clim_GM(ybgn, yend, fbase = '/nas/personal/usijimay/obs/SST/COBESST2_CLIMSRV/netCDF/cobe-sst2.'):
# def read_COBESST2_clim_GM(ybgn, yend, fbase = '', cann = False):
    
#     vary = read_COBESST2_GM(ybgn, yend, fbase = fbase, cann = cann)

#     return np.mean(vary, axis=0)

# def read_ERSST5(ybgn, yend, filename = '', varname = 'sst', dtype = 'nc', lonname = 'lon', latname = 'lat', cann = False):
    
#     if filename == '':
#         dirbase =  dbo.DirbaseDefault()
#         filename = dirbase + '/SST/ERSSTv5/sst.mnmean.nc'

#     lon, lat, var = read_nc(filename, varname = varname, lonname = lonname, latname = latname)
#     var = var[12*(ybgn-1854):12*(yend+1-1854)].reshape(-1,12,89,180)

#     if cann:
#         var = np.average(var, axis=1, weights = calendar.mdays[1:])

#     return lon, lat, var

# def read_input4MIPs(ybgn, yend, filename = '', varname = 'tos', dtype = 'nc', lonname = 'lon', latname = 'lat', cann = False, camip = False, dirbase =  dbo.DirbaseDefault()):
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


# def read_HadISST(ybgn, yend, filename = '', varname = 'sst', dtype = 'nc', lonname = 'longitude', latname = 'latitude', cann = False):
    
#     if filename == '':
#         dirbase =  dbo.DirbaseDefault()
#         filename = dirbase + '/SST/HadISST1/HadISST_sst.nc'

#     lon, lat, var = read_nc(filename, varname = varname, lonname = lonname, latname = latname)
#     var = var[12*(ybgn-1870):12*(yend+1-1870)].reshape(-1,12,180,360)

#     if cann:
#         var = np.average(var, axis=1, weights = calendar.mdays[1:])

#     return lon, lat, var

# def read_HadSST4(ybgn, yend, filename = '', varname = 'tos', dtype = 'nc', lonname = 'longitude', latname = 'latitude', cann = False):
    
#     if filename == '':
#         dirbase =  dbo.DirbaseDefault()
#         filename = dirbase + '/SST/HadSST4/HadSST.4.0.1.0_median.nc'

#     lon, lat, var = read_nc(filename, varname = varname, lonname = lonname, latname = latname)
#     var = var[12*(ybgn-1850):12*(yend+1-1850)].reshape(-1,12,36,72)

#     if cann:
#         var = np.average(var, axis=1, weights = calendar.mdays[1:])

#     return lon, lat, var


# def read_ICOADS(ybgn, yend, filename = '', varname = 'sst', dtype = 'nc', lonname = 'lon', latname = 'lat', cann = False):
    
#     if filename == '':
#         dirbase =  dbo.DirbaseDefault()
#         filename = dirbase + '/SST/ICOADS/sst.mean.nc'

#     lon, lat, var = read_nc(filename, varname = varname, lonname = lonname, latname = latname)
#     var = var[12*(ybgn-1800):12*(yend+1-1800)].reshape(-1,12,90,180)

#     if cann:
#         var = np.average(var, axis=1, weights = calendar.mdays[1:])

#     return lon, lat, var


# def read_MGDSST(ybgn, yend, res = 'mon1x1', filename = '', varname = '', dtype = 'grads', lonname = 'lon', latname = 'lat', cann = False):
    
#     if filename == '':
#         dirbase =  dbo.DirbaseDefault()
#         if res == 'mon1x1':
#             filename = dirbase + '/SST/MGD-SST/grads_1x1_monthly/mgd-sst.'
#             lon = np.arange(0.5, 360.5)
#             lat = np.arange(-89.5, 90.5)

#     for year in range(ybgn, yend+1):
#         for mon in range(1,13):
#             var0 = np.fromfile(filename+str(year)+str(mon).zfill(2), '>f').reshape(180,360)
#             if mon == 1:
#                 var = var0[np.newaxis]
#             else:
#                 var = np.vstack((var, var0[np.newaxis]))

#         if cann:
#             var = np.average(var, axis=0, weights = calendar.mdays[1:])
#         if year == ybgn:
#             vary = var[np.newaxis]
#         else:
#             vary = np.vstack((vary, var[np.newaxis]))

#     vary = np.ma.masked_array(vary, mask = (vary > 1.e2))

#     return lon, lat, vary

# def read_HadSST4_GM_csv(ybgn, yend, filename = '', varname = 'anomaly', cann = False):

#     if filename == '':
#         dirbase =  dbo.DirbaseDefault()
#         if cann:
#             filename = dirbase + '/SST/HadSST4/HadSST.4.0.1.0_annual_GLOBE.csv'
#         else:
#             filename = dirbase + '/SST/HadSST4/HadSST.4.0.1.0_monthly_GLOBE.csv'

#     df = pd.read_csv(filename)
#     vary = np.array(df[varname])[ybgn-1850:yend+1-ybgn]

#     return vary


def read_nc(filename, varname = 'tos', lonname = 'lon', latname = 'lat'):
    
    nc = netCDF4.Dataset(filename, 'r')
    # lon = nc.variables['lon'][:]
    # lat = nc.variables['lat'][:]
    
    lon = nc.variables[lonname][:]
    lat = nc.variables[latname][:]    
    var = nc.variables[varname][:]        
    
    return lon, lat, var


# def read_mgd_jpn(fname, fdir = dbo.DirbaseDefault()+"/SST/MGD-SST/near-goos/netCDF4/"):
#     nc = netCDF4.Dataset(fdir+fname, 'r')
#     lon = nc.variables['lon'][:]
#     lat = nc.variables['lat'][:]
#     sst = nc.variables['tos'][:]
    
#     return lon, lat, sst

# # def DirbaseDefault():
# #     import os
# #     import sys
# #     sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../machine")
# #     import varsrv    

# #     dirbase = varsrv.datadirname()

# #     return dirbase

