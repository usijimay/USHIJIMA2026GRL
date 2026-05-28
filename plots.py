import os
import sys
import calendar
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cmocean.cm as cmo
import seaborn as sns
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE)
import mriagcm3.grid.mriagcm as ag
import mriagcm3.read_clm as mrc
import obs.read_wind_module as rw
import cmip.cmip_mm as cmm
import config.config as cf
import config.fig_module as fm


sns.set_theme(style = 'whitegrid', font_scale = 1.)

expid0 = 'MPE3_agcm_cntl'
exptyp = 'region'
areasns = ['glb', 'snp', 'exsnp', 'wnp', 'ceq', 'enp']
expids = np.array(list(map(lambda x: 'MPE3_agcm_EMS35_annclm_'+x, areasns))).astype(object)

dirbase = cf.datadir()

ybgn = 1985; yend = 2014
dpi = None
# dpi = 900

def main(dpi = 900):
    global lon, lat
    global var0, varm0, varc0
    global var, varm, varc
    global varmo, varco, rvarco

    suff = '.png'        
    figdir =  cf.figdir(dpi = dpi)
   
    R0 = 6.375e6    
    lonmin=120; lonmax=240
    
    msko = np.fromfile(dirbase+'/AGCM/cnst/omsk_TL159.dat', '>f').reshape(160,320)[::-1]
    msk = msko.copy()    

    lon, lat = ag.lonlat()
    sst0M, sstM = read_sst(expid0, expids, ybgn, yend, msk = msko)

    varf = am(sstM-sst0M, axis=1)    
    nf = 1
    pngfile=figdir+'fig'+str(nf)+suff
    fm.fig1(pngfile, lon, lat, varf, lonr = [0, 359.9, 60], latr = [-90, 90, 30], vr=[-1.6, 1.6, 5], cmap = cmo.balance, flabel = ['GLB', 'PAC', 'GLB-PAC', 'WNP', 'EQ', 'ENP'], bbox = dict(facecolor='white', alpha=0.9), dpi = dpi)

    R0 = 6.375e6
    Rd = 2.87e2
    Cp = 1.004e3
    lev0 = np.array([1.e5, 9.25e4, 8.5e4, 7.e4, 6.e4, 5.e4, 4.e4, 3.e4, 2.5e4, 2.e4, 1.5e4, 1.e4, 7.e3, 5.e3, 3.e3, 2.e3, 1.e3, 5.e2, 1.e2])    
    ktgt0 = 9

    lonoa, latoa, levoa, uaoM = rw.read_JRA55_UP_CLM(ybgn, yend, level = 1.e-2*lev0, fbase = dirbase+'/obs/WindProfile/JRA55/MONCLM/anl_p125_ugrd.')
    ulto = ZonalMean(lonoa, am(uaoM), lonmin=lonmin, lonmax=lonmax)    
    lmxo = cmm.u1d2lpeak(ulto[ktgt0], latoa, latmin = 15, latmax = 65, mode = '')
    
    models, lmxaem, lmxcem = cmm.latupeak(ybgn, yend, lonmin = lonmin, lonmax = lonmax, level = 20000, mode = '') 
    lono, lato, levo, uacM, uaaM, dbdycM, dbdyaM, dbdzcM, dbdzaM, egrcM, egraM = cmm.read_datas_MMM(ybgn, yend, am, dirbase = dirbase)
    lon, lat, lev, ua0M, uaM = read_amip3D(expid0, expids, 'hs_ua.', 'ua', ybgn, yend)    
    
    ktgt = np.where(lev == 200)[0][0]
    
    ultc = ZonalMean(lono, uacM, lonmin=lonmin, lonmax=lonmax)
    ulta = ZonalMean(lono, uaaM, lonmin=lonmin, lonmax=lonmax)

    lmxc = cmm.u1d2lpeak(ultc[ktgt0], lato, latmin = 15, latmax = 65, mode = '')
    lmxa = cmm.u1d2lpeak(ulta[ktgt0], lato, latmin = 15, latmax = 65, mode = '')
    for nm, model in enumerate(models):
        model = models[nm]
        if nm == 0:
            latmp = np.array(lmxaem[model])
            lctmp = np.array(lmxcem[model])            
        else:
            latmp = np.r_[latmp, np.array(lmxaem[model])]
            lctmp = np.r_[lctmp, np.array(lmxcem[model])]                     
            
    labels = ['', 'AMIP-JRA55', 'historical-JRA55', 'historical-AMIP', 'GLB-CNTL', 'PAC-CNTL', '(GLB-PAC)-CNTL', 'WNP-CNTL', 'EQ-CNTL', 'ENP-CNTL']

    bbox = dict(facecolor='white', alpha=0.9)    
    latminca = 32; latmaxca = 44; latintca = 7
    vmin = -8; vmax = 8; vint = 5; rt = 10
    lonminf = 90; lonmaxf = 270; lonintf = 60
    latminf =-20; latmaxf = 80; latintf = 20        
    dxax = 3; dyax = 1.2
    fontsizexy = 10
    dxc = 0.04; dyc = 0.08
    unitx = 1.02; unity = -2.4; unitcbr = r'[${\rm m \ s^{-1}}$]'

    plt.rcParams['font.size'] = 10
    
    ntop = 8; ntop1 = ntop-3 
    rmap = 2
    nf += 1
    pngfile=figdir+'fig'+str(nf)+suff
    print(pngfile)    
    fig = plt.figure(figsize=(8,10), constrained_layout=True)    
    gs = gridspec.GridSpec(ntop+rmap*3, 3, figure=fig)
    ax = fig.add_subplot(gs[0:ntop1,:])    
    for nm, model in enumerate(models):
        model = models[nm]                        
        ax.bar(1/6+nm, lmxaem[model], width = 0.33, color = 'r')
        ax.bar(1/2+nm, lmxcem[model], width = 0.33, color = 'b')
                        
    nm += 1
    ax.bar(1/6+nm, lmxa, width = 0.33, color = 'r')
    ax.bar(1/2+nm, lmxc, width = 0.33, color = 'b')                                    
    ax.bar(4/3+nm, lmxo, width = 0.33, color = 'k')
    
    ax.set_xlim(0, nm+2)
    ax.set_xticks(0.5+np.arange(nm+2))
    ax.set_xticklabels(np.r_[models, ['Multi Model'], ['JRA55']])
    ax.tick_params(axis='x', labelrotation=90)
    ax.set_ylim(latminca, latmaxca)
    ax.set_yticks(np.linspace(latminca, latmaxca, latintca))
    nfg = 0
    label = '('+chr(ord("a")+nfg)+')'+labels[nfg]
    ax.text(0.01*(nm+2), 0.02*latminca+0.98*latmaxca, label, ha = 'left', va = 'top', bbox = bbox)
    
    nn = ntop
    uaoMrgd = cmm.intp2D(lonoa, latoa, am(uaoM)[9], lono, lato)
    varf = np.ma.array([uaaM[9]-uaoMrgd, uacM[9]-uaoMrgd, uacM[9]-uaaM[9]])
    varl = np.ma.array([uaoMrgd, uaoMrgd, uaaM[9]])            
    for nc in range(3):        
        ax = fig.add_subplot(gs[nn:nn+rmap,nc], projection = ccrs.PlateCarree(central_longitude=180))
        ax.set_extent([lonminf, lonmaxf, latminf, latmaxf], crs = ccrs.PlateCarree())
        ll = ax.contour(lono, lato, varl[nc], np.linspace(-100, 100, 21), transform = ccrs.PlateCarree(), colors = 'k')
        ll.clabel(fmt='%1.0f', fontsize=fontsizexy)
        image = ax.contourf(lono, lato, varf[nc], np.linspace(vmin, vmax, (vint-1)*rt+1), extend = "both", cmap = cmo.balance, transform = ccrs.PlateCarree())        
        ax.add_feature(cfeature.LAND, color = 'w')
        ax.coastlines(lw=1, color = 'grey')        

        nfg += 1
        label = '('+chr(ord("a")+nfg)+')'+labels[nfg]
        ax.text(lonminf-180+dxc*(lonmaxf-lonminf), latmaxf-dyc*(latmaxf-latminf), label, ha = 'left', va = 'top', bbox = bbox, zorder = 30)                
        
        xticks = np.arange(lonminf-360, lonmaxf+361, lonintf)
        yticks = np.arange(latminf-360, latmaxf+361, latintf)                
        gl = ax.gridlines(crs=ccrs.PlateCarree(), linewidth = 0.25, color = 'k')                                    
        gl.xlocator = mticker.FixedLocator(xticks)
        gl.ylocator = mticker.FixedLocator(yticks)        
        if np.mod(nc,3) == 0:
            for latc in range(latminf, latmaxf+1, latintf):
                if int(latc) == 0:
                    txt = '0'
                elif latc > 0:
                    txt = str(int(latc))+'N'
                else:
                    txt = str(int(-latc))+'S'                            
                ax.text(lonminf-180-dyax, latc, txt, ha = 'right', va = 'center', fontsize = fontsizexy)                                    
        
    nn += rmap
    for nm in range(6):
        ax = fig.add_subplot(gs[nn+rmap*int(nm/3):nn+rmap*(int(nm/3)+1),np.mod(nm,3)], projection = ccrs.PlateCarree(central_longitude=180))
        ax.set_extent([lonminf, lonmaxf, latminf, latmaxf], crs = ccrs.PlateCarree())

        ll = ax.contour(lon, lat, am(ua0M[:,ktgt]), np.linspace(-100, 100, 21), transform = ccrs.PlateCarree(), colors = 'k')
        ll.clabel(fmt='%1.0f', fontsize=fontsizexy)
        
        image = ax.contourf(lon, lat, am(uaM[nm,:,ktgt]-ua0M[:,ktgt]), np.linspace(vmin, vmax, (vint-1)*rt+1), extend = "both", cmap = cmo.balance, transform = ccrs.PlateCarree())
        
        nfg += 1
        label = '('+chr(ord("a")+nfg)+')'+labels[nfg]
        ax.text(lonminf-180+dxc*(lonmaxf-lonminf), latmaxf-dyc*(latmaxf-latminf), label, ha = 'left', va = 'top', bbox = bbox, zorder = 30)
        ax.add_feature(cfeature.LAND, color = 'w')
        ax.coastlines(lw=1, color = 'grey')

        xticks = np.arange(lonminf-360, lonmaxf+361, lonintf)
        yticks = np.arange(latminf-360, latmaxf+361, latintf)                        
        gl = ax.gridlines(crs=ccrs.PlateCarree(), linewidth = 0.25, color = 'k')                                    
        gl.xlocator = mticker.FixedLocator(xticks)
        gl.ylocator = mticker.FixedLocator(yticks)         
        if nm >= 3:
            for lonc in range(lonminf, lonmaxf+1, lonintf):
                if np.mod(np.round(lonc), 360) == 0.:                    
                    txt = '0'                        
                elif np.round(lonc) < 180:                    
                    txt = str(int(np.round(lonc)))+'E'
                elif np.round(lonc) > 180:
                    txt = str(int(np.round(360-lonc)))+'W'
                else:
                    txt = '180'
                ax.text(lonc-180, latminf-dxax, txt, ha = 'center', va = 'top', fontsize = fontsizexy)        
            
        if np.mod(nm,3) == 0:
            for latc in range(latminf, latmaxf+1, latintf):
                if int(latc) == 0:
                    txt = '0'
                elif latc > 0:
                    txt = str(int(latc))+'N'
                else:
                    txt = str(int(-latc))+'S'                            
                ax.text(lonminf-180-dyax, latc, txt, ha = 'right', va = 'center', fontsize = fontsizexy)                            
           
            
    cax = fig.add_axes([0.1, 0.04, 0.83, 0.01])
    cbar = plt.colorbar(image, cax = cax, orientation = 'horizontal', ticks = np.linspace(vmin, vmax, vint))
    cax.text(unitx, unity, unitcbr, transform=cax.transAxes)
    
    fig.subplots_adjust(top=0.98, bottom=0.08, left = 0.08, right=0.95, hspace = 0.6, wspace=0.1)            
    if dpi is None:
        plt.savefig(pngfile)
    else:
        plt.savefig(pngfile, dpi = dpi)                
        

    kmax = np.where(lev == 100)[0][0]+1    
    ualat0M = ZonalMean(lon, am(ua0M[:,:kmax], axis=0), lonmin = lonmin, lonmax = lonmax)
    ualatM = ZonalMean(lon, am(uaM[:,:,:kmax], axis=1), lonmin = lonmin, lonmax = lonmax)    
    vlatM = ualatM - ualat0M
    vlat0M = ualat0M[:]

    ultorgd = cmm.intp2D(latoa, 1.e-2*lev0, ulto, lat, lev[:kmax])
    ultargd = cmm.intp2D(lato,  1.e-2*lev0, ulta, lat, lev[:kmax])
    ultcrgd = cmm.intp2D(lato,  1.e-2*lev0, ultc, lat, lev[:kmax])        

    varf = np.vstack(((ultargd-ultorgd)[np.newaxis], (ultcrgd-ultorgd)[np.newaxis], (ultcrgd-ultargd)[np.newaxis], vlatM[:]))
    varl = np.vstack((ultorgd[np.newaxis], ultorgd[np.newaxis], ultargd[np.newaxis], np.tile(vlat0M, (6,1,1))))

    lon, lat, leve, uv0M, uvM = read_amip3D(expid0, expids, 'hs_uva_8dhp_Lanczos.', 'uva', ybgn, yend)
    uvlat0M = ZonalMean(lon, uv0M, lonmin = lonmin, lonmax = lonmax)
    uvlatM = ZonalMean(lon, uvM, lonmin = lonmin, lonmax = lonmax)

    lon, lat, leve, vt0M, vtM = read_amip3D(expid0, expids, 'hs_vta_8dhp_Lanczos.', 'vta', ybgn, yend)
    vtlat0M = ZonalMean(lon, vt0M, lonmin = lonmin, lonmax = lonmax)
    vtlatM = ZonalMean(lon, vtM, lonmin = lonmin, lonmax = lonmax)
    
    Rd = 2.87e2
    Cp = 1.004e3
    fsin = 2*np.pi/4.3082e4*np.sin(np.deg2rad(lat))

    lon, lat, lev, ta0M, taM = read_amip3D(expid0, expids, 'hs_ta.', 'ta', ybgn, yend)
    pt0M = ta0M * ((1.e3/lev)[:,np.newaxis,np.newaxis])**(Rd/Cp)
    ptM = taM * ((1.e3/lev)[:,np.newaxis,np.newaxis])**(Rd/Cp)
    ptlat0M = ZonalMean(lon, pt0M, lonmin = lonmin, lonmax = lonmax)
    ptlatM = ZonalMean(lon, ptM, lonmin = lonmin, lonmax = lonmax)

    dptdzlat0M = (ptlat0M.T[:,2:]-ptlat0M.T[:,:-2]).T/(lev[2:,np.newaxis]-lev[:-2,np.newaxis])
    dptdzlatM = (ptlatM.T[:,2:]-ptlatM.T[:,:-2]).T/(lev[2:,np.newaxis]-lev[:-2,np.newaxis])    
    
    dptdzlat0M = np.ma.concatenate([np.nan*np.ones_like(dptdzlat0M.T[:,:1]), dptdzlat0M.T, np.nan*np.ones_like(dptdzlat0M.T[:,-1:])], axis=1).T
    dptdzlatM = np.ma.concatenate([np.nan*np.ones_like(dptdzlatM.T[:,:1]), dptdzlatM.T, np.nan*np.ones_like(dptdzlatM.T[:,-1:])], axis=1).T    

    k2ke = np.where(np.isin(lev, leve))[0]    
    ezlat0M = - fsin * vtlat0M * ((1.e3/leve)[:,np.newaxis])**(Rd/Cp)/(dptdzlat0M[:,k2ke])
    ezlatM  = - fsin * vtlatM * ((1.e3/leve)[:,np.newaxis])**(Rd/Cp)/(dptdzlatM[:,:,k2ke])
    
    evecx  = am(-uvlatM, axis=1)
    evecx0 = am(-uvlat0M)
    evecy  = am(-ezlatM, axis=1)
    evecy0 = am(-ezlat0M)

    evfct0 = 2.e5
    evfct = 1.e6


    vecx = np.array([np.nan*np.ones_like(evecx0), np.nan*np.ones_like(evecx0), evecx0/R0/np.deg2rad(1)*evfct0, 
                     (evecx[0]-evecx0)/R0/np.deg2rad(1)*evfct, (evecx[1]-evecx0)/R0/np.deg2rad(1)*evfct, (evecx[2]-evecx0)/R0/np.deg2rad(1)*evfct, 
                     (evecx[3]-evecx0)/R0/np.deg2rad(1)*evfct, (evecx[4]-evecx0)/R0/np.deg2rad(1)*evfct, (evecx[5]-evecx0)/R0/np.deg2rad(1)*evfct
    ])

    vecy = np.array([np.nan*np.ones_like(evecy0), np.nan*np.ones_like(evecy0), evecy0*1.e-1*evfct0, 
                     (evecy[0]-evecy0)*1.e-1*evfct, (evecy[1]-evecy0)*1.e-1*evfct, (evecy[2]-evecy0)*1.e-1*evfct, 
                     (evecy[3]-evecy0)*1.e-1*evfct, (evecy[4]-evecy0)*1.e-1*evfct, (evecy[5]-evecy0)*1.e-1*evfct
    ])    

    cefvxs = [0, 0, 1/R0/np.deg2rad(1)*evfct0, 0, 0, 1/R0/np.deg2rad(1)*evfct, 0, 0, 0]
    cefvys = [0, 0, 1.e-1*evfct0, 0, 0, 1.e-1*evfct, 0, 0, 0]    

    lvecxs = [0, 0,     5, 0, 0,     1, 0, 0, 0]
    lvecys = [0, 0, 5.e-3, 0, 0, 1.e-3, 0, 0, 0]

    tvecxs = np.array(lvecxs).astype(str).astype(object) + r" ${\rm m^2 \ s^{-2}}$"; tvecxs[np.array(lvecxs) == 0] = ''
    tvecys = np.array(1.e2*np.array(lvecys)).astype(str).astype(object) + r" ${\rm Pa \ m \ s^{-2}}$"; tvecys[np.array(lvecys) == 0] = ''


       
    labels = ['AMIP-JRA55', 'historical-JRA55', 'historical-AMIP', 'GLB-CNTL', 'PAC-CNTL', '(GLB-PAC)-CNTL', 'WNP-CNTL', 'EQ-CNTL', 'ENP-CNTL']    
    vcols = ['k', 'k', 'g', 'k', 'k', 'k', 'k', 'k', 'k']    
    ncols = 3; nrows = round(np.shape(varf)[0]/ncols)
    vr = [-6, 6, 5]
    levl = np.linspace(-80, 80, 41)
    cmap = cmo.balance    
    yr = [850, 100, 4]
    xr = [-20, 60, 5]        

            
    nf += 1
    pngfile=figdir+'fig'+str(nf)+suff
    print(pngfile)
    plot_ulatlev(pngfile, lev[:kmax], lat, varf, varl, ncols, nrows, vr = vr, levl = levl, cmap = cmap, xr = xr, yr = yr, fsizex = 8, fsizey = 8, labels = labels, vecx = vecx[:,2:], vecy = vecy[:,2:], iskp=5, levv = leve[2:], jskp=1, scale=1, scale_units='xy', vcols = vcols, dpi= dpi, cefvxs = cefvxs, cefvys = cefvys, lvecxs = lvecxs, lvecys = lvecys, tvecxs = tvecxs, tvecys = tvecys)    


    k2ke = np.where(np.isin(lev, leve))[0]    
    evz0M = - fsin[:,np.newaxis] * vt0M * ((1.e3/leve)[:,np.newaxis,np.newaxis])**(Rd/Cp)/(dptdzlat0M[:,k2ke,:,np.newaxis])
    evzM  = - fsin[:,np.newaxis] * vtM * ((1.e3/leve)[:,np.newaxis,np.newaxis])**(Rd/Cp)/(dptdzlatM[:,:,k2ke,:,np.newaxis])        

    lon, lat, lev, ta0M, taM = read_amip3D(expid0, expids, 'hs_ta.', 'ta', ybgn, yend)    
    lon, lat, lev, gha0M, ghaM = read_amip3D(expid0, expids, 'hs_gha.', 'gha', ybgn, yend)

    ta0M  = am(ta0M,  axis=0)
    taM   = am(taM,   axis=1)
    gha0M = am(gha0M, axis=0)
    ghaM  = am(ghaM,  axis=1)
    
    pt0M = ta0M * ((1.e3/lev)[:,np.newaxis,np.newaxis])**(Rd/Cp)
    ptM =  taM  * ((1.e3/lev)[:,np.newaxis,np.newaxis])**(Rd/Cp)        
    
    NN0M = (9.81/pt0M.T[:,:,1:-1] * (pt0M.T[:,:,2:]-pt0M.T[:,:,:-2])/(gha0M.T[:,:,2:]-gha0M.T[:,:,:-2])).T
    NNM = (9.81/ptM.T[:,:,1:-1] * (ptM.T[:,:,2:]-ptM.T[:,:,:-2])/(ghaM.T[:,:,2:]-ghaM.T[:,:,:-2])).T

    NN0M = np.ma.concatenate([np.nan*np.ones_like(NN0M.T[:,:,:1]), NN0M.T, np.nan*np.ones_like(NN0M.T[:,:,-1:])], axis=2).T
    NNM = np.ma.concatenate([np.nan*np.ones_like(NNM.T[:,:,:1]), NNM.T, np.nan*np.ones_like(NNM.T[:,:,-1:])], axis=2).T

    N0M = np.sqrt(np.maximum(NN0M,0.))
    NM  = np.sqrt(np.maximum(NNM,0.))
        
    dbdy0M = (9.81/pt0M.T[:,1:-1] * (pt0M.T[:,2:]-pt0M.T[:,:-2])).T/(R0*np.deg2rad(lat[2:]-lat[:-2])[:,np.newaxis])
    dbdyM = (9.81/ptM.T[:,1:-1] * (ptM.T[:,2:]-ptM.T[:,:-2])).T/(R0*np.deg2rad(lat[2:]-lat[:-2])[:,np.newaxis])    
    dbdy0M = np.ma.concatenate([dbdy0M.T[:,:1], dbdy0M.T, dbdy0M.T[:,-1:]], axis=1).T
    dbdyM = np.ma.concatenate([dbdyM.T[:,:1], dbdyM.T, dbdyM.T[:,-1:]], axis=1).T

    egr0M = 0.31/N0M*np.abs(dbdy0M)*86400.
    egrM = 0.31/NM*np.abs(dbdyM)*86400.    
        
    varf = np.ma.array([
        1.e3*am(evzM[0,:,2] - evz0M[:,2], axis=0), 1.e3*am(evzM[1,:,2] - evz0M[:,2], axis=0), 1.e3*am(evzM[3,:,2] - evz0M[:,2], axis=0), 
        1.e2*(egrM[0][6]-egr0M[6]), 1.e2*(egrM[1][6]-egr0M[6]), 1.e2*(egrM[3][6]-egr0M[6]),
        1.e8*(np.abs(dbdyM[0][6])-np.abs(dbdy0M[6])), 1.e8*(np.abs(dbdyM[1][6])-np.abs(dbdy0M[6])), 1.e8*(np.abs(dbdyM[3][6])-np.abs(dbdy0M[6])), 
        1.e4*(NM[0][6]-N0M[6]), 1.e4*(NM[1][6]-N0M[6]), 1.e4*(NM[3][6]-N0M[6])
    ])

    
    varl = np.ma.array([
        1.e3*am(evz0M[:,2], axis=0), 1.e3*am(evz0M[:,2], axis=0), 1.e3*am(evz0M[:,2], axis=0),        
        1.e2*egr0M[6], 1.e2*egr0M[6], 1.e2*egr0M[6], 
        1.e8*dbdy0M[6], 1.e8*dbdy0M[6], 1.e8*dbdy0M[6], 
        1.e4*N0M[6], 1.e4*N0M[6], 1.e4*N0M[6]
    ])
    

    vr = np.array([
        [-1.2, 1.2, 5], [-1.2, 1.2, 5], [-1.2, 1.2, 5],
        [-8, 8, 5], [-8, 8, 5], [-8, 8, 5], 
        [-6, 6, 5], [-6, 6, 5], [-6, 6, 5],
        [-8, 8, 5], [-8, 8, 5], [-8, 8, 5], 
    ])
    lines = np.array([np.arange(-7,-7+16), np.arange(-7,-7+16), np.arange(-7,-7+16), 
                      np.linspace(0,150,16), np.linspace(0,150,16), np.linspace(0,150,16), 
                      np.linspace(-60,60,16), np.linspace(-60,60,16), np.linspace(-60,60,16), 
                      np.linspace(75,150,16), np.linspace(75,150,16), np.linspace(75,150,16)
    ])
    
    labels = np.tile(np.array([r'$\mathbf{E}}$', 'EGR', r'$|\partial B/\partial y|$', r'$N$']), (3,1)).T.reshape(-1)    
    unitcbrs = [r'[$\times 10^{-1} \ {\rm Pa \ m \ s^{-2}}$]', r'[$\times 10^{-2} \ {\rm day^{-1}}$]', r'[$\times 10^{-8} \ {\rm s^{-2}}$]', r'[$\times 10^{-4} \ {\rm s^{-1}}$]']
    tlabel = ['GLB', 'PAC', 'WNP']
    
    nf += 1
    pngfile=figdir+'fig'+str(nf)+suff
    fm.fig1(pngfile, lon, lat, varf, varfl = varl, lonr = [90, 270, 60], latr = [20, 80, 20], vr=vr, lines = lines, cmap = cmo.balance, flabel = labels, bbox = dict(facecolor='white', alpha=0.9), sngl_cbar = False, fsizey = 5.6, cbrf4 = True, cfig2 = False, dxc = 0.04, dyc = 0.12, top = .99, btm = 0.08, dycb = 0.056, cbt = 0.016, dxcb = 0.25, unitcbr = unitcbrs, unitx = 1.3, unity = -2.8, left = 0.05, right = 0.95, dpi = dpi, tlabel = tlabel, hspace = 0.15, wspace = 0.13)    

    varf = np.ma.array([
        1.e3*am(evzM[2,:,2] - evz0M[:,2], axis=0), 1.e3*am(evzM[4,:,2] - evz0M[:,2], axis=0), 1.e3*am(evzM[5,:,2] - evz0M[:,2], axis=0), 
        1.e2*(egrM[2][6]-egr0M[6]), 1.e2*(egrM[4][6]-egr0M[6]), 1.e2*(egrM[5][6]-egr0M[6]),
        1.e8*(np.abs(dbdyM[2][6])-np.abs(dbdy0M[6])), 1.e8*(np.abs(dbdyM[4][6])-np.abs(dbdy0M[6])), 1.e8*(np.abs(dbdyM[5][6])-np.abs(dbdy0M[6])), 
        1.e4*(NM[0][6]-N0M[6]), 1.e4*(NM[1][6]-N0M[6]), 1.e4*(NM[3][6]-N0M[6])
    ])

    
    varl = np.ma.array([
        1.e3*am(evz0M[:,2], axis=0), 1.e3*am(evz0M[:,2], axis=0), 1.e3*am(evz0M[:,2], axis=0),        
        1.e2*egr0M[6], 1.e2*egr0M[6], 1.e2*egr0M[6], 
        1.e8*dbdy0M[6], 1.e8*dbdy0M[6], 1.e8*dbdy0M[6], 
        1.e4*N0M[6], 1.e4*N0M[6], 1.e4*N0M[6]
    ])
    
    vr = np.array([
        [-1.2, 1.2, 5], [-1.2, 1.2, 5], [-1.2, 1.2, 5],
        [-8, 8, 5], [-8, 8, 5], [-8, 8, 5], 
        [-6, 6, 5], [-6, 6, 5], [-6, 6, 5],
        [-8, 8, 5], [-8, 8, 5], [-8, 8, 5], 
    ])
    
    lines = np.array([np.arange(-7,-7+16), np.arange(-7,-7+16), np.arange(-7,-7+16), 
                      np.linspace(0,150,16), np.linspace(0,150,16), np.linspace(0,150,16), 
                      np.linspace(-60,60,16), np.linspace(-60,60,16), np.linspace(-60,60,16), 
                      np.linspace(75,150,16), np.linspace(75,150,16), np.linspace(75,150,16)
    ])
    

    labels = np.tile(np.array([r'$\mathbf{E}}$', 'EGR', r'$|\partial B/\partial y|$', r'$N$']), (3,1)).T.reshape(-1)    
    unitcbrs = [r'[$\times 10^{-1} \ {\rm Pa \ m \ s^{-2}}$]', r'[$\times 10^{-2} \ {\rm day^{-1}}$]', r'[$\times 10^{-8} \ {\rm s^{-2}}$]', r'[$\times 10^{-4} \ {\rm s^{-1}}$]']
    tlabel = ['GLB-PAC', 'EQ', 'ENP']
    nf = 3
    pngfile=figdir+'figS'+str(nf)+suff
    fm.fig1(pngfile, lon, lat, varf, varfl = varl, lonr = [90, 270, 60], latr = [20, 80, 20], vr=vr, lines = lines, cmap = cmo.balance, flabel = labels, bbox = dict(facecolor='white', alpha=0.9), sngl_cbar = False, fsizey = 5.6, cbrf4 = True, cfig2 = False, dxc = 0.04, dyc = 0.12, top = .99, btm = 0.08, dycb = 0.056, cbt = 0.016, dxcb = 0.25, unitcbr = unitcbrs, unitx = 1.3, unity = -2.8, left = 0.05, right = 0.95, dpi = dpi, tlabel = tlabel, hspace = 0.15, wspace = 0.13)    
    
    varf = np.ma.array([1.e2*(egrcM[2]-egraM[2]), 1.e8*(np.abs(dbdycM[2])-np.abs(dbdyaM[2])), 1.e4*(np.sqrt(dbdzcM[2])-np.sqrt(dbdzaM[2]))])
    varl = np.ma.array([1.e2*egraM[2], 1.e8*dbdyaM[2], 1.e4*np.sqrt(dbdzaM[2])])
    
    vr = np.array([[-8, 8, 5], [-6, 6, 5], [-8, 8, 5]])
    lines = np.array([np.linspace(0,150,16), np.linspace(-60,60,16), np.linspace(75,150,16) ])
    labels = ['EGR', r'$|\partial B/\partial y|$', r'$N$']    
    unitcbrs = [r'[$\times 10^{-2} {\rm day^{-1}}$]', r'[$\times 10^{-8} \ {\rm s^{-2}}$]', r'[$\times 10^{-4} \ {\rm s^{-1}}$]']
    
    nf += 1
    pngfile=figdir+'figS'+str(nf)+suff
    fm.fig1(pngfile, lono, lato, varf, varfl = varl, lonr = [90, 270, 60], latr = [20, 80, 20], vr=vr, lines = lines, cmap = cmo.balance, flabel = labels, bbox = dict(facecolor='white', alpha=0.9), sngl_cbar = False, fsizey = 9, cbrf4 = True, cfig2 = False, dxc = 0.02, dyc = 0.06, top = .96, btm = 0.12, dycb = 0.05, cbt = 0.010, dxcb = 0.25, unitcbr = unitcbrs, unitx = 1.3, unity = -2.6, left = 0.08, right = 0.92, dpi = dpi, hspace = 0.3, wspace = 0.13, ncols = 1)        


