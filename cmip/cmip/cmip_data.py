import os
import sys
import numpy as np
import netCDF4
import calendar

def datadirbase(regrid = True, mipera = 6, crpublic = False, vartyp = 'O'):
    BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(BASE)
    import config.config as cf    
    
    if regrid:
        if vartyp == 'O':
            grdname = '100deg-360x180'                    
        else:
            grdname = '250deg-144x73'

        dirbase = cf.datadir()+'/CMIP/regrid/'+grdname+'/CMIP6/'                
    else:
        dirbase = cf.datadir()+'/CMIP/CMIP6/'        

    return dirbase

def modeldir(varname, model, expid, dirbase = '',  regrid = False, mipera = 6, interval = 'mon'):

    if dirbase == '':
        dirbase = datadirbase(regrid = regrid, mipera = mipera)

    activity = expid2activity(expid)  
    TID = TableID(varname, interval = interval)
    mdir =  dirbase+activity+'/'+expid+'/'+TID+'/'+varname+'/'+model + '/'

    return mdir

    
def datafile(varname, model, expid, ybgn = 1981, yend = 2000, dirbase = '',  pforcingdir = 'r1i1p', spf = False, regrid = False, prgd = 'gn', grdtyp = ' ', spg = False, showcomment = False, suff = '.nc', mipera = 6, interval = 'mon', ctop = False, nlev = -1):

    inputdir = modeldir(varname, model, expid, dirbase = dirbase, regrid = regrid, mipera = mipera, interval = interval)

    forcingdirs = np.sort(os.listdir(inputdir))
    n = 0
    for forcingdir in forcingdirs:
        if pforcingdir in forcingdir:
            n += 1
            break
    
    if n == 0:
        forcingdir = forcingdirs[0]
        if spf:
            sys.exit('no forcing directory including ' + pforcingdir)
        else:
            if showcomment:
                print('use forcing type ' + forcingdir  + ' in this case')        

    inputdir = inputdir + forcingdir + '/'
    
    n = 0
    for grdf in os.listdir(inputdir):
        if regrid:
            if 'gr' in grdf:
                grdtypdir = grdf
                n = n + 1
        else:
            if prgd in grdf:
                grdtypdir = grdf
                n = n + 1

    for grdf in os.listdir(inputdir):                
        if grdf == grdtyp:
            grdtypdir = grdf
                
    if regrid:
        if n == 0:
            if spg:
                sys.exit('no general grid (1x1) in ' + inputdir)
            else:
                grdtypdir = os.listdir(inputdir)[0]
                if showcomment:                
                    print('no general grid (1x1) in ' + inputdir +', use ' +grdtypdir  + ' in this case')
        elif n>1:
            if showcomment:
                print('use grid type ' +grdtypdir  + ' in this case')        
    else:
        if n == 0:
            if spg:
                sys.exit('no native grid in ' + inputdir)
            else:
                grdtypdir = os.listdir(inputdir)[0]
                if showcomment:
                    print('no native grid in ' + inputdir +', use ' + grdtypdir  + ' in this case')
        elif n>1:
            if showcomment:
                print('use grid type ' +grdtypdir  + ' in this case')        

                
    inputdir = inputdir + grdtypdir + '/'
    vdate = np.sort(os.listdir(inputdir))[-1]

    if(np.size(os.listdir(inputdir)) >1):
        if showcomment:
            print('use version ' + vdate  + ' in this case (new version)')              

    inputdir = inputdir + vdate + '/'

    if regrid:
        if nlev == -1:
            clev = ''
        else:
            clev = 'L'+str(nlev)
    else:
        clev = ''

    n = 0
    input_file = np.array([], dtype = 'str')
    nsf = len(suff)
    for inputfile in np.sort(os.listdir(inputdir)):
        if ctop:
            if (varname+'top_' in inputfile) == False:
                continue
        else:
            if (varname+'_' in inputfile) == False:
                continue
            if len(clev) > 0:
                if (clev in inputfile) == False:
                    continue                    

        if (inputfile[-nsf:] == suff):
            yfbgn = int(inputfile[:-nsf+1][-14:-10])
            yfend = int(inputfile[:-nsf+1][-7:-3])            
            if (ybgn <= yfend) * (yfbgn <= yend):
                input_file = np.append(input_file, inputdir + inputfile)
        
    if np.size(input_file) > 1:
        input_file = np.sort(input_file)

    return input_file

