import os
import sys
# import glob
import calendar
# import pygrib
# import netCDF4
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
# import matplotlib.gridspec as gridspec
import matplotlib.ticker as mticker
# import matplotlib.path as mpath
import cartopy.crs as ccrs
# import cartopy.feature as cfeature
import cmocean.cm as cmo
import seaborn as sns
# sys.path.append("./")
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE)
# import uas_mriagcm_diff as sv
# sys.path.append("../SHARED_SCRIPT")
# import map_cartopy as mc
# sys.path.append("../mri-agcm3")
# import grid.mriagcm as ag
# import anl3d2anl2d as a323
# import extract_mnt3d as em3
# import anl2clm as a2c
# import mriagcm3.anl2clm as a2c
import mriagcm3.read_clm as mrc
# sys.path.append("../obs")
# import u850 as uof
# import ua as uof
# import read_wind_module as rw
# sys.path.append("../remap_tools")
# import remap_tools.linear_interpolate as li
# import locale
# locale.setlocale(locale.LC_TIME, 'en_US.UTF-8')

sns.set_theme(style = 'whitegrid', font_scale = 1.)
import cmip.cmip_mm as cmm
import config.config as cf
import config.fig_module as fm

expid0 = 'MPE3_agcm_cntl'
exptyp = 'region'
areasns = ['glb', 'snp', 'exsnp', 'wnp', 'ceq', 'enp']
expids = np.array(list(map(lambda x: 'MPE3_agcm_EMS35_annclm_'+x, areasns))).astype(object)
# exptyp = 'season'
# areasns = ['ann', 'mon']
# # areasns = ['glb', 'snp', 'exsnp']
# expids = np.array(list(map(lambda x: 'MPE3_agcm_EMS35_'+x+'clm_glb', areasns))).astype(object)


ybgn = 1985; yend = 2014
# cobs = True
# cmriesm = True
# cobs = False
# cmriesm = False
cintm = False
# dpi = None
dpi = 900
dirbase = '/data16/theme-C/usijimay'

def main(cintm = False, dpi = 900):
    global lon, lat
    global var0, varm0, varc0
    global var, varm, varc
    global varmo, varco, rvarco

    suff = '.png'    
    # # figdir='fig/251224/SI/'
    # # date = '20260107/'
    # # date = '20260116/'
    # date = '20260413/'        
    # # RES = 'ORG/'
    # # dpi = None
    # RES = 'High/'
    # dpi = 900
    # figdir = 'fig/'+date+RES+'SI/'    
    # if os.path.isdir(figdir) == False:
    #     os.makedirs(figdir)    

    figdir =  cf.figdir(dpi = dpi)    
        
    R0 = 6.375e6    
    lonmin=120; lonmax=240

    lono, lato, toso = cmm.read_sst_amip(ybgn, yend, cann = True, dirbase = dirbase+'/obs')
    
    models, lonuem, latuem, levuem, lonvem, latvem, levvem, lonwem, latwem, levwem, lontem, lattem, levtem, toscfem, uacfem, uaafem, vacfem, vaafem, wacfem, waafem, tacfem, taafem, zgcfem, zgafem, dbdycfem, dbdyafem, dbdzcfem, dbdzafem, egrcfem, egrafem = cmm.read_datas_MM(ybgn, yend, am0, 9999, cem = True, dirbase = dirbase)

    
    nf = 2
    pngfile=figdir+'figS'+str(nf)+suff
    fm.figS1(pngfile, models, lono, lato, toscfem, toso, lonr = [0, 359.9, 120], latr = [-90, 90, 30], vr=[-2.4, 2.4, 5], cmap = cmo.balance, tlabel = models, ncols = 4, fsizey = 10, dpi = dpi)

    ktgt0 = 9    
    nf = 1
    pngfile=figdir+'figS'+str(nf)+suff
    fm.figS2(pngfile, models, lonuem, latuem, uacfem, uaafem, ktgt0, lonr = [90, 270, 60], latr = [-20, 80, 20], vr=[-12, 12, 5], lines = np.linspace(-100, 100, 21), cmap = cmo.balance, tlabel = models, ncols = 4, fsizey = 11, dpi = dpi)
    
    

            