def plot_ulatlev(pngfile, lev, lat, varf, varl, ncols, nrows, xr = [-90,90], yr = [1000, 0], vr = [-12, 12, 5], rt = 10, level = [], levl = np.linspace(-100, 100, 101), latl = [], latf = [], fontsize = 10, fsizex = 8, fsizey = 8, cmap = cmo.balance, extend = 'both', sngl_cbar = True, vecx = [], vecy = [], levv = [], scale = 1, scale_units = 'xy', iskp = 1, jskp = 1, vcols = ['w'], unitx = 1.02, unity = -2.9, unitcbr = r'[${\rm m \ s^{-1}}$]', labels = [], bbox = dict(facecolor='white', alpha=0.9), dxc = 0.04, dyc = 0.04, dpi = None, crarw = True, cefvxs = [], cefvys = [], lvecxs = [], lvecys = [], tvecxs = [], tvecys = []):

    nexp = np.shape(varf)[0]
    plt.rcParams['font.size'] = fontsize
    fig = plt.figure(figsize = (fsizex, fsizey))    
    ax = np.reshape(fig.subplots(nrows, ncols), (nrows, ncols))

    jm = np.size(lat); km = np.size(lev)
    X, Y = np.meshgrid(lat, lev)
    if np.size(levv) == 0:
        Xv, Yv = X, Y
        kmv = km
    else:
        Xv, Yv = np.meshgrid(lat, levv)
        kmv = np.size(levv)
    
    if np.size(varl) == jm*km:
        varl = np.tile(varl[np.newaxis].T, nexp).T
    if np.size(latl) == km:
        latl = np.tile(latl[np.newaxis].T, nexp).T
    if np.size(latf) == km:
        latf = np.tile(latf[np.newaxis].T, nexp).T

    if np.size(vecx) == jm*kmv:
        vecx = np.tile(vecx[np.newaxis].T, nexp).T
    if np.size(vecy) == jm*kmv:
        vecy = np.tile(vecy[np.newaxis].T, nexp).T

    if np.size(level) == 0:
        level = np.linspace(vr[0], vr[1], (vr[2]-1)*rt+1)

    if np.size(vcols) == 1:
        vcols = np.tile(vcols, nexp)
        
    
    nn = -1
    for nr in range(nrows):
        for nc in range(ncols):
            nn += 1
            if nn < nexp:
                image = ax[nr,nc].contourf(X, Y, varf[nn], level, extend = extend, cmap = cmap)
                if sngl_cbar == False:
                    cbar = plt.colorbar(image, ax = ax[nr, nc], orientation = 'horizontal', ticks = np.linspace(vr[0], vr[1], vr[2]))
                ll = ax[nr,nc].contour(X, Y, varl[nn], levl, colors = 'k', linewidths = 0.5)
                ll.clabel(fmt='%1.0f', fontsize=fontsize)                
                if np.size(latl) != 0:
                    ax[nr,nc].plot(latl[nn], lev, 'y', linewidth = 2)                    
                if np.size(latf) != 0:
                    ax[nr,nc].plot(latf[nn], lev, 'g', linewidth = 2)                

                if (np.size(vecx) != 0) *  (np.size(vecy) != 0):
                    ax[nr,nc].quiver(Xv[::jskp,::iskp], Yv[::jskp,::iskp], vecx[nn,::jskp,::iskp], vecy[nn,::jskp,::iskp], color = vcols[nn], facecolor = vcols[nn], edgecolor = vcols[nn], linewidths = 1, angles='xy', scale = scale, scale_units = scale_units, headwidth=5, headlength = 5, headaxislength = 1)
                    
                    if crarw:
                        if np.size(cefvxs) > 0:                        
                            if cefvxs[nn] > 0:
                                ax[nr,nc].quiver(-0.1*xr[0]+1.1*xr[1], 0.4*yr[0]+0.6*yr[1], lvecxs[nn]*cefvxs[nn], 0, color = vcols[nn], facecolor = vcols[nn], edgecolor = vcols[nn], linewidths = 1, angles='xy', scale = scale, scale_units = scale_units, headwidth=5, headlength = 5, headaxislength = 1, clip_on = False)
                                ax[nr,nc].text(-0.02*xr[0]+1.02*xr[1], 0.38*yr[0]+0.62*yr[1], tvecxs[nn], color = vcols[nn], ha = 'left', va = 'bottom', fontsize = 10)
                                
                        if np.size(cefvxs) > 0:                                                        
                            if cefvys[nn] > 0:
                                ax[nr,nc].quiver(-0.1*xr[0]+1.1*xr[1], 0.4*yr[0]+0.6*yr[1], 0, lvecys[nn]*cefvys[nn], color = vcols[nn], facecolor = vcols[nn], edgecolor = vcols[nn], linewidths = 1, angles='xy', scale = scale, scale_units = scale_units, headwidth=5, headlength = 5, headaxislength = 1, clip_on = False)
                                ax[nr,nc].text(-0.1*xr[0]+1.1*xr[1], 0.55*yr[0]+0.45*yr[1], tvecys[nn], color = vcols[nn], ha = 'center', va = 'top', rotation = 270, fontsize = 10)
                                    
                                    
                ax[nr,nc].set_xlim(xr[0], xr[1])
                if np.size(xr) == 3:
                    xticks = np.linspace(xr[0], xr[1], xr[2])
                    ax[nr,nc].set_xticks(xticks)
                    xlabels = xticks.astype(int).astype(str).astype(object)+'N'
                    xlabels[xticks == 0] = '0'
                    xlabels[xticks  < 0]  =  (-xticks[xticks < 0]).astype(int).astype(str).astype(object)+'S'
                    ax[nr,nc].set_xticklabels(xlabels)                     
                ax[nr,nc].set_ylim(yr[0], yr[1])
                if np.size(yr) == 3:
                    ax[nr,nc].set_yticks(np.linspace(yr[0], yr[1], yr[2]))
                    ax[nr,nc].set_yticklabels(np.linspace(yr[0], yr[1], yr[2]).astype(int).astype(str).astype(object)+'hPa') 

                if nr != nrows-1:
                    ax[nr,nc].tick_params(labelbottom=False)                    
                if nc != 0:
                    ax[nr,nc].tick_params(labelleft=False)

                ax[nr,nc].set_axisbelow(False)
                ax[nr, nc].grid(True, color="w", linewidth=1.0, alpha = 0.50)                
                if np.size(labels) > 0:
                    label = '('+chr(ord("a")+nn)+')'+labels[nn]
                else:
                    label = '('+chr(ord("a")+nn)+')'

                ax[nr,nc].text(xr[0]+dxc*(xr[1]-xr[0]), yr[1]-dyc*(yr[1]-yr[0]), label, ha = 'left', va = 'top', bbox = bbox, zorder = 30)
            else:
                ax[nr,nc].remove()

    cax = fig.add_axes([0.12, 0.04, 0.82, 0.01])
    cbar = plt.colorbar(image, cax = cax, orientation = 'horizontal', ticks = np.linspace(vr[0], vr[1], vr[2]))
    cax.text(unitx, unity, unitcbr, transform=cax.transAxes)

    fig.subplots_adjust(top=0.98, bottom=0.1, left = 0.10, right=0.92, hspace = 0.1, wspace=0.16)                    
    if dpi is None:
        plt.savefig(pngfile)
    else:
        plt.savefig(pngfile, dpi = dpi)                
             

