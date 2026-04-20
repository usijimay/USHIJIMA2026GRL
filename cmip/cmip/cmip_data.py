import os
import sys
import numpy as np
import netCDF4
import calendar
import socket


def datadirbase(regrid = True, mipera = 6, crpublic = False, vartyp = 'O'):
    # sys.path.append("../../machine")
    sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/../../machine")
    import varsrv
    if regrid:
        dirbase = varsrv.datadirname()+'/CMIP/regrid/woa1x1/CMIP'+str(mipera)+'/'
        if crpublic:
            if (vartyp[0] == 'O') or (vartyp[0] == 'o') or (vartyp[0] == 'S') or (vartyp[0] == 's'):
                dirbase='/Public/CMIPs/regrid/CMIP6/100deg-360x180/'
            else:
                dirbase='/Public/CMIPs/regrid/CMIP6/250deg-144x73/'            
    else:
        if 'asteroid' in socket.gethostname() or 'artemis' in socket.gethostname():                 
            if crpublic:
                dirbase='/Public/CMIPs/CMIP6/'                 
            else:
                dirbase = '/data16/theme-C/usijimay/CMIP/CMIP6/'
                
        elif 'glb' in socket.gethostname():
            if crpublic:                
                dirbase = '/net/NasB2019/NasB2019_2/cmip/CMIP6_old/'
            else:
                dirbase = '/nas/personal/usijimay/CMIP/regrid/woa1x1/CMIP6/'

    return dirbase

def modeldir(varname, model, expid, dirbase = '',  regrid = False, mipera = 6, interval = 'mon'):

    if dirbase == '':
        dirbase = datadirbase(regrid = regrid, mipera = mipera)

    activity = expid2activity(expid)  
    TID = TableID(varname, interval = interval)
    mdir =  dirbase+activity+'/'+expid+'/'+TID+'/'+varname+'/'+model + '/'

    return mdir

    
def datafiles(varname, model, expid, ybgn = 1981, yend = 2000, dirbase = '',  pforcingdir = 'r1i1p', spf = False, regrid = False, prgd = 'gn', grdtyp = ' ', spg = False, showcomment = False, pexpid='historical', suff = '.nc', mipera = 6, interval = 'mon', ctop = False, nlev = -1):
# def input_file_cmips(varname, model, expid, ybgn = 1981, yend = 2000, dirbase = '',  pforcingdir = 'r1i1p', spf = False, regrid = False, prgd = 'gn', grdtyp = ' ', spg = False, showcomment = False, pexpid='historical', suff = '.nc', mipera = 6, interval = 'mon'):

    if ('ssp' in expid)*(ybgn < 2015):
        input_fileb = datafile(varname, model, expid, ybgn = 2015, yend = yend, dirbase = dirbase,  pforcingdir = pforcingdir, spf = spf, regrid = regrid, prgd = prgd, grdtyp = grdtyp, spg = spg, showcomment = showcomment, suff = suff, ctop = ctop, nlev = nlev)
        # nc = netCDF4.Dataset(input_fileb[0])
        # esm = nc.parent_variant_label
        # spf = esm
        input_filea = datafile(varname, model, pexpid, ybgn = ybgn, yend = 2014, dirbase = dirbase,  pforcingdir = pforcingdir, spf = spf, regrid = regrid, prgd = prgd, grdtyp = grdtyp, spg = spg, showcomment = showcomment, suff = suff, ctop = ctop, nlev = nlev)
        input_file = np.r_[input_filea, input_fileb]
    else:
        input_file = datafile(varname, model, expid, ybgn = ybgn, yend = yend, dirbase = dirbase,  pforcingdir = pforcingdir, spf = spf, regrid = regrid, prgd = prgd, grdtyp = grdtyp, spg = spg, showcomment = showcomment, suff = suff, ctop = ctop, nlev = nlev)

    return input_file

