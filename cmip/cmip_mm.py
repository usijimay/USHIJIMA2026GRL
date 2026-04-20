import os
import sys
import calendar
import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import cmocean.cm as cmo
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../cmip")
import cmip.cmip_data as cd
from scipy import interpolate
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../io_interface")
import io_interface.nc_write as ncw
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../obs")
import read_sst_module as rs


def read_sst_amip(ybgn, yend, cann = True, dirbase = '/data16/theme-C/usijimay/obs'):
    
    lono, lato, toso = rs.read_input4MIPs(ybgn, yend, cann = cann, dirbase = dirbase)
    tosM = np.mean(toso, axis=0) - 273.15
    
    return lono, lato, tosM


def latupeak(ybgn, yend, models = None, lonmin = 120, lonmax = 240, level = 20000, mode = '', dirbase = '/data16/theme-C/usijimay'):
    
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


def latupeaks(ybgn, yend, models = None, lonmin = 120, lonmax = 240, level = 20000, mode = '', dirbase = '/data16/theme-C/usijimay'):
    
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
        print(model)
        if varname == 'tos':
            lon, lat, varM = ReadData2d(varname, model, expid, ybgn, yend, regrid = True)
        else:
            lon, lat, lev, varM = ReadData3d(varname, model, expid, ybgn, yend, regrid = False)            
        
        lonem[model] = lon
        latem[model] = lat
        levem[model] = lev
        if cann:
            varsem[model] = am(varM, axis=1)
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
        print(model)
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