def plot_ulatlev(pngfile, lev, lat, varf, varl, ncols, nrows, xr = [-90,90], yr = [1000, 0], vr = [-12, 12, 5], rt = 10, level = [], levl = np.linspace(-100, 100, 101), latl = [], latf = [], fontsize = 10, fsizex = 8, fsizey = 8, cmap = cmo.balance, extend = 'both', sngl_cbar = True, vecx = [], vecy = [], levv = [], scale = 1, scale_units = 'xy', iskp = 1, jskp = 1, vcols = ['w'], unitx = 1.02, unity = -2.9, unitcbr = r'[${\rm m \ s^{-1}}$]', labels = [], bbox = dict(facecolor='white', alpha=0.7), dxc = 0.04, dyc = 0.04):

    nexp = np.shape(varf)[0]
    plt.rcParams['font.size'] = fontsize
    # fig = plt.figure(figsize = (fsizex, fsizey), constrained_layout=True)
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
                ax[nr,nc].contour(X, Y, varl[nn], levl, colors = 'k', linewidths = 0.5)
                if np.size(latl) != 0:
                    ax[nr,nc].plot(latl[nn], lev, 'y', linewidth = 2)                    
                if np.size(latf) != 0:
                    ax[nr,nc].plot(latf[nn], lev, 'g', linewidth = 2)                

                if (np.size(vecx) != 0) *  (np.size(vecy) != 0):
                    ax[nr,nc].quiver(Xv[::jskp,::iskp], Yv[::jskp,::iskp], vecx[nn,::jskp,::iskp], vecy[nn,::jskp,::iskp], color = vcols[nn], facecolor = vcols[nn], edgecolor = vcols[nn], linewidths = 1, angles='xy', scale = scale, scale_units = scale_units, headwidth=5, headlength = 5, headaxislength = 1)    

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
                    ax[nr,nc].set_xticklabels([])
                if nc != 0:
                    ax[nr,nc].set_yticklabels([])

                if np.size(labels) > 0:
                    label = '('+chr(ord("a")+nn)+')'+labels[nn]
                else:
                    label = '('+chr(ord("a")+nn)+')'

                ax[nr,nc].text(xr[0]+dxc*(xr[1]-xr[0]), yr[1]-dyc*(yr[1]-yr[0]), label, ha = 'left', va = 'top', bbox = bbox)                    
            else:
                ax[nr,nc].remove()
    # plt.show()

    cax = fig.add_axes([0.12, 0.04, 0.82, 0.01])
    cbar = plt.colorbar(image, cax = cax, orientation = 'horizontal', ticks = np.linspace(vr[0], vr[1], vr[2]))
    cax.text(unitx, unity, unitcbr, transform=cax.transAxes)
    # plt.tight_layout()
    
    fig.subplots_adjust(top=0.98, bottom=0.1, left = 0.10, right=0.96, hspace = 0.1, wspace=0.16)                
    plt.savefig(pngfile)
     


# def plots_ulat(expid0, expid, level, suff, lat, vlat0M, vlatM, vlatoM = [], vlatcM = [], cobs = False, cmriesm = False, latminfit=30, latmaxfit=45, xr0 = [-12,12], xr = [6, 12], er = [-0.5, 0.5], dlr = [-2.5,0.5], dsr = [-0.5, 2.]):
    
#     jj = np.where((latminfit<lat)*(lat< latmaxfit))[0]    
#     ams, bms, cms = polyfit2d(lat[jj], vlatM[:,jj])
#     am0, bm0, cm0 = polyfit2d(lat[jj], vlat0M[jj])    
#     vlatMsc = ams[:,np.newaxis] * (lat - bms[:,np.newaxis])**2 + cms[:,np.newaxis]
#     vlat0Msc = am0 * (lat - bm0)**2 + cm0
    
#     if cobs:
#         amo, bmo, cmo = polyfit2d(lat[jj], vlatoM[jj]) 
#         vlatoMsc = amo * (lat - bmo)**2 + cmo
#     else:
#         vlatoMsc = []
#     if cmriesm:        
#         amc, bmc, cmc = polyfit2d(lat[jj], vlatcM[jj])    
#         vlatcMsc = amc * (lat - bmc)**2 + cmc        
#     else:
#         vlatcMsc = []
            
