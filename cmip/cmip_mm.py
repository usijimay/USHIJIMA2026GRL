import os
import sys
import calendar
import netCDF4
import numpy as np
from scipy import interpolate
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)
import config.config as cf
import cmip.cmip.cmip_data as cd
import obs.read_sst_module as rs
import io_interface.io_interface.nc_write as ncw


def read_sst_amip(ybgn, yend, cann = True, dirbase = cf.datadir()+'/obs'):
    
    lono, lato, toso = rs.read_input4MIPs(ybgn, yend, cann = cann, dirbase = dirbase)
    tosM = np.mean(toso, axis=0) - 273.15
    
    return lono, lato, tosM


def latupeak(ybgn, yend, models = None, lonmin = 120, lonmax = 240, level = 20000, mode = '', dirbase = cf.datadir()):
    
    models, lonem, latem, levem, uaaMem = read_data3D_MM('ua',       'amip', ybgn, yend, models = models, cann = True)
    models, lonem, latem, levem, uacMem = read_data3D_MM('ua', 'historical', ybgn, yend, models = models, cann = True)    

    lmxaem = {}
    lmxcem = {}    
    for model in models:
        ulta0 = ZonalMean(lonem[model], uaaMem[model], lonmin=lonmin, lonmax=lonmax)
        ultc0 = ZonalMean(lonem[model], uacMem[model], lonmin=lonmin, lonmax=lonmax)
        
        ulta = interpolate.interp1d(levem[model], ulta0, axis=0)(level)
        ultc = interpolate.interp1d(levem[model], ultc0, axis=0)(level)        
        
        lmxaem[model] = u1d2lpeak(ulta, latem[model], latmin = 15, latmax = 65, mode = mode)
        lmxcem[model] = u1d2lpeak(ultc, latem[model], latmin = 15, latmax = 65, mode = mode)

    return models, lmxaem, lmxcem


def latupeaks(ybgn, yend, models = None, lonmin = 120, lonmax = 240, level = 20000, mode = '', dirbase = cf.datadir()):
    
    models, lonem, latem, levem, uaasm = read_data3D('ua',       'amip', ybgn, yend, models = models, cann = True)
    models, lonem, latem, levem, uacsm = read_data3D('ua', 'historical', ybgn, yend, models = models, cann = True)    

    lmxaem = {}
    lmxcem = {}    
    for model in models:
        ulta0 = ZonalMean(lonem[model], uaasm[model], lonmin=lonmin, lonmax=lonmax)
        ultc0 = ZonalMean(lonem[model], uacsm[model], lonmin=lonmin, lonmax=lonmax)
        
        ulta = interpolate.interp1d(levem[model], ulta0, axis=1)(level)
        ultc = interpolate.interp1d(levem[model], ultc0, axis=1)(level)
        
        lmxa = np.zeros(yend-ybgn+1)
        lmxc = np.zeros(yend-ybgn+1)        
        for n in range(yend-ybgn+1):
            lmxa[n] = u1d2lpeak(ulta[n], latem[model], latmin = 15, latmax = 65, mode = mode)
            lmxc[n] = u1d2lpeak(ultc[n], latem[model], latmin = 15, latmax = 65, mode = mode)            
            
        lmxaem[model] = lmxa
        lmxcem[model] = lmxc

    return models, lmxaem, lmxcem


def read_data3D(varname, expid, ybgn, yend, models = None, cann = True):

    if models is None:
        models = read_models()
        
    lonem = {}
    latem = {}
    levem = {}
    varsem = {}
    nmdls = np.size(models)
    for nmdl in range(nmdls):
        model = models[nmdl]
        if varname == 'tos':
            lon, lat, varM = ReadData2dClim(varname, model, expid, ybgn, yend, regrid = True)
            lev = np.array([])
        else:
            lon, lat, lev, varM = ReadData3dClim(varname, model, expid, ybgn, yend, regrid = False)            
        
        lonem[model] = lon
        latem[model] = lat
        levem[model] = lev
        if cann:
            varsem[model] = am(varM, axis=0)
        else:
            varsem[model] = varM             

    return models, lonem, latem, levem, varsem