def read_datas_MM(ybgn, yend, fnc, ns, models = None, cem = False, dirbase = '/data16/theme-C/usijimay'):

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
        print(model)

        lono, lato, tosM = ReadData2dClim('tos', model, 'historical', ybgn, yend, regrid = True, dirbase = dirbase)

        lonu, latu, levu, uacM = ReadData3dClim('ua', model, 'historical', ybgn, yend, regrid = False, dirbase = dirbase)
        lonv, latv, levv, vacM = ReadData3dClim('va', model, 'historical', ybgn, yend, regrid = False, dirbase = dirbase)
        lonw, latw, levw, wacM = ReadData3dClim('wap', model, 'historical', ybgn, yend, regrid = False, dirbase = dirbase)
        lont, latt, levt, tacM = ReadData3dClim('ta', model, 'historical', ybgn, yend, regrid = False, dirbase = dirbase)
        lont, latt, levt, zgcM = ReadData3dClim('zg', model, 'historical', ybgn, yend, regrid = False, dirbase = dirbase)

        lonu, latu, levu, uaaM = ReadData3dClim('ua', model, 'amip', ybgn, yend, regrid = False, dirbase = dirbase)
        lonv, latv, levv, vaaM = ReadData3dClim('va', model, 'amip', ybgn, yend, regrid = False, dirbase = dirbase)
        lonw, latw, levw, waaM = ReadData3dClim('wap', model, 'amip', ybgn, yend, regrid = False, dirbase = dirbase)
        lont, latt, levt, taaM = ReadData3dClim('ta', model, 'amip', ybgn, yend, regrid = False, dirbase = dirbase)
        lont, latt, levt, zgaM = ReadData3dClim('zg', model, 'amip', ybgn, yend, regrid = False, dirbase = dirbase)
        
        lonuem[model] = lonu
        latuem[model] = latu
        levuem[model] = levu
        lonvem[model] = lonv
        latvem[model] = latv
        levvem[model] = levv
        lonwem[model] = lonw
        latwem[model] = latw
        levwem[model] = levw
        lontem[model] = lont
        lattem[model] = latt
        levtem[model] = levt
        tosMem[model] = tosM
        uacMem[model] = uacM
        vacMem[model] = vacM
        wacMem[model] = wacM
        tacMem[model] = tacM
        zgcMem[model] = zgcM
        uaaMem[model] = uaaM
        vaaMem[model] = vaaM
        waaMem[model] = waaM
        taaMem[model] = taaM
        zgaMem[model] = zgaM

        if cem:
            if nmdl == 0:
                tosMM = tosM.copy()/nmdls
                uacMM = intp3D(lonu, latu, levu, uacM, lono, lato, lev0)/nmdls
                vacMM = intp3D(lonv, latv, levv, vacM, lono, lato, lev0)/nmdls
                wacMM = intp3D(lonw, latw, levw, wacM, lono, lato, lev0)/nmdls
                tacMM = intp3D(lont, latt, levt, tacM, lono, lato, lev0)/nmdls
                zgcMM = intp3D(lont, latt, levt, zgcM, lono, lato, lev0)/nmdls
                uaaMM = intp3D(lonu, latu, levu, uaaM, lono, lato, lev0)/nmdls
                vaaMM = intp3D(lonv, latv, levv, vaaM, lono, lato, lev0)/nmdls
                waaMM = intp3D(lonw, latw, levw, waaM, lono, lato, lev0)/nmdls
                taaMM = intp3D(lont, latt, levt, taaM, lono, lato, lev0)/nmdls
                zgaMM = intp3D(lont, latt, levt, zgaM, lono, lato, lev0)/nmdls
            else:
                tosMM = tosMM + tosM.copy()/nmdls
                uacMM = uacMM + intp3D(lonu, latu, levu, uacM, lono, lato, lev0)/nmdls
                vacMM = vacMM + intp3D(lonu, latv, levv, vacM, lono, lato, lev0)/nmdls
                wacMM = wacMM + intp3D(lonw, latw, levw, wacM, lono, lato, lev0)/nmdls
                tacMM = tacMM + intp3D(lont, latt, levt, tacM, lono, lato, lev0)/nmdls
                zgcMM = zgcMM + intp3D(lont, latt, levt, zgcM, lono, lato, lev0)/nmdls
                uaaMM = uaaMM + intp3D(lonu, latu, levu, uaaM, lono, lato, lev0)/nmdls
                vaaMM = vaaMM + intp3D(lonv, latv, levv, vaaM, lono, lato, lev0)/nmdls
                waaMM = waaMM + intp3D(lonw, latw, levw, waaM, lono, lato, lev0)/nmdls
                taaMM = taaMM + intp3D(lont, latt, levt, taaM, lono, lato, lev0)/nmdls
                zgaMM = zgaMM + intp3D(lont, latt, levt, zgaM, lono, lato, lev0)/nmdls

    if cem:
        model = 'Multi-Model Mean'
        lonuem[model] = lono
        latuem[model] = lato
        levuem[model] = lev0
        lonvem[model] = lono
        latvem[model] = lato
        levvem[model] = lev0
        lonwem[model] = lono
        latwem[model] = lato
        levwem[model] = lev0
        lontem[model] = lono
        lattem[model] = lato
        levtem[model] = lev0
        tosMem[model] = tosMM
        uacMem[model] = uacMM
        vacMem[model] = vacMM
        wacMem[model] = wacMM
        tacMem[model] = tacMM
        zgcMem[model] = zgcMM
        uaaMem[model] = uaaMM
        vaaMem[model] = vaaMM
        waaMem[model] = waaMM
        taaMem[model] = taaMM
        zgaMem[model] = zgaMM            
        models = np.r_[models, [model]]
        
 
    toscfem = {}
    uaafem = {}
    vaafem = {}
    waafem = {}
    taafem = {}
    zgafem = {}
    dbdyafem = {}
    dbdzafem = {}
    egrafem = {}  
    uacfem = {}
    vacfem = {}
    wacfem = {}
    tacfem = {}
    zgcfem = {}
    dbdycfem = {}
    dbdzcfem = {}
    egrcfem  = {}          
    for model in models:
        toscf0 = fnc(tosMem[model], ns)
        uacf0 = fnc(uacMem[model], ns)
        uaaf0 = fnc(uaaMem[model], ns)
        vacf0 = fnc(vacMem[model], ns)
        vaaf0 = fnc(vaaMem[model], ns)
        wacf0 = fnc(wacMem[model], ns)
        waaf0 = fnc(waaMem[model], ns)
        tacf0 = ((fnc(tacMem[model], ns).T * (1.e5/levtem[model])**(Rd/Cp))).T
        taaf0 = ((fnc(taaMem[model], ns).T * (1.e5/levtem[model])**(Rd/Cp))).T
        zgcf0 = fnc(zgcMem[model], ns)
        zgaf0 = fnc(zgaMem[model], ns)        
            
        if latuem[model][0] != latvem[model][0]:
            vacf0 = interpolate.interp1d(latvem[model], vacf0, kind = 'linear', axis=-2, fill_value = 'extrapolate')(np.array(latuem[model]))
            vaaf0 = interpolate.interp1d(latvem[model], vaaf0, kind = 'linear', axis=-2, fill_value = 'extrapolate')(np.array(latuem[model]))
        if latuem[model][0] != latwem[model][0]:
            wacf0 = interpolate.interp1d(latwem[model], wacf0, kind = 'linear', axis=-2, fill_value = 'extrapolate')(np.array(latuem[model]))
            waaf0 = interpolate.interp1d(latwem[model], waaf0, kind = 'linear', axis=-2, fill_value = 'extrapolate')(np.array(latuem[model]))
                
        dbdycf0 = (9.81/tacf0.T[:,1:-1] * (tacf0.T[:,2:]-tacf0.T[:,:-2])).T/(R0*np.deg2rad(lattem[model][2:]-lattem[model][:-2]))[:,np.newaxis]
        dbdycf0 = np.ma.concatenate([np.nan*np.ones_like(dbdycf0.T[:,:1]), dbdycf0.T, np.nan*np.ones_like(dbdycf0.T[:,-1:])], axis=1).T
            
        dbdyaf0 = (9.81/taaf0.T[:,1:-1] * (taaf0.T[:,2:]-taaf0.T[:,:-2])).T/(R0*np.deg2rad(lattem[model][2:]-lattem[model][:-2]))[:,np.newaxis]
        dbdyaf0 = np.ma.concatenate([np.nan*np.ones_like(dbdyaf0.T[:,:1]), dbdyaf0.T, np.nan*np.ones_like(dbdyaf0.T[:,-1:])], axis=1).T
                
        dbdzcf0 = (9.81/tacf0.T[:,:,1:-1] * (tacf0.T[:,:,2:]-tacf0.T[:,:,:-2])/(zgcf0.T[:,:,2:]-zgcf0.T[:,:,:-2])).T
        dbdzcf0 = np.ma.concatenate([np.nan*np.ones_like(dbdzcf0.T[:,:,:1]), dbdzcf0.T, np.nan*np.ones_like(dbdzcf0.T[:,:,-1:])], axis=2).T
            
        dbdzaf0 = (9.81/taaf0.T[:,:,1:-1] * (taaf0.T[:,:,2:]-taaf0.T[:,:,:-2])/(zgaf0.T[:,:,2:]-zgaf0.T[:,:,:-2])).T
        dbdzaf0 = np.ma.concatenate([np.nan*np.ones_like(dbdzaf0.T[:,:,:1]), dbdzaf0.T, np.nan*np.ones_like(dbdzaf0.T[:,:,-1:])], axis=2).T                
            
        egrcf0 = 0.31*np.abs(dbdycf0)/np.sqrt(np.maximum(dbdzcf0, 1.e-12)) * 86400.
        egraf0 = 0.31*np.abs(dbdyaf0)/np.sqrt(np.maximum(dbdzaf0, 1.e-12)) * 86400.
        
        toscfem[model] = toscf0
        uaafem[model] = uaaf0
        vaafem[model] = vaaf0
        waafem[model] = waaf0
        taafem[model] = taaf0
        zgafem[model] = zgaf0
        dbdyafem[model] = dbdyaf0
        dbdzafem[model] = dbdzaf0
        egrafem[model] = egraf0
        
        uacfem[model] = uacf0
        vacfem[model] = vacf0
        wacfem[model] = wacf0
        tacfem[model] = tacf0
        zgcfem[model] = zgcf0
        dbdycfem[model] = dbdycf0
        dbdzcfem[model] = dbdzcf0
        egrcfem[model] = egrcf0
            

    return models, lonuem, latuem, levuem, lonvem, latvem, levvem, lonwem, latwem, levwem, lontem, lattem, levtem, toscfem, uacfem, uaafem, vacfem, vaafem, wacfem, waafem, tacfem, taafem, zgcfem, zgafem, dbdycfem, dbdyafem, dbdzcfem, dbdzafem, egrcfem, egrafem