#     label0 = expid0.replace('MPE4_amip_', '')                   
#     labels = []    
#     expnames = expid0
#     for expid in expids:
#         # label = expid
#         # label = expid.replace('MPE4_amip_', '')
#         label = expid.replace('MPE4_amip_mri10_', '')           
#         expnames=expnames+'_'+label
#         labels = np.r_[labels, [label]]
#     if cobs:
#         expnames=expnames+'_JRA55'
#     if cmriesm:
#         expnames=expnames+'_MRIESM2'        
        
#     figdir='fig/'+expnames+'/'    
#     if os.path.isdir(figdir) == False:
#         os.makedirs(figdir)
    

#     pngfile=figdir+expnames+'_U'+str(level)+'-lat_NP'+suff
#     plot_ulat(pngfile, np.r_[labels, [label0]], lat, np.ma.vstack((vlatM, vlat0M[np.newaxis])), xmin=0, xmax=xr0[1], latmin=20, latmax=60, vlatoM = vlatoM, vlatcM = vlatcM)    

#     pngfile=figdir+expnames+'_U'+str(level)+'-lat_TNP'+suff
#     plot_ulat(pngfile, np.r_[labels, [label0]], lat, np.ma.vstack((vlatM, vlat0M[np.newaxis])), xmin=xr0[0], xmax=xr0[1], latmin=-15, latmax=90, vlatoM = vlatoM, vlatcM = vlatcM)

#     pngfile=figdir+expnames+'_U'+str(level)+'-lat_NSP'+suff
#     plot_ulat(pngfile, np.r_[labels, [label0]], lat, np.ma.vstack((vlatM, vlat0M[np.newaxis])), xmin=xr0[0], xmax=xr0[1], latmin=-90, latmax=90, vlatoM = vlatoM, vlatcM = vlatcM)

#     pngfile=figdir+expnames+'_U'+str(level)+'-lat_FNP'+suff    
#     plot_ulat(pngfile, np.r_[labels, [label0]], lat, np.ma.vstack((vlatM, vlat0M[np.newaxis])), xmin=xr[0], xmax=xr[1], latmin=latminfit, latmax=latmaxfit, vlatoM = vlatoM, vlatcM = vlatcM, vlatsM = np.sum(vlatM[1:]-vlat0M, axis=0)+vlat0M)    
    
#     pngfile=figdir+expnames+'_cntl_glb_U'+str(level)+'-lat_FNP'+suff
#     plot_ulat(pngfile, np.r_[labels[:1], [label0]], lat, np.ma.vstack((vlatM[:1], vlat0M[np.newaxis])), xmin=xr[0], xmax=xr[1], latmin=latminfit, latmax=latmaxfit, vlatoM = vlatoM, vlatcM = vlatcM)    
    
#     pngfile=figdir+expnames+'_U'+str(level)+'-lat_fit_NP'+suff
#     plot_ulat(pngfile, np.r_[labels, [label0]], lat, np.ma.vstack((vlatMsc, vlat0Msc[np.newaxis])), xmin=xr[0], xmax=xr[1], latmin=latminfit, latmax=latmaxfit, vlatoM = vlatoMsc, vlatcM = vlatcMsc)    

#     pngfile=figdir+expnames+'_U'+str(level)+'-lat_fit_err_NP'+suff
#     plot_ulat(pngfile, np.r_[labels, [label0]], lat, np.ma.vstack((vlatM, vlat0M[np.newaxis]))-np.ma.vstack((vlatMsc, vlat0Msc[np.newaxis])), xmin=er[0], xmax=er[1], latmin=latminfit, latmax=latmaxfit)    

#     pngfile=figdir+expnames+'_U'+str(level)+'_jetpos_fit_bar_NP'+suff
#     plot_abcbar(pngfile, labels, ams/ams[0] * (bms-bm0), fontsize = 12, abcr = (bms[:1]-bm0) - np.sum(ams[1:]/ams[0] * (bms[1:]-bm0)), ymin = dlr[0], ymax = dlr[1])