def read_data3D_MM(varname, expid, ybgn, yend, models = None, cann = True):

    if models is None:
        models = read_models()
        
    lonem = {}
    latem = {}
    levem = {}
    varMem = {}
    nmdls = np.size(models)
    for nmdl in range(nmdls):
        model = models[nmdl]
        if varname == 'tos':
            lon, lat, varM = ReadData2dClim(varname, model, expid, ybgn, yend, regrid = True)
        else:
            lon, lat, lev, varM = ReadData3dClim(varname, model, expid, ybgn, yend, regrid = False)            
        
        lonem[model] = lon
        latem[model] = lat
        levem[model] = lev
        if cann:
            varMem[model] = am(varM)
        else:
            varMem[model] = varM             

    return models, lonem, latem, levem, varMem


def read_datas_MM(ybgn, yend, fnc, models = None, cem = False, dirbase = cf.datadir()):

    if models == None:
        models = read_models()
        
    R0 = 6.375e6
    Rd = 2.87e2
    Cp = 1.004e3
    lev0 = np.array([1.e5, 9.25e4, 8.5e4, 7.e4, 6.e4, 5.e4, 4.e4, 3.e4, 2.5e4, 2.e4, 1.5e4, 1.e4, 7.e3, 5.e3, 3.e3, 2.e3, 1.e3, 5.e2, 1.e2])
    
    lonuem = {}
    latuem = {}
    levuem = {}
    lonvem = {}
    latvem = {}
    levvem = {}
    lonwem = {}
    latwem = {}
    levwem = {}
    lontem = {}
    lattem = {}
    levtem = {}
    tosMem = {}
    uacMem = {}
    vacMem = {}
    wacMem = {}
    zgcMem = {}
    tacMem = {}
    uaaMem = {}
    vaaMem = {}
    waaMem = {}
    taaMem = {}
    zgaMem = {}

    nmdls = np.size(models)
    for nmdl in range(nmdls):
        model = models[nmdl]

        lono, lato, tosM = ReadData2dClim('tos', model, 'historical', ybgn, yend, regrid = True, dirbase = dirbase)

        lonu, latu, levu, uacM = ReadData3dClim('ua', model, 'historical', ybgn, yend, regrid = False, dirbase = dirbase)
        lonu, latu, levu, uaaM = ReadData3dClim('ua', model, 'amip', ybgn, yend, regrid = False, dirbase = dirbase)
        
        lonuem[model] = lonu
        latuem[model] = latu
        levuem[model] = levu
        tosMem[model] = tosM
        uacMem[model] = uacM
        uaaMem[model] = uaaM

        if cem:
            if nmdl == 0:
                tosMM = tosM.copy()/nmdls
                uacMM = intp3D(lonu, latu, levu, uacM, lono, lato, lev0)/nmdls
                uaaMM = intp3D(lonu, latu, levu, uaaM, lono, lato, lev0)/nmdls
            else:
                tosMM = tosMM + tosM.copy()/nmdls
                uacMM = uacMM + intp3D(lonu, latu, levu, uacM, lono, lato, lev0)/nmdls
                uaaMM = uaaMM + intp3D(lonu, latu, levu, uaaM, lono, lato, lev0)/nmdls

    if cem:
        model = 'Multi-Model Mean'
        lonuem[model] = lono
        latuem[model] = lato
        levuem[model] = lev0
        tosMem[model] = tosMM
        uacMem[model] = uacMM
        uaaMem[model] = uaaMM
        models = np.r_[models, [model]]
         
    toscfem = {}
    uaafem = {}
    uacfem = {}
    for model in models:
        toscf0 = fnc(tosMem[model])
        uacf0 = fnc(uacMem[model])
        uaaf0 = fnc(uaaMem[model])
        
        toscfem[model] = toscf0
        uaafem[model] = uaaf0
        uacfem[model] = uacf0

    return models, lonuem, latuem, levuem, toscfem, uacfem, uaafem