def read_datas_MMM(ybgn, yend, fnc, ns, models = None, cintm = False, dirbase = '/data16/theme-C/usijimay'):

    if models == None:
        models = read_models()

    model = 'EMS'+str(np.size(models))


    lon, lat, tosMM = ReadData2dMMClim('tos', models, 'historical', ybgn, yend, regrid = True, dirbase = dirbase)    
    if cintm:
        lono, lato, toso = rs.read_sst(ybgn, yend, dataname = 'input4MIPs', cann = False)        
    lev = np.array([1.e5, 9.25e4, 8.5e4, 7.e4, 6.e4, 5.e4, 4.e4, 3.e4, 2.5e4, 2.e4, 1.5e4, 1.e4, 7.e3, 5.e3, 3.e3, 2.e3, 1.e3, 5.e2, 1.e2])

    lonu, latu, levu, uacMM = ReadData3dMMClim('ua', models, 'historical', ybgn, yend, regrid = False, dirbase = dirbase, lon = lon, lat = lat, lev = lev)
    if cintm:        
        lonv, latv, levv, vacMM = ReadData3dMMClim('va', models, 'historical', ybgn, yend, regrid = False, dirbase = dirbase, lon = lon, lat = lat, lev = lev)
        lonw, latw, levw, wacMM = ReadData3dMMClim('wap', models, 'historical', ybgn, yend, regrid = False, dirbase = dirbase, lon = lon, lat = lat, lev = lev)
    lont, latt, levt, tacMM = ReadData3dMMClim('ta', models, 'historical', ybgn, yend, regrid = False, dirbase = dirbase, lon = lon, lat = lat, lev = lev)
    lont, latt, levt, zgcMM = ReadData3dMMClim('zg', models, 'historical', ybgn, yend, regrid = False, dirbase = dirbase, lon = lon, lat = lat, lev = lev)
    
    lonu, latu, levu, uaaMM = ReadData3dMMClim('ua', models, 'amip', ybgn, yend, regrid = False, dirbase = dirbase, lon = lon, lat = lat, lev = lev)
    if cintm:        
        lonv, latv, levv, vaaMM = ReadData3dMMClim('va', models, 'amip', ybgn, yend, regrid = False, dirbase = dirbase, lon = lon, lat = lat, lev = lev)
        lonw, latw, levw, waaMM = ReadData3dMMClim('wap', models, 'amip', ybgn, yend, regrid = False, dirbase = dirbase, lon = lon, lat = lat, lev = lev)
    lont, latt, levt, taaMM = ReadData3dMMClim('ta', models, 'amip', ybgn, yend, regrid = False, dirbase = dirbase, lon = lon, lat = lat, lev = lev)
    lont, latt, levt, zgaMM = ReadData3dMMClim('zg', models, 'amip', ybgn, yend, regrid = False, dirbase = dirbase, lon = lon, lat = lat, lev = lev)
    
            
    R0 = 6.375e6
    Rd = 2.87e2
    Cp = 1.004e3
            
    if cintm:            
        toscf0 = fnc(tosMM, ns)
        tosaf0 = fnc(toso, ns)
    uacf0 = fnc(uacMM, ns)
    uaaf0 = fnc(uaaMM, ns)
    if cintm:    
        vacf0 = fnc(vacMM, ns)
        vaaf0 = fnc(vaaMM, ns)
        wacf0 = fnc(wacMM, ns)
        waaf0 = fnc(waaMM, ns)
    tacf0 = ((fnc(tacMM, ns).T * (1.e5/lev)**(Rd/Cp))).T
    taaf0 = ((fnc(taaMM, ns).T * (1.e5/lev)**(Rd/Cp))).T
    zgcf0 = fnc(zgcMM, ns)
    zgaf0 = fnc(zgaMM, ns)        

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

    if cintm:
        return lon, lat, lev, toscf0, tosaf0, uacf0, uaaf0, vacf0, vaaf0, wacf0, waaf0, tacf0, taaf0, zgcf0, zgaf0, dbdycf0, dbdyaf0, dbdzcf0, dbdzaf0, egrcf0, egraf0
    else:
        return lon, lat, lev, uacf0, uaaf0, dbdycf0, dbdyaf0, dbdzcf0, dbdzaf0, egrcf0, egraf0