#     yy = np.r_[cms[:1]-cm0, (cms[1:]-cm0)+(ams[1:]*bms[1:]**2-am0*bm0**2)-(2*am0*bm0*ams[1:]/ams[0]*(bms[1:]-bm0)+(ams[1:]-am0)*bm0**2)]
#     pngfile=figdir+expnames+'_U'+str(level)+'_jetspeed_fit_bar_NP'+suff
#     plot_abcbar(pngfile, labels, yy, fontsize = 12, abcr = yy[:1]-np.sum(yy[1:]), ymin = dsr[0], ymax = dsr[1])
        

def read_amip2D(expid0, expids, fbase, varname, ybgn, yend, msk = []):

    nexps = np.size(expids)
    for nexp in range(nexps):
        print(expids[nexp])
        lon, lat, var0 = a2c.ReadData2DClm(expids[nexp], fbase, varname, ybgn, yend, dirbase = dirbase + '/TSE-C/AMIP/', dirbase0 = dirbase + '/TSE-C/AMIP/')
        if nexp == 0:
            varM = var0[np.newaxis]
        else:
            varM = np.ma.vstack((varM, var0[np.newaxis]))

    varM = omsk(varM, msk)

    lon, lat, var0M = a2c.ReadData2DClm(expid0, fbase, varname, ybgn, yend, dirbase = dirbase + '/TSE-C/AMIP/', dirbase0 = dirbase + '/TSE-C/AMIP/')
    var0M = omsk(var0M, msk)    

    return lon, lat, var0M, varM

    
def read_amip3D(expid0, expids, fbase, varname, ybgn, yend, msk = []):

    nexps = np.size(expids)
    for nexp in range(nexps):
        print(expids[nexp])
        lon, lat, lev, var0 = a2c.ReadData3DClm(expids[nexp], fbase, varname, ybgn, yend, dirbase = dirbase + '/TSE-C/AMIP/', dirbase0 = dirbase + '/TSE-C/AMIP/')
        if nexp == 0:
            varM = var0[np.newaxis]
        else:
            varM = np.ma.vstack((varM, var0[np.newaxis]))

    varM = omsk(varM, msk)

    lon, lat, lev, var0M = a2c.ReadData3DClm(expid0, fbase, varname, ybgn, yend, dirbase = dirbase + '/TSE-C/AMIP/', dirbase0 = dirbase + '/TSE-C/AMIP/')
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

def am0(var, ns, axis=0):

    if np.size(var) == 0:
        varann = var
    else:
        day = np.array(calendar.mdays[1:])        
        varann = np.average(var, weights = day, axis=axis)

    return varann

def sm(var, axis=0, nr=1):

    if np.size(var) == 0:
        # varsm = var
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


def djfm(var, axis=0, nr=1):

    if np.size(var) == 0:
        vdjf = var
    else:
        nshps = np.arange(np.size(np.shape(var)), dtype = int)    
        vdjf = sm(var, axis=axis).transpose(np.r_[axis, nshps[:axis], nshps[1+axis:]])[0]

    return vdjf

def polyfit2d(x, var, axis=-1):
    shape = np.shape(var)
    # na = np.size(shape)
    # if axis == -1:
    #     axis = na - 1
        
    # nn = np.prod(np.r_[shape[:axis], shape[axis+1:]]).astype(int)
    # var = var.reshape(nn, shape[])
    # for n in range(nn)
    if axis == -1:
        var = var.reshape(np.r_[-1, shape[axis]])        
        nn = np.prod(shape[:axis]).astype(int)
        if nn > 1:
            a = np.zeros(nn)
            b = np.zeros(nn)
            c = np.zeros(nn)            
        for n in range(np.shape(var)[0]):
            a0, b0, c0 = np.polyfit(x, var[n], 2)
            if nn > 1:
                a[n] = a0
                # b[n] = b0
                # c[n] = c0
                b[n] = -0.5*b0/a0
                c[n] = c0 - 0.25*b0*b0/a0
            else:
                a = a0
                b = -0.5*b0/a0
                c = c0 - 0.25*b0*b0/a0
                
    return a, b, c
            