def datafile(varname, model, expid, ybgn = 1981, yend = 2000, dirbase = '',  pforcingdir = 'r1i1p', spf = False, regrid = False, prgd = 'gn', grdtyp = ' ', spg = False, showcomment = False, suff = '.nc', mipera = 6, interval = 'mon', ctop = False, nlev = -1):
# def input_file_cmip(varname, model, expid, ybgn = 1981, yend = 2000, dirbase = '',  pforcingdir = 'r1i1p', spf = False, regrid = False, prgd = 'gn', grdtyp = ' ', spg = False, showcomment = False, suff = '.nc', mipera = 6, interval = 'mon'):

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
            # if(np.size(os.listdir(inputdir)) >1):
            if showcomment:
                print('use forcing type ' + forcingdir  + ' in this case')        

    inputdir = inputdir + forcingdir + '/'
    
    # print(os.listdir(inputdir))
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
    # print(inputdir)
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

        # print(inputfile)        
        # if (inputfile[-2:] == 'nc'):
        if (inputfile[-nsf:] == suff):
            yfbgn = int(inputfile[:-nsf+1][-14:-10])
            yfend = int(inputfile[:-nsf+1][-7:-3])            
            # if (n==0)*(expid == 'piControl'):
            #     ybgn = ybgn + yfbgn - 1850
            #     yend = yend + yfbgn - 1850            
            if (ybgn <= yfend) * (yfbgn <= yend):
                input_file = np.append(input_file, inputdir + inputfile)
            
    if np.size(input_file) > 1:
        input_file = np.sort(input_file)

    return input_file


def datafile_fx(varname, model, expid, dirbase = '',  pforcingdir = 'r1i1p', spf = False, regrid = False, prgd = 'gn', grdtyp = ' ', spg = False, showcomment = False, mipera = 6, interval = 'fx'):
# def input_file_cmip_fx(varname, model, expid, dirbase = '',  pforcingdir = 'r1i1p', spf = False, regrid = False, prgd = 'gn', grdtyp = ' ', spg = False, showcomment = False, mipera = mipera):


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
            # if(np.size(os.listdir(inputdir)) >1):
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

    n = 0
    input_file = np.array([], dtype = 'str')
    for inputfile in np.sort(os.listdir(inputdir)):
        if(inputfile[-2:] == 'nc'):
            input_file = np.append(input_file, inputdir + inputfile)
            
    if np.size(input_file) > 1:
        input_file = np.sort(input_file)

    return input_file


def EnsembleMember(varname, model, expid, ybgn = -1, yend = 10000, dirbase = '',  regrid = False, pexpid='historical', suff = '.nc', mipera = 6, interval = 'mon', pforce = [], cedefalt = True):
    
    mdir = modeldir(varname, model, expid, dirbase = dirbase,  regrid = regrid, mipera = mipera, interval = interval)
    print(ybgn, yend)
    if os.path.isdir(mdir):
        esms = np.sort(os.listdir(mdir)).astype(object)
        esma = np.array([], 'object')
        esmb = np.array([], 'object')
        esmc = np.array([], 'object')
        for esm in esms:
            fnameins = datafiles(varname, model, expid, ybgn = ybgn, yend = yend, regrid = regrid, dirbase = dirbase, pforcingdir = esm)

            # print(esm, fnameins)
            if int(np.sort(fnameins)[-1][-9:-5]) < yend:
                continue
            if int(np.sort(fnameins)[0][-16:-12]) > ybgn:
                continue
            if cedefalt:
                if ('CanESM5' in model)*('p1f' in esm):
                    continue
                if ('CNRM-ESM2-1' in model)*('126' in expid)*('r4' in esm):
                    continue
            # print(esm, fnameins)

            if esm[2] == 'i':
                if (esm[3:5] == '1p'):
                    esma = np.append(esma, esm)        
            if esm[3] == 'i':
                esmb = np.append(esmb, esm)
            if esm[4] == 'i':
                esmc = np.append(esmc, esm)
        esms = np.r_[esma, esmb, esmc]
    else:
        esms = []

    return esms