def read_models():
    
    ampmdl = os.listdir('/Public/CMIPs/CMIP6/CMIP/amip/Amon/uas/')
    cmpmdla = os.listdir('/Public/CMIPs/CMIP6/CMIP/historical/Amon/uas/')
    cmpmdlo = os.listdir('/Public/CMIPs/regrid/CMIP6/100deg-360x180/CMIP/historical/Omon/tos/')    

    models = np.intersect1d(np.intersect1d(ampmdl, cmpmdla), cmpmdlo)
    models = models['CAS-ESM2-0' != models]
    models = models['ICON-ESM-LR' != models]
    models = models['IITM-ESM' != models]
    models = models['GISS-E2-1-G' != models]

    print(np.size(models))
    
    return models    
                

def plot_ulatlev(pngfile, lev, lat, varf, varl, ncols, nrows, xr = [-90,90], yr = [1000, 0], vr = [-12, 12, 5], rt = 10, level = [], levl = np.linspace(-100, 100, 101), latl = [], latf = [], fontsize = 12, fsizex = 8, fsizey = 11, cmap = cmo.balance, extend = 'both', sngl_cbar = False, vecx = [], vecy = [], scale = 1, scale_units = 'xy', iskp = 1, jskp = 1, labels = []):

    nexp = np.shape(varf)[0]
    plt.rcParams['font.size'] = fontsize
    fig = plt.figure(figsize = (fsizex, fsizey))
    ax = np.reshape(fig.subplots(nrows, ncols), (nrows, ncols))

    jm = np.size(lat); km = np.size(lev)
    if np.size(varl) == jm*km:
        varl = np.tile(varl[np.newaxis].T, nexp).T
    if np.size(latl) == km:
        latl = np.tile(latl[np.newaxis].T, nexp).T
    if np.size(latf) == km:
        latf = np.tile(latf[np.newaxis].T, nexp).T

    if np.size(vecx) == jm*km:
        vecx = np.tile(vecx[np.newaxis].T, nexp).T
    if np.size(vecy) == jm*km:
        vecy = np.tile(vecy[np.newaxis].T, nexp).T

    X, Y = np.meshgrid(lat, lev)
    nn = -1
    for nr in range(nrows):
        for nc in range(ncols):
            nn += 1            
            if nn < nexp:
                if np.size(vr[0]) > 1:
                    vr0 = vr[nn]
                else:
                    vr0 = vr
                if np.size(levl[0]) > 1:
                    levl0 = levl[nn]
                else:
                    levl0 = levl
                if np.size(level) == 0:
                    level0 = np.linspace(vr0[0], vr0[1], (vr0[2]-1)*rt+1)

                image = ax[nr,nc].contourf(X, Y, varf[nn], level0, extend = extend, cmap = cmap)
                if sngl_cbar == False:
                    cbar = plt.colorbar(image, ax = ax[nr, nc], orientation = 'horizontal', ticks = np.linspace(vr0[0], vr0[1], vr0[2]))
                ax[nr,nc].contour(X, Y, varl[nn], levl0, colors = 'k', linewidths = 0.5)
                if np.size(latl) != 0:
                    ax[nr,nc].plot(latl[nn], lev, 'y', linewidth = 2)                    
                if np.size(latf) != 0:
                    ax[nr,nc].plot(latf[nn], lev, 'g', linewidth = 2)                
                
                if (np.size(vecx) != 0) *  (np.size(vecy) != 0):
                    ax[nr,nc].quiver(X[::jskp,::iskp], Y[::jskp,::iskp], vecx[nn,::jskp,::iskp], vecy[nn,::jskp,::iskp], color = 'w', linewidths = 1, angles='xy', scale = scale, scale_units = scale_units, headwidth=5, headlength = 5, headaxislength = 1)    

                ax[nr,nc].set_xlim(xr[0], xr[1])
                ax[nr,nc].set_ylim(yr[0], yr[1])
                if np.size(xr) == 3:
                    ax[nr,nc].set_xticks(np.linspace(xr[0], xr[1], xr[2]))
                if np.size(yr) == 3:
                    ax[nr,nc].set_yticks(np.linspace(yr[0], yr[1], yr[2]))
                if np.size(labels) > nn:
                    ax[nr,nc].set_title(labels[nn])
            else:
                ax[nr,nc].remove()
    plt.tight_layout()
    plt.savefig(pngfile)