def ReadData2d(input_file, varname, ybgn, yend, regrid = True, cann = False):
    nc = netCDF4.Dataset(input_file[0], 'r')
    
    if 'lon' in nc.variables:
        lon = nc.variables['lon'][:]
    elif 'longitude' in nc.variables:
        lon = nc.variables['longitude'][:]
    elif 'nav_lon' in nc.variables:
        lon = nc.variables['nav_lon'][:]                

    if 'lat' in nc.variables:
        lat = nc.variables['lat'][:]
    elif 'latitude' in nc.variables:
        lat = nc.variables['latitude'][:]
    elif 'nav_lat' in nc.variables:
        lat = nc.variables['nav_lat'][:]

    if np.size(input_file) > 1:
        ifile = input_file.copy()
        input_file = np.array([], dtype = 'str')
        for n in range(np.size(ifile)):
            yfbgn = int(ifile[n][-16:-12])
            yfend = int(ifile[n][-9:-5])
            if (ybgn <= yfend) * (yfbgn <= yend):
                input_file = np.append(input_file, ifile[n])     


    if np.size(input_file) == 1:
        nc = netCDF4.Dataset(input_file[0], 'r')
        yfbgn = int(input_file[0][-16:-12])
        nbgn = (ybgn-yfbgn)*12
        nend = (yend-yfbgn+1)*12
        time = nc.variables['time'][nbgn:nend]
        var = nc.variables[varname][nbgn:nend]        

    else:
        for n in range(np.size(input_file)):            
            nc = netCDF4.Dataset(input_file[n], 'r')
            if n == 0:
                yfbgn = int(input_file[n][-16:-12])
                nbgn = (ybgn-yfbgn)*12
                var = nc.variables[varname][nbgn:]
                time = nc.variables['time'][nbgn:]                
            elif n == (np.size(input_file)-1):
                yfbgn = int(input_file[n][-16:-12])
                nend = (yend-yfbgn+1)*12                
                var = np.ma.concatenate([var, nc.variables[varname][:nend]], 0)
                time = np.append(time, nc.variables['time'][:nend])
            else:
                time = np.append(time, nc.variables['time'][:])
                var = np.ma.concatenate([var, nc.variables[varname][:]], 0)

    if cann:
        im = np.size(lon); jm = np.size(lat)
        var = np.average(var.reshape(-1,12,jm,im), axis=1, weights = calendar.mdays[1:])


    return lon, lat, time, var


def ReadData3d(input_file, varname, ybgn, yend, lonname = 'lon', latname = 'lat', levname = 'lev', timename = 'time', cann = False):
    nc = netCDF4.Dataset(input_file[0], 'r')

    if 'lon' in nc.variables:
        lon = nc.variables['lon'][:]
    elif 'longitude' in nc.variables:
        lon = nc.variables['longitude'][:]
    elif 'nav_lon' in nc.variables:
        lon = nc.variables['nav_lon'][:]                
    else:
        lon = nc.variables[lonname][:]


    if 'lat' in nc.variables:
        lat = nc.variables['lat'][:]
    elif 'latitude' in nc.variables:
        lat = nc.variables['latitude'][:]
    elif 'nav_lat' in nc.variables:
        lat = nc.variables['nav_lat'][:]
    else:
        lat = nc.variables[latname][:]

    if 'lev' in nc.variables:
        lev = nc.variables['lev'][:]
    if 'plev' in nc.variables:
        lev = nc.variables['plev'][:]
    elif 'olevel' in nc.variables:
        lev = nc.variables['olevel'][:]
    elif 'depth' in nc.variables:
        lev = nc.variables['depth'][:]
    elif 'deptht' in nc.variables:
        lev = nc.variables['deptht'][:]        
    else:
        lev = nc.variables[levname][:]

    if np.size(input_file) > 1:
        ifile = input_file.copy()
        input_file = np.array([], dtype = 'str')
        for n in range(np.size(ifile)):
            yfbgn = int(ifile[n][-16:-12])
            yfend = int(ifile[n][-9:-5])
            if (ybgn <= yfend) * (yfbgn <= yend):
                input_file = np.append(input_file, ifile[n])     

    if np.size(input_file) == 1:
        nc = netCDF4.Dataset(input_file[0], 'r')
        yfbgn = int(input_file[0][-16:-12])
        nbgn = (ybgn-yfbgn)*12
        nend = (yend-yfbgn+1)*12
        time = nc.variables[timename][nbgn:nend]
        var = nc.variables[varname][nbgn:nend]        
        nc.close()
    else:
        for n in range(np.size(input_file)):            
            nc = netCDF4.Dataset(input_file[n], 'r')
            yfbgn = int(input_file[n][-16:-12])
            if n == 0:
                nbgn = (ybgn-yfbgn)*12
                var = nc.variables[varname][nbgn:]
                time = nc.variables[timename][nbgn:]                
            elif n == (np.size(input_file)-1):
                yfbgn = int(input_file[n][-16:-12])
                nend = (yend-yfbgn+1)*12                
                var = np.ma.concatenate([var, nc.variables[varname][:nend]], 0)
                time = np.append(time, nc.variables[timename][:nend])
            else:
                var = np.ma.concatenate([var, nc.variables[varname][:]], 0)
                time = np.append(time, nc.variables[timename][:])
            nc.close()
    
    if cann:
        im = np.size(lon); jm = np.size(lat); km = np.size(lev)
        var = np.average(var.reshape(-1,12,km,jm,im), axis=1, weights = calendar.mdays[1:])


    return lon, lat, lev, time, var


def expid2activity(expid):
    if expid == 'historical':
        activity = 'CMIP'
    elif expid == 'piControl':
        activity = 'CMIP'
    elif expid == 'amip':
        activity = 'CMIP'
    elif 'ssp' in expid:
        activity = 'ScenarioMIP'
    else:
        axtivity = ''
        sys.exit('check Experiment Id of CMIP and add its actipidy')

    return activity

def TableID(varname, interval = 'mon'):
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import cmip_varnames as cv
    ovarnames  = cv.vartyp2varnames('O')
    avarnames  = cv.vartyp2varnames('A')
    sivarnames = cv.vartyp2varnames('SI')
    
    if varname in ovarnames:
        TID = 'O'+interval
    elif varname in avarnames:
        if interval == 'fx':
            TID = interval
        else:
            TID = 'A'+interval
    elif varname in sivarnames:
        TID = 'SI'+interval
    else:
        TID = ''
        sys.exit('check varname and the directory of the varnames')

    return TID    