def each_plot_map(expid0, expids, lon, lat, var0M, varM, yearc, lonmin = 120, lonmax = 240, lonint = 30, latmin = 20, latmax = 60, latint = 10, varcM = []):

    imin = np.argmin(np.abs(lon-lonmin)) -1; imax = np.argmin(np.abs(lon-lonmax)) +2
    jmin = np.argmin(np.abs(lat-latmin)) -1; jmax = np.argmin(np.abs(lat-latmax)) +2

    day = np.array(calendar.mdays[1:])
    
    figdir='fig/'+expid0+'/'
    if os.path.isdir(figdir) == False:
        os.makedirs(figdir)
        
    pngfile=figdir+expid0+'_U'+str(level)+'_'+yearc+'_monthly_clm.png'
    if os.path.isfile(pngfile) == False:
        print(pngfile)        
        vr = [-20, 20, 5]# ; rt = 5
        mc.surface_map_mc_ctp(pngfile, lon, lat, var0M, 4, 3, vr=vr, cmap = cmo.balance, extend='both', fontsize=11, labels = calendar.month_abbr[1:], sngl_cbar = True, fsizex = 12)


    nexps = np.size(expids)
    for nexp in range(nexps):
        figdir='fig/'+expids[nexp]+'/'
        if os.path.isdir(figdir) == False:
            os.makedirs(figdir)
            
        pngfile=figdir+expids[nexp]+'_U'+str(level)+'_'+yearc+'_monthly_clm.png'
        if os.path.isfile(pngfile) == False:
            print(pngfile)                    
            vr = [-20, 20, 5]# ; rt = 5
            mc.surface_map_mc_ctp(pngfile, lon, lat, varM[nexp], 4, 3, vr=vr, cmap = cmo.balance, extend='both', fontsize=11, labels = calendar.month_abbr[1:], sngl_cbar = True, fsizex = 12)

        pngfile=figdir+expids[nexp]+'_U'+str(level)+'a_'+expid0 + '_'+yearc+'_monthly_clm.png'
        print(pngfile)                
        vr = [-6, 6, 5]# ; rt = 5
        mc.surface_map_mc_ctp(pngfile, lon, lat, varM[nexp] - var0M, 4, 3, vr=vr, cmap = cmo.balance, extend='both', fontsize=11, labels = calendar.month_abbr[1:], sngl_cbar = True, fsizex = 12)

        pngfile=figdir+expids[nexp]+'_U'+str(level)+'a_NP_'+expid0 + '_'+yearc+'_monthly_clm.png'
        print(pngfile)                
        vr = [-8, 8, 5]# ; rt = 5
        mc.surface_map_mc_ctp(pngfile, lon[imin:imax], lat[jmin:jmax], (varM[nexp]-var0M)[:,jmin:jmax,imin:imax], 4, 3, vr=vr, cmap = cmo.balance, extend='both', fontsize=11, labels = calendar.month_abbr[1:], sngl_cbar = True, fsizex = 12, xlim = [lonmin, lonmax], ylim = [latmin, latmax], lon_interval = lonint, lat_interval = latint)

        pngfile=figdir+expids[nexp]+'_U'+str(level)+'a_NP_'+expid0 + '_'+yearc+'_sclm_clm.png'
        print(pngfile)                
        vr = [-8, 8, 5]# ; rt = 5
        # vr = [-4, 4, 5]# ; rt = 5
        # vr = [-2, 2, 5]# ; rt = 5                
        mc.surface_map_mc_ctp(pngfile, lon[imin:imax], lat[jmin:jmax], (np.sum(np.roll((varM[nexp]-var0M)[:,jmin:jmax,imin:imax].T*day,1,axis=0).reshape(imax-imin,jmax-jmin, 4,3), axis=3)/np.sum(np.roll(day,1).reshape(4,3), axis=1)).T , 2, 2, vr=vr, cmap = cmo.balance, extend='both', fontsize=11, labels = ['DJF', 'MAM', 'JJA', 'SON'], sngl_cbar = True, fsizex = 8, xlim = [lonmin, lonmax], ylim = [latmin, latmax], lon_interval = lonint, lat_interval = latint)


    if np.size(varcM) > 0:
        figdir='fig/'+'MRI-ESM2'+'/'
        if os.path.isdir(figdir) == False:
            os.makedirs(figdir)
            
        pngfile=figdir+'MRI-ESM2'+'_U'+str(level)+'_'+yearc+'_monthly_clm.png'
        if os.path.isfile(pngfile) == False:
            print(pngfile)                    
            vr = [-20, 20, 5]# ; rt = 5
            mc.surface_map_mc_ctp(pngfile, lon, lat, varcM, 4, 3, vr=vr, cmap = cmo.balance, extend='both', fontsize=11, labels = calendar.month_abbr[1:], sngl_cbar = True, fsizex = 12)

        pngfile=figdir+'MRI-ESM2'+'_U'+str(level)+'a_'+expid0 + '_'+yearc+'_monthly_clm.png'
        print(pngfile)                
        vr = [-6, 6, 5]# ; rt = 5
        mc.surface_map_mc_ctp(pngfile, lon, lat, varcM - var0M, 4, 3, vr=vr, cmap = cmo.balance, extend='both', fontsize=11, labels = calendar.month_abbr[1:], sngl_cbar = True, fsizex = 12)

        pngfile=figdir+'MRI-ESM2'+'_U'+str(level)+'a_NP_'+expid0 + '_'+yearc+'_monthly_clm.png'
        print(pngfile)                
        vr = [-8, 8, 5]# ; rt = 5
        mc.surface_map_mc_ctp(pngfile, lon[imin:imax], lat[jmin:jmax], (varcM-var0M)[:,jmin:jmax,imin:imax], 4, 3, vr=vr, cmap = cmo.balance, extend='both', fontsize=11, labels = calendar.month_abbr[1:], sngl_cbar = True, fsizex = 12, xlim = [lonmin, lonmax], ylim = [latmin, latmax], lon_interval = lonint, lat_interval = latint)

        pngfile=figdir+'MRI-ESM2'+'_U'+str(level)+'a_NP_'+expid0 + '_'+yearc+'_sclm_clm.png'
        print(pngfile)                
        vr = [-8, 8, 5]# ; rt = 5
        # vr = [-4, 4, 5]# ; rt = 5
        # vr = [-2, 2, 5]# ; rt = 5                
        mc.surface_map_mc_ctp(pngfile, lon[imin:imax], lat[jmin:jmax], (np.sum(np.roll((varcM-var0M)[:,jmin:jmax,imin:imax].T*day,1,axis=0).reshape(imax-imin,jmax-jmin, 4,3), axis=3)/np.sum(np.roll(day,1).reshape(4,3), axis=1)).T , 2, 2, vr=vr, cmap = cmo.balance, extend='both', fontsize=11, labels = ['DJF', 'MAM', 'JJA', 'SON'], sngl_cbar = True, fsizex = 8, xlim = [lonmin, lonmax], ylim = [latmin, latmax], lon_interval = lonint, lat_interval = latint)
        
        
        
        # if cobs:
        #     pngfile=figdir+expid0+'_'+expids[nexp]+'_U'+str(level)+'a_NP_JRA_'+expid0 + '_'+str(ybgn)+'-'+str(yend)+'_Feb_clm.png'
        #     # vr = [-8, 8, 5]# ; rt = 5
        #     vr = [-4, 4, 5]# ; rt = 5
        #     # vr = [-2, 2, 5]# ; rt = 5
        #     varf = np.ma.array([var0M[1]-rvaroM[1], varM[nexp,1]-rvaroM[1], varM[nexp,1]-var0M[1]])
        #     # mc.surface_map_mc_ctp(pngfile, lon[imin:imax], lat[jmin:jmax], varf[:,jmin:jmax,imin:imax], 1, 3, vr=vr, cmap = cmo.balance, extend='both', fontsize=11, labels = ['COBE-A - JRA55', 'LR-A - JRA55', 'LR-A - COBE-A'], sngl_cbar = True, fsizex = 8, xlim = [lonmin, lonmax], ylim = [latmin, latmax], lon_interval = lonint, lat_interval = latint)
        #     mc.surface_map_mc_ctp(pngfile, lon[imin:imax], lat[jmin:jmax], varf[:,jmin:jmax,imin:imax], 3, 1, vr=vr, cmap = cmo.balance, extend='both', fontsize=11, labels = ['COBE-A - JRA55', 'LR-A - JRA55', 'LR-A - COBE-A'], sngl_cbar = True, fsizex = 3.5, fsizey = 4,xlim = [lonmin, lonmax], ylim = [latmin, latmax], lon_interval = lonint, lat_interval = latint)            



    