def plot_ulatlev_em(pngfile, models, levem, latem, varaem, varcem, ncols, nrows, xr = [-90,90], yr = [1000, 0], vr = [-12, 12, 5], rt = 10, level = [], levl = np.linspace(-100, 100, 101), latl = [], latf = [], fontsize = 12, fsizex = 8, fsizey = 16, cmap = cmo.balance, extend = 'both', cem = True, vecx = {}, vecy = [], vecx0 = [], vecy0 = [], scale = 1, scale_units = 'xy', iskp = 1, jskp = 1, vecxf0 = 4.e5/6.375e6, vecyf0 = 4.e5*1.e-2*1.e-2, vecxf = 1.e6/6.375e6, vecyf = 1.e-2*1.e6*1.e-2, vlatem = [], vlevem = []):

    nexp = np.size(models)
    model0 = 'EMS'+str(np.size(models))
    lat0 = latem[model0]; lev0 = 1.e-2*levem[model0]
    plt.rcParams['font.size'] = fontsize
    fig = plt.figure(figsize = (fsizex, fsizey))
    ax = np.reshape(fig.subplots(nrows, ncols), (nrows, ncols))

    if np.size(level) == 0:
        level = np.linspace(vr[0], vr[1], (vr[2]-1)*rt+1)


    nn = -1
    for nr in range(nrows):
        for nc in range(ncols):
            nn += 1
            if nn < nexp:
                model = models[nn]
                lat = latem[model]; lev = 1.e-2*levem[model]
                X, Y = np.meshgrid(lat, lev)                
                image = ax[nr,nc].contourf(X, Y, varcem[model]-varaem[model], level, extend = extend, cmap = cmap)
                ax[nr,nc].contour(X, Y, varaem[model], levl, colors = 'k', linewidths = 0.5)
                if np.size(latl) != 0:
                    ax[nr,nc].plot(latl[model], lev, 'y', linewidth = 2)                    
                if np.size(latf) != 0:
                    ax[nr,nc].plot(latf[model], lev, 'g', linewidth = 2)                

                if (np.size(vecx) != 0) *  (np.size(vecy) != 0):
                    if (np.size(vlatem) != 0)*(np.size(vlevem) != 0):
                        vlat = vlatem[model]
                        vlev = 1.e-2*vlevem[model]
                    else:
                        vlat = lat
                        vlev = lev
                    X, Y = np.meshgrid(vlat, vlev)                
                    if (np.size(vecx0) != 0) *  (np.size(vecy0) != 0):
                        vx = vecxf*(vecx[model]-vecx0[model])/np.deg2rad(lat[1]-lat[0])
                        vy = vecyf*(vecy[model]-vecy0[model])
                    else:
                        vx = vecxf0*vecx[model]/np.deg2rad(lat[1]-lat[0])
                        vy = vecyf0*vecy[model]
                    

                    ax[nr,nc].quiver(X[::jskp,::iskp], Y[::jskp,::iskp], vx[::jskp,::iskp], vy[::jskp,::iskp], color = 'blue', linewidths = 1, angles='xy', scale = scale, scale_units = scale_units, headwidth=5, headlength = 5, headaxislength = 1)    

                ax[nr,nc].set_xlim(xr[0], xr[1])
                ax[nr,nc].set_ylim(yr[0], yr[1])
                if np.size(xr) == 3:
                    ax[nr,nc].set_xticks(np.linspace(xr[0], xr[1], xr[2]))
                if np.size(yr) == 3:
                    ax[nr,nc].set_yticks(np.linspace(yr[0], yr[1], yr[2]))
                ax[nr,nc].set_title(model)
                if nn == 0:
                    varaMM = intp2D(lat, lev, varaem[model], lat0, lev0)/nexp
                    varcMM = intp2D(lat, lev, varcem[model], lat0, lev0)/nexp
                    if (np.size(vecx) != 0) *  (np.size(vecy) != 0):
                        vxMM = intp2D(vlat, vlev, vx, lat0, lev0)/nexp
                        vyMM = intp2D(vlat, vlev, vy, lat0, lev0)/nexp
                    if np.size(latl) != 0:
                        latlMM = latl[model]/nexp
                    if np.size(latf) != 0:
                        latfMM = latf[model]/nexp
                else:
                    varaMM = varaMM + intp2D(lat, lev, varaem[model], lat0, lev0)/nexp
                    varcMM = varcMM + intp2D(lat, lev, varcem[model], lat0, lev0)/nexp
                    if (np.size(vecx) != 0) *  (np.size(vecy) != 0):
                        vxMM = vxMM + intp2D(vlat, vlev, vx, lat0, lev0)/nexp
                        vyMM = vyMM + intp2D(vlat, vlev, vy, lat0, lev0)/nexp
                    if np.size(latl) != 0:
                        latlMM = latlMM + latl[model]/nexp
                    if np.size(latf) != 0:
                        latfMM = latfMM + latf[model]/nexp

                if nc == 0:
                    if nr == nrows-1:
                        ax[nr,nc].tick_params(labelbottom=True, labelleft=True)
                    else:
                        ax[nr,nc].tick_params(labelbottom=False, labelleft=True)
                else:
                    if nr == nrows-1:
                        ax[nr,nc].tick_params(labelbottom=True, labelleft=False)
                    elif (nr == nrows-2)*(nc > nexp - (nrows-1)*ncols):
                        ax[nr,nc].tick_params(labelbottom=True, labelleft=False)
                    else:
                        ax[nr,nc].tick_params(labelbottom=False, labelleft=False)
            elif nn == nexp:
                model = model0
                lat = latem[model]; lev = 1.e-2*levem[model]
                
                X, Y = np.meshgrid(lat, lev)                
                image = ax[nr,nc].contourf(X, Y, varcMM-varaMM, level, extend = extend, cmap = cmap)
                ax[nr,nc].contour(X, Y, varaMM, levl, colors = 'k', linewidths = 0.5)
                if np.size(latl) != 0:
                    ax[nr,nc].plot(latlMM, lev, 'y', linewidth = 2)                    
                if np.size(latf) != 0:
                    ax[nr,nc].plot(latfMM, lev, 'g', linewidth = 2)                
                if (np.size(vecx) != 0) *  (np.size(vecy) != 0):
                    ax[nr,nc].quiver(X[::jskp,::iskp], Y[::jskp,::iskp], vxMM[::jskp,::iskp], vyMM[::jskp,::iskp], color = 'blue', linewidths = 1, angles='xy', scale = scale, scale_units = scale_units, headwidth=5, headlength = 5, headaxislength = 1)    


                ax[nr,nc].set_xlim(xr[0], xr[1])
                ax[nr,nc].set_ylim(yr[0], yr[1])
                if np.size(xr) == 3:
                    ax[nr,nc].set_xticks(np.linspace(xr[0], xr[1], xr[2]))
                if np.size(yr) == 3:
                    ax[nr,nc].set_yticks(np.linspace(yr[0], yr[1], yr[2]))

                ax[nr,nc].set_title(model)
                if nc == 0:
                    ax[nr,nc].tick_params(labelbottom=True, labelleft=True)
                else:
                    ax[nr,nc].tick_params(labelbottom=True, labelleft=False)
            else:
                ax[nr,nc].remove()


    plt.tight_layout()
    plt.savefig(pngfile)