def read_amip3D(expid0, expids, fbase, varname, ybgn, yend, msk = []):

    nexps = np.size(expids)
    for nexp in range(nexps):
        lon, lat, lev, var0 = mrc.ReadData3DClm(expids[nexp], fbase, varname, ybgn, yend, dirbase = dirbase + '/TSE-C/AMIP/', dirbase0 = dirbase + '/TSE-C/AMIP/')
        if nexp == 0:
            varM = var0[np.newaxis]
        else:
            varM = np.ma.vstack((varM, var0[np.newaxis]))

    varM = omsk(varM, msk)

    lon, lat, lev, var0M = mrc.ReadData3DClm(expid0, fbase, varname, ybgn, yend, dirbase = dirbase + '/TSE-C/AMIP/', dirbase0 = dirbase + '/TSE-C/AMIP/')
    var0M = omsk(var0M, msk)    

    return lon, lat, lev, var0M, varM


def omsk(varM, msk):

    if np.size(msk) > 0:
        msk0 = 1-varM.mask.astype(float)
        if np.shape(msk0) == np.shape(varM):
            varM = varM.data * msk0 * msk - 9.99e33 * (1- msk0 * msk)
        else:
            varM = varM.data * msk - 9.99e33 * (1-msk)
        
        varM = np.ma.masked_array(varM, mask = (varM<-9.99e31), fill_value = -9.99e33)

    return varM