def read_datas_MMM(ybgn, yend, fnc, models = None, dirbase = cf.datadir()):

    if models == None:
        models = read_models()

    model = 'EMS'+str(np.size(models))

    lon, lat, tosMM = ReadData2dMMClim('tos', models, 'historical', ybgn, yend, regrid = True, dirbase = dirbase)    
    lev = np.array([1.e5, 9.25e4, 8.5e4, 7.e4, 6.e4, 5.e4, 4.e4, 3.e4, 2.5e4, 2.e4, 1.5e4, 1.e4, 7.e3, 5.e3, 3.e3, 2.e3, 1.e3, 5.e2, 1.e2])

    lonu, latu, levu, uacMM = ReadData3dMMClim('ua', models, 'historical', ybgn, yend, regrid = False, dirbase = dirbase, lon = lon, lat = lat, lev = lev)
    lont, latt, levt, tacMM = ReadData3dMMClim('ta', models, 'historical', ybgn, yend, regrid = False, dirbase = dirbase, lon = lon, lat = lat, lev = lev)
    lont, latt, levt, zgcMM = ReadData3dMMClim('zg', models, 'historical', ybgn, yend, regrid = False, dirbase = dirbase, lon = lon, lat = lat, lev = lev)
    
    lonu, latu, levu, uaaMM = ReadData3dMMClim('ua', models, 'amip', ybgn, yend, regrid = False, dirbase = dirbase, lon = lon, lat = lat, lev = lev)
    lont, latt, levt, taaMM = ReadData3dMMClim('ta', models, 'amip', ybgn, yend, regrid = False, dirbase = dirbase, lon = lon, lat = lat, lev = lev)
    lont, latt, levt, zgaMM = ReadData3dMMClim('zg', models, 'amip', ybgn, yend, regrid = False, dirbase = dirbase, lon = lon, lat = lat, lev = lev)
    
            
    R0 = 6.375e6
    Rd = 2.87e2
    Cp = 1.004e3
            
    uacf0 = fnc(uacMM)
    uaaf0 = fnc(uaaMM)
    tacf0 = ((fnc(tacMM).T * (1.e5/lev)**(Rd/Cp))).T
    taaf0 = ((fnc(taaMM).T * (1.e5/lev)**(Rd/Cp))).T
    zgcf0 = fnc(zgcMM)
    zgaf0 = fnc(zgaMM)        

    dbdycf0 = (9.81/tacf0.T[:,1:-1] * (tacf0.T[:,2:]-tacf0.T[:,:-2])).T/(R0*np.deg2rad(lat[2:]-lat[:-2]))[:,np.newaxis]
    dbdycf0 = np.ma.concatenate([np.nan*np.ones_like(dbdycf0.T[:,:1]), dbdycf0.T, np.nan*np.ones_like(dbdycf0.T[:,-1:])], axis=1).T
    
    dbdyaf0 = (9.81/taaf0.T[:,1:-1] * (taaf0.T[:,2:]-taaf0.T[:,:-2])).T/(R0*np.deg2rad(lat[2:]-lat[:-2]))[:,np.newaxis]
    dbdyaf0 = np.ma.concatenate([np.nan*np.ones_like(dbdyaf0.T[:,:1]), dbdyaf0.T, np.nan*np.ones_like(dbdyaf0.T[:,-1:])], axis=1).T
    
    dbdzcf0 = (9.81/tacf0.T[:,:,1:-1] * (tacf0.T[:,:,2:]-tacf0.T[:,:,:-2])/(zgcf0.T[:,:,2:]-zgcf0.T[:,:,:-2])).T
    dbdzcf0 = np.ma.concatenate([np.nan*np.ones_like(dbdzcf0.T[:,:,:1]), dbdzcf0.T, np.nan*np.ones_like(dbdzcf0.T[:,:,-1:])], axis=2).T
    
    dbdzaf0 = (9.81/taaf0.T[:,:,1:-1] * (taaf0.T[:,:,2:]-taaf0.T[:,:,:-2])/(zgaf0.T[:,:,2:]-zgaf0.T[:,:,:-2])).T
    dbdzaf0 = np.ma.concatenate([np.nan*np.ones_like(dbdzaf0.T[:,:,:1]), dbdzaf0.T, np.nan*np.ones_like(dbdzaf0.T[:,:,-1:])], axis=2).T
    
    egrcf0 = 0.31*np.abs(dbdycf0)/np.sqrt(np.maximum(dbdzcf0, 1.e-12)) * 86400.
    egraf0 = 0.31*np.abs(dbdyaf0)/np.sqrt(np.maximum(dbdzaf0, 1.e-12)) * 86400.

    return lon, lat, lev, uacf0, uaaf0, dbdycf0, dbdyaf0, dbdzcf0, dbdzaf0, egrcf0, egraf0

    