def ReadData2dClim(varname, model, expid, ybgn, yend, regrid = False, dirbase = '/data16/theme-C/usijimay'):    
    
    TID = cd.TableID(varname)
    if regrid:
        if TID[0] == 'A':
            grdname = '250deg-144x73'
        else:
            grdname = '100deg-360x180'
        fnameins = cd.datafiles(varname, model, expid, ybgn = ybgn, yend = yend, regrid = regrid, dirbase = '/Public/CMIPs/regrid/CMIP6/'+grdname+'/')
        fnamec = fnameins[-1][:-16].replace('/Public/CMIPs/regrid/CMIP6/'+grdname+'/', dirbase + '/CMIP/regrid/'+grdname+'_CLIM/CMIP6/')+str(ybgn)+'01-'+str(yend)+'12_clm.nc'
    else:
        fnameins = cd.datafiles(varname, model, expid, ybgn = ybgn, yend = yend, regrid = regrid, dirbase = '/Public/CMIPs/CMIP6/')
        fnamec = fnameins[-1][:-16].replace('/Public/CMIPs/CMIP6/', dirbase+'/CMIP/CMIP6/CLIM/')+str(ybgn)+'01-'+str(yend)+'12_clm.nc'

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


def ReadData3dClim(varname, model, expid, ybgn, yend, regrid = False, dirbase = '/data16/theme-C/usijimay'):
    
    TID = cd.TableID(varname)
    if regrid:
        if TID[0] == 'A':
            grdname = '250deg-144x73'
        else:
            grdname = '100deg-360x180'
        fnameins = cd.datafiles(varname, model, expid, ybgn = ybgn, yend = yend, regrid = regrid, dirbase = '/Public/CMIPs/regrid/CMIP6/'+grdname+'/')
        fnamec = fnameins[-1][:-16].replace('/Public/CMIPs/regrid/CMIP6/'+grdname+'/', dirbase+'/CMIP/regrid/'+grdname+'_CLIM/CMIP6/')+str(ybgn)+'01-'+str(yend)+'12_clm.nc'
    else:
        fnameins = cd.datafiles(varname, model, expid, ybgn = ybgn, yend = yend, regrid = regrid, dirbase = '/Public/CMIPs/CMIP6/')
        fnamec = fnameins[-1][:-16].replace('/Public/CMIPs/CMIP6/', dirbase+'/CMIP/CMIP6/CLIM/')+str(ybgn)+'01-'+str(yend)+'12_clm.nc'

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