def EsmEMout(esms):
    
    for esm in esms:
        realn = int(esm[1:esm.find('i')])
        initn = int(esm[esm.find('i')+1:esm.find('p')])
        physn = int(esm[esm.find('p')+1:esm.find('f')])
        if len(esm) > esm.find('f') + 1:
            forcn = int(esm[esm.find('f')+1:])
        else:
            forcn = 0

        if esm == esms[0]:
            rmin = realn; rmax = realn
            imin = initn; imax = initn
            pmin = physn; pmax = physn
            fmin = forcn; fmax = forcn
        else:
            rmin = np.minimum(realn, rmin); rmax = np.maximum(realn, rmax)
            imin = np.minimum(initn, imin); imax = np.maximum(initn, imax)
            pmin = np.minimum(physn, pmin); pmax = np.maximum(physn, pmax)
            fmin = np.minimum(forcn, fmin); fmax = np.maximum(forcn, fmax)        
        
    if rmin == rmax:
        realc = 'r' + str(realn)
    else:
        realc = 'r' + str(int(rmin)).zfill(3) + '-' + str(int(rmax)).zfill(3)
    if imin == imax:
        initc = 'i' + str(initn)
    else:
        # initc = 'i' + str(int(imin)).zfill(3) + '-' + str(int(imax)).zfill(3)        
        initc = 'i' + str(int(imin)) + '-' + str(int(imax))
    if pmin == pmax:
        physc = 'p' + str(physn)
    else:
        # physc = 'p' + str(int(pmin)).zfill(3) + '-' + str(int(pmax)).zfill(3)        
        physc = 'p' + str(int(pmin)) + '-' + str(int(pmax))        
    if fmin == fmax:
        if forcn == 0:
            forcc = 'f'
        else:
            forcc = 'f'+str(forcn)
    else:
        # forcc = 'f'+str(int(fmin)).zfill(3) + '-' + +str(int(fmax)).zfill(3)        
        forcc = 'f'+str(int(fmin)) + '-' + +str(int(fmax))        

    esmout = realc+initc+physc+forcc

    return esmout



def ReadData2d(input_file, varname, ybgn, yend, regrid = True, cann = False):
    nc = netCDF4.Dataset(input_file[0], 'r')
    # if regrid:
    #     lon = nc.variables['lon'][:]
    #     lat = nc.variables['lat'][:]
    # else:
    #     lon = nc.variables['longitude'][:]
    #     lat = nc.variables['latitude'][:]
    
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
        # time = nc.variables['time'][:]
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
                # var = np.concatenate([var, nc.variables[varname][:nend]], 0)
                var = np.ma.concatenate([var, nc.variables[varname][:nend]], 0)
                time = np.append(time, nc.variables['time'][:nend])
                # var = np.concatenate([var, nc.variables[varname][:nend-nt]], 0)
            else:
                time = np.append(time, nc.variables['time'][:])
                # var = np.concatenate([var, nc.variables[varname][:]], 0)
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
        # nc = netCDF4.Dataset(input_file[0], 'r', diskless=True)
        # time = nc.variables['time'][:]
        yfbgn = int(input_file[0][-16:-12])
        nbgn = (ybgn-yfbgn)*12
        nend = (yend-yfbgn+1)*12
        time = nc.variables[timename][nbgn:nend]
        var = nc.variables[varname][nbgn:nend]        
        # var0 = nc.variables[varname]
        # var = var0[nbgn:nend]        
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
                # var = np.concatenate([var, nc.variables[varname][:nend]], 0)
                var = np.ma.concatenate([var, nc.variables[varname][:nend]], 0)
                time = np.append(time, nc.variables[timename][:nend])
                # var = np.concatenate([var, nc.variables[varname][:nend-nt]], 0)
            else:
                # var = np.concatenate([var, nc.variables[varname][:]], 0)
                var = np.ma.concatenate([var, nc.variables[varname][:]], 0)
                time = np.append(time, nc.variables[timename][:])
            nc.close()
    
    if cann:
        im = np.size(lon); jm = np.size(lat); km = np.size(lev)
        var = np.average(var.reshape(-1,12,km,jm,im), axis=1, weights = calendar.mdays[1:])


    return lon, lat, lev, time, var


def ReadData3dMon(input_file, varname, ybgn, yend, mon, lonname = 'lon', latname = 'lat', levname = 'lev', timename = 'time'):
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
    elif 'olevel' in nc.variables:
        lev = nc.variables['olevel'][:]
    elif 'depth' in nc.variables:
        lev = nc.variables['depth'][:]
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
        # nc = netCDF4.Dataset(input_file[0], 'r', diskless=True)
        # time = nc.variables['time'][:]
        yfbgn = int(input_file[0][-16:-12])
        nbgn = (ybgn-yfbgn)*12+mon-1
        nend = (yend-yfbgn+1)*12+mon-1
        time = nc.variables[timename][nbgn:nend:12]
        var = nc.variables[varname][nbgn:nend:12]        
        # var0 = nc.variables[varname]
        # var = var0[nbgn:nend]        
        nc.close()
    else:
        for n in range(np.size(input_file)):            
            nc = netCDF4.Dataset(input_file[n], 'r')
            if n == 0:
                yfbgn = int(input_file[n][-16:-12])
                nbgn = (ybgn-yfbgn)*12+mon-1
                var = nc.variables[varname][nbgn::12]
                time = nc.variables[timename][nbgn::12]                
            elif n == (np.size(input_file)-1):
                yfbgn = int(input_file[n][-16:-12])
                nend = (yend-yfbgn+1)*12+mon-1
                # nend = (yend-yfbgn)*12+mon
                # var = np.concatenate([var, nc.variables[varname][:nend]], 0)
                var = np.ma.concatenate([var, nc.variables[varname][mon-1:nend:12]], 0)
                time = np.append(time, nc.variables[timename][mon-1:nend:12])
                # var = np.concatenate([var, nc.variables[varname][:nend-nt]], 0)
            else:
                # var = np.concatenate([var, nc.variables[varname][:]], 0)
                var = np.ma.concatenate([var, nc.variables[varname][mon-1::12]], 0)
                time = np.append(time, nc.variables[timename][:])
            nc.close()

    return lon, lat, lev, time, var