def read_models(dirbase = cf.datadir()):
    
    models = np.array(['ACCESS-CM2', 'ACCESS-ESM1-5', 'BCC-CSM2-MR', 'CAMS-CSM1-0',
                       'CMCC-CM2-HR4', 'CMCC-CM2-SR5', 'CNRM-CM6-1', 'CNRM-CM6-1-HR',
                       'CNRM-ESM2-1', 'CanESM5', 'EC-Earth3', 'EC-Earth3-AerChem',
                       'EC-Earth3-CC', 'EC-Earth3-Veg', 'EC-Earth3-Veg-LR', 'FGOALS-f3-L',
                       'GFDL-CM4', 'GFDL-ESM4', 'GISS-E2-2-G', 'HadGEM3-GC31-LL',
                       'HadGEM3-GC31-MM', 'INM-CM4-8', 'INM-CM5-0', 'IPSL-CM6A-LR',
                       'KACE-1-0-G', 'KIOST-ESM', 'MIROC-ES2L', 'MIROC6',
                       'MPI-ESM-1-2-HAM', 'MPI-ESM1-2-HR', 'MPI-ESM1-2-LR', 'MRI-ESM2-0',
                       'NESM3', 'NorCPM1', 'UKESM1-0-LL'])

    
    return models    
                

def ReadData2dClim(varname, model, expid, ybgn, yend, regrid = False, dirbase = cf.datadir()):    
    
    TID = cd.TableID(varname)
    if regrid:
        if TID[0] == 'A':
            grdname = '250deg-144x73'
        else:
            grdname = '100deg-360x180'
        fnameins = cd.datafile(varname, model, expid, ybgn = ybgn, yend = yend, regrid = regrid, dirbase = dirbase+'/CMIP/regrid/'+grdname+'/')        
        fnamec = fnameins[-1][:-16].replace(dirbase+'/CMIP/regrid/'+grdname+'/', dirbase + '/CMIP/regrid/'+grdname+'_CLIM/CMIP6/')+str(ybgn)+'01-'+str(yend)+'12_clm.nc'        
    else:
        fnameins = cd.datafile(varname, model, expid, ybgn = ybgn, yend = yend, regrid = regrid, dirbase = dirbase+'/CMIP/CMIP6/')        
        fnamec = fnameins[-1][:-16].replace(dirbase+'/CMIP/CMIP6/', dirbase+'/CMIP/CMIP6/CLIM/')+str(ybgn)+'01-'+str(yend)+'12_clm.nc'        

    if os.path.isfile(fnamec):
        nc = netCDF4.Dataset(fnamec, 'r')
        lon = nc.variables['lon'][:]
        lat = nc.variables['lat'][:]
        varM = nc.variables[varname][:]
    else:
        lon, lat, time, var = cd.ReadData2d(fnameins, varname, ybgn, yend)
        im = np.size(lon); jm = np.size(lat)
        var = var.reshape(-1,12,jm,im)
        varM = np.mean(var, axis=0)
        fdir = os.path.dirname(fnamec)
        if os.path.isdir(fdir) == False:
            os.makedirs(fdir)
        ncw.write_woa1x1_3d(fnamec, np.arange(12), lon, lat, varM, varname)      

    return lon, lat, varM