def ReadData3d(varname, model, expid, ybgn, yend, regrid = False, dirbase = '/data16/theme-C/usijimay'):
    
    TID = cd.TableID(varname)
    if regrid:
        if TID[0] == 'A':
            grdname = '250deg-144x73'
        else:
            grdname = '100deg-360x180'
        fnameins = cd.datafiles(varname, model, expid, ybgn = ybgn, yend = yend, regrid = regrid, dirbase = '/Public/CMIPs/regrid/CMIP6/'+grdname+'/')
    else:
        fnameins = cd.datafiles(varname, model, expid, ybgn = ybgn, yend = yend, regrid = regrid, dirbase = '/Public/CMIPs/CMIP6/')

    lon, lat, lev, time, var = cd.ReadData3d(fnameins, varname, ybgn, yend)
    im = np.size(lon); jm = np.size(lat); km = np.size(lev)
    var = var.reshape(-1,12,km,jm,im)        

    return lon, lat, lev, var


def ReadData2dMMClim(varname, models, expid, ybgn, yend, regrid = False, dirbase = '/data16/theme-C/usijimay', lon = [], lat = []):    

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


def ReadData3dMMClim(varname, models, expid, ybgn, yend, regrid = False, dirbase = '/data16/theme-C/usijimay', lon = [], lat = [], lev = []):    

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
            print(nm, model)
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