def var_func(input_file, varname, ybgn, yend, lonname = 'lon', latname = 'lat', levname = 'lev', timename = 'time'):
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

    lev = nc.variables[levname][:]
    
    if np.size(input_file) == 1:
        nc = netCDF4.Dataset(input_file[0], 'r')
        # time = nc.variables['time'][:]
        yfbgn = int(input_file[0][-16:-12])
        nbgn = (ybgn-yfbgn)*12
        nend = (yend-yfbgn+1)*12
        time = nc.variables[timename][nbgn:nend]
        var = nc.variables[varname][nbgn:nend]        

    else:
        for n in range(np.size(input_file)):            
            nc = netCDF4.Dataset(input_file[n], 'r')
            if n == 0:
                yfbgn = int(input_file[n][-16:-12])
                nbgn = (ybgn-yfbgn)*12
                var = nc.variables[varname][nbgn:]
                time = nc.variables[timename][nbgn:]                
            elif n == (np.size(input_file)-1):
                yfbgn = int(input_file[n][-16:-12])
                nend = (yend-yfbgn+1)*12                
                # var = np.concatenate([var, nc.variables[varname][:nend]], 0)
                var = np.ma.concatenate([var, nc.variables[varname][:nend]], 0)
                time = np.append(time, nc.variables[timename][:nend])
                # var = np.concatenate([var, nc.variables[varname][:nend-nt]], 0)
            else:
                # var = np.concatenate([var, nc.variables[varname][:]], 0)
                var = np.ma.concatenate([var, nc.variables[varname][:]], 0)
                time = np.append(time, nc.variables[timename][:])

    return lon, lat, lev, time, var


def var_func2D(input_file, varname, ybgn, yend):
    nc = netCDF4.Dataset(input_file[0], 'r')
    lon = nc.variables['lon'][:]
    lat = nc.variables['lat'][:]

    if np.size(input_file) == 1:
        nc = netCDF4.Dataset(input_file[0], 'r')
        # time = nc.variables['time'][:]
        yfbgn = int(input_file[0][-16:-12])
        nbgn = (ybgn-yfbgn)*12
        nend = (yend-yfbgn+1)*12
        time = nc.variables['time'][:]
        var = nc.variables[varname][nbgn:nend]        

    else:
        for n in range(np.size(input_file)):            
            nc = netCDF4.Dataset(input_file[n], 'r')
            if n == 0:
                time = nc.variables['time'][:]
                yfbgn = int(input_file[n][-16:-12])
                nbgn = (ybgn-yfbgn)*12
                var = nc.variables[varname][nbgn:]
            elif n == (np.size(input_file)-1):
                yfbgn = int(input_file[n][-16:-12])
                nend = (yend-yfbgn+1)*12                
                var = np.concatenate([var, nc.variables[varname][:nend]], 0)
                time = np.append(time, nc.variables['time'][:])
                # var = np.concatenate([var, nc.variables[varname][:nend-nt]], 0)
            else:
                time = np.append(time, nc.variables['time'][:])
                var = np.concatenate([var, nc.variables[varname][:]], 0)

    return lon, lat, var