def ReadData3dClim(varname, model, expid, ybgn, yend, regrid = False, dirbase = cf.datadir()):
    
    TID = cd.TableID(varname)
    if regrid:
        if TID[0] == 'A':
            grdname = '250deg-144x73'
        else:
            grdname = '100deg-360x180'
        fnameins = cd.datafile(varname, model, expid, ybgn = ybgn, yend = yend, regrid = regrid, dirbase = dirbase+'/CMIP/regrid/'+grdname+'/')        
        fnamec = fnameins[-1][:-16].replace(dirbase+'/CMIP/regrid/'+grdname+'/', dirbase + '/CMIP/regrid/'+grdname+'_CLIM/CMIP6/')+str(ybgn)+'01-'+str(yend)+'12_clm.nc'                
    else:
        fnameins = cd.datafile(varname, model, expid, ybgn = ybgn, yend = yend, regrid = regrid, dirbase = dirbase+'/CMIP/CMIP6/')        
        fnamec = fnameins[-1][:-16].replace(dirbase+'/CMIP/CMIP6/', dirbase+'/CMIP/CMIP6/CLIM/')+str(ybgn)+'01-'+str(yend)+'12_clm.nc'                
        
    if os.path.isfile(fnamec):
        nc = netCDF4.Dataset(fnamec, 'r')
        lon = nc.variables['lon'][:]
        lat = nc.variables['lat'][:]
        lev = nc.variables['depth'][:]
        varM = nc.variables[varname][:]
    else:
        lon, lat, lev, time, var = cd.ReadData3d(fnameins, varname, ybgn, yend)
        im = np.size(lon); jm = np.size(lat); km = np.size(lev)
        var = var.reshape(-1,12,km,jm,im)
        varM = np.mean(var, axis=0)
        fdir = os.path.dirname(fnamec)
        if os.path.isdir(fdir) == False:
            os.makedirs(fdir)
        ncw.write_woa1x1_4d(fnamec, np.arange(12), lev, lon, lat, varM, varname)
        

    return lon, lat, lev, varM


def ReadData2dMMClim(varname, models, expid, ybgn, yend, regrid = False, dirbase = cf.datadir(), lon = [], lat = []):    

    nms = np.size(models)
    model = 'EMS'+str(nms)
    TID = cd.TableID(varname)
    forcing = 'r1i1p1f1'; grd = 'gr'
    fnamec = dirbase + '/CMIP/CMIP6/CLIM/CMIP/'+expid+'/'+TID+'/'+varname+'/'+model+'/'+forcing+'/gr/v20251226/'+varname+'_'+TID+'_'+model+'_'+expid+'_'+forcing+'_'+grd+'_'+str(ybgn)+'01-'+str(yend)+'12_clm.nc'

    if os.path.isfile(fnamec):
        nc = netCDF4.Dataset(fnamec, 'r')
        lon = nc.variables['lon'][:]
        lat = nc.variables['lat'][:]
        varM = nc.variables[varname][:]
    else:
        for nm, model in enumerate(models):
            lon0, lat0, var0 = ReadData2dClim(varname, model, expid, ybgn, yend, regrid = regrid)            
            if regrid:
                if nm == 0:
                    varM = var0[:]/nms
                else:
                    varM+= var0[:]/nms
            else:
                if nm == 0:                    
                    varM = intp2D(lon0, lat0, var0, lon, lat)/nms
                else:
                    varM+= intp2D(lon0, lat0, var0, lon, lat)/nms

        if regrid:
            lon = lon0[:]; lat = lat0[:]

        fdir = os.path.dirname(fnamec)
        if not os.path.isdir(fdir):
            os.makedirs(fdir)
        ncw.write_woa1x1_3d(fnamec, np.arange(12), lon, lat, varM, varname)      

    return lon, lat, varM


def ReadData3dMMClim(varname, models, expid, ybgn, yend, regrid = False, dirbase = cf.datadir(), lon = [], lat = [], lev = []):    

    nms = np.size(models)
    model = 'EMS'+str(nms)
    TID = cd.TableID(varname)
    forcing = 'r1i1p1f1'; grd = 'gr'
    fnamec = dirbase + '/CMIP/CMIP6/CLIM/CMIP/'+expid+'/'+TID+'/'+varname+'/'+model+'/'+forcing+'/gr/v20251226/'+varname+'_'+TID+'_'+model+'_'+expid+'_'+forcing+'_'+grd+'_'+str(ybgn)+'01-'+str(yend)+'12_clm.nc'

    if os.path.isfile(fnamec):
        nc = netCDF4.Dataset(fnamec, 'r')
        lon = nc.variables['lon'][:]
        lat = nc.variables['lat'][:]
        lev = nc.variables['depth'][:]        
        varM = nc.variables[varname][:]
    else:
        for nm, model in enumerate(models):
            lon0, lat0, lev0, var0 = ReadData3dClim(varname, model, expid, ybgn, yend, regrid = regrid) 
            if regrid:
                if nm == 0:
                    varM = var0[:]/nms
                else:
                    varM+= var0[:]/nms
            else:
                if nm == 0:                    
                    varM = intp3D(lon0, lat0, lev0, var0, lon, lat, lev)/nms
                else:
                    varM+= intp3D(lon0, lat0, lev0, var0, lon, lat, lev)/nms

        if regrid:
            lon = lon0[:]; lat = lat0[:]; lev = lev0

        fdir = os.path.dirname(fnamec)
        if not os.path.isdir(fdir):
            os.makedirs(fdir)
            
        ncw.write_woa1x1_4d(fnamec, np.arange(12), lev, lon, lat, varM, varname)        

    return lon, lat, lev, varM



    