def plot_ulat(pngfile, expids, lat, vlatM, xmin = 0, xmax = 10, latmin = 20, latmax = 60, fontsize = 12, vlatoM = [], vlatcM = [], vlatV = [], vlatoV = [], vlatcV = [], vlatsM = []):

    print(pngfile)
    nexps = np.size(expids)
    ncadd = 0
    plt.rcParams['font.size'] = fontsize
    fig, ax = plt.subplots()
        
    if np.size(vlatcM) > 0:
        # ncadd += 1
        # ax.plot(vlatcM, lat, color = cm.viridis(0.), label = 'MRI-ESM2.0', linewidth = 4)
        ax.plot(vlatcM, lat, '--', color = cm.viridis(0.), label = 'MRI-ESM2.0', linewidth = 4)        
        if np.size(vlatcV) > 0:
            ax.fill_betweenx(lat, vlatcM-np.sqrt(vlatcV), vlatcM+np.sqrt(vlatcV), color = cm.viridis(1.), alpha = 0.25)                

    if np.size(vlatsM) > 0:        
        ncadd += 1
        ax.plot(vlatsM, lat, color = cm.viridis((ncadd-1)/(nexps+ncadd-1)), label = 'sum', linewidth = 4)        
    
    for nexp in range(nexps):
        ax.plot(vlatM[nexp], lat, color = cm.viridis((nexp+ncadd)/(nexps+ncadd-1)), label = expids[nexp], linewidth = 4)        
        if np.size(vlatV) > 0:
            ax.fill_betweenx(lat, vlatM[nexp]-np.sqrt(vlatV[nexp]), vlatM[nexp]+np.sqrt(vlatV[nexp]), color = cm.viridis((nexp+1)/(nexps+ncadd)), alpha = 0.25)

        
    if np.size(vlatoM) > 0:
        ax.plot(vlatoM, lat, color = 'k', label = 'JRA55', linewidth = 4)
        # if np.size(vlatoV) > 0:
        #     ax.fill_betweenx(lat, vlatoM-np.sqrt(vlatoV), vlatoM+np.sqrt(vlatoV), 'k', alpha = 0.25)                        
        
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(latmin, latmax)
    # ax.set_xticks(np.arange(np.min(year), np.max(year)+1, xint))
    # ax.set_yticks(np.linspace(ymin,ymax,yint))    
    ax.legend()
    # plt.show()
    plt.savefig(pngfile)