def am0(var, nn, axis=0):

    if np.size(var) == 0:
        varann = var
    else:
        day = np.array(calendar.mdays[1:])        
        varann = np.average(var, weights = day, axis=axis)

    return varann


def sm(var, axis=0, nr=1):

    if np.size(var) == 0:
        varsm = np.tile(var, 4)
    else:
        day = np.roll(np.array(calendar.mdays[1:]), nr).reshape(4,3)
        for n in range(axis):
            day = day[np.newaxis]
        shape = np.array(np.shape(var)).astype(int)
        varsm = np.roll(var, nr, axis=axis).reshape(np.r_[shape[:axis],4,3,shape[axis+1:]])
        varsm = (np.sum(varsm.T * day.T, axis=-2-axis)/np.sum(day.T, axis=-2-axis)).T
        
    return varsm

def sm0(var, nn, axis=0, nr=1):

    if np.size(var) == 0:
        varsm0 = var
    else:
        day = np.roll(np.array(calendar.mdays[1:]), nr).reshape(4,3)
        for n in range(axis):
            day = day[np.newaxis]
        shape = np.array(np.shape(var)).astype(int)
        varsm = np.roll(var, nr, axis=axis).reshape(np.r_[shape[:axis],4,3,shape[axis+1:]])
        varsm = (np.sum(varsm.T * day.T, axis=-2-axis)/np.sum(day.T, axis=-2-axis)).T
        if axis==0:
            varsm0 = varsm[nn]
        elif axis==1:
            varsm0 = varsm[:,nn]
        elif axis==2:
            varsm0 = varsm[:,:,nn]
        elif axis==3:
            varsm0 = varsm[:,:,:,nn]
        elif axis==4:
            varsm0 = varsm[:,:,:,:,nn]                        
        
    return varsm0

def omsk(varM, msk):

    if np.size(msk) > 0:
        if type(varM) is np.ma.MaskedArray:    
            msk0 = 1-varM.mask.astype(float)
        else:
            msk0 = 1-np.isnan(varM).astype(float)
        if np.shape(msk0) == np.shape(varM):
            varM = varM.data * msk0 * msk - 9.99e33 * (1- msk0 * msk)
        else:
            varM = varM.data * msk - 9.99e33 * (1-msk)

        varM = np.ma.masked_array(varM, mask = (varM<-9.99e31), fill_value = -9.99e33)

    return varM