def u1d2lpeak(u1d, lat, latmin = 15, latmax = 65, mode = 'quad'):

    jmin = np.where(lat >= latmin)[0][0]
    jmax = np.where(lat <= latmax)[0][-1]+1    
    jtgt = jmin+np.argmax(u1d[jmin:jmax])     
    if 'quad' in mode:
        dun = u1d[jtgt+1]-u1d[jtgt]
        dus = u1d[jtgt]-u1d[jtgt-1]
        latn = 0.5*(lat[jtgt]+lat[jtgt+1])
        lats = 0.5*(lat[jtgt-1]+lat[jtgt])
        lmax = (dun*lats-dus*latn)/(dun-dus)
    else:
        cef = np.polyfit(lat[jtgt-5:jtgt+6], u1d[jtgt-5:jtgt+6], 2)        
        lmax = - 0.5*cef[1]/cef[0]

    return lmax


def intp3D(lon0, lat0, lev0, var0, lon, lat, lev):
    
    varx = var0.copy()
    if type(var0) is np.ma.MaskedArray:
        msk = 1-var0.mask.astype(float)
        varx = var0.data
        varx[msk==0] = np.nan
    varx = interpolate.interp1d(lon0, varx, kind = 'linear',    axis=-1, fill_value = 'extrapolate')(np.array(lon))
    vary = interpolate.interp1d(lat0, varx, kind = 'linear', axis=-2, fill_value = 'extrapolate')(np.array(lat))
    varz = interpolate.interp1d(lev0, vary, kind = 'linear',    axis=-3, fill_value = 'extrapolate')(np.array(lev))

    var = varz.copy()
    if type(var0) is np.ma.MaskedArray:
        var[np.isnan(varz)] = -9.99e33
        var = np.ma.array(var, mask = np.isnan(varz), fill_value = -9.99e33)

    return var

def intp2D(lat0, lev0, var0, lat, lev):

    vary = var0.copy()
    if type(var0) is np.ma.MaskedArray:    
        msk = 1-var0.mask.astype(float)
        vary = var0.data
        vary[msk==0] = np.nan
    vary = interpolate.interp1d(lat0, vary, kind = 'linear', axis=-1, fill_value = 'extrapolate')(np.array(lat))
    varz = interpolate.interp1d(lev0, vary, kind = 'linear',    axis=-2, fill_value = 'extrapolate')(np.array(lev))

    var = varz.copy()
    if type(var0) is np.ma.MaskedArray:
        var[np.isnan(varz)] = -9.99e33
        var = np.ma.array(var, mask = np.isnan(varz), fill_value = -9.99e33)

    return var


def ZonalMean(lon, var, axis = 0, lonmin = 120, lonmax = 240):

    if lonmax > 360:
        lon = np.r_[lon, lon+360]
        var = np.ma.vstack((var.T, var.T)).T

    imin = np.argmin(np.abs(lon-lonmin)); imax = np.argmin(np.abs(lon-lonmax)) + 1
    vlat = np.mean(var.T[imin:imax], axis=0).T

    return vlat


def am(var, axis=0):

    if np.size(var) == 0:
        varann = var
    else:
        day = np.array(calendar.mdays[1:])        
        varann = np.average(var, weights = day, axis=axis)

    return varann