def plot_abcbar(pngfile, labels, abcs, fontsize = 12, abco = [], abcc = [], abcr = [], ymin = 0, ymax = 10):

    print(pngfile)

    plt.rcParams['font.size'] = fontsize
    fig, ax = plt.subplots()    
    nvar = np.size(labels)

    xticks = labels.copy()
    ax.bar(0.5+np.arange(nvar), abcs, color = 'k')        
    if np.size(abcr) > 0:
        nvar = nvar + 1
        xticks = np.r_[xticks, np.array(['Non Linear'])]
        ax.bar(nvar-0.5, abcr, color = 'k')

        
    ax.set_xlim(0, nvar)
    ax.set_ylim(ymin, ymax)
    ax.set_xticks(0.5+np.arange(nvar))
    ax.set_xticklabels(xticks)
    # ax.set_xticks(np.arange(np.min(year), np.max(year)+1, xint))
    # ax.set_yticks(np.linspace(ymin,ymax,yint))    
    # ax.legend()
    # plt.show()
    plt.savefig(pngfile)

def read_sst(expid0, expids, ybgn, yend, msk = []):

    for expid in expids:
        if  'EMS35' in expid:
            area = expid[expid.rfind('_')+1:]
            data = dirbase+'/AGCM/CMIP_BIAS/EMS35_anom_v2/sst_TL159_CMIP6AMIP_1985-2014_annclm_'+area+'_anom_YYYY.dat'            
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

    
main(cintm = cintm, dpi = dpi)