def ZonalMean(lon, var, axis = 0, lonmin = 120, lonmax = 240):

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


def read_sst(expid0, expids, ybgn, yend, msk = []):

    for expid in expids:
        if  'EMS35' in expid:
            area = expid[expid.rfind('_')+1:]
            data = dirbase+'/AGCM/CMIP_BIAS/EMS35_anom/sst_TL159_CMIP6AMIP_1985-2014_annclm_'+area+'_anom_YYYY.dat'            
        for year in range(ybgn, yend+1):
            var00 = np.fromfile(data.replace('YYYY', str(year)), '>f').reshape(12,160,320)[:,::-1]-273.15
            if year == ybgn:
                var0 = var00/(yend-ybgn+1)
            else:
                var0 = var0 + var00/(yend-ybgn+1)
                
        if expid == expids[0]:
            varM = var0[np.newaxis]
        else:
            varM = np.ma.vstack((varM, var0[np.newaxis]))

    varM = omsk(np.ma.array(varM), msk)            
            
    data0 = dirbase+'/obs/SST/input4MIPs/model/sst_TL159_CMIP6AMIP_YYYY.dat'
    for year in range(ybgn, yend+1):
        var00 = np.fromfile(data0.replace('YYYY', str(year)), '>f').reshape(12,160,320)[:,::-1]-273.15
        if year == ybgn:
            var0M = var00/(yend-ybgn+1)
        else:
            var0M = var0M + var00/(yend-ybgn+1)
        
        
    var0M = omsk(np.ma.array(var0M), msk)    

    return var0M, varM

main(dpi = dpi)