def var_func2D_gn(input_file, varname, ybgn, yend):
    nc = netCDF4.Dataset(input_file[0], 'r')
    lon = nc.variables['longitude'][:]
    lat = nc.variables['latitude'][:]
    lonv = nc.variables['vertices_longitude'][:]
    latv = nc.variables['vertices_latitude'][:]

    if np.size(input_file) == 1:
        nc = netCDF4.Dataset(input_file[0], 'r')
        # time = nc.variables['time'][:]
        yfbgn = int(input_file[0][-16:-12])
        nbgn = (ybgn-yfbgn)*12
        nend = (yend-yfbgn+1)*12
        time = nc.variables['time'][:]
        var = nc.variables[varname][nbgn:nend]        

    else:
        for n in range(np.size(input_file)):            
            nc = netCDF4.Dataset(input_file[n], 'r')
            if n == 0:
                time = nc.variables['time'][:]
                yfbgn = int(input_file[n][-16:-12])
                nbgn = (ybgn-yfbgn)*12
                var = nc.variables[varname][nbgn:]
            elif n == (np.size(input_file)-1):
                yfbgn = int(input_file[n][-16:-12])
                nend = (yend-yfbgn+1)*12                
                var = np.concatenate([var, nc.variables[varname][:nend]], 0)
                time = np.append(time, nc.variables['time'][:])
                # var = np.concatenate([var, nc.variables[varname][:nend-nt]], 0)
            else:
                time = np.append(time, nc.variables['time'][:])
                var = np.concatenate([var, nc.variables[varname][:]], 0)

    return lon, lat, lonv, latv, var


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

# def scnr2scnrdir(scenario):
#     activity = expid2actividy(scenario)
#     scenariodir = activity + '/'
#     return scenariodir
    
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

def varname2order(varname):
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    import cmip_varnames as cv
    varname0Ds  = cv.order2varnames(0)
    varname1Ds  = cv.order2varnames(1)
    varname2Ds  = cv.order2varnames(2)
    varname3Ds  = cv.order2varnames(3)
    
    if varname in varname0Ds:
        order = 0        
    elif varname in varname1Ds:
        order = 1        
    elif varname in varname2Ds:
        order = 2        
    elif varname in varname3Ds:
        order = 3        
    else:
        order = -999
        sys.exit('check varname and the directory of the varnames')

    return order 
        

def dimensionname(model, grd = 'gn', urgd = False, cread = False, fname = ''):

    lonname = 'longitude'
    latname = 'latitude'
    levname = 'lev'
    timename = 'time'
    # lonname = 'lon'
    # latname = 'lat'
    # levname = 'lev'
    # timename = 'time'

    if 'CESM2' in model:
        lonname = 'lon'
        latname = 'lat'
    if 'GFDL' in model:
        lonname = 'lon'
        latname = 'lat'
    if 'GISS-E2-1' in model:
        lonname = 'lon'
        latname = 'lat'

    if grd == 'gn':
        if 'CNRM' in model:
            lonname = 'lon'
            latname = 'lat'
        if 'CAS' in model:
            lonname = 'lon'
            latname = 'lat'            
        if 'KIOST' in model:
            lonname = 'lon'
            latname = 'lat'
        if 'NESM3' in model:
            lonname = 'lon'
            latname = 'lat'
        if 'IPSL-CM5A2' in model:
            levname = 'deptht'
            lonname = 'nav_lon'
            latname = 'nav_lat'        
        if 'IPSL-CM6A' in model:
            levname = 'olevel'
            lonname = 'nav_lon'
            latname = 'nav_lat'
            
    if grd == 'gr':
        if 'E2SM' in model:
            lonname = 'lon'
            latname = 'lat'
        if 'E3SM' in model:
            lonname = 'lon'
            latname = 'lat'
        if 'INM' in model:
            lonname = 'lon'
            latname = 'lat'
        # if 'INM-CM4-8' in model:
        #     lonname = 'lon'
        #     latname = 'lat'                    
        # if 'INM-CM5-0' in model:
        #     lonname = 'lon'
        #     latname = 'lat'
        if 'MIROC-ES2L' in model:
            lonname = 'lon'
            latname = 'lat'
        if 'MRI' in model:
            lonname = 'lon'
            latname = 'lat'                        
            
    if urgd:
        lonname = 'lon'
        latname = 'lat'
        levname = 'depth'
        timename = 'time'
        
    if cread:
        nc = netCDF4.Dataset(fname, 'r')
        for key in nc.variables.keys():
            if 'lon' in key:
                lonname = key
            if 'lat' in key:
                latname = key
            if ('dep' in key) or ('lev' in key):
                levname = key
            if 'time' == key:
                timename = key

    return lonname, latname, levname, timename


