import os
import numpy as np
import netCDF4
import sys
import calendar
import locale
import matplotlib.pyplot as plt
import cmocean.cm as cmo
# sys.path.append("/home/usijimay/anl_esm/anlpy/SHARED_SCRIPT")
# sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/.")
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)
# print(os.path.dirname(os.path.abspath(__file__))+"/.")
# import config as cf
# sys.path.append(cf.libdir()+"/SHARED_SCRIPT")
import map.map_cartopy as mc
import matplotlib.cm as cm
# import linear_interpolate as li
from scipy import interpolate
from scipy.interpolate import griddata
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
import matplotlib.path as mpath
from mpl_toolkits.mplot3d import Axes3D

def fig1(pngfile, lon, lat, varf, varfl = [], lonr = [120, 210, 30], latr = [20, 50, 10], level = [''], vr=[-999,-999,21], rt = 10, lines = [0.], cmap = cmo.balance, vticklabel = [''], fsizex = 8, fsizey = 3.2, lwdth = 1, cntcol = 'k', dxc = 0.04, dyc = 0.08, dxax = 3., dyax = 1.2, ctght = False, fontsize = 10, unitcbr = r'[${}^\circ$C]', unitx = 1.02, unity = -3, bgc = 'w', sngl_cbar = True, dycb = 0.08, cbt = 0.025, top = 0.96, btm = 0.18, fontsizexy = 10, flabel = [], flabelc = 'k', bbox = [], tlabel = [], dyt = 0.02, clonlatedge = True, cfig2 = False, ncols = 3, dxcb = 0., cbrf4 = False, cbrf5 = False, left = 0.05, right = 0.96, dpi = None, textzo = 30, hspace = None, wspace = None): 

    # dxc = 0.015; dyc = 0.05; no back ground color
    # dxc = 0.04; dyc = 0.10; back ground color    
    print(pngfile)
    R0 = 6.375e6
    lonmin, lonmax, lonint = lonr
    latmin, latmax, latint = latr
    # nrows = int(np.shape(varf)[0]/3)
    # ncols = 3

    nrows = int(np.shape(varf)[0]/ncols)
    
    plt.rcParams['font.size'] = fontsize
    
    fig = plt.figure(figsize = (fsizex, fsizey))
    plt.subplots_adjust(left=left, right = right, top = top, bottom = btm, hspace = hspace, wspace = wspace)                
    # if (hspace is None) * (wspace is None):
    #     plt.subplots_adjust(left=left, right = right, top = top, bottom = btm)        
    # else:
    #     if hspace is None:
    #         plt.subplots_adjust(left=left, right = right, top = top, bottom = btm, wspace = wspace)
    #     elif wspace is None:
    #         plt.subplots_adjust(left=left, right = right, top = top, bottom = btm, hspace = hspace)
    #     else:
    #         plt.subplots_adjust(left=left, right = right, top = top, bottom = btm, hspace = hspace, wspace = wspace)            
            
    # ax = mc.set_maps(fig, nrows, ncols, xlim = [lonmin, lonmax], ylim = [latmin, latmax], lon_interval = lonint, lat_interval = latint, lw_ax = 0.25)
    # if np.size(varfl) > 0:
    #     ax, lls = mc.imcs(ax, lon, lat, varfl, nrows, ncols, level = lines, lfontsize = 9, lwidth = 1.0, cntcol = cntcol)         
    # ax, images, vticks, vticklabels = mc.imcfs(ax, lon, lat, varf, nrows, ncols, vr = vr, rt = rt, level = level, cmap = cmap, vticklabel = vticklabel)
    # ax = fig.subplots(nrows, ncols, subplot_kw = dict(projection = ccrs.PlateCarree(central_longitude=180)))
    ax = fig.subplots(nrows, ncols, subplot_kw = dict(projection = ccrs.PlateCarree(central_longitude=180))).reshape(nrows, ncols)

    nm = 0
    for n in range(nrows):
        for m in range(ncols):
            nm = nm + 1
            if nm > np.shape(varf)[0]:
                continue

            if np.size(varfl) > 0:
                if np.size(lines[0]) > 1:
                    ax0, ll0 = mc.imc(ax[n][m], lon, lat, varfl[nm-1], levels=lines[nm-1], lfontsize = fontsizexy, cntcol = cntcol)
                else:
                    ax0, ll0 = mc.imc(ax[n][m], lon, lat, varfl[nm-1], levels=lines, lfontsize = fontsizexy, cntcol = cntcol)

            if np.size(lines[0]) > 1:                    
                ax0, image0, vtick0, vticklabel0 = mc.imcf(ax[n][m], lon, lat, varf[nm-1], vr=vr[nm-1], rt = rt, cmap = cmap)
            else:
                ax0, image0, vtick0, vticklabel0 = mc.imcf(ax[n][m], lon, lat, varf[nm-1], vr=vr, rt = rt, cmap = cmap)
                
            ax[n][m] = ax0

            ax[n][m].add_feature(cfeature.LAND, color = 'w')
            ax[n][m].coastlines(lw=1, color = 'grey')  
            ax[n][m] = mc.ax_setgrd(ax[n][m], xlim = [lonmin, lonmax], ylim = [latmin, latmax], lon_interval = lonint, lat_interval = latint, lw_ax = 0.25)            
            if nm == 1:
                images = [image0]
                vticks = [vtick0]
                vticklabels = [vticklabel0]                                
            else:
                images.append(image0)
                vticks.append(vtick0)
                vticklabels.append(vticklabel0)                
    nfg = 0    

       
    nfg = 0    
    for nr in range(nrows):
        if sngl_cbar:
            if nr == nrows-1:
                caxl = ax[nr,0].get_position()
                caxr = ax[nr,-1].get_position()
                caxv = ax[nr,0].get_position()
                cax = fig.add_axes([caxl.x0+0.5*dxcb, caxv.y0-dycb,caxr.x1-caxl.x0-dxcb, cbt])        
                cbar = plt.colorbar(images[ncols*nr], cax = cax, orientation = 'horizontal', ticks = vticks[ncols*nr])                
                if unitcbr != '':
                    cax.text(unitx, unity, unitcbr, transform=cax.transAxes)    
                cbars = [cbar]
                if np.size(vticklabels) != 1:
                    if np.size(vticklabels[0]) > 1:                        
                        cbar.ax.set_xticklabels(vticklabels[0])
        elif cbrf4:
            caxl = ax[nr,0].get_position()
            caxr = ax[nr,-1].get_position()
            caxv = ax[nr,0].get_position()
            if nr == nrows -1:
                cax = fig.add_axes([caxl.x0+0.5*dxcb, caxv.y0-dycb,caxr.x1-caxl.x0-dxcb, cbt])
            else:
                cax = fig.add_axes([caxl.x0+0.5*dxcb, caxv.y0-dycb*0.6,caxr.x1-caxl.x0-dxcb, cbt])
                
            cbar = plt.colorbar(images[ncols*nr], cax = cax, orientation = 'horizontal', ticks = vticks[ncols*nr])                
            if np.size(unitcbr) == 1:
                if unitcbr != '':
                    cax.text(unitx, unity, unitcbr, transform=cax.transAxes)                            
            else:
                # cax.text(unitx, unity, unitcbr[nr], transform=cax.transAxes)
                cax.text(unitx, unity, unitcbr[nr], transform=cax.transAxes, ha = 'right')
            cbars = [cbar]
            if np.size(vticklabels) != 1:
                if np.size(vticklabels[0]) > 1:                        
                    cbar.ax.set_xticklabels(vticklabels[ncols*nr])
                        
        elif cbrf5:
            if nr == nrows-1:
                for nc in range(ncols):
                    # cbar = plt.colorbar(images[ncols*nr+nc], ax = ax[nr,nc], orientation = 'horizontal', ticks = vticks[ncols*nr+nc])
                    # if unitcbr != '':
                    #     cax.text(unitx, unity, unitcbr, transform=cax.transAxes)                    
                    cax0 = ax[nr,nc].get_position()
                    cax  = fig.add_axes([cax0.x0+0.5*dxcb, cax0.y0-dycb,cax0.x1-cax0.x0-dxcb, cbt])        
                    cbar = plt.colorbar(images[ncols*nr+nc], cax = cax, orientation = 'horizontal', ticks = vticks[ncols*nr+nc])
                    if np.size(unitcbr) == 1:
                        if unitcbr != '':
                            cax.text(unitx, unity, unitcbr, transform=cax.transAxes)
                    else:
                        cax.text(unitx, unity, unitcbr[nc], transform=cax.transAxes)                            
                    cbars = [cbar]
                    if np.size(vticklabels) != 1:
                        if np.size(vticklabels[0]) > 1:                        
                            cbar.ax.set_xticklabels(vticklabels[ncols*nr+nc])
        else:
            caxl = ax[nr,0].get_position()
            caxr = ax[nr,-1].get_position()
            caxv = ax[nr,0].get_position()
            cax = fig.add_axes([caxl.x0, caxv.y0-0.05,caxr.x1-caxl.x0, 0.01])        
            cbar = plt.colorbar(images[ncols*nr], cax = cax, orientation = 'horizontal', ticks = vticks[ncols*nr])
            if unitcbr != '':
                cax.text(unitx, unity, unitcbr, transform=cax.transAxes)    
            cbars = [cbar]
            if np.size(vticklabels) != 1:
                if vticklabels[0] != ['']:
                    cbar.ax.set_xticklabels(vticklabels[0])

        for nc in range(ncols):
            label = '('+chr(ord("a")+nfg)+')'
            if np.size(flabel) > 0:
                label = label + ' ' + flabel[nfg]

            if np.size(bbox) == 0:
                if bgc == '':
                    ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), label, ha = 'left', va = 'top', color = flabelc, zorder = textzo)
                else:
                    ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), label, ha = 'left', va = 'top', backgroundcolor = bgc, color = flabelc, zorder = textzo)
            else:
                if cfig2:
                    ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), label, ha = 'right', va = 'bottom', bbox = bbox, zorder = textzo)                    
                else:
                    ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), label, ha = 'left', va = 'top', bbox = bbox, zorder = textzo)

            if np.size(tlabel) > 0:
                if np.size(tlabel) == ncols:
                    if nr == 0:
                        ax[nr,nc].text(0.5*(lonr[1]+lonr[0])-180, latr[1]+dyt*(latr[1]-latr[0]), tlabel[nc], ha = 'center', va = 'bottom')
                else:
                    ax[nr,nc].text(0.5*(lonr[1]+lonr[0])-180, latr[1]+dyt*(latr[1]-latr[0]), tlabel[nr*ncols+nc], ha = 'center', va = 'bottom')
                    
            nfg += 1            
            if clonlatedge:
                if nr == nrows-1:
                    for lonc in np.arange(lonr[0], lonr[1]+1, lonr[2]):
                        if np.mod(np.round(lonc), 360) == 0.:                    
                            txt = '0'                        
                        elif np.round(lonc) < 180:                    
                            txt = str(int(np.round(lonc)))+'E'
                        elif np.round(lonc) > 180:
                            txt = str(int(np.round(360-lonc)))+'W'
                        else:
                            txt = '180'
                        # print(lonc, txt)
                        # ax[nr, nc].text(lonc, latr[0], txt, ha = 'center', va = 'top')
                        ax[nr,nc].text(lonc-180, latr[0]-dxax, txt, ha = 'center', va = 'top', fontsize = fontsizexy)
                if nc == 0:                        
                    for latc in np.arange(latr[0], latr[1]+1, latr[2]):
                        if int(latc) == 0:
                            txt = '0'
                        elif latc > 0:
                            txt = str(int(latc))+'N'
                        else:
                            txt = str(int(-latc))+'S'                            
                        ax[nr,nc].text(lonr[0]-180-dyax, latc, txt, ha = 'right', va = 'center', fontsize = fontsizexy)                
            else:
                nfg += 1
                for lonc in np.arange(lonr[0], lonr[1]+1, lonr[2]):
                    if np.round(lonc) < 180:                    
                        txt = str(np.round(lonc))+'E'
                    elif np.round(lonc) > 180:
                        txt = str(np.round(360-lonc))+'W'
                    else:
                        txt = '180'                    
                    # ax[nr, nc].text(lonc, latr[0], txt, ha = 'center', va = 'top')
                    ax[nr,nc].text(lonc-180, latr[0]-dxax, txt, ha = 'center', va = 'top', fontsize = fontsizexy)         
                for latc in np.arange(latr[0], latr[1]+1, latr[2]):
                    # ax[nr, nc].text(lonr[0], latc, str(int(latc))+'N', ha = 'right', va = 'center')
                    ax[nr,nc].text(lonr[0]-180-dyax, latc, str(int(latc))+'N', ha = 'right', va = 'center', fontsize = fontsizexy)                
                    
    if ctght:
        plt.tight_layout()
    plt.savefig(pngfile)
    if dpi is None:
        plt.savefig(pngfile)
    else:
        plt.savefig(pngfile, dpi = dpi)                
    plt.close()        
    

def figS1(pngfile, models, lon, lat, varf, varfl, lonr = [0, 359.9, 120], latr = [-90, 90, 30], level = [''], vr=[-999,-999,21], rt = 10, lines = [0.], cmap = cmo.balance, vticklabel = [''], fsizex = 8, fsizey = 10, lwdth = 1, cntcol = 'k', dxc = 0.04, dyc = 0.08, dxax = 3., dyax = 1.2, ctght = False, fontsize = 10, unitcbr = r'[${}^\circ$C]', unitx = 1.03, unity = -2.0, bgc = 'w', sngl_cbar = True, dycb = 0.04, cbt = 0.012, top = 0.96, btm = 0.08, fontsizexy = 8, flabel = [], flabelc = 'k', bbox = [], tlabel = [], dyt = 0.02, clonlatedge = True, cfig2 = False, ncols = 4, dxcb = 0., cbrf5 = False, left = 0.05, right = 0.96, dpi = None): 


    print(pngfile)
    R0 = 6.375e6
    lonmin, lonmax, lonint = lonr
    latmin, latmax, latint = latr

    # nrows = int(np.shape(varf)[0]/ncols)
    nrows = int((np.shape(models)[0]-1)/ncols)+1
    
    plt.rcParams['font.size'] = fontsize
    
    fig = plt.figure(figsize = (fsizex, fsizey))
    plt.subplots_adjust(left=left, right = right, top = top, bottom = btm)    
    # ax = mc.set_maps(fig, nrows, ncols, xlim = [lonmin, lonmax], ylim = [latmin, latmax], lon_interval = lonint, lat_interval = latint, lw_ax = 0.25)    
    # if np.size(varfl) > 0:        
    #     ax, lls = mc.imcs(ax, lon, lat, varfl, nrows, ncols, level = lines, lfontsize = 9, lwidth = 1.0, cntcol = cntcol)             
    # ax, images, vticks, vticklabels = mc.imcfs(ax, lon, lat, varf, nrows, ncols, vr = vr, rt = rt, level = level, cmap = cmap, vticklabel = vticklabel)

    ax = fig.subplots(nrows, ncols, subplot_kw = dict(projection = ccrs.PlateCarree(central_longitude=180)))
                
    nm = 0
    for n in range(nrows):
        for m in range(ncols):
            nm = nm + 1
            if nm > np.shape(models)[0]:
                continue            

            ax0, image0, vtick0, vticklabel0 = mc.imcf(ax[n][m], lon, lat, varf[models[nm-1]]-varfl, vr=vr, rt = rt, cmap = cmap)
            ax[n][m] = ax0

            ax[n][m].add_feature(cfeature.LAND, color = 'w')
            # ax[n][m].coastlines(lw=2)
            ax[n][m].coastlines(lw=1, color = 'grey')              
            ax[n][m] = mc.ax_setgrd(ax[n][m], xlim = [lonmin, lonmax], ylim = [latmin, latmax], lon_interval = lonint, lat_interval = latint, lw_ax = 0.25)
            
            if nm == 1:
                images = [image0]
                vticks = [vtick0]
                vticklabels = [vticklabel0]                                
            else:
                images.append(image0)
                vticks.append(vtick0)
                vticklabels.append(vticklabel0)                
    nfg = 0    
    for nr in range(nrows):
        if sngl_cbar:
            if nr == nrows-1:
                caxl = ax[nr,0].get_position()
                caxr = ax[nr,-1].get_position()
                caxv = ax[nr,0].get_position()
                cax = fig.add_axes([caxl.x0+0.5*dxcb, caxv.y0-dycb,caxr.x1-caxl.x0-dxcb, cbt])        
                cbar = plt.colorbar(images[ncols*nr], cax = cax, orientation = 'horizontal', ticks = vticks[ncols*nr])                
                if unitcbr != '':
                    cax.text(unitx, unity, unitcbr, transform=cax.transAxes)    
                cbars = [cbar]
                if np.size(vticklabels) != 1:
                    if np.size(vticklabels[0]) > 1:                        
                        cbar.ax.set_xticklabels(vticklabels[0])
        elif cbrf5:
            if nr == nrows-1:
                for nc in range(3):
                    # cbar = plt.colorbar(images[ncols*nr+nc], ax = ax[nr,nc], orientation = 'horizontal', ticks = vticks[ncols*nr+nc])
                    # if unitcbr != '':
                    #     cax.text(unitx, unity, unitcbr, transform=cax.transAxes)                    
                    cax0 = ax[nr,nc].get_position()
                    cax  = fig.add_axes([cax0.x0+0.5*dxcb, cax0.y0-dycb,cax0.x1-cax0.x0-dxcb, cbt])        
                    cbar = plt.colorbar(images[ncols*nr+nc], cax = cax, orientation = 'horizontal', ticks = vticks[ncols*nr+nc])
                    if np.size(unitcbr) == 1:
                        if unitcbr != '':
                            cax.text(unitx, unity, unitcbr, transform=cax.transAxes)
                    else:
                        cax.text(unitx, unity, unitcbr[nc], transform=cax.transAxes)                            
                    cbars = [cbar]
                    if np.size(vticklabels) != 1:
                        if np.size(vticklabels[0]) > 1:                        
                            cbar.ax.set_xticklabels(vticklabels[ncols*nr+nc])
        else:
            caxl = ax[nr,0].get_position()
            caxr = ax[nr,-1].get_position()
            caxv = ax[nr,0].get_position()
            cax = fig.add_axes([caxl.x0, caxv.y0-0.05,caxr.x1-caxl.x0, 0.01])        
            cbar = plt.colorbar(images[ncols*nr], cax = cax, orientation = 'horizontal', ticks = vticks[ncols*nr])
            if unitcbr != '':
                cax.text(unitx, unity, unitcbr, transform=cax.transAxes)    
            cbars = [cbar]
            if np.size(vticklabels) != 1:
                if vticklabels[0] != ['']:
                    cbar.ax.set_xticklabels(vticklabels[0])

        for nc in range(ncols):
            # label = '('+chr(ord("a")+nfg)+')'
            # if np.size(flabel) > 0:
            #     label = label + ' ' + flabel[nfg]

            # if np.size(bbox) == 0:
            #     if bgc == '':
            #         ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), label, ha = 'left', va = 'top', color = flabelc)
            #     else:
            #         ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), label, ha = 'left', va = 'top', backgroundcolor = bgc, color = flabelc)
            # else:
            #     if cfig2:
            #         ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), label, ha = 'right', va = 'bottom', bbox = bbox)                    
            #     else:
            #         ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), label, ha = 'left', va = 'top', bbox = bbox)

            if np.size(tlabel) > 0:
                if np.size(tlabel) == nc:
                    if nr == 0:
                        ax[nr,nc].text(0.5*(lonr[1]+lonr[0])-180, latr[1]+dyt*(latr[1]-latr[0]), tlabel[nc], ha = 'center', va = 'bottom')
                else:
                    ax[nr,nc].text(0.5*(lonr[1]+lonr[0])-180, latr[1]+dyt*(latr[1]-latr[0]), tlabel[nr*ncols+nc], ha = 'center', va = 'bottom')
                
            nfg += 1            
            if clonlatedge:
                if nr == nrows-1:
                    for lonc in np.arange(lonr[0], lonr[1]+1, lonr[2]):
                        if np.mod(np.round(lonc), 360) == 0.:                    
                            txt = '0'                        
                        elif np.round(lonc) < 180:                    
                            txt = str(int(np.round(lonc)))+'E'
                        elif np.round(lonc) > 180:
                            txt = str(int(np.round(360-lonc)))+'W'
                        else:
                            txt = '180'
                        print(lonc, txt)
                        # ax[nr, nc].text(lonc, latr[0], txt, ha = 'center', va = 'top')
                        ax[nr,nc].text(lonc-180, latr[0]-dxax, txt, ha = 'center', va = 'top', fontsize = fontsizexy)
                if nc == 0:                        
                    for latc in np.arange(latr[0], latr[1]+1, latr[2]):
                        if int(latc) == 0:
                            txt = '0'
                        elif latc > 0:
                            txt = str(int(latc))+'N'
                        else:
                            txt = str(int(-latc))+'S'                            
                        ax[nr,nc].text(lonr[0]-180-dyax, latc, txt, ha = 'right', va = 'center', fontsize = fontsizexy)                
            else:
                nfg += 1
                for lonc in np.arange(lonr[0], lonr[1]+1, lonr[2]):
                    if np.round(lonc) < 180:                    
                        txt = str(np.round(lonc))+'E'
                    elif np.round(lonc) > 180:
                        txt = str(np.round(360-lonc))+'W'
                    else:
                        txt = '180'                    
                    # ax[nr, nc].text(lonc, latr[0], txt, ha = 'center', va = 'top')
                    ax[nr,nc].text(lonc-180, latr[0]-dxax, txt, ha = 'center', va = 'top', fontsize = fontsizexy)         
                for latc in np.arange(latr[0], latr[1]+1, latr[2]):
                    # ax[nr, nc].text(lonr[0], latc, str(int(latc))+'N', ha = 'right', va = 'center')
                    ax[nr,nc].text(lonr[0]-180-dyax, latc, str(int(latc))+'N', ha = 'right', va = 'center', fontsize = fontsizexy)                
                    
    if ctght:
        plt.tight_layout()
    # plt.savefig(pngfile)
    if dpi is None:
        plt.savefig(pngfile)
    else:
        plt.savefig(pngfile, dpi = dpi)                
    plt.close()        

def figS2(pngfile, models, lon, lat, varf, varfl, ktgt, lonr = [90, 270, 60], latr = [-20, 80, 20], level = [''], vr=[-999,-999,21], rt = 10, lines = [0.], cmap = cmo.balance, vticklabel = [''], fsizex = 8, fsizey = 10.5, lwdth = 1, cntcol = 'k', dxc = 0.04, dyc = 0.08, dxax = 3., dyax = 1.2, ctght = False, fontsize = 10, unitcbr = r'[${\rm m \ s^{-1}}$]', unitx = 1.02, unity = -1.8, bgc = 'w', sngl_cbar = True, dycb = 0.04, cbt = 0.012, top = 0.98, btm = 0.07, fontsizexy = 8, flabel = [], flabelc = 'k', bbox = [], tlabel = [], dyt = 0.02, clonlatedge = True, cfig2 = False, ncols = 4, dxcb = 0., cbrf5 = False, left = 0.05, right = 0.96, dpi = None):

    print(pngfile)
    R0 = 6.375e6
    lonmin, lonmax, lonint = lonr
    latmin, latmax, latint = latr

    # nrows = int(np.shape(varf)[0]/ncols)
    nrows = int((np.shape(models)[0]-1)/ncols)+1
    
    plt.rcParams['font.size'] = fontsize
    
    fig = plt.figure(figsize = (fsizex, fsizey))
    plt.subplots_adjust(left=left, right = right, top = top, bottom = btm)    
    # ax = mc.set_maps(fig, nrows, ncols, xlim = [lonmin, lonmax], ylim = [latmin, latmax], lon_interval = lonint, lat_interval = latint, lw_ax = 0.25)
    ax = fig.subplots(nrows, ncols, subplot_kw = dict(projection = ccrs.PlateCarree(central_longitude=180)))

    nm = 0
    for n in range(nrows):
        for m in range(ncols):
            nm = nm + 1
            if nm > np.shape(models)[0]:
                continue            

            ax0, ll0 = mc.imc(ax[n][m], lon[models[nm-1]], lat[models[nm-1]], varfl[models[nm-1]][ktgt], levels=lines, lfontsize = fontsize)            
            ax0, image0, vtick0, vticklabel0 = mc.imcf(ax[n][m], lon[models[nm-1]], lat[models[nm-1]], varf[models[nm-1]][ktgt]-varfl[models[nm-1]][ktgt], vr=vr, rt = rt, cmap = cmap)
            ax[n][m] = ax0

            ax[n][m].add_feature(cfeature.LAND, color = 'w')
            # ax[n][m].coastlines(lw=2)
            ax[n][m].coastlines(lw=1, color = 'grey')              
            ax[n][m] = mc.ax_setgrd(ax[n][m], xlim = [lonmin, lonmax], ylim = [latmin, latmax], lon_interval = lonint, lat_interval = latint, lw_ax = 0.25)            
            if nm == 1:
                images = [image0]
                vticks = [vtick0]
                vticklabels = [vticklabel0]                                
            else:
                images.append(image0)
                vticks.append(vtick0)
                vticklabels.append(vticklabel0)                
    nfg = 0    
    for nr in range(nrows):
        if sngl_cbar:
            if nr == nrows-1:
                caxl = ax[nr,0].get_position()
                caxr = ax[nr,-1].get_position()
                caxv = ax[nr,0].get_position()
                cax = fig.add_axes([caxl.x0+0.5*dxcb, caxv.y0-dycb,caxr.x1-caxl.x0-dxcb, cbt])        
                cbar = plt.colorbar(images[ncols*nr], cax = cax, orientation = 'horizontal', ticks = vticks[ncols*nr])                
                if unitcbr != '':
                    cax.text(unitx, unity, unitcbr, transform=cax.transAxes)    
                cbars = [cbar]
                if np.size(vticklabels) != 1:
                    if np.size(vticklabels[0]) > 1:                        
                        cbar.ax.set_xticklabels(vticklabels[0])
        elif cbrf5:
            if nr == nrows-1:
                for nc in range(3):
                    # cbar = plt.colorbar(images[ncols*nr+nc], ax = ax[nr,nc], orientation = 'horizontal', ticks = vticks[ncols*nr+nc])
                    # if unitcbr != '':
                    #     cax.text(unitx, unity, unitcbr, transform=cax.transAxes)                    
                    cax0 = ax[nr,nc].get_position()
                    cax  = fig.add_axes([cax0.x0+0.5*dxcb, cax0.y0-dycb,cax0.x1-cax0.x0-dxcb, cbt])        
                    cbar = plt.colorbar(images[ncols*nr+nc], cax = cax, orientation = 'horizontal', ticks = vticks[ncols*nr+nc])
                    if np.size(unitcbr) == 1:
                        if unitcbr != '':
                            cax.text(unitx, unity, unitcbr, transform=cax.transAxes)
                    else:
                        cax.text(unitx, unity, unitcbr[nc], transform=cax.transAxes)                            
                    cbars = [cbar]
                    if np.size(vticklabels) != 1:
                        if np.size(vticklabels[0]) > 1:                        
                            cbar.ax.set_xticklabels(vticklabels[ncols*nr+nc])
        else:
            caxl = ax[nr,0].get_position()
            caxr = ax[nr,-1].get_position()
            caxv = ax[nr,0].get_position()
            cax = fig.add_axes([caxl.x0, caxv.y0-0.05,caxr.x1-caxl.x0, 0.01])        
            cbar = plt.colorbar(images[ncols*nr], cax = cax, orientation = 'horizontal', ticks = vticks[ncols*nr])
            if unitcbr != '':
                cax.text(unitx, unity, unitcbr, transform=cax.transAxes)    
            cbars = [cbar]
            if np.size(vticklabels) != 1:
                if vticklabels[0] != ['']:
                    cbar.ax.set_xticklabels(vticklabels[0])

        for nc in range(ncols):
            # label = '('+chr(ord("a")+nfg)+')'
            # if np.size(flabel) > 0:
            #     label = label + ' ' + flabel[nfg]

            # if np.size(bbox) == 0:
            #     if bgc == '':
            #         ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), label, ha = 'left', va = 'top', color = flabelc)
            #     else:
            #         ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), label, ha = 'left', va = 'top', backgroundcolor = bgc, color = flabelc)
            # else:
            #     if cfig2:
            #         ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), label, ha = 'right', va = 'bottom', bbox = bbox)                    
            #     else:
            #         ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), label, ha = 'left', va = 'top', bbox = bbox)

            if np.size(tlabel) > 0:
                if np.size(tlabel) == nc:
                    if nr == 0:
                        ax[nr,nc].text(0.5*(lonr[1]+lonr[0])-180, latr[1]+dyt*(latr[1]-latr[0]), tlabel[nc], ha = 'center', va = 'bottom')
                else:
                    ax[nr,nc].text(0.5*(lonr[1]+lonr[0])-180, latr[1]+dyt*(latr[1]-latr[0]), tlabel[nr*ncols+nc], ha = 'center', va = 'bottom')
                
            nfg += 1            
            if clonlatedge:
                if nr == nrows-1:
                    for lonc in np.arange(lonr[0], lonr[1]+1, lonr[2]):
                        if np.mod(np.round(lonc), 360) == 0.:                    
                            txt = '0'                        
                        elif np.round(lonc) < 180:                    
                            txt = str(int(np.round(lonc)))+'E'
                        elif np.round(lonc) > 180:
                            txt = str(int(np.round(360-lonc)))+'W'
                        else:
                            txt = '180'
                        print(lonc, txt)
                        # ax[nr, nc].text(lonc, latr[0], txt, ha = 'center', va = 'top')
                        ax[nr,nc].text(lonc-180, latr[0]-dxax, txt, ha = 'center', va = 'top', fontsize = fontsizexy)
                if nc == 0:                        
                    for latc in np.arange(latr[0], latr[1]+1, latr[2]):
                        if int(latc) == 0:
                            txt = '0'
                        elif latc > 0:
                            txt = str(int(latc))+'N'
                        else:
                            txt = str(int(-latc))+'S'                            
                        ax[nr,nc].text(lonr[0]-180-dyax, latc, txt, ha = 'right', va = 'center', fontsize = fontsizexy)                
            else:
                nfg += 1
                for lonc in np.arange(lonr[0], lonr[1]+1, lonr[2]):
                    if np.round(lonc) < 180:                    
                        txt = str(np.round(lonc))+'E'
                    elif np.round(lonc) > 180:
                        txt = str(np.round(360-lonc))+'W'
                    else:
                        txt = '180'                    
                    # ax[nr, nc].text(lonc, latr[0], txt, ha = 'center', va = 'top')
                    ax[nr,nc].text(lonc-180, latr[0]-dxax, txt, ha = 'center', va = 'top', fontsize = fontsizexy)         
                for latc in np.arange(latr[0], latr[1]+1, latr[2]):
                    # ax[nr, nc].text(lonr[0], latc, str(int(latc))+'N', ha = 'right', va = 'center')
                    ax[nr,nc].text(lonr[0]-180-dyax, latc, str(int(latc))+'N', ha = 'right', va = 'center', fontsize = fontsizexy)                
                    
    if ctght:
        plt.tight_layout()
    # plt.savefig(pngfile)
    if dpi is None:
        plt.savefig(pngfile)
    else:
        plt.savefig(pngfile, dpi = dpi)                
    plt.close()        
    

    
    
# def fig1(pngfile, lon, lat, varf, varfl = [], vartrk = [], lonr = [120, 210, 30], latr = [20, 50, 10], level = [''], vr=[-999,-999,21], rt = 10, lines = [0.], cmap = cmo.balance, vticklabel = [''], fsizex = 8, fsizey = 1.5, lcol = 'k', lwdth = 1, cntcol = 'k', dxc = 0.015, dyc = 0.25, dxax = 1.5, dyax = 1.2, ctght = False, fontsize = 10, unitcbr = r'[${}^\circ$C]', unitx = 1.02, unity = -2.6, ncols = 3, fontsizexy = 8, flabel = [], flabelc = 'k', bbox = [], cbox = False, clonlatedge = True):

#     print(pngfile)
#     R0 = 6.375e6
#     lonmin, lonmax, lonint = lonr
#     latmin, latmax, latint = latr
#     nrows = int(np.shape(varf)[0]/ncols)

#     # ntrck0 = np.shape(vartrk[0])[0]
#     # ntrck  = np.shape(vartrk[1])[0]
    
#     plt.rcParams['font.size'] = fontsize
#     fig = plt.figure(figsize = (fsizex, fsizey))
#     plt.subplots_adjust(left=0.05, right = 0.96, top = 1.1, bottom = 0.1)       
#     ax = mc.set_maps(fig, nrows, ncols, xlim = [lonmin, lonmax], ylim = [latmin, latmax], lon_interval = lonint, lat_interval = latint)
    
#     ax, images, vticks, vticklabels = mc.imcfs(ax, lon, lat, varf, nrows, ncols, vr = vr, rt = rt, level = level, cmap = cmap, vticklabel = vticklabel)
#     if np.size(varfl) > 0:
#         ax, lls = mc.imcs(ax, lon, lat, varfl, nrows, ncols, level = lines, lfontsize = 8, lwidth = 1.0, cntcol = cntcol)     
    
#     nfg = 0    
#     for nr in range(nrows):
#         caxl = ax[nr,0].get_position()
#         caxr = ax[nr,-1].get_position()
#         caxv = ax[nr,0].get_position()
#         # for m0 in range(ncols):
#         #     ax[n1+1,m0].remove()
#         #     cax = fig.add_axes([caxl.x0, 0.5*(caxv.y0+caxv.y1),caxr.x1-caxl.x0,0.01])
#         # cax = fig.add_axes([caxl.x0, caxv.y0-0.02*(nrows-nr)-0.018*nr,caxr.x1-caxl.x0, 0.015])
#         # cax = fig.add_axes([caxl.x0, caxv.y0-0.15,caxr.x1-caxl.x0, 0.03])
#         # cax = fig.add_axes([caxl.x0, caxv.y0-0.2,caxr.x1-caxl.x0, 0.05])
#         cax = fig.add_axes([caxl.x0, caxv.y0-0.16,caxr.x1-caxl.x0, 0.05])                        
#         cbar = plt.colorbar(images[2*nr+1], cax = cax, orientation = 'horizontal', ticks = vticks[2*nr+1])
#         if unitcbr != '':
#             cax.text(unitx, unity, unitcbr, transform=cax.transAxes)    
#         cbars = [cbar]
#         if np.size(vticklabels) != 1:
#             if vticklabels[0] != ['']:
#                 cbar.ax.set_xticklabels(vticklabels[0])
        
#         for nc in range(ncols):
#             # if np.size(vartrk) > 0:
#             if len(vartrk) > 0:                
#                 # ntrs = np.size(vartrk[nc][0])
#                 ntrs = np.shape(vartrk[nc][0])[0]
#                 for ntr in range(ntrs):
#                     ax[nr,nc].plot(vartrk[nc][0][ntr]-180, vartrk[nc][1][ntr], color = lcol, linewidth = lwdth)
#                     # print(vartrk[nc][0][ntr], vartrk[nc][1][ntr])
            
#             # ax[nr,nc].text(lonr[0]-180+5, latr[1]-8-2, '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')
#             # ax[nr,nc].text(lonr[0]-180+5, latr[1]-0.2*(latr[1]-latr[0]), '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')
#             # ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')

#             label = '('+chr(ord("a")+nfg)+')'
#             if np.size(flabel) > 0:
#                 label = label + ' ' + flabel[nfg]

#             if np.size(bbox) == 0:
#                 if bgc == '':
#                     ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), label, ha = 'left', va = 'bottom', color = flabelc)
#                 else:
#                     ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), label, ha = 'left', va = 'bottom', backgroundcolor = bgc, color = flabelc)
#             else:
#                 ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), label, ha = 'left', va = 'bottom', bbox = bbox)
            
#             nfg += 1
#             for lonc in np.arange(lonr[0], lonr[1]+1, lonr[2]):
#                 if np.round(lonc) < 180:                    
#                     txt = str(np.round(lonc))+'E'
#                 elif np.round(lonc) > 180:
#                     txt = str(np.round(360-lonc))+'W'
#                 else:
#                     txt = '180'
#                 if clonlatedge:
#                     if nr == nrows-1:
#                         # ax[nr, nc].text(lonc, latr[0], txt, ha = 'center', va = 'top')                    
#                         ax[nr,nc].text(lonc-180, latr[0]-dxax, txt, ha = 'center', va = 'top', fontsize = fontsizexy)
#                 else:
#                     ax[nr,nc].text(lonc-180, latr[0]-dxax, txt, ha = 'center', va = 'top', fontsize = fontsizexy)
                    
#             for latc in np.arange(latr[0], latr[1]+1, latr[2]):
#                 if clonlatedge:
#                     if nc == 0:                    
#                         # ax[nr, nc].text(lonr[0], latc, str(int(latc))+'N', ha = 'right', va = 'center')
#                         ax[nr,nc].text(lonr[0]-180-dyax, latc, str(int(latc))+'N', ha = 'right', va = 'center', fontsize = fontsizexy)                
#                 else:
#                     ax[nr,nc].text(lonr[0]-180-dyax, latc, str(int(latc))+'N', ha = 'right', va = 'center', fontsize = fontsizexy)                
                    
#     if cbox:
#         ax[-1,-1].plot([143, 200], [25, 25], 'g', linewidth = 3, transform=ccrs.PlateCarree())
#         ax[-1,-1].plot([143, 200], [40, 40], 'g', linewidth = 3, transform=ccrs.PlateCarree())
#         ax[-1,-1].plot([143, 143], [25, 40], 'g', linewidth = 3, transform=ccrs.PlateCarree())
#         ax[-1,-1].plot([200, 200], [25, 40], 'g', linewidth = 3, transform=ccrs.PlateCarree())
        
#     if ctght:
#         plt.tight_layout()
#     plt.savefig(pngfile)
#     plt.close()        

# # def fig06(pngfile, lon, lat, varf, varfl = [], vartrk = [], lonr = [120, 210, 30], latr = [20, 50, 10], level = [''], vr=[-999,-999,21], rt = 10, lines = [0.], cmap = cmo.balance, vticklabel = [''], fsizex = 8, fsizey = 6.5, lcol = 'k', lwdth = 1, cntcol = 'k', dxc = 0.015, dyc = 0.3, dxax = 3., dyax = 1.2, ctght = False, fontsize = 10, unitcbr = r'[${}^\circ$C]', unitx = 0.98, unity = -3., bgc = 'w', sngl_cbar = True):
# def fig2(pngfile, lon, lat, varf, varfl = [], vartrk = [], lonr = [120, 210, 30], latr = [20, 50, 10], level = [''], vr=[-999,-999,21], rt = 10, lines = [0.], cmap = cmo.balance, vticklabel = [''], fsizex = 8, fsizey = 6.5, lcol = 'k', lwdth = 1, cntcol = 'k', dxc = 0.03, dyc = 0.09, dxax = 3., dyax = 1.2, ctght = False, fontsize = 10, unitcbr = r'[${}^\circ$C]', unitx = 0.98, unity = -3., bgc = 'w', sngl_cbar = True, lonv = [], latv = [], varx = [], vary = [], angles = 'xy', scale = 2.e-2, scale_units = 'xy', headwidth = 5, headlength = 3, headaxislength = 2, vcol = 'g', dycb = 0.05, cbt = 0.01, top = 0.98, btm = 0.1, fontsizexy = 8, flabel = [], flabelc = 'k', bbox = [], tlabel = [], dyt = 0.02, clonlatedge = True, cfig2 = True, ncols = 3):   

    
#     # dxc = 0.015; dyc = 0.05; no back ground color
#     # dxc = 0.04; dyc = 0.10; back ground color    
#     print(pngfile)
#     R0 = 6.375e6
#     lonmin, lonmax, lonint = lonr
#     latmin, latmax, latint = latr
#     # nrows = int(np.shape(varf)[0]/3)
#     # ncols = 3

#     nrows = int(np.shape(varf)[0]/ncols)
    
#     plt.rcParams['font.size'] = fontsize
#     # plt.rcParams["figure.subplot.left"]  = 0.02
#     # plt.rcParams["figure.subplot.right"] = 0.98
#     # plt.rcParams["figure.subplot.bottom"] = 0.02
#     # plt.rcParams["figure.subplot.top"] = 0.98

    
#     fig = plt.figure(figsize = (fsizex, fsizey))
#     # fig.subplots_adjust(left=-1., right = 2., top = 2., bottom = -1.)        
#     plt.subplots_adjust(left=0.05, right = 0.96, top = top, bottom = btm)    
#     ax = mc.set_maps(fig, nrows, ncols, xlim = [lonmin, lonmax], ylim = [latmin, latmax], lon_interval = lonint, lat_interval = latint)

#     ax, images, vticks, vticklabels = mc.imcfs(ax, lon, lat, varf, nrows, ncols, vr = vr, rt = rt, level = level, cmap = cmap, vticklabel = vticklabel)
#     if np.size(varfl) > 0:
#         ax, lls = mc.imcs(ax, lon, lat, varfl, nrows, ncols, level = lines, lfontsize = 9, lwidth = 1.0, cntcol = cntcol)     

#     if (np.size(varx) != 0)*(np.size(vary) != 0):
#         if np.size(lonv) == 0:
#             lonv = lon.copy()
#         if np.size(latv) == 0:
#             latv = lat.copy()            
#         ax = mc.vecs(ax, lonv, latv, varx, vary, nrows, ncols, angles = angles, scale = scale, scale_units = scale_units, headwidth = headwidth, headlength = headlength, headaxislength = headaxislength, vcol = vcol)

#         # # X, Y = np.meshgrid(np.linspace(lonr[0], lonr[0]+0.4*lonr[2], 2), np.linspace(latr[0], latr[0]+0.8*latr[2], 2))
#         # # X, Y = np.meshgrid(np.linspace(lonr[0], lonr[0]+0.15*lonr[2], 2), np.linspace(latr[0], latr[0]+0.1*latr[2], 2))
#         # # X, Y = np.meshgrid(np.linspace(180+lonr[0], 180+lonr[0]+0.15*lonr[2], 2), np.linspace(latr[0], latr[0]+0.1*latr[2], 2))
#         # X, Y = np.meshgrid(np.linspace(180+lonr[0], 180+lonr[0]+0.15*lonr[2], 2), np.linspace(latr[1], latr[1]+0.01*latr[2], 2))    
#         # vunit0 = np.zeros((2,2))
#         # vunitx = np.zeros((2,2))
#         # vunity = np.zeros((2,2))        
#         # vunitx[-1,-1] = 0.1/np.cos(np.deg2rad(latr[0]+0.8*latr[2]))
#         # vunity[-1,-1] = 0.1

#         # # ax[0,0].quiver(X, Y, vunitx, vunit0, angles = angles, scale = scale, scale_units = scale_units, headwidth = headwidth, headlength = headlength, headaxislength = headaxislength, color = vcol, transform = ccrs.PlateCarree())
#         # # ax[0,0].quiver(X, Y, vunit0, vunity, angles = angles, scale = scale, scale_units = scale_units, headwidth = headwidth, headlength = headlength, headaxislength = headaxislength, color = vcol, transform = ccrs.PlateCarree())
#         # # ax[0,0].quiver(X, Y, vunit0, vunity, angles = angles, scale = scale, scale_units = scale_units, headwidth = headwidth, headlength = headlength, headaxislength = headaxislength, color = 'g', transform = ccrs.PlateCarree())
#         # ax[0,0].quiver(X, Y, vunit0, vunity, angles = angles, scale = scale, scale_units = scale_units, headwidth = headwidth, headlength = headlength, headaxislength = headaxislength, color = 'g')                        
#         # # ax[0,0].text(lonr[0]+0.2*lonr[2], latr[0]+0.05*latr[2], r': $0.1 \ {\rm m \ s^{-1}}$', transform=ccrs.PlateCarree(), fontsize = 9)
#         # ax[0,0].text(lonr[0]+0.2*lonr[2], latr[1]+0.05*latr[2], r': $0.1 \ {\rm m \ s^{-1}}$', transform=ccrs.PlateCarree(), fontsize = 9)                    

#         cax0 = ax[0,0].get_position()
#         cax = fig.add_axes([cax0.x0, cax0.y1+1.e-3, cax0.x1-cax0.x0, (1-cax0.y1)-2.e-3])
        
#         cax.quiver(0.05*(lonr[1]-lonr[0]), 0.3, 0.1/np.cos(np.deg2rad(35)), 0., angles = angles, scale = scale, scale_units = scale_units, headwidth = headwidth, headlength = headlength, headaxislength = headaxislength, color = 'g')
#         cax.text(0.15*(lonr[1]-lonr[0]), 0.1, r': $0.1 \ {\rm m \ s^{-1}}$', fontsize = fontsize)        
#         cax.set_xlim(0,lonr[1]-lonr[0])
#         cax.set_ylim(0,1)
#         cax.axis("off")
        
#         # ax[0,0].quiver(lonr[0]+0.1*lonr[2], latr[0]+0.2*latr[2], .1, 0., angles = angles, scale = scale, scale_units = scale_units, headwidth = headwidth, headlength = headlength, headaxislength = headaxislength, color = vcol, transform = ccrs.PlateCarree())
#         # ax[0,0].quiver(180+lonr[0]+0.1*lonr[2], latr[0]+0.2*latr[2], .1, 0., angles = angles, scale = scale, scale_units = scale_units, headwidth = headwidth, headlength = headlength, headaxislength = headaxislength, color = vcol)        

        
#     nfg = 0    
#     for nr in range(nrows):
#         if sngl_cbar:
#             if nr == nrows-1:
#                 caxl = ax[nr,0].get_position()
#                 caxr = ax[nr,-1].get_position()
#                 caxv = ax[nr,0].get_position()
#                 # for m0 in range(ncols):
#                 #     ax[n1+1,m0].remove()
#                 #     cax = fig.add_axes([caxl.x0, 0.5*(caxv.y0+caxv.y1),caxr.x1-caxl.x0,0.01])
#                 # cax = fig.add_axes([caxl.x0, caxv.y0-0.02*(nrows-nr)-0.018*nr,caxr.x1-caxl.x0, 0.015])
#                 cax = fig.add_axes([caxl.x0, caxv.y0-dycb,caxr.x1-caxl.x0, cbt])        
#                 cbar = plt.colorbar(images[ncols*nr], cax = cax, orientation = 'horizontal', ticks = vticks[ncols*nr])
#                 if unitcbr != '':
#                     cax.text(unitx, unity, unitcbr, transform=cax.transAxes)    
#                 cbars = [cbar]
#                 if np.size(vticklabels) != 1:
#                     # if vticklabels[0] != ['']:
#                     if np.size(vticklabels[0]) > 1:                        
#                         cbar.ax.set_xticklabels(vticklabels[0])
#         else:
#             caxl = ax[nr,0].get_position()
#             caxr = ax[nr,-1].get_position()
#             caxv = ax[nr,0].get_position()
#             # for m0 in range(ncols):
#             #     ax[n1+1,m0].remove()
#             #     cax = fig.add_axes([caxl.x0, 0.5*(caxv.y0+caxv.y1),caxr.x1-caxl.x0,0.01])
#             # cax = fig.add_axes([caxl.x0, caxv.y0-0.02*(nrows-nr)-0.018*nr,caxr.x1-caxl.x0, 0.015])
#             cax = fig.add_axes([caxl.x0, caxv.y0-0.05,caxr.x1-caxl.x0, 0.01])        
#             cbar = plt.colorbar(images[ncols*nr], cax = cax, orientation = 'horizontal', ticks = vticks[ncols*nr])
#             if unitcbr != '':
#                 cax.text(unitx, unity, unitcbr, transform=cax.transAxes)    
#             cbars = [cbar]
#             if np.size(vticklabels) != 1:
#                 if vticklabels[0] != ['']:
#                     cbar.ax.set_xticklabels(vticklabels[0])
                
#         for nc in range(ncols):
#             # if np.size(vartrk) > 0:
#             if len(vartrk) > 0:                
#                 # ntrs = np.size(vartrk[nc][0])
#                 ntrs = np.shape(vartrk[nc][0])[0]
#                 for ntr in range(ntrs):
#                     ax[nr,nc].plot(vartrk[nc][0][ntr]-180, vartrk[nc][1][ntr], color = lcol, linewidth = lwdth)
#                     # print(vartrk[nc][0][ntr], vartrk[nc][1][ntr])
            
#             # ax[nr,nc].text(lonr[0]-180+5, latr[1]-8-2, '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')
#             # ax[nr,nc].text(lonr[0]-180+5, latr[1]-0.2*(latr[1]-latr[0]), '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')
#             label = '('+chr(ord("a")+nfg)+')'
#             if np.size(flabel) > 0:
#                 label = label + ' ' + flabel[nfg]

#             if np.size(bbox) == 0:
#                 if bgc == '':
#                     ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), label, ha = 'left', va = 'top', color = flabelc)
#                 else:
#                     ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), label, ha = 'left', va = 'top', backgroundcolor = bgc, color = flabelc)
#             else:
                
#                 # ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), label, ha = 'left', va = 'top', bbox = bbox)
#                 if cfig2:
#                     ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), label, ha = 'right', va = 'bottom', bbox = bbox)
#                 else:
#                     ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), label, ha = 'left', va = 'top', bbox = bbox)
#                 # ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), label, ha = 'left', va = 'top', weight = 'bold')                
                

#             if np.size(tlabel) > 0:
#                 if nr == 0:
#                     ax[nr,nc].text(0.5*(lonr[1]+lonr[0])-180, latr[1]+dyt*(latr[1]-latr[0]), tlabel[nc], ha = 'center', va = 'bottom')
                
#             # ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom', backgroundcolor = bgc)            

#             nfg += 1            
#             if clonlatedge:
#                 if nr == nrows-1:
#                     for lonc in np.arange(lonr[0], lonr[1]+1, lonr[2]):
#                         if np.round(lonc) < 180:                    
#                             txt = str(np.round(lonc))+'E'
#                         elif np.round(lonc) > 180:
#                             txt = str(np.round(360-lonc))+'W'
#                         else:
#                             txt = '180'                    
#                         # ax[nr, nc].text(lonc, latr[0], txt, ha = 'center', va = 'top')
#                         ax[nr,nc].text(lonc-180, latr[0]-dxax, txt, ha = 'center', va = 'top', fontsize = fontsizexy)
#                 if nc == 0:                        
#                     for latc in np.arange(latr[0], latr[1]+1, latr[2]):
#                         # ax[nr, nc].text(lonr[0], latc, str(int(latc))+'N', ha = 'right', va = 'center')
#                         ax[nr,nc].text(lonr[0]-180-dyax, latc, str(int(latc))+'N', ha = 'right', va = 'center', fontsize = fontsizexy)                
#             else:
#                 nfg += 1
#                 for lonc in np.arange(lonr[0], lonr[1]+1, lonr[2]):
#                     if np.round(lonc) < 180:                    
#                         txt = str(np.round(lonc))+'E'
#                     elif np.round(lonc) > 180:
#                         txt = str(np.round(360-lonc))+'W'
#                     else:
#                         txt = '180'                    
#                     # ax[nr, nc].text(lonc, latr[0], txt, ha = 'center', va = 'top')
#                     ax[nr,nc].text(lonc-180, latr[0]-dxax, txt, ha = 'center', va = 'top', fontsize = fontsizexy)         
#                 for latc in np.arange(latr[0], latr[1]+1, latr[2]):
#                     # ax[nr, nc].text(lonr[0], latc, str(int(latc))+'N', ha = 'right', va = 'center')
#                     ax[nr,nc].text(lonr[0]-180-dyax, latc, str(int(latc))+'N', ha = 'right', va = 'center', fontsize = fontsizexy)                
                    
#     if ctght:
#         plt.tight_layout()
#     # plt.subplots_adjust(left=0.05, right = 0.95, top = 0.95, bottom = 0.05)
#     # plt.subplots_adjust(left=0., right = 1., top = 1., bottom = 0.)
#     # fig.subplots_adjust(left=-1., right = 2., top = 2., bottom = -1.)         
#     plt.savefig(pngfile)
#     plt.close()        
    

# def fig4(pngfile, lon, lat, varf, varfl = [], vartrk = [], lonr = [120, 240, 30], latr = [15, 45, 15], level = [''], vr=[-999,-999,21], rt = 10, lines = [0.], cmap = cmo.balance, vticklabel = [''], fsizex = 8, fsizey = 5, lcol = 'k', lwdth = 1, cntcol = 'k', dxc = 0.015, dyc = 0.15, dxax = 4., dyax = 1.2, ctght = False, fontsize = 10, unitcbr = r'[m]', unitx = 1.02, unity = -1.5, ncols = 3, vtrtgt = [], xmintrk = 140, xmaxtrk = 170, tmintrks = [16, 16, -.8], tmaxtrks = [21, 21, 3.2], tinttrks = [6, 6, 6], xtgt = 143, xticks = np.linspace(140, 170, 4), xticklabels = ['140E', '150E', '160E', '170E'], latmintrk = 34, latmaxtrk = 40, latinttrk = 4, fontsizexy = 8):

#     print(pngfile)
#     R0 = 6.375e6
#     lonmin, lonmax, lonint = lonr
#     latmin, latmax, latint = latr
#     nrowm = int(np.shape(varf)[0]/ncols)
#     # nrowl = 2
#     # nrows = nrowm + nrowl
#     nrows = nrowm

#     # ntrck0 = np.shape(vartrk[0])[0]
#     # ntrck  = np.shape(vartrk[1])[0]
    
#     plt.rcParams['font.size'] = fontsize
#     fig = plt.figure(figsize = (fsizex, fsizey))
#     # plt.subplots_adjust(left=0.05, right = 0.96, top = 0.98, bottom = 0.1)
#     plt.subplots_adjust(left=0.05, right = 0.96, top = 1.05, bottom = 0.1)            
#     ax = mc.set_maps(fig, nrows, ncols, xlim = [lonmin, lonmax], ylim = [latmin, latmax], lon_interval = lonint, lat_interval = latint)
    
#     ax, images, vticks, vticklabels = mc.imcfs(ax, lon, lat, varf, nrows, ncols, vr = vr, rt = rt, level = level, cmap = cmap, vticklabel = vticklabel)
#     if np.size(varfl) > 0:
#         ax, lls = mc.imcs(ax, lon, lat, varfl, nrows, ncols, level = lines, lfontsize = 8, lwidth = 1.0, cntcol = cntcol)     
    
#     nfg = 0    
#     for nr in range(nrowm):
#         caxl = ax[nr,0].get_position()
#         caxr = ax[nr,-1].get_position()
#         caxv = ax[nr,0].get_position()
#         # for m0 in range(ncols):
#         #     ax[n1+1,m0].remove()
#         #     cax = fig.add_axes([caxl.x0, 0.5*(caxv.y0+caxv.y1),caxr.x1-caxl.x0,0.01])
#         # cax = fig.add_axes([caxl.x0, caxv.y0-0.02*(nrows-nr)-0.018*nr,caxr.x1-caxl.x0, 0.015])
#         # cax = fig.add_axes([caxl.x0, caxv.y0-0.15,caxr.x1-caxl.x0, 0.03])
#         # cax = fig.add_axes([caxl.x0, caxv.y0-0.075,caxr.x1-caxl.x0, 0.02])
#         cax = fig.add_axes([caxl.x0, caxv.y0-0.13,caxr.x1-caxl.x0, 0.03])                        
#         cbar = plt.colorbar(images[2*nr+1], cax = cax, orientation = 'horizontal', ticks = vticks[2*nr+1])
#         if unitcbr != '':
#             cax.text(unitx, unity, unitcbr, transform=cax.transAxes)    
#         cbars = [cbar]
#         if np.size(vticklabels) != 1:
#             if vticklabels[0] != ['']:
#                 cbar.ax.set_xticklabels(vticklabels[0])
        
#         for nc in range(ncols):
#             # if np.size(vartrk) > 0:
#             if len(vartrk) > 0:                
#                 # ntrs = np.size(vartrk[nc][0])
#                 ntrs = np.shape(vartrk[nc][0])[0]
#                 for ntr in range(ntrs):
#                     ax[nr,nc].plot(vartrk[nc][0][ntr]-180, vartrk[nc][1][ntr], color = lcol, linewidth = lwdth)
#                     # print(vartrk[nc][0][ntr], vartrk[nc][1][ntr])

#             if nc < 2:
#                 # nmax = np.where((xtgt<vtrtgt[nc][0][:-1])*(vtrtgt[nc][0][1:]<=xtgt))[0][0]
#                 nmax = np.where((xmintrk<vtrtgt[nc][0][:-1])*(vtrtgt[nc][0][1:]<=xmintrk))[0][0]                
#                 ax[nr,nc].plot(vtrtgt[nc][0][:nmax]-180, vtrtgt[nc][-1][:nmax], color = 'g', linewidth = 2*lwdth)     
#             # ax[nr,nc].text(lonr[0]-180+5, latr[1]-8-2, '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')
#             # ax[nr,nc].text(lonr[0]-180+5, latr[1]-0.2*(latr[1]-latr[0]), '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')
#             # ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')
#             # ax[nr,nc].text(lonr[0]-180+0.03*(lonr[1]-lonr[0]), latr[1]-0.4*(latr[1]-latr[0]), '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom', backgroundcolor = 'w')
#             # ax[nr,nc].text(lonr[0]-180+0.03*(lonr[1]-lonr[0]), latr[1]-0.2*(latr[1]-latr[0]), r'$\ \ \ \ $', ha = 'left', va = 'bottom', backgroundcolor = 'w', fontsize = 5)
#             ax[nr,nc].text(lonr[0]-180+0.03*(lonr[1]-lonr[0]), latr[1]-0.3*(latr[1]-latr[0]), '     ', ha = 'left', va = 'bottom', backgroundcolor = 'w', fontsize = 6)            
#             ax[nr,nc].text(lonr[0]-180+0.025*(lonr[1]-lonr[0]), latr[1]-0.35*(latr[1]-latr[0]),  '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')             
            
#             nfg += 1
#             for lonc in np.arange(lonr[0], lonr[1]+1, lonr[2]):
#                 if np.round(lonc) < 180:                    
#                     txt = str(np.round(lonc))+'E'
#                 elif np.round(lonc) > 180:
#                     txt = str(np.round(360-lonc))+'W'
#                 else:
#                     txt = '180'                    
#                 # ax[nr, nc].text(lonc, latr[0], txt, ha = 'center', va = 'top')
#                 ax[nr,nc].text(lonc-180, latr[0]-dxax, txt, ha = 'center', va = 'top', fontsize = fontsizexy) 
#             for latc in np.arange(latr[0], latr[1]+1, latr[2]):
#                 # ax[nr, nc].text(lonr[0], latc, str(int(latc))+'N', ha = 'right', va = 'center')
#                 ax[nr,nc].text(lonr[0]-180-dyax, latc, str(int(latc))+'N', ha = 'right', va = 'center', fontsize = fontsizexy)                



#     dx0 = R0 * np.cos(np.deg2rad(0.5*(vtrtgt[0][4][:-1]+vtrtgt[0][4][1:]))) * np.deg2rad(np.diff(vtrtgt[0][0]))
#     dy0 = R0 * np.deg2rad(np.diff(vtrtgt[0][4]))       
#     ln0 = np.sqrt(dx0**2+dy0**2)                
#     au0 = ln0/vtrtgt[0][3][1:]
#     # aul  = interpolate.interp1d(0.5*(vtrtgt[0][0][:-1]+vtrtgt[0][0][1:]), aul0, fill_value = 'extrapolate')(0.5*(lonLI[:-1]+lonLI[1:]))
    
#     dx  = R0 * np.cos(np.deg2rad(0.5*(vtrtgt[1][4][:-1]+vtrtgt[1][4][1:]))) * np.deg2rad(np.diff(vtrtgt[1][0]))
#     dy  = R0 * np.deg2rad(np.diff(vtrtgt[1][4]))          
#     ln  = np.sqrt(dx**2+dy**2)                
#     au  = ln/vtrtgt[1][3][1:]
    
#     # lath = interpolate.interp1d(vtrtgt[1][0], vtrtgt[1][4], fill_value = 'extrapolate')(lonLI)
#     # auh  = interpolate.interp1d(0.5*(vtrtgt[1][0][:-1]+vtrtgt[1][0][1:]), auh0, fill_value = 'extrapolate')(0.5*(lonLI[:-1]+lonLI[1:]))        
    
        
#     if np.size(vtrtgt) > 0:
#         for nc in range(3):
#             caxl = ax[0,nc].get_position()
#             axadd0 = fig.add_axes([caxl.x0, 0.4,  caxl.x1-caxl.x0, 0.25])  
#             axadd  = fig.add_axes([caxl.x0, 0.05, caxl.x1-caxl.x0, 0.25])
#             if nc < 2:
#                 axadd0.plot(vtrtgt[nc][0], vtrtgt[nc][-1], 'k', linewidth = 2)
                
#                 axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1], 'k', linewidth = 2)
                
#                 i = np.argmin(np.abs(vtrtgt[nc][0]-xtgt))
#                 tnd = vtrtgt[nc][2][6] - vtrtgt[nc][2][1]
#                 axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'g', linewidth = 2)                
#                 # # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'g', linewidth = 2, label = r'$T^\prime_{ADV}$')                                 
#                 # tnd = vtrtgt[nc][2][7] - vtrtgt[nc][2][1]                
#                 # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], ':g', linewidth = 2)
#                 # tnd = vtrtgt[nc][2][6] - vtrtgt[nc][2][7]                
#                 # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], '--g', linewidth = 2)                                

#                 if nc == 0:
#                     axadd.text(xmintrk+0.01*(xmaxtrk-xmintrk), tmintrks[nc]+0.2*(tmaxtrks[nc]-tmintrks[nc]), r'$T^\prime_{ADV}$', color = 'g', fontsize = fontsize)
            
#                 tnd = vtrtgt[nc][2][2] - vtrtgt[nc][2][6]
#                 axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'r', linewidth = 2)

#                 # tnd = vtrtgt[nc][2][8] - vtrtgt[nc][2][9]
#                 # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], ':r', linewidth = 2)
#                 # tnd = vtrtgt[nc][2][2] - vtrtgt[nc][2][6] - (vtrtgt[nc][2][8] - vtrtgt[nc][2][9])
#                 # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], '--r', linewidth = 2)         

#                 if nc == 0:
#                     axadd.text(xmintrk+0.15*(xmaxtrk-xmintrk), tmintrks[nc]+0.2*(tmaxtrks[nc]-tmintrks[nc]), r'$T_{EDD}$', color = 'r', fontsize = fontsize)
                                    
#                 tnd = vtrtgt[nc][2][3]                
#                 # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'm', linewidth = 2)
#                 axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'c', linewidth = 2)
#                 if nc == 0:
#                     axadd.text(xmintrk+0.01*(xmaxtrk-xmintrk), tmintrks[nc]+0.02*(tmaxtrks[nc]-tmintrks[nc]), r'$T_{SGS}$', color = 'c', fontsize = fontsize)
                    
#                 tnd = vtrtgt[nc][2][4]
#                 axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'b', linewidth = 2)
#                 if nc == 0:
#                     axadd.text(xmintrk+0.15*(xmaxtrk-xmintrk), tmintrks[nc]+0.02*(tmaxtrks[nc]-tmintrks[nc]), r'$T_{SFC}$', color = 'b', fontsize = fontsize)
                    
#                 # tnd = vtrtgt[nc][2][5]
#                 # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'c', linewidth = 2)                                
#             else:
#                 vint0 = interpolate.interp1d(vtrtgt[0][0], vtrtgt[0][-1], fill_value = 'extrapolate')(vtrtgt[1][0])
#                 axadd0.plot(vtrtgt[1][0], vtrtgt[1][-1]-vint0, 'k', linewidth = 2)
                
#                 vint = interpolate.interp1d(vtrtgt[0][0], vtrtgt[0][1], fill_value = 'extrapolate')(vtrtgt[1][0])
#                 axadd.plot(vtrtgt[1][0], vtrtgt[1][1]-vint, 'k', linewidth = 2)

#                 i0 = np.argmin(np.abs(vtrtgt[0][0]-xtgt))
#                 i  = np.argmin(np.abs(vtrtgt[1][0]-xtgt))
#                 dt0 = vtrtgt[1][1][i] - vtrtgt[0][1][i0]
                
#                 tnd0 = vtrtgt[0][2][6] - vtrtgt[0][2][1]
#                 tnd  = vtrtgt[1][2][6] - vtrtgt[1][2][1]                
#                 dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
#                 axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'g', linewidth = 2)

#                 # tnd0 = vtrtgt[0][2][7] - vtrtgt[0][2][1]
#                 # tnd  = vtrtgt[1][2][7] - vtrtgt[1][2][1]
#                 # dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
#                 # axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], ':g', linewidth = 2)

#                 # tnd0 = vtrtgt[0][2][6] - vtrtgt[0][2][7]
#                 # tnd  = vtrtgt[1][2][6] - vtrtgt[1][2][7]
#                 # dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
#                 # axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], '--g', linewidth = 2)

                
#                 tnd0 = vtrtgt[0][2][2] - vtrtgt[0][2][6]
#                 tnd  = vtrtgt[1][2][2] - vtrtgt[1][2][6]                
#                 dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
#                 axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'r', linewidth = 2)

#                 # tnd0 = vtrtgt[0][2][8] - vtrtgt[0][2][9]
#                 # tnd  = vtrtgt[1][2][8] - vtrtgt[1][2][9]
#                 # dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
#                 # axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], ':r', linewidth = 2)

#                 # tnd0 = vtrtgt[0][2][2] - vtrtgt[0][2][6] - (vtrtgt[0][2][8] - vtrtgt[0][2][9])
#                 # tnd  = vtrtgt[1][2][2] - vtrtgt[1][2][6] - (vtrtgt[1][2][8] - vtrtgt[1][2][9])
#                 # dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
#                 # axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], '--r', linewidth = 2)
                
#                 tnd0 = vtrtgt[0][2][3]
#                 tnd  = vtrtgt[1][2][3]
#                 dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
#                 # axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'm', linewidth = 2)
#                 axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'c', linewidth = 2)                

#                 tnd0 = vtrtgt[0][2][4]
#                 tnd  = vtrtgt[1][2][4]
#                 dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
#                 axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'b', linewidth = 2)

#                 # tnd0 = vtrtgt[0][2][5]
#                 # tnd  = vtrtgt[1][2][5]
#                 # dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
#                 # axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'c', linewidth = 2)


#                 dx0 = R0 * np.cos(np.deg2rad(0.5*(vtrtgt[0][4][:-1]+vtrtgt[0][4][1:]))) * np.deg2rad(np.diff(vtrtgt[0][0]))
#                 dy0 = R0 * np.deg2rad(np.diff(vtrtgt[0][4]))       
#                 ln0 = np.sqrt(dx0**2+dy0**2)                
#                 au0 = ln0/vtrtgt[0][3][1:]                
#                 qt0 = np.diff(vtrtgt[0][2][4])/vtrtgt[0][3][1:]

                
#                 dx  = R0 * np.cos(np.deg2rad(0.5*(vtrtgt[1][4][:-1]+vtrtgt[1][4][1:]))) * np.deg2rad(np.diff(vtrtgt[1][0]))
#                 dy  = R0 * np.deg2rad(np.diff(vtrtgt[1][4]))          
#                 ln  = np.sqrt(dx**2+dy**2)                
#                 au  = ln/vtrtgt[1][3][1:]                                
#                 qt  = np.diff(vtrtgt[1][2][4])/vtrtgt[1][3][1:]


#                 ltb = interpolate.interp1d(vtrtgt[0][0], vtrtgt[0][4], fill_value = 'extrapolate')(vtrtgt[1][0])
#                 dxb = R0 * np.cos(np.deg2rad(0.5*(ltb[:-1]+ltb[1:]))) * np.deg2rad(np.diff(vtrtgt[1][0]))
#                 dyb = R0 * np.deg2rad(np.diff(ltb))
#                 lnb = np.sqrt(dxb**2+dyb**2)
#                 aub = interpolate.interp1d(0.5*(vtrtgt[0][0][:-1]+vtrtgt[0][0][1:]), au0, fill_value = 'extrapolate')(0.5*(vtrtgt[1][0][:-1]+vtrtgt[1][0][1:]))
#                 qtb = interpolate.interp1d(0.5*(vtrtgt[0][0][:-1]+vtrtgt[0][0][1:]), qt0, fill_value = 'extrapolate')(0.5*(vtrtgt[1][0][:-1]+vtrtgt[1][0][1:]))
                
#                 dtndq = np.zeros(i+1)
#                 dtndu = np.zeros(i+1)
#                 dtndl = np.zeros(i+1)                
#                 for ii in range(i):
#                     # dtndq[ii+1] = dtndq[ii] - (qt[i-ii-1] - qtb[i-ii-1])*lnb[i-ii-1]/aub[i-ii-1]
#                     dtndq[ii+1] = dtndq[ii] - (qt[i-ii-1] - qtb[i-ii-1])*lnb[i-ii-1]/au[i-ii-1]                    
#                     dtndu[ii+1] = dtndu[ii] - qtb[i-ii-1]*lnb[i-ii-1]*(1/au[i-ii-1]-1/aub[i-ii-1])
#                     # dtndl[ii+1] = dtndl[ii] - qtb[i-ii-1]*(ln[i-ii-1]-lnb[i-ii-1])/aub[i-ii-1]
#                     dtndl[ii+1] = dtndl[ii] - qtb[i-ii-1]*(ln[i-ii-1]-lnb[i-ii-1])/au[i-ii-1]                     

#                 xx = 0.5*(vtrtgt[1][0][:-1]+vtrtgt[1][0][1:])[:i+1][::-1]
                
#                 axadd.plot(xx, dt0+dtndq, ':b', linewidth = 2)
#                 axadd.plot(xx, dt0+dtndu, '--b', linewidth = 2)
#                 axadd.plot(xx, dt0+dtndl, 'b', linestyle = 'dashdot', linewidth = 2)


#                 di  = np.argmin(np.abs(vtrtgt[1][0]-xmintrk)) - i
#                 dtndq = np.zeros(di+1)
#                 dtndu = np.zeros(di+1)
#                 dtndl = np.zeros(di+1)                
#                 for ii in range(di):
#                     # dtndq[ii+1] = dtndq[ii] + (qt[i+ii] - qtb[i+ii])*lnb[i+ii]/aub[i+ii]
#                     dtndq[ii+1] = dtndq[ii] + (qt[i+ii] - qtb[i+ii])*lnb[i+ii]/au[i+ii]                    
#                     dtndu[ii+1] = dtndu[ii] + qtb[i+ii]*lnb[i+ii]*(1/au[i+ii]-1/aub[i+ii])
#                     # dtndl[ii+1] = dtndl[ii] + qtb[i+ii]*(ln[i+ii]-lnb[i+ii])/aub[i+ii]
#                     dtndl[ii+1] = dtndl[ii] + qtb[i+ii]*(ln[i+ii]-lnb[i+ii])/au[i+ii]                     

#                 xx = 0.5*(vtrtgt[1][0][:-1]+vtrtgt[1][0][1:])[i:i+di+1]
#                 axadd.plot(xx, dt0+dtndq, ':b', linewidth = 2)
#                 axadd.plot(xx, dt0+dtndu, '--b', linewidth = 2)
#                 axadd.plot(xx, dt0+dtndl, 'b', linestyle = 'dashdot', linewidth = 2)
                
#             axadd.set_xlim(xmintrk, xmaxtrk)
#             axadd.set_xticks(xticks)
#             axadd.set_xticklabels(xticklabels)                        
#             axadd.set_ylim(tmintrks[nc], tmaxtrks[nc])
#             axadd.set_yticks(np.linspace(tmintrks[nc], tmaxtrks[nc], tinttrks[nc]))
#             # axadd.text(xmintrk+dxc*(xmaxtrk-xmintrk), tmaxtrks[nc]-0.12*(tmaxtrks[nc]-tmintrks[nc]), '('+chr(ord("a")+nc+3)+')', ha = 'left', va = 'bottom')
#             # axadd.text(xmintrk+dxc*(xmaxtrk-xmintrk), tmaxtrks[nc]-dyc*(tmaxtrks[nc]-tmintrks[nc]), '('+chr(ord("a")+nc+3)+')', ha = 'left', va = 'bottom')
#             axadd.text(xmintrk+dxc*(xmaxtrk-xmintrk), tmaxtrks[nc]-dyc*(tmaxtrks[nc]-tmintrks[nc]), '('+chr(ord("a")+nc+6)+')', ha = 'left', va = 'bottom')                        
#             # axadd.text(xmintrk+dxc*(xmaxtrk-xmintrk), tmintrks[nc]+0.02*(tmaxtrks[nc]-tmintrks[nc]), '('+chr(ord("a")+nc+3)+')', ha = 'left', va = 'bottom')
#             axadd.text(xmintrk-0.15*(xmaxtrk-xmintrk), tmaxtrks[nc]+0.05*(tmaxtrks[nc]-tmintrks[nc]), r'[${}^\circ$C]', ha = 'left', va = 'bottom')

#             axadd0.set_xlim(xmintrk, xmaxtrk)
#             axadd0.set_xticks(xticks)
#             axadd0.set_xticklabels(xticklabels)
#             if nc == 2:
#                 ymin = -4; ymax = 2; yint = 4
#             else:
#                 ymin = latmintrk; ymax = latmaxtrk; yint = latinttrk

#             axadd0.set_ylim(ymin, ymax)
#             axadd0.set_yticks(np.linspace(ymin, ymax, yint))
#             if nc == 2:
#                 ylabel = np.linspace(ymin, ymax, yint).astype(int).astype(str).astype(object) + r'${}^\circ$'
#             else:
#                 # ylabel = np.linspace(ymin, ymax, yint).astype(int).astype(str).astype(object) + r'${}^\circ$ N'
#                 ylabel = np.linspace(ymin, ymax, yint).astype(int).astype(str).astype(object) + 'N'                                
#             axadd0.set_yticklabels(ylabel)
            
#             axadd0.text(xmintrk+dxc*(xmaxtrk-xmintrk), ymax-dyc*(ymax-ymin), '('+chr(ord("a")+nc+3)+')', ha = 'left', va = 'bottom')            
#             # axadd0.text(xmintrk-0.1*(xmaxtrk-xmintrk), ymax+0.05*(ymax-ymin), '[N]', ha = 'left', va = 'bottom')   
#             # if nc == 0:
#             #     axadd.legend()
            
            
#         for nc in range(3):
#             for nr in range(nrowl):
#                 ax[nrowm+nr,nc].remove()
            
#     if ctght:
#         plt.tight_layout()
#     plt.savefig(pngfile)
#     plt.close()        


def fig4(pngfile, lon, lat, varf, varfl = [], vartrk = [], lonr = [120, 240, 30], latr = [15, 45, 15], level = [''], vr=[-999,-999,21], rt = 10, lines = [0.], cmap = cmo.balance, vticklabel = [''], fsizex = 8, fsizey = 5, lcol = 'k', lwdth = 1, cntcol = 'k', dxc = 0.015, dyc = 0.15, dycb = 0.08, cbt = 0.03, dxax = 4., dyax = 1.2, ctght = False, fontsize = 10, unitcbr = r'[m]', unitx = 1.02, unity = -1.5, ncols = 2, vtrtgt = [], xmintrk = 140, xmaxtrk = 170, tmintrks = [16, 16, -.8], tmaxtrks = [21, 21, 3.2], tinttrks = [6, 6, 6], xtgt = 143, xticks = np.linspace(140, 170, 4), xticklabels = ['140E', '150E', '160E', '170E'], latmintrk = 34, latmaxtrk = 40, latinttrk = 4, fontsizexy = 8, flabel = [], clonlatedge = True):

    
    print(pngfile)
    R0 = 6.375e6
    lonmin, lonmax, lonint = lonr
    latmin, latmax, latint = latr
    nrowm = int(np.shape(varf)[0]/ncols)
    # nrowl = 2
    # nrows = nrowm + nrowl
    nrows = nrowm
    
    plt.rcParams['font.size'] = fontsize
    fig = plt.figure(figsize = (fsizex, fsizey))
    # plt.subplots_adjust(left=0.05, right = 0.96, top = 0.98, bottom = 0.1)
    if nrows == 2:
        plt.subplots_adjust(left=0.05, right = 0.96, top = .95, bottom = 0.15)
    elif nrows == 1:
        plt.subplots_adjust(left=0.05, right = 0.96, top = .95, bottom = 0.15)   
    else:
        plt.subplots_adjust(left=0.05, right = 0.96, top = 1.5, bottom = 0.1)
        
        
    ax = mc.set_maps(fig, nrows, ncols, xlim = [lonmin, lonmax], ylim = [latmin, latmax], lon_interval = lonint, lat_interval = latint)
    
    ax, images, vticks, vticklabels = mc.imcfs(ax, lon, lat, varf, nrows, ncols, vr = vr, rt = rt, level = level, cmap = cmap, vticklabel = vticklabel)
    if np.size(varfl) > 0:

        ax, lls = mc.imcs(ax, lon, lat, varfl, nrows, ncols, level = lines, lfontsize = 8, lwidth = 1.0, cntcol = cntcol)     

    caxl = ax[-1,0].get_position()
    caxr = ax[-1,-1].get_position()
    caxv = ax[-1,0].get_position()
    cax = fig.add_axes([caxl.x0, caxv.y0-dycb,caxr.x1-caxl.x0, cbt])
    cbar = plt.colorbar(images[-1], cax = cax, orientation = 'horizontal', ticks = vticks[-1])        
    if unitcbr != '':
        cax.text(unitx, unity, unitcbr, transform=cax.transAxes)    
    # cbars = [cbar]
    # if np.size(vticklabels) != 1:
    #     if vticklabels[0] != ['']:
    #         cbar.ax.set_xticklabels(vticklabels[0])
        
    nfg = 0    
    for nr in range(nrowm):        
        for nc in range(ncols):
            # if np.size(vartrk) > 0:
            if len(vartrk) > 0:                
                # ntrs = np.size(vartrk[nc][0])
                ntrs = np.shape(vartrk[nfg][0])[0]
                for ntr in range(ntrs):
                    ax[nr,nc].plot(vartrk[nfg][0][ntr]-180, vartrk[nfg][1][ntr], color = lcol, linewidth = lwdth)
                    # print(vartrk[nc][0][ntr], vartrk[nc][1][ntr])

                nmax = np.where((xmintrk<vtrtgt[nfg][0][:-1])*(vtrtgt[nfg][0][1:]<=xmintrk))[0][0]                
                ax[nr,nc].plot(vtrtgt[nfg][0][:nmax]-180, vtrtgt[nfg][-1][:nmax], color = 'g', linewidth = 2)
            # ax[nr,nc].text(lonr[0]-180+5, latr[1]-8-2, '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')
            # ax[nr,nc].text(lonr[0]-180+5, latr[1]-0.2*(latr[1]-latr[0]), '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')
            # ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')
            # ax[nr,nc].text(lonr[0]-180+0.03*(lonr[1]-lonr[0]), latr[1]-0.4*(latr[1]-latr[0]), '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom', backgroundcolor = 'w')
            # ax[nr,nc].text(lonr[0]-180+0.03*(lonr[1]-lonr[0]), latr[1]-0.2*(latr[1]-latr[0]), r'$\ \ \ \ $', ha = 'left', va = 'bottom', backgroundcolor = 'w', fontsize = 5)
            # ax[nr,nc].text(lonr[0]-180+0.03*(lonr[1]-lonr[0]), latr[1]-0.3*(latr[1]-latr[0]), '     ', ha = 'left', va = 'bottom', backgroundcolor = 'w', fontsize = 6)

            label = '('+chr(ord("a")+nfg)+')'
            if np.size(flabel) > 0:
                label = label + ' ' + flabel[nfg]
            
            ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]),  label, ha = 'left', va = 'bottom')             
            
            # nfg += 1
            # for lonc in np.arange(lonr[0], lonr[1]+1, lonr[2]):
            #     if np.round(lonc) < 180:                    
            #         txt = str(np.round(lonc))+'E'
            #     elif np.round(lonc) > 180:
            #         txt = str(np.round(360-lonc))+'W'
            #     else:
            #         txt = '180'                    
            #     # ax[nr, nc].text(lonc, latr[0], txt, ha = 'center', va = 'top')
            #     # ax[nr,nc].text(lonc-180, latr[0]-dxax, txt, ha = 'center', va = 'top', fontsize = fontsizexy)
            #     ax[nr,nc].text(lonc-180, dxax*latr[0]+(1-dxax)*latr[1], txt, ha = 'center', va = 'top', fontsize = fontsizexy) 
            # for latc in np.arange(latr[0], latr[1]+1, latr[2]):
            #     # ax[nr, nc].text(lonr[0], latc, str(int(latc))+'N', ha = 'right', va = 'center')
            #     ax[nr,nc].text((lonr[0]-180)*dyax+(lonr[1]-180)*(1-dyax), latc, str(int(latc))+'N', ha = 'right', va = 'center', fontsize = fontsizexy)                

            nfg += 1
            if clonlatedge:
                if nr == nrows-1:
                    for lonc in np.arange(lonr[0], lonr[1]+1, lonr[2]):
                        if np.round(lonc) < 180:                    
                            txt = str(np.round(lonc))+'E'
                        elif np.round(lonc) > 180:
                            txt = str(np.round(360-lonc))+'W'
                        else:
                            txt = '180'                    
                        # ax[nr, nc].text(lonc, latr[0], txt, ha = 'center', va = 'top')
                        ax[nr,nc].text(lonc-180, latr[0]-dxax, txt, ha = 'center', va = 'top', fontsize = fontsizexy)
                if nc == 0:                        
                    for latc in np.arange(latr[0], latr[1]+1, latr[2]):
                        # ax[nr, nc].text(lonr[0], latc, str(int(latc))+'N', ha = 'right', va = 'center')
                        ax[nr,nc].text(lonr[0]-180-dyax, latc, str(int(latc))+'N', ha = 'right', va = 'center', fontsize = fontsizexy)                
            else:
                for lonc in np.arange(lonr[0], lonr[1]+1, lonr[2]):
                    if np.round(lonc) < 180:                    
                        txt = str(np.round(lonc))+'E'
                    elif np.round(lonc) > 180:
                        txt = str(np.round(360-lonc))+'W'
                    else:
                        txt = '180'                    
                    # ax[nr, nc].text(lonc, latr[0], txt, ha = 'center', va = 'top')
                    ax[nr,nc].text(lonc-180, latr[0]-dxax, txt, ha = 'center', va = 'top', fontsize = fontsizexy)         
                for latc in np.arange(latr[0], latr[1]+1, latr[2]):
                    # ax[nr, nc].text(lonr[0], latc, str(int(latc))+'N', ha = 'right', va = 'center')
                    ax[nr,nc].text(lonr[0]-180-dyax, latc, str(int(latc))+'N', ha = 'right', va = 'center', fontsize = fontsizexy)                
                


    # dx0 = R0 * np.cos(np.deg2rad(0.5*(vtrtgt[0][4][:-1]+vtrtgt[0][4][1:]))) * np.deg2rad(np.diff(vtrtgt[0][0]))
    # dy0 = R0 * np.deg2rad(np.diff(vtrtgt[0][4]))       
    # ln0 = np.sqrt(dx0**2+dy0**2)                
    # au0 = ln0/vtrtgt[0][3][1:]
    # # aul  = interpolate.interp1d(0.5*(vtrtgt[0][0][:-1]+vtrtgt[0][0][1:]), aul0, fill_value = 'extrapolate')(0.5*(lonLI[:-1]+lonLI[1:]))
    
    # dx  = R0 * np.cos(np.deg2rad(0.5*(vtrtgt[1][4][:-1]+vtrtgt[1][4][1:]))) * np.deg2rad(np.diff(vtrtgt[1][0]))
    # dy  = R0 * np.deg2rad(np.diff(vtrtgt[1][4]))          
    # ln  = np.sqrt(dx**2+dy**2)                
    # au  = ln/vtrtgt[1][3][1:]
    
    # # lath = interpolate.interp1d(vtrtgt[1][0], vtrtgt[1][4], fill_value = 'extrapolate')(lonLI)
    # # auh  = interpolate.interp1d(0.5*(vtrtgt[1][0][:-1]+vtrtgt[1][0][1:]), auh0, fill_value = 'extrapolate')(0.5*(lonLI[:-1]+lonLI[1:]))        
    
        
    # if np.size(vtrtgt) > 0:
    #     for nc in range(3):
    #         caxl = ax[0,nc].get_position()
    #         axadd0 = fig.add_axes([caxl.x0, 0.4,  caxl.x1-caxl.x0, 0.25])  
    #         axadd  = fig.add_axes([caxl.x0, 0.05, caxl.x1-caxl.x0, 0.25])
    #         if nc < 2:
    #             axadd0.plot(vtrtgt[nc][0], vtrtgt[nc][-1], 'k', linewidth = 2)
                
    #             axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1], 'k', linewidth = 2)
                
    #             i = np.argmin(np.abs(vtrtgt[nc][0]-xtgt))
    #             tnd = vtrtgt[nc][2][6] - vtrtgt[nc][2][1]
    #             axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'g', linewidth = 2)                
    #             # # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'g', linewidth = 2, label = r'$T^\prime_{ADV}$')                                 
    #             # tnd = vtrtgt[nc][2][7] - vtrtgt[nc][2][1]                
    #             # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], ':g', linewidth = 2)
    #             # tnd = vtrtgt[nc][2][6] - vtrtgt[nc][2][7]                
    #             # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], '--g', linewidth = 2)                                

    #             if nc == 0:
    #                 axadd.text(xmintrk+0.01*(xmaxtrk-xmintrk), tmintrks[nc]+0.2*(tmaxtrks[nc]-tmintrks[nc]), r'$T^\prime_{ADV}$', color = 'g', fontsize = fontsize)
            
    #             tnd = vtrtgt[nc][2][2] - vtrtgt[nc][2][6]
    #             axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'r', linewidth = 2)

    #             # tnd = vtrtgt[nc][2][8] - vtrtgt[nc][2][9]
    #             # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], ':r', linewidth = 2)
    #             # tnd = vtrtgt[nc][2][2] - vtrtgt[nc][2][6] - (vtrtgt[nc][2][8] - vtrtgt[nc][2][9])
    #             # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], '--r', linewidth = 2)         

    #             if nc == 0:
    #                 axadd.text(xmintrk+0.15*(xmaxtrk-xmintrk), tmintrks[nc]+0.2*(tmaxtrks[nc]-tmintrks[nc]), r'$T_{EDD}$', color = 'r', fontsize = fontsize)
                                    
    #             tnd = vtrtgt[nc][2][3]                
    #             # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'm', linewidth = 2)
    #             axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'c', linewidth = 2)
    #             if nc == 0:
    #                 axadd.text(xmintrk+0.01*(xmaxtrk-xmintrk), tmintrks[nc]+0.02*(tmaxtrks[nc]-tmintrks[nc]), r'$T_{SGS}$', color = 'c', fontsize = fontsize)
                    
    #             tnd = vtrtgt[nc][2][4]
    #             axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'b', linewidth = 2)
    #             if nc == 0:
    #                 axadd.text(xmintrk+0.15*(xmaxtrk-xmintrk), tmintrks[nc]+0.02*(tmaxtrks[nc]-tmintrks[nc]), r'$T_{SFC}$', color = 'b', fontsize = fontsize)
                    
    #             # tnd = vtrtgt[nc][2][5]
    #             # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'c', linewidth = 2)                                
    #         else:
    #             vint0 = interpolate.interp1d(vtrtgt[0][0], vtrtgt[0][-1], fill_value = 'extrapolate')(vtrtgt[1][0])
    #             axadd0.plot(vtrtgt[1][0], vtrtgt[1][-1]-vint0, 'k', linewidth = 2)
                
    #             vint = interpolate.interp1d(vtrtgt[0][0], vtrtgt[0][1], fill_value = 'extrapolate')(vtrtgt[1][0])
    #             axadd.plot(vtrtgt[1][0], vtrtgt[1][1]-vint, 'k', linewidth = 2)

    #             i0 = np.argmin(np.abs(vtrtgt[0][0]-xtgt))
    #             i  = np.argmin(np.abs(vtrtgt[1][0]-xtgt))
    #             dt0 = vtrtgt[1][1][i] - vtrtgt[0][1][i0]
                
    #             tnd0 = vtrtgt[0][2][6] - vtrtgt[0][2][1]
    #             tnd  = vtrtgt[1][2][6] - vtrtgt[1][2][1]                
    #             dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
    #             axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'g', linewidth = 2)

    #             # tnd0 = vtrtgt[0][2][7] - vtrtgt[0][2][1]
    #             # tnd  = vtrtgt[1][2][7] - vtrtgt[1][2][1]
    #             # dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
    #             # axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], ':g', linewidth = 2)

    #             # tnd0 = vtrtgt[0][2][6] - vtrtgt[0][2][7]
    #             # tnd  = vtrtgt[1][2][6] - vtrtgt[1][2][7]
    #             # dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
    #             # axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], '--g', linewidth = 2)

                
    #             tnd0 = vtrtgt[0][2][2] - vtrtgt[0][2][6]
    #             tnd  = vtrtgt[1][2][2] - vtrtgt[1][2][6]                
    #             dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
    #             axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'r', linewidth = 2)

    #             # tnd0 = vtrtgt[0][2][8] - vtrtgt[0][2][9]
    #             # tnd  = vtrtgt[1][2][8] - vtrtgt[1][2][9]
    #             # dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
    #             # axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], ':r', linewidth = 2)

    #             # tnd0 = vtrtgt[0][2][2] - vtrtgt[0][2][6] - (vtrtgt[0][2][8] - vtrtgt[0][2][9])
    #             # tnd  = vtrtgt[1][2][2] - vtrtgt[1][2][6] - (vtrtgt[1][2][8] - vtrtgt[1][2][9])
    #             # dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
    #             # axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], '--r', linewidth = 2)
                
    #             tnd0 = vtrtgt[0][2][3]
    #             tnd  = vtrtgt[1][2][3]
    #             dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
    #             # axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'm', linewidth = 2)
    #             axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'c', linewidth = 2)                

    #             tnd0 = vtrtgt[0][2][4]
    #             tnd  = vtrtgt[1][2][4]
    #             dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
    #             axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'b', linewidth = 2)

    #             # tnd0 = vtrtgt[0][2][5]
    #             # tnd  = vtrtgt[1][2][5]
    #             # dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
    #             # axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'c', linewidth = 2)


    #             dx0 = R0 * np.cos(np.deg2rad(0.5*(vtrtgt[0][4][:-1]+vtrtgt[0][4][1:]))) * np.deg2rad(np.diff(vtrtgt[0][0]))
    #             dy0 = R0 * np.deg2rad(np.diff(vtrtgt[0][4]))       
    #             ln0 = np.sqrt(dx0**2+dy0**2)                
    #             au0 = ln0/vtrtgt[0][3][1:]                
    #             qt0 = np.diff(vtrtgt[0][2][4])/vtrtgt[0][3][1:]

                
    #             dx  = R0 * np.cos(np.deg2rad(0.5*(vtrtgt[1][4][:-1]+vtrtgt[1][4][1:]))) * np.deg2rad(np.diff(vtrtgt[1][0]))
    #             dy  = R0 * np.deg2rad(np.diff(vtrtgt[1][4]))          
    #             ln  = np.sqrt(dx**2+dy**2)                
    #             au  = ln/vtrtgt[1][3][1:]                                
    #             qt  = np.diff(vtrtgt[1][2][4])/vtrtgt[1][3][1:]


    #             ltb = interpolate.interp1d(vtrtgt[0][0], vtrtgt[0][4], fill_value = 'extrapolate')(vtrtgt[1][0])
    #             dxb = R0 * np.cos(np.deg2rad(0.5*(ltb[:-1]+ltb[1:]))) * np.deg2rad(np.diff(vtrtgt[1][0]))
    #             dyb = R0 * np.deg2rad(np.diff(ltb))
    #             lnb = np.sqrt(dxb**2+dyb**2)
    #             aub = interpolate.interp1d(0.5*(vtrtgt[0][0][:-1]+vtrtgt[0][0][1:]), au0, fill_value = 'extrapolate')(0.5*(vtrtgt[1][0][:-1]+vtrtgt[1][0][1:]))
    #             qtb = interpolate.interp1d(0.5*(vtrtgt[0][0][:-1]+vtrtgt[0][0][1:]), qt0, fill_value = 'extrapolate')(0.5*(vtrtgt[1][0][:-1]+vtrtgt[1][0][1:]))
                
    #             dtndq = np.zeros(i+1)
    #             dtndu = np.zeros(i+1)
    #             dtndl = np.zeros(i+1)                
    #             for ii in range(i):
    #                 # dtndq[ii+1] = dtndq[ii] - (qt[i-ii-1] - qtb[i-ii-1])*lnb[i-ii-1]/aub[i-ii-1]
    #                 dtndq[ii+1] = dtndq[ii] - (qt[i-ii-1] - qtb[i-ii-1])*lnb[i-ii-1]/au[i-ii-1]                    
    #                 dtndu[ii+1] = dtndu[ii] - qtb[i-ii-1]*lnb[i-ii-1]*(1/au[i-ii-1]-1/aub[i-ii-1])
    #                 # dtndl[ii+1] = dtndl[ii] - qtb[i-ii-1]*(ln[i-ii-1]-lnb[i-ii-1])/aub[i-ii-1]
    #                 dtndl[ii+1] = dtndl[ii] - qtb[i-ii-1]*(ln[i-ii-1]-lnb[i-ii-1])/au[i-ii-1]                     

    #             xx = 0.5*(vtrtgt[1][0][:-1]+vtrtgt[1][0][1:])[:i+1][::-1]
                
    #             axadd.plot(xx, dt0+dtndq, ':b', linewidth = 2)
    #             axadd.plot(xx, dt0+dtndu, '--b', linewidth = 2)
    #             axadd.plot(xx, dt0+dtndl, 'b', linestyle = 'dashdot', linewidth = 2)


    #             di  = np.argmin(np.abs(vtrtgt[1][0]-xmintrk)) - i
    #             dtndq = np.zeros(di+1)
    #             dtndu = np.zeros(di+1)
    #             dtndl = np.zeros(di+1)                
    #             for ii in range(di):
    #                 # dtndq[ii+1] = dtndq[ii] + (qt[i+ii] - qtb[i+ii])*lnb[i+ii]/aub[i+ii]
    #                 dtndq[ii+1] = dtndq[ii] + (qt[i+ii] - qtb[i+ii])*lnb[i+ii]/au[i+ii]                    
    #                 dtndu[ii+1] = dtndu[ii] + qtb[i+ii]*lnb[i+ii]*(1/au[i+ii]-1/aub[i+ii])
    #                 # dtndl[ii+1] = dtndl[ii] + qtb[i+ii]*(ln[i+ii]-lnb[i+ii])/aub[i+ii]
    #                 dtndl[ii+1] = dtndl[ii] + qtb[i+ii]*(ln[i+ii]-lnb[i+ii])/au[i+ii]                     

    #             xx = 0.5*(vtrtgt[1][0][:-1]+vtrtgt[1][0][1:])[i:i+di+1]
    #             axadd.plot(xx, dt0+dtndq, ':b', linewidth = 2)
    #             axadd.plot(xx, dt0+dtndu, '--b', linewidth = 2)
    #             axadd.plot(xx, dt0+dtndl, 'b', linestyle = 'dashdot', linewidth = 2)
                
    #         axadd.set_xlim(xmintrk, xmaxtrk)
    #         axadd.set_xticks(xticks)
    #         axadd.set_xticklabels(xticklabels)                        
    #         axadd.set_ylim(tmintrks[nc], tmaxtrks[nc])
    #         axadd.set_yticks(np.linspace(tmintrks[nc], tmaxtrks[nc], tinttrks[nc]))
    #         # axadd.text(xmintrk+dxc*(xmaxtrk-xmintrk), tmaxtrks[nc]-0.12*(tmaxtrks[nc]-tmintrks[nc]), '('+chr(ord("a")+nc+3)+')', ha = 'left', va = 'bottom')
    #         # axadd.text(xmintrk+dxc*(xmaxtrk-xmintrk), tmaxtrks[nc]-dyc*(tmaxtrks[nc]-tmintrks[nc]), '('+chr(ord("a")+nc+3)+')', ha = 'left', va = 'bottom')
    #         axadd.text(xmintrk+dxc*(xmaxtrk-xmintrk), tmaxtrks[nc]-dyc*(tmaxtrks[nc]-tmintrks[nc]), '('+chr(ord("a")+nc+6)+')', ha = 'left', va = 'bottom')                        
    #         # axadd.text(xmintrk+dxc*(xmaxtrk-xmintrk), tmintrks[nc]+0.02*(tmaxtrks[nc]-tmintrks[nc]), '('+chr(ord("a")+nc+3)+')', ha = 'left', va = 'bottom')
    #         axadd.text(xmintrk-0.15*(xmaxtrk-xmintrk), tmaxtrks[nc]+0.05*(tmaxtrks[nc]-tmintrks[nc]), r'[${}^\circ$C]', ha = 'left', va = 'bottom')

    #         axadd0.set_xlim(xmintrk, xmaxtrk)
    #         axadd0.set_xticks(xticks)
    #         axadd0.set_xticklabels(xticklabels)
    #         if nc == 2:
    #             ymin = -4; ymax = 2; yint = 4
    #         else:
    #             ymin = latmintrk; ymax = latmaxtrk; yint = latinttrk

    #         axadd0.set_ylim(ymin, ymax)
    #         axadd0.set_yticks(np.linspace(ymin, ymax, yint))
    #         if nc == 2:
    #             ylabel = np.linspace(ymin, ymax, yint).astype(int).astype(str).astype(object) + r'${}^\circ$'
    #         else:
    #             # ylabel = np.linspace(ymin, ymax, yint).astype(int).astype(str).astype(object) + r'${}^\circ$ N'
    #             ylabel = np.linspace(ymin, ymax, yint).astype(int).astype(str).astype(object) + 'N'                                
    #         axadd0.set_yticklabels(ylabel)
            
    #         axadd0.text(xmintrk+dxc*(xmaxtrk-xmintrk), ymax-dyc*(ymax-ymin), '('+chr(ord("a")+nc+3)+')', ha = 'left', va = 'bottom')            
    #         # axadd0.text(xmintrk-0.1*(xmaxtrk-xmintrk), ymax+0.05*(ymax-ymin), '[N]', ha = 'left', va = 'bottom')   
    #         # if nc == 0:
    #         #     axadd.legend()
            
            
    #     for nc in range(3):
    #         for nr in range(nrowl):
    #             ax[nrowm+nr,nc].remove()
            
    if ctght:
        plt.tight_layout()
    plt.savefig(pngfile)
    plt.close()        

def fig5(pngfile, vtrtgt = [], fsizex = 8, fsizey = 5, lcol = 'k', lwdth = 1, cntcol = 'k', dxc = 0.015, dyc = 0.15, dxax = 4., dyax = 1.2, ctght = False, fontsize = 10, unitcbr = r'[m]', unitx = 1.02, unity = -1.5, ncols = 3, xmintrk = 140, xmaxtrk = 170, tmintrks = [16, 16, -.8], tmaxtrks = [21, 21, 3.2], tinttrks = [6, 6, 6], xtgt = 143, xticks = np.linspace(140, 170, 4), xticklabels = ['140E', '150E', '160E', '170E'], latmintrk = 34, latmaxtrk = 40, latinttrk = 4, fontsizexy = 8, explabel = ['LR', 'HR', 'HR-LR'], cfrc = True, cqul = True):

    print(pngfile)
    R0 = 6.375e6
    # lonmin, lonmax, lonint = lonr
    # latmin, latmax, latint = latr
    # ncols = 3
    nrows = 2

    # ntrck0 = np.shape(vartrk[0])[0]
    # ntrck  = np.shape(vartrk[1])[0]
    
    plt.rcParams['font.size'] = fontsize
    fig = plt.figure(figsize = (fsizex, fsizey))
    # plt.subplots_adjust(left=0.05, right = 0.96, top = 0.98, bottom = 0.1)
    # plt.subplots_adjust(left=0.05, right = 0.96, top = 1.05, bottom = 0.1)
    ax = fig.subplots(nrows, ncols).reshape(nrows, ncols) 
    
    
    dx0 = R0 * np.cos(np.deg2rad(0.5*(vtrtgt[0][4][:-1]+vtrtgt[0][4][1:]))) * np.deg2rad(np.diff(vtrtgt[0][0]))
    dy0 = R0 * np.deg2rad(np.diff(vtrtgt[0][4]))       
    ln0 = np.sqrt(dx0**2+dy0**2)                
    au0 = ln0/vtrtgt[0][3][1:]
    # aul  = interpolate.interp1d(0.5*(vtrtgt[0][0][:-1]+vtrtgt[0][0][1:]), aul0, fill_value = 'extrapolate')(0.5*(lonLI[:-1]+lonLI[1:]))
    
    dx  = R0 * np.cos(np.deg2rad(0.5*(vtrtgt[1][4][:-1]+vtrtgt[1][4][1:]))) * np.deg2rad(np.diff(vtrtgt[1][0]))
    dy  = R0 * np.deg2rad(np.diff(vtrtgt[1][4]))          
    ln  = np.sqrt(dx**2+dy**2)                
    au  = ln/vtrtgt[1][3][1:]
    
    # lath = interpolate.interp1d(vtrtgt[1][0], vtrtgt[1][4], fill_value = 'extrapolate')(lonLI)
    # auh  = interpolate.interp1d(0.5*(vtrtgt[1][0][:-1]+vtrtgt[1][0][1:]), auh0, fill_value = 'extrapolate')(0.5*(lonLI[:-1]+lonLI[1:]))        
            
    for nc in range(3):
        if nc < 2:
            ax[0,nc].plot(vtrtgt[nc][0], vtrtgt[nc][-1], 'k', linewidth = 2)                
            ax[1,nc].plot(vtrtgt[nc][0], vtrtgt[nc][1], 'k', linewidth = 2)

            if cfrc:
                i = np.argmin(np.abs(vtrtgt[nc][0]-xtgt))
                tnd = vtrtgt[nc][2][6] - vtrtgt[nc][2][1]
                ax[1,nc].plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'g', linewidth = 2)                       

                if nc == 0:
                    # ax[1,nc].text(xmintrk+0.01*(xmaxtrk-xmintrk), tmintrks[nc]+0.15*(tmaxtrks[nc]-tmintrks[nc]), r'$T^\prime_{ADV}$', color = 'g', fontsize = fontsize)
                    ax[1,nc].text(xmintrk+0.01*(xmaxtrk-xmintrk), tmintrks[nc]+0.15*(tmaxtrks[nc]-tmintrks[nc]), r'$T_{VAD}$', color = 'g', fontsize = fontsize)                
            
                tnd = vtrtgt[nc][2][2] - vtrtgt[nc][2][6]
                ax[1,nc].plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'r', linewidth = 2)

                if nc == 0:
                    # ax[1,nc].text(xmintrk+0.18*(xmaxtrk-xmintrk), tmintrks[nc]+0.15*(tmaxtrks[nc]-tmintrks[nc]), r'$T_{EDD}$', color = 'r', fontsize = fontsize)
                    ax[1,nc].text(xmintrk+0.18*(xmaxtrk-xmintrk), tmintrks[nc]+0.15*(tmaxtrks[nc]-tmintrks[nc]), r'$T_{RED}$', color = 'r', fontsize = fontsize)                
                                    
                tnd = vtrtgt[nc][2][3]                
                # ax[1,nc].plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'm', linewidth = 2)
                ax[1,nc].plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'c', linewidth = 2)
                if nc == 0:
                    ax[1,nc].text(xmintrk+0.01*(xmaxtrk-xmintrk), tmintrks[nc]+0.02*(tmaxtrks[nc]-tmintrks[nc]), r'$T_{SGS}$', color = 'c', fontsize = fontsize)
                    
                tnd = vtrtgt[nc][2][4]
                ax[1,nc].plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'b', linewidth = 2)
                if nc == 0:
                    ax[1,nc].text(xmintrk+0.18*(xmaxtrk-xmintrk), tmintrks[nc]+0.02*(tmaxtrks[nc]-tmintrks[nc]), r'$T_{SFC}$', color = 'b', fontsize = fontsize)
                    
                # tnd = vtrtgt[nc][2][5]
                # ax[1,nc].plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'c', linewidth = 2)                                
        else:
            vint0 = interpolate.interp1d(vtrtgt[0][0], vtrtgt[0][-1], fill_value = 'extrapolate')(vtrtgt[1][0])
            ax[0,nc].plot(vtrtgt[1][0], vtrtgt[1][-1]-vint0, 'k', linewidth = 2)

            vint = interpolate.interp1d(vtrtgt[0][0], vtrtgt[0][1], fill_value = 'extrapolate')(vtrtgt[1][0])
            ax[1,nc].plot(vtrtgt[1][0], vtrtgt[1][1]-vint, 'k', linewidth = 2)

            if cfrc:                            
                # i0 = np.argmin(np.abs(vtrtgt[0][0]-xtgt))
                i0 = np.where((vtrtgt[0][0][:-1]>=xtgt)*(vtrtgt[0][0][1:]<xtgt))[0][0]
                i  = np.argmin(np.abs(vtrtgt[1][0]-xtgt))
                # dt0 = vtrtgt[1][1][i] - vtrtgt[0][1][i0]
                dt0 = vtrtgt[1][1][i] - (vtrtgt[0][1][i0]*(vtrtgt[0][0][i0+1]-xtgt)+vtrtgt[0][1][i0+1]*(xtgt-vtrtgt[0][0][i0]))/(vtrtgt[0][0][i0+1]-vtrtgt[0][0][i0])
                
                tnd0 = vtrtgt[0][2][6] - vtrtgt[0][2][1]
                tnd  = vtrtgt[1][2][6] - vtrtgt[1][2][1]                
                dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                ax[1,nc].plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'g', linewidth = 2)
            
                
                tnd0 = vtrtgt[0][2][2] - vtrtgt[0][2][6]
                tnd  = vtrtgt[1][2][2] - vtrtgt[1][2][6]                
                dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                ax[1,nc].plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'r', linewidth = 2)
                
                tnd0 = vtrtgt[0][2][3]
                tnd  = vtrtgt[1][2][3]
                dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                # ax[1,nc].plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'm', linewidth = 2)
                ax[1,nc].plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'c', linewidth = 2)                
            
                tnd0 = vtrtgt[0][2][4]
                tnd  = vtrtgt[1][2][4]
                dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                ax[1,nc].plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'b', linewidth = 2)
            
                # tnd0 = vtrtgt[0][2][5]
                # tnd  = vtrtgt[1][2][5]
                # dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                # ax[1,nc].plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'c', linewidth = 2)

                if cqul:
                    dx0 = R0 * np.cos(np.deg2rad(0.5*(vtrtgt[0][4][:-1]+vtrtgt[0][4][1:]))) * np.deg2rad(np.diff(vtrtgt[0][0]))
                    dy0 = R0 * np.deg2rad(np.diff(vtrtgt[0][4]))       
                    ln0 = np.sqrt(dx0**2+dy0**2)                
                    au0 = ln0/vtrtgt[0][3][1:]                
                    qt0 = np.diff(vtrtgt[0][2][4])/vtrtgt[0][3][1:]        
            
                    dx  = R0 * np.cos(np.deg2rad(0.5*(vtrtgt[1][4][:-1]+vtrtgt[1][4][1:]))) * np.deg2rad(np.diff(vtrtgt[1][0]))
                    dy  = R0 * np.deg2rad(np.diff(vtrtgt[1][4]))          
                    ln  = np.sqrt(dx**2+dy**2)                
                    au  = ln/vtrtgt[1][3][1:]                                
                    qt  = np.diff(vtrtgt[1][2][4])/vtrtgt[1][3][1:]
            

                    ltb = interpolate.interp1d(vtrtgt[0][0], vtrtgt[0][4], fill_value = 'extrapolate')(vtrtgt[1][0])
                    dxb = R0 * np.cos(np.deg2rad(0.5*(ltb[:-1]+ltb[1:]))) * np.deg2rad(np.diff(vtrtgt[1][0]))
                    dyb = R0 * np.deg2rad(np.diff(ltb))
                    lnb = np.sqrt(dxb**2+dyb**2)
                    aub = interpolate.interp1d(0.5*(vtrtgt[0][0][:-1]+vtrtgt[0][0][1:]), au0, fill_value = 'extrapolate')(0.5*(vtrtgt[1][0][:-1]+vtrtgt[1][0][1:]))
                    qtb = interpolate.interp1d(0.5*(vtrtgt[0][0][:-1]+vtrtgt[0][0][1:]), qt0, fill_value = 'extrapolate')(0.5*(vtrtgt[1][0][:-1]+vtrtgt[1][0][1:]))
                    
            
                    dtndq = np.zeros(i+1)
                    dtndu = np.zeros(i+1)
                    dtndl = np.zeros(i+1)                
                    for ii in range(i):
                        # # # ---- original ---- # #
                        # # dtndq[ii+1] = dtndq[ii] - (qt[i-ii-1] - qtb[i-ii-1])*lnb[i-ii-1]/aub[i-ii-1]
                        # dtndq[ii+1] = dtndq[ii] - (qt[i-ii-1] - qtb[i-ii-1])*lnb[i-ii-1]/au[i-ii-1]                    
                        # dtndu[ii+1] = dtndu[ii] - qtb[i-ii-1]*lnb[i-ii-1]*(1/au[i-ii-1]-1/aub[i-ii-1])
                        # # dtndl[ii+1] = dtndl[ii] - qtb[i-ii-1]*(ln[i-ii-1]-lnb[i-ii-1])/aub[i-ii-1]
                        # dtndl[ii+1] = dtndl[ii] - qtb[i-ii-1]*(ln[i-ii-1]-lnb[i-ii-1])/au[i-ii-1]                     
                        # # # ---- original ---- # #
                        
                        # # ---- original 10/08---- # #
                        # dtndq[ii+1] = dtndq[ii] - (qt[i-ii-1] - qtb[i-ii-1])*lnb[i-ii-1]/aub[i-ii-1]
                        dtndq[ii+1] = dtndq[ii] - (qt[i-ii-1] - qtb[i-ii-1])*ln[i-ii-1]/au[i-ii-1]                    
                        dtndu[ii+1] = dtndu[ii] - qt[i-ii-1]*ln[i-ii-1]*(1/au[i-ii-1]-1/aub[i-ii-1])
                        dtndl[ii+1] = dtndl[ii] - qt[i-ii-1]*(ln[i-ii-1]-lnb[i-ii-1])/au[i-ii-1]                     
                        # # ---- original ---- # #
                        
                        # # # ---- R1 ---- # #
                        # # dtndq[ii+1] = dtndq[ii] - (qt[i-ii-1] - qtb[i-ii-1])*ln[i-ii-1]/au[i-ii-1]                    
                        # # dtndu[ii+1] = dtndu[ii] - qt[i-ii-1]*ln[i-ii-1]*(1/au[i-ii-1]-1/aub[i-ii-1])
                        # # dtndl[ii+1] = dtndl[ii] - qt[i-ii-1]*(ln[i-ii-1]-lnb[i-ii-1])/au[i-ii-1]
                        # dtndq[ii+1] = dtndq[ii] - (qt[i-ii-1] - qtb[i-ii-1])*lnb[i-ii-1]/aub[i-ii-1]                    
                        # dtndu[ii+1] = dtndu[ii] - qtb[i-ii-1]*lnb[i-ii-1]*(1/au[i-ii-1]-1/aub[i-ii-1])
                        # dtndl[ii+1] = dtndl[ii] - qtb[i-ii-1]*(ln[i-ii-1]-lnb[i-ii-1])/aub[i-ii-1]                                
                        # # # ---- R1 ---- # #                 
                
                    xx = 0.5*(vtrtgt[1][0][:-1]+vtrtgt[1][0][1:])[:i+1][::-1]
            
                    # ax[1,nc].plot(xx, dt0+dtndq, ':b', linewidth = 2)
                    # ax[1,nc].plot(xx, dt0+dtndu, '--b', linewidth = 2)
                    # ax[1,nc].plot(xx, dt0+dtndl, 'b', linestyle = 'dashdot', linewidth = 2)
                    
                    ax[1,nc].plot(xx, dt0+dtndq, ':b', linewidth = 1.5, label = r'$\Delta T_{SFT}$')
                    ax[1,nc].plot(xx, dt0+dtndu, '--b', linewidth = 1.5, label = r'$\Delta T_{SFU}$')
                    # ax[1,nc].plot(xx, dt0+dtndl, 'b', linestyle = 'dashdot', linewidth = 1.5, label = r'$\Delta T_{SFL}$')
                    ax[1,nc].plot(xx, dt0+dtndl, 'b', linestyle = 'dashdot', linewidth = 1.0, label = r'$\Delta T_{SFL}$')                        
                    ax[1,nc].legend(ncol=3, bbox_to_anchor=(0.5, -0.03), loc='lower center', fontsize = fontsize, handlelength=1.5, edgecolor='w', labelspacing = 0.2, borderpad = 0., handletextpad = 0.1, columnspacing = 0.32)
                    
                    
                    i1 = np.argmin(np.abs(xx-143))
                    i2 = np.argmin(np.abs(xx-150))
                    print(xx[i1], xx[i2])
                    print('143E-150E', dtndq[i2]-dtndq[i1], dtndu[i2]-dtndu[i1], dtndl[i2]-dtndl[i1], dtndq[i2]-dtndq[i1]+dtndu[i2]-dtndu[i1]+dtndl[i2]-dtndl[i1])
                    i1 = np.argmin(np.abs(xx-150))
                    i2 = np.argmin(np.abs(xx-160))
                    print(xx[i1], xx[i2])            
                    print('150E-160E', dtndq[i2]-dtndq[i1], dtndu[i2]-dtndu[i1], dtndl[i2]-dtndl[i1], dtndq[i2]-dtndq[i1]+dtndu[i2]-dtndu[i1]+dtndl[i2]-dtndl[i1])
                    i1 = np.argmin(np.abs(xx-160))
                    i2 = np.argmin(np.abs(xx-170))
                    print(xx[i1], xx[i2])            
                    print('160E-170E', dtndq[i2]-dtndq[i1], dtndu[i2]-dtndu[i1], dtndl[i2]-dtndl[i1], dtndq[i2]-dtndq[i1]+dtndu[i2]-dtndu[i1]+dtndl[i2]-dtndl[i1])
                
                
                    # i1 = np.argmin(np.abs(vtrtgt[1][0]-150))
                    # i2 = np.argmin(np.abs(vtrtgt[1][0]-143))            
                    # print('143E-150E',
                    #       np.sum(aub[i1:i2]*np.diff(vtrtgt[1][0][i1:i2+1]))/np.sum(np.diff(vtrtgt[1][0][i1:i2+1])),
                    #       np.sum(au[i1:i2]* np.diff(vtrtgt[1][0][i1:i2+1]))/np.sum(np.diff(vtrtgt[1][0][i1:i2+1])),
                    #       np.sum(au[i1:i2]* np.diff(vtrtgt[1][0][i1:i2+1]))/np.sum(np.diff(vtrtgt[1][0][i1:i2+1]))/(np.sum(aub[i1:i2]*np.diff(vtrtgt[1][0][i1:i2+1]))/np.sum(np.diff(vtrtgt[1][0][i1:i2+1]))))
                    
                    # i1 = np.argmin(np.abs(vtrtgt[1][0]-160))
                    # i2 = np.argmin(np.abs(vtrtgt[1][0]-150))                        
                    # print('150E-160E',
                    #       np.sum(aub[i1:i2]*np.diff(vtrtgt[1][0][i1:i2+1]))/np.sum(np.diff(vtrtgt[1][0][i1:i2+1])),
                    #       np.sum(au[i1:i2]* np.diff(vtrtgt[1][0][i1:i2+1]))/np.sum(np.diff(vtrtgt[1][0][i1:i2+1])),
                    #       np.sum(au[i1:i2]* np.diff(vtrtgt[1][0][i1:i2+1]))/np.sum(np.diff(vtrtgt[1][0][i1:i2+1]))/(np.sum(aub[i1:i2]*np.diff(vtrtgt[1][0][i1:i2+1]))/np.sum(np.diff(vtrtgt[1][0][i1:i2+1]))))
                    
                    # i1 = np.argmin(np.abs(vtrtgt[1][0]-170))
                    # i2 = np.argmin(np.abs(vtrtgt[1][0]-160))                        
                    # print('160E-170E',
                    #       np.sum(aub[i1:i2]*np.diff(vtrtgt[1][0][i1:i2+1]))/np.sum(np.diff(vtrtgt[1][0][i1:i2+1])),
                    #       np.sum(au[i1:i2]* np.diff(vtrtgt[1][0][i1:i2+1]))/np.sum(np.diff(vtrtgt[1][0][i1:i2+1])),
                    #       np.sum(au[i1:i2]* np.diff(vtrtgt[1][0][i1:i2+1]))/np.sum(np.diff(vtrtgt[1][0][i1:i2+1]))/(np.sum(aub[i1:i2]*np.diff(vtrtgt[1][0][i1:i2+1]))/np.sum(np.diff(vtrtgt[1][0][i1:i2+1]))))
            
                
                
                
                    # ax[1,nc].plot(xx, dt0+dtndq+dtndu+dtndl, 'ob', linewidth = 2)
                    # ax[1,nc].plot(xx[::10], (dt0+dtndq+dtndu+dtndl)[::10], 'ob', linewidth = None)            
                    # ax[1,nc].plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'ob', linewidth = 2)
                    # ax[1,nc].plot(xx, interpolate.interp1d(vtrtgt[1][0], dt0+dtnd-dtnd[i], fill_value = 'extrapolate')(xx), color = 'grey', linewidth = 2)
                    # ax[1,nc].plot(xx, interpolate.interp1d(vtrtgt[1][0], dt0+dtnd-dtnd[i], fill_value = 'extrapolate')(xx)-dtndq-dtndu-dtndl, color = 'grey', linewidth = 2)                        
                    
            
                    di  = np.argmin(np.abs(vtrtgt[1][0]-xmintrk)) - i
                    dtndq = np.zeros(di+1)
                    dtndu = np.zeros(di+1)
                    dtndl = np.zeros(di+1)                
                    for ii in range(di):
                        # # # # ---- original ---- # #                
                        # # dtndq[ii+1] = dtndq[ii] + (qt[i+ii] - qtb[i+ii])*lnb[i+ii]/aub[i+ii]
                        # dtndq[ii+1] = dtndq[ii] + (qt[i+ii] - qtb[i+ii])*lnb[i+ii]/au[i+ii]                    
                        # dtndu[ii+1] = dtndu[ii] + qtb[i+ii]*lnb[i+ii]*(1/au[i+ii]-1/aub[i+ii])
                        # # dtndl[ii+1] = dtndl[ii] + qtb[i+ii]*(ln[i+ii]-lnb[i+ii])/aub[i+ii]
                        # dtndl[ii+1] = dtndl[ii] + qtb[i+ii]*(ln[i+ii]-lnb[i+ii])/au[i+ii]                     
                        # # # # ---- original ---- # #
                        
                        # # # ---- original ---- # #                
                        dtndq[ii+1] = dtndq[ii] + (qt[i+ii] - qtb[i+ii])*ln[i+ii]/au[i+ii]                    
                        dtndu[ii+1] = dtndu[ii] + qt[i+ii]*ln[i+ii]*(1/au[i+ii]-1/aub[i+ii])
                        dtndl[ii+1] = dtndl[ii] + qt[i+ii]*(ln[i+ii]-lnb[i+ii])/au[i+ii]                     
                        # # # ---- original ---- # #
                    
                        # # # # ---- R1 ---- # #                
                        # dtndq[ii+1] = dtndq[ii] + (qt[i+ii] - qtb[i+ii])*ln[i+ii]/au[i+ii]                    
                        # dtndu[ii+1] = dtndu[ii] + qt[i+ii]*ln[i+ii]*(1/au[i+ii]-1/aub[i+ii])
                        # dtndl[ii+1] = dtndl[ii] + qt[i+ii]*(ln[i+ii]-lnb[i+ii])/au[i+ii]                     
                        # # # # ---- R1 ---- # #                

                
                    xx = 0.5*(vtrtgt[1][0][:-1]+vtrtgt[1][0][1:])[i:i+di+1]
                    ax[1,nc].plot(xx, dt0+dtndq, ':b', linewidth = 2)
                    ax[1,nc].plot(xx, dt0+dtndu, '--b', linewidth = 2)
                    ax[1,nc].plot(xx, dt0+dtndl, 'b', linestyle = 'dashdot', linewidth = 2)
                    
                    # ax[1,nc].plot(xx[::10], (dt0+dtndq+dtndu+dtndl)[::10], 'ob', linewidth = None)
                    # ax[1,nc].plot(xx, interpolate.interp1d(vtrtgt[1][0], dt0+dtnd-dtnd[i], fill_value = 'extrapolate')(xx)-dtndq-dtndu-dtndl, color = 'grey', linewidth = 2)            
                    
        ax[1,nc].set_xlim(xmintrk, xmaxtrk)
        ax[1,nc].set_xticks(xticks)
        ax[1,nc].set_xticklabels(xticklabels)                        
        ax[1,nc].set_ylim(tmintrks[nc], tmaxtrks[nc])
        ax[1,nc].set_yticks(np.linspace(tmintrks[nc], tmaxtrks[nc], tinttrks[nc]))
        # ax[1,nc].text(xmintrk+dxc*(xmaxtrk-xmintrk), tmaxtrks[nc]-0.12*(tmaxtrks[nc]-tmintrks[nc]), '('+chr(ord("a")+nc+3)+')', ha = 'left', va = 'bottom')
        # ax[1,nc].text(xmintrk+dxc*(xmaxtrk-xmintrk), tmaxtrks[nc]-dyc*(tmaxtrks[nc]-tmintrks[nc]), '('+chr(ord("a")+nc+3)+')', ha = 'left', va = 'bottom')
        ax[1,nc].text(xmintrk+dxc*(xmaxtrk-xmintrk), tmaxtrks[nc]-dyc*(tmaxtrks[nc]-tmintrks[nc]), '('+chr(ord("a")+nc+3)+')', ha = 'left', va = 'bottom')
        # ax[1,nc].text(xmintrk+dxc*(xmaxtrk-xmintrk), tmaxtrks[nc]-dyc*(tmaxtrks[nc]-tmintrks[nc]), '('+chr(ord("a")+nc+3)+') Temperature', ha = 'left', va = 'bottom', bbox = dict(facecolor='white', alpha=0.7))
        
        # ax[1,nc].text(xmintrk+dxc*(xmaxtrk-xmintrk), tmintrks[nc]+0.02*(tmaxtrks[nc]-tmintrks[nc]), '('+chr(ord("a")+nc+3)+')', ha = 'left', va = 'bottom')
        # ax[1,nc].text(xmintrk-0.15*(xmaxtrk-xmintrk), tmaxtrks[nc]+0.05*(tmaxtrks[nc]-tmintrks[nc]), r'[${}^\circ$C]', ha = 'left', va = 'bottom')
        ax[1,nc].text(xmintrk-0.21*(xmaxtrk-xmintrk), tmaxtrks[nc]+0.08*(tmaxtrks[nc]-tmintrks[nc]), r'[${}^\circ$C]', ha = 'left', va = 'bottom')        

        ax[0,nc].set_xlim(xmintrk, xmaxtrk)
        ax[0,nc].set_xticks(xticks)
        ax[0,nc].set_xticklabels(xticklabels)
        if nc == 2:
            ymin = -4; ymax = 2; yint = 4
        else:
            ymin = latmintrk; ymax = latmaxtrk; yint = latinttrk

        ax[0,nc].set_ylim(ymin, ymax)
        ax[0,nc].set_yticks(np.linspace(ymin, ymax, yint))
        if nc == 2:
            ylabel = np.linspace(ymin, ymax, yint).astype(int).astype(str).astype(object) + r'${}^\circ$'
        else:
            # ylabel = np.linspace(ymin, ymax, yint).astype(int).astype(str).astype(object) + r'${}^\circ$ N'
            ylabel = np.linspace(ymin, ymax, yint).astype(int).astype(str).astype(object) + 'N'                                
        ax[0,nc].set_yticklabels(ylabel)
        
        ax[0,nc].text(xmintrk+dxc*(xmaxtrk-xmintrk), ymax-dyc*(ymax-ymin), '('+chr(ord("a")+nc+0)+')', ha = 'left', va = 'bottom')
        # ax[0,nc].text(xmintrk+dxc*(xmaxtrk-xmintrk), ymax-dyc*(ymax-ymin), '('+chr(ord("a")+nc+0)+') Latitude', ha = 'left', va = 'bottom', bbox = dict(facecolor='white', alpha=0.7))        
        # ax[0,nc].text(xmintrk-0.1*(xmaxtrk-xmintrk), ymax+0.05*(ymax-ymin), '[N]', ha = 'left', va = 'bottom')
        ax[0,nc].text(0.5*xmintrk+0.5*xmaxtrk, -0.01*ymin+1.01*ymax, explabel[nc], color = 'k', fontsize = fontsize, ha = 'center', va = 'bottom')       
        
        # if nc == 0:
        #     ax[1,nc].legend()
        
            
        # for nc in range(3):
        #     for nr in range(nrowl):
        #         ax[nrowm+nr,nc].remove()
            
    if ctght:
        plt.tight_layout()
    plt.savefig(pngfile)
    plt.close()        
    
    

    
def fig6(pngfile, lon, lat, varf, varfl = [], vartrk = [], lonr = [120, 210, 30], latr = [20, 50, 10], level = [''], vr=[-999,-999,21], rt = 10, lines = [0.], cmap = cmo.balance, vticklabel = [''], fsizex = 8, fsizey = 7, lcol = 'k', lwdth = 1, cntcol = 'k', dxc = 0.03, dyc = 0.09, dxax = 3., dyax = 1.2, ctght = False, fontsize = 10, unitcbr = r'[${}^\circ$C]', unitx0 = 0.98, unitx1 = 1.02, unity = -2.6, bgc = '', dycb = 0.06, cbt = 0.015, btm = 0.1, fontsizexy = 8, flabel = [], bbox = [], flabelc = 'k', tlabel = [], clonlatedge = True, skp3 = False):

    # dxc = 0.015; dyc = 0.35; no back ground color
    # dxc = 0.03; dyc = 0.5; back ground color    
    print(pngfile)
    R0 = 6.375e6
    lonmin, lonmax, lonint = lonr
    latmin, latmax, latint = latr
    nrows = int(np.shape(varf)[0]/3)
    ncols = 3
    
    # if skp3:
    #     nrows = int(np.shape(varf)[0]/3)
    #     ncols = 3
    # else:
    #     nrows = int(np.shape(varf)[0]/2)
    #     ncols = 2
        
    plt.rcParams['font.size'] = fontsize
    fig = plt.figure(figsize = (fsizex, fsizey))
    # plt.subplots_adjust(left=0.05, right = 0.95, top = 1., bottom = 0.1)
    plt.subplots_adjust(left=0.05, right = 0.95, top = 1., bottom = btm)                    
    ax = mc.set_maps(fig, nrows, ncols, xlim = [lonmin, lonmax], ylim = [latmin, latmax], lon_interval = lonint, lat_interval = latint)
    ax, images, vticks, vticklabels = mc.imcfs(ax, lon, lat, varf, nrows, ncols, vr = vr, rt = rt, level = level, cmap = cmap, vticklabel = vticklabel)
    if np.size(varfl) > 0:
        ax, lls = mc.imcs(ax, lon, lat, varfl, nrows, ncols, level = lines, lfontsize = 9, lwidth = 1.0, cntcol = cntcol)     
    
    nfg = 0    
    for nr in range(nrows):
        caxl = ax[nr,0].get_position()
        caxr = ax[nr,1].get_position()
        caxv = ax[nr,0].get_position()
        # for m0 in range(ncols):
        #     ax[n1+1,m0].remove()
        #     cax = fig.add_axes([caxl.x0, 0.5*(caxv.y0+caxv.y1),caxr.x1-caxl.x0,0.01])
        # cax = fig.add_axes([caxl.x0, caxv.y0-0.02*(nrows-nr)-0.018*nr,caxr.x1-caxl.x0, 0.015])
        # cax = fig.add_axes([caxl.x0, caxv.y0-0.04,caxr.x1-caxl.x0, 0.01])
        dx = caxr.x1-caxl.x0
        rdx = 0.8
        cax = fig.add_axes([caxl.x0+0.5*(1-rdx)*dx, caxv.y0-dycb, rdx*dx, cbt])      
        cbar = plt.colorbar(images[ncols*nr], cax = cax, orientation = 'horizontal', ticks = vticks[ncols*nr])
        if np.size(unitcbr) == 1:
            if unitcbr != '':
                cax.text(unitx0, unity, unitcbr, transform=cax.transAxes)
        else:
            cax.text(unitx0, unity, unitcbr[ncols*nr+2], transform=cax.transAxes)
            
        cbars = [cbar]
        if np.size(vticklabels) != 1:
            if vticklabels[0] != ['']:
                cbar.ax.set_xticklabels(vticklabels[0])

        caxl = ax[nr,-1].get_position()
        caxr = ax[nr,-1].get_position()
        caxv = ax[nr,-1].get_position()
        # for m0 in range(ncols):
        #     ax[n1+1,m0].remove()
        #     cax = fig.add_axes([caxl.x0, 0.5*(caxv.y0+caxv.y1),caxr.x1-caxl.x0,0.01])
        # cax = fig.add_axes([caxl.x0, caxv.y0-0.02*(nrows-nr)-0.018*nr,caxr.x1-caxl.x0, 0.015])
        # cax = fig.add_axes([caxl.x0, caxv.y0-0.04,caxr.x1-caxl.x0, 0.01])
        # cax = fig.add_axes([caxl.x0, caxv.y0-0.06,caxr.x1-caxl.x0, 0.015])                        
        dx = caxr.x1-caxl.x0
        # cax = fig.add_axes([caxl.x0+0.5*(1-rdx)*dx, caxv.y0-0.06, rdx*dx, 0.015])
        cax = fig.add_axes([caxl.x0+0.5*(1-rdx)*dx, caxv.y0-dycb, rdx*dx, cbt])              
        cbar = plt.colorbar(images[ncols*nr+2], cax = cax, orientation = 'horizontal', ticks = vticks[ncols*nr+2])
        if np.size(unitcbr) == 1:
            if unitcbr != '':
                cax.text(unitx1, unity, unitcbr, transform=cax.transAxes)
        else:
            cax.text(unitx1, unity, unitcbr[ncols*nr+2], transform=cax.transAxes)
                
            cbars = [cbar]
        if np.size(vticklabels) != 1:
            if vticklabels[0] != ['']:
                cbar.ax.set_xticklabels(vticklabels[0])
                
        for nc in range(ncols):
            # if np.size(vartrk) > 0:
            if len(vartrk) > 0:                
                # ntrs = np.size(vartrk[nc][0])
                ntrs = np.shape(vartrk[nc][0])[0]
                for ntr in range(ntrs):
                    ax[nr,nc].plot(vartrk[nc][0][ntr]-180, vartrk[nc][1][ntr], color = lcol, linewidth = lwdth)
                    # print(vartrk[nc][0][ntr], vartrk[nc][1][ntr])
            
            # ax[nr,nc].text(lonr[0]-180+5, latr[1]-8-2, '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')
            # ax[nr,nc].text(lonr[0]-180+5, latr[1]-0.2*(latr[1]-latr[0]), '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')
            label = '('+chr(ord("a")+nfg)+')'
            if np.size(flabel) > 0:
                label = label + ' ' + flabel[nfg]
                
            # if bgc == '':
            #     ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), label, ha = 'left', va = 'bottom')
            # else:
            #     ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), label, ha = 'left', va = 'bottom', backgroundcolor = bgc)

            if np.size(bbox) == 0:
                if bgc == '':
                    ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), label, ha = 'left', va = 'top', color = flabelc)
                else:
                    ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), label, ha = 'left', va = 'top', backgroundcolor = bgc, color = flabelc)
            else:
                ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), label, ha = 'left', va = 'top', bbox = bbox)

            if np.size(tlabel) > 0:
                if nr == 0:
                    ax[nr,nc].text(0.5*(lonr[1]+lonr[0])-180, latr[1]+0.02*(latr[1]-latr[0]), tlabel[nc], ha = 'center', va = 'bottom')
                    
            nfg += 1
            if skp3*(np.mod(nc,3)==0):
                nfg -= 1
                
            if clonlatedge:
                if nr == nrows-1:
                    for lonc in np.arange(lonr[0], lonr[1]+1, lonr[2]):
                        if np.round(lonc) < 180:                    
                            txt = str(np.round(lonc))+'E'
                        elif np.round(lonc) > 180:
                            txt = str(np.round(360-lonc))+'W'
                        else:
                            txt = '180'                    
                        # ax[nr, nc].text(lonc, latr[0], txt, ha = 'center', va = 'top')
                        ax[nr,nc].text(lonc-180, latr[0]-dxax, txt, ha = 'center', va = 'top', fontsize = fontsizexy)
                if nc == 0:                        
                    for latc in np.arange(latr[0], latr[1]+1, latr[2]):
                        # ax[nr, nc].text(lonr[0], latc, str(int(latc))+'N', ha = 'right', va = 'center')
                        ax[nr,nc].text(lonr[0]-180-dyax, latc, str(int(latc))+'N', ha = 'right', va = 'center', fontsize = fontsizexy)                
            else:
                for lonc in np.arange(lonr[0], lonr[1]+1, lonr[2]):
                    if np.round(lonc) < 180:                    
                        txt = str(np.round(lonc))+'E'
                    elif np.round(lonc) > 180:
                        txt = str(np.round(360-lonc))+'W'
                    else:
                        txt = '180'                    
                    # ax[nr, nc].text(lonc, latr[0], txt, ha = 'center', va = 'top')
                    ax[nr,nc].text(lonc-180, latr[0]-dxax, txt, ha = 'center', va = 'top', fontsize = fontsizexy)         
                for latc in np.arange(latr[0], latr[1]+1, latr[2]):
                    # ax[nr, nc].text(lonr[0], latc, str(int(latc))+'N', ha = 'right', va = 'center')
                    ax[nr,nc].text(lonr[0]-180-dyax, latc, str(int(latc))+'N', ha = 'right', va = 'center', fontsize = fontsizexy)                
                    
                
            # nfg += 1
            # for lonc in np.arange(lonr[0], lonr[1]+1, lonr[2]):
            #     if np.round(lonc) < 180:                    
            #         txt = str(np.round(lonc))+'E'
            #     elif np.round(lonc) > 180:
            #         txt = str(np.round(360-lonc))+'W'
            #     else:
            #         txt = '180'                    
            #     # ax[nr, nc].text(lonc, latr[0], txt, ha = 'center', va = 'top')
            #     ax[nr,nc].text(lonc-180, latr[0]-dxax, txt, ha = 'center', va = 'top', fontsize = fontsizexy)                
            # for latc in np.arange(latr[0], latr[1]+1, latr[2]):
            #     # ax[nr, nc].text(lonr[0], latc, str(int(latc))+'N', ha = 'right', va = 'center')
            #     ax[nr,nc].text(lonr[0]-180-dyax, latc, str(int(latc))+'N', ha = 'right', va = 'center', fontsize = fontsizexy)                

    if ctght:
        plt.tight_layout()
    plt.savefig(pngfile)
    plt.close()        


def fig7(pngfile, lon, lat, varf, varfl = [], vartrk = [], lonr = [120, 210, 30], latr = [20, 50, 10], level = [''], vr=[-999,-999,21], rt = 10, lines = [0.], cmap = cmo.balance, vticklabel = [''], fsizex = 8, fsizey = 6.5, lcol = 'k', lwdth = 1, cntcol = 'k', dxc = 0.015, dyc = 0.24, dxax = 3., dyax = 1.2, ctght = False, fontsize = 10, unitcbr = r'[${}^\circ$C]', unitx = 0.98, unity = -3., bgc = 'w', sngl_cbar = True, lonv = [], latv = [], varx = [], vary = [], angles = 'xy', scale = 2.e-2, scale_units = 'xy', headwidth = 5, headlength = 3, headaxislength = 2, vcol = 'g', dycb = 0.05, cbt = 0.01, btm = 0.1, fontsizexy = 8, flabel = [], bbox = [], flabelc = 'k', tlabel = [], dyt = 0.02, cfig2 = False, ncols = 3):

    fig2(pngfile, lon, lat, varf, varfl = varfl, vartrk = vartrk, lonr = lonr, latr = latr, level = level, vr=vr, rt = rt, lines = lines, cmap = cmap, vticklabel = vticklabel, fsizex = fsizex, fsizey = fsizey, lcol = lcol, lwdth = lwdth, cntcol = cntcol, dxc = dxc, dyc = dyc, dxax = dxax, dyax = dyax, ctght = ctght, fontsize = fontsize, unitcbr = unitcbr, unitx = unitx, unity = unity, bgc = bgc, sngl_cbar = sngl_cbar, lonv = lonv, latv = latv, varx = varx, vary = vary, angles = angles, scale = scale, scale_units = scale_units, headwidth = headwidth, headlength = headlength, headaxislength = headaxislength, vcol = vcol, dycb = dycb, cbt = cbt, btm = btm, fontsizexy = fontsizexy, flabel = flabel, bbox = bbox, tlabel = tlabel, dyt = dyt, cfig2 = cfig2, ncols = ncols)

def fig8(pngfile, lon, lat, varf, varfl = [], vartrk = [], lonr = [120, 210, 30], latr = [20, 50, 10], level = [''], vr=[-999,-999,21], rt = 10, lines = [0.], cmap = cmo.balance, vticklabel = [''], fsizex = 8, fsizey = 6.5, lcol = 'k', lwdth = 1, cntcol = 'k', dxc = 0.015, dyc = 0.24, dxax = 3., dyax = 1.2, ctght = False, fontsize = 10, unitcbr = r'[${}^\circ$C]', unitx = 0.98, unity = -3., bgc = 'w', sngl_cbar = True, lonv = [], latv = [], varx = [], vary = [], angles = 'xy', scale = 2.e-2, scale_units = 'xy', headwidth = 5, headlength = 3, headaxislength = 2, vcol = 'g', dycb = 0.05, cbt = 0.01, btm = 0.1, fontsizexy = 8, flabel = [], bbox = [], flabelc = 'k', tlabel = [], dyt = 0.02, cfig2 = False):

    fig2(pngfile, lon, lat, varf, varfl = varfl, vartrk = vartrk, lonr = lonr, latr = latr, level = level, vr=vr, rt = rt, lines = lines, cmap = cmap, vticklabel = vticklabel, fsizex = fsizex, fsizey = fsizey, lcol = lcol, lwdth = lwdth, cntcol = cntcol, dxc = dxc, dyc = dyc, dxax = dxax, dyax = dyax, ctght = ctght, fontsize = fontsize, unitcbr = unitcbr, unitx = unitx, unity = unity, bgc = bgc, sngl_cbar = sngl_cbar, lonv = lonv, latv = latv, varx = varx, vary = vary, angles = angles, scale = scale, scale_units = scale_units, headwidth = headwidth, headlength = headlength, headaxislength = headaxislength, vcol = vcol, dycb = dycb, cbt = cbt, btm = btm, fontsizexy = fontsizexy, flabel = flabel, bbox = bbox, tlabel = tlabel, dyt = dyt, cfig2 = cfig2)

# def fig9(pngfile, lon, lat, varf, varfl = [], vartrk = [], lonr = [120, 210, 30], latr = [20, 50, 10], level = [''], vr=[-999,-999,21], rt = 10, lines = [0.], cmap = cmo.balance, vticklabel = [''], fsizex = 8, fsizey = 7, lcol = 'k', lwdth = 1, cntcol = 'k', dxc = 0.015, dyc = 0.3, dxax = 3., dyax = 1.2, ctght = False, fontsize = 10, unitcbr = r'[${}^\circ$C]', unitx0 = 0.98, unitx1 = 1.02, unity = -2.6, bgc = '', dycb = 0.06, cbt = 0.015, btm = 0.1, fontsizexy = 8):

#     fig5(pngfile, lon, lat, varf, varfl = varfl, vartrk = vartrk, lonr = lonr, latr = latr, level = level, vr=vr, rt = rt, lines = lines, cmap = cmap, vticklabel = vticklabel, fsizex = fsizex, fsizey = fsizey, lcol = lcol, lwdth = lwdth, cntcol = cntcol, dxc = dxc, dyc = dyc, dxax = dxax, dyax = dyax, ctght = ctght, fontsize = fontsize, unitcbr = unitcbr, unitx = unitx, unity = unity, bgc = bgc, dycb = dycb, cbt = cbt, btm = btm, fontsizexy = fontsizexy)
    
    
    
    

def fig01_org(pngfile, lon, lat, varf, varfl = [], vartrk = [], lonr = [120, 240, 30], latr = [20, 50, 10], level = [''], vr=[-999,-999,21], rt = 10, lines = [0.], cmap = cmo.balance, xmintrk = 120, xmaxtrk = 240, tmintrks = [15,15], tmaxtrks = [21,21], tinttrks = [4,4], cdf = False, clg = True, vticklabel = [''], rmx = 10, cnrm = False):

    print(pngfile)
    R0 = 6.375e6
    lonmin, lonmax, lonint = lonr
    latmin, latmax, latint = latr
    nrows = int(np.shape(varf)[0]/2)
    ncols = 2
    netr = 4
    ntrck = np.shape(vartrk)[0]
    nrmax = int(netr/2)*ntrck
    
    # lonlatc = '_'+str(lonmin)+'-'+str(lonmax)+'E'+'-'+str(latmin)+'-'+str(latmax)+'N'
    imin = np.maximum(np.argmin(np.abs(lon-0.5-lonmin)), 1); imax = np.argmin(np.abs(lon+0.5-lonmax)) + 1
    jmin = np.maximum(np.argmin(np.abs(lat-0.5-latmin)), 1); jmax = np.argmin(np.abs(lat+0.5-latmax)) + 1

    plt.rcParams['font.size'] = 11
    fig = plt.figure(figsize = (11, 11))
    ax = mc.set_maps(fig, nrows+nrmax, ncols, xlim = [lonmin, lonmax], ylim = [latmin, latmax], lon_interval = lonint, lat_interval = latint)
    
    ax, images, vticks, vticklabels = mc.imcfs(ax, lon[imin-1:imax+1], lat[jmin-1:jmax+1], varf[:,jmin-1:jmax+1,imin-1:imax+1], nrows, ncols, vr = vr, rt = rt, level = level, cmap = cmap, vticklabel = vticklabel)
    if np.size(varfl) > 0:
        ax, lls = mc.imcs(ax, lon[imin-1:imax+1], lat[jmin-1:jmax+1], varfl[:,jmin-1:jmax+1,imin-1:imax+1], nrows, ncols, level = lines, lfontsize = 9, lwidth = 1.0)            
    nfg = 0    
    for nr in range(nrows):
        caxl = ax[nr,0].get_position()
        caxr = ax[nr,-1].get_position()
        caxv = ax[nr,0].get_position()
        # for m0 in range(ncols):
        #     ax[n1+1,m0].remove()
        #     cax = fig.add_axes([caxl.x0, 0.5*(caxv.y0+caxv.y1),caxr.x1-caxl.x0,0.01])
        cax = fig.add_axes([caxl.x0, caxv.y0-0.02*(nrows-nr)-0.018*nr,caxr.x1-caxl.x0, 0.015])
        cbar = plt.colorbar(images[2*nr+1], cax = cax, orientation = 'horizontal', ticks = vticks[2*nr+1])
        cbars = [cbar]
        if np.size(vticklabels) != 1:
            if vticklabels[0] != ['']:
                cbar.ax.set_xticklabels(vticklabels[0])
                
        for nc in range(ncols):
            # ax[nr,nc].plot(vartrk[0][0][0][0], vartrk[0][0][4][0], 'g', marker = 'x', markersize = 4)
            # ax[nr,nc].plot(vartrk[1][0][0][0], vartrk[1][0][4][0], 'g', marker = 's', markersize = 4)
            # ax[nr,nc].plot(vartrk[0][0][0][0]-180, vartrk[0][0][4][0], 'orange', marker = 'x', markersize = 8)
            # ax[nr,nc].plot(vartrk[1][0][0][0]-180, vartrk[1][0][4][0], 'g', marker = 'x', markersize = 8)            
            ax[nr,nc].text(vartrk[0][0][0][0]-180, vartrk[0][0][4][0], 'x', color = 'orange', fontsize = 20, fontweight = 'bold', ha = 'center', va = 'center')
            ax[nr,nc].text(vartrk[1][0][0][0]-180, vartrk[1][0][4][0], 'x', color = 'g', fontsize = 20, fontweight = 'bold', ha = 'center', va = 'center')

            # if nr == 1:
                # ax[nr,nc].plot(vartrk[0][nc][0]-180, vartrk[0][nc][4], color = 'orange', linewidth = 1)
                # ax[nr,nc].plot(vartrk[1][nc][0]-180, vartrk[1][nc][4], color = 'g', linewidth = 1)                        

            ax[nr,nc].plot(vartrk[0][nc][0]-180, vartrk[0][nc][4], color = 'orange', linewidth = 1)
            ax[nr,nc].plot(vartrk[1][nc][0]-180, vartrk[1][nc][4], color = 'g', linewidth = 1)                        
                
            
            ax[nr,nc].text(lonr[0]-180+5, latr[1]-8, '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')
            nfg += 1
            for lonc in np.arange(lonr[0], lonr[1]+1, lonr[2]):
                if np.round(lonc) < 180:                    
                    txt = str(np.round(lonc))+'E'
                elif np.round(lonc) > 180:
                    txt = str(np.round(360-lonc))+'W'
                else:
                    txt = '180'                    
                # ax[nr, nc].text(lonc, latr[0], txt, ha = 'center', va = 'top')
                ax[nr,nc].text(lonc-180, latr[0]-2, txt, ha = 'center', va = 'top', fontsizexy = fontsizexy)
            for latc in np.arange(latr[0], latr[1]+1, latr[2]):
                # ax[nr, nc].text(lonr[0], latc, str(int(latc))+'N', ha = 'right', va = 'center')
                ax[nr,nc].text(lonr[0]-180-2, latc, str(int(latc))+'N', ha = 'right', va = 'center')                
        
                
    for nt in range(ntrck):
        dlon = 0.1
        xmaxtrk = vartrk[nt][0][0][0]
        # if rmx > 0:        
        #     lonLI = xmintrk -0.5*rmx + dlon * (np.arange(int((xmaxtrk-xmintrk+0.5*rmx)/dlon)+3)-1)            
        # else:
        #     # lonLI = xmintrk + dlon * np.arange(int((xmaxtrk-xmintrk)/dlon)+1)
        #     lonLI = xmintrk + dlon * (np.arange(int((xmaxtrk-xmintrk)/dlon)+3)-1)
        lonLI = xmintrk + dlon * (np.arange(int((xmaxtrk-xmintrk)/dlon)+3)-1)            
        # lonLI = np.min(lon) + dlon * np.arange(int((np.max(lon)-np.min(lon))/dlon)+1)  
        # iiminM = np.where(lonLI > np.min(vartrk[nt][0][0]))[0][0]
        # iimaxM = np.where(lonLI < np.max(vartrk[nt][0][0]))[0][-1] + 1
        
        # iiminMb = np.where(lonLI > np.min(vartrk[nt][1][0]))[0][0]
        # iimaxMb = np.where(lonLI < np.max(vartrk[nt][1][0]))[0][-1] + 1

        mlttMMb= vartrk[nt][0][1]
        mlttMM = vartrk[nt][1][1]

        # dmlttMM13b  = [vartrk[nt][0][1], vartrk[nt][0][2][2]+vartrk[nt][0][2][3]-vartrk[nt][0][2][1], vartrk[nt][0][2][4]+vartrk[nt][0][2][5]]
        # dmlttMM13 = [vartrk[nt][1][1], vartrk[nt][1][2][2]+vartrk[nt][1][2][3]-vartrk[nt][1][2][1], vartrk[nt][1][2][4]+vartrk[nt][1][2][5]]

        # dmlttMM13b = [vartrk[nt][0][1], vartrk[nt][0][2][2]+vartrk[nt][0][2][3]-vartrk[nt][0][2][1], vartrk[nt][0][2][4]+vartrk[nt][0][2][5], vartrk[nt][0][1]+vartrk[nt][0][2][1]]
        # dmlttMM13  = [vartrk[nt][1][1], vartrk[nt][1][2][2]+vartrk[nt][1][2][3]-vartrk[nt][1][2][1], vartrk[nt][1][2][4]+vartrk[nt][1][2][5], vartrk[nt][1][1]+vartrk[nt][1][2][1]]
        dmlttMM13b = [vartrk[nt][0][1], vartrk[nt][0][2][2]+vartrk[nt][0][2][3]-vartrk[nt][0][2][1], vartrk[nt][0][2][4]+vartrk[nt][0][2][5]]
        dmlttMM13  = [vartrk[nt][1][1], vartrk[nt][1][2][2]+vartrk[nt][1][2][3]-vartrk[nt][1][2][1], vartrk[nt][1][2][4]+vartrk[nt][1][2][5]]        

        dmlttMM1b = [vartrk[nt][0][2][2]+vartrk[nt][0][2][3]-vartrk[nt][0][2][1],
                     vartrk[nt][0][2][6]-vartrk[nt][0][2][1],vartrk[nt][0][2][7], 
                     vartrk[nt][0][2][2]+vartrk[nt][0][2][3]-vartrk[nt][0][2][6]-vartrk[nt][0][2][7]]
        
        dmlttMM1  = [vartrk[nt][1][2][2]+vartrk[nt][1][2][3]-vartrk[nt][1][2][1],
                     vartrk[nt][1][2][6]-vartrk[nt][1][2][1],vartrk[nt][1][2][7], 
                     vartrk[nt][1][2][2]+vartrk[nt][1][2][3]-vartrk[nt][1][2][6]-vartrk[nt][1][2][7]]        


        dxl0 = R0 * np.cos(np.deg2rad(0.5*(vartrk[nt][0][4][:-1]+vartrk[nt][0][4][1:]))) * np.deg2rad(np.diff(vartrk[nt][0][0]))
        dyl0 = R0 * np.deg2rad(np.diff(vartrk[nt][0][4]))          
        lnl0 = np.sqrt(dxl0**2+dyl0**2)                
        aul0 = lnl0/vartrk[nt][0][3][1:]

        latl = interpolate.interp1d(vartrk[nt][0][0], vartrk[nt][0][4], fill_value = 'extrapolate')(lonLI)
        aul  = interpolate.interp1d(0.5*(vartrk[nt][0][0][:-1]+vartrk[nt][0][0][1:]), aul0, fill_value = 'extrapolate')(0.5*(lonLI[:-1]+lonLI[1:]))
        
        dxh0 = R0 * np.cos(np.deg2rad(0.5*(vartrk[nt][1][4][:-1]+vartrk[nt][1][4][1:]))) * np.deg2rad(np.diff(vartrk[nt][1][0]))
        dyh0 = R0 * np.deg2rad(np.diff(vartrk[nt][1][4]))          
        lnh0 = np.sqrt(dxh0**2+dyh0**2)                
        auh0 = lnh0/vartrk[nt][1][3][1:]

        lath = interpolate.interp1d(vartrk[nt][1][0], vartrk[nt][1][4], fill_value = 'extrapolate')(lonLI)
        auh  = interpolate.interp1d(0.5*(vartrk[nt][1][0][:-1]+vartrk[nt][1][0][1:]), auh0, fill_value = 'extrapolate')(0.5*(lonLI[:-1]+lonLI[1:]))        

        cols = ['k', 'b', 'r', 'g', 'c']        
        for ne in range(netr):
            # axl = ax[nr+nt*netr+ne+1, 0].get_position()
            # axr = ax[nr+nt*netr+ne+1,-1].get_position()                    
            # axadd = fig.add_axes([axl.x0, axl.y0, axr.x1-axl.x0, axl.y1-axl.y0])
            # axadd = fig.add_axes([0.55, 0.1, 0.4, 0.35])
            nc = np.mod(ne,2)
            nr = nt*int(netr/2)+int(ne/2)
            
            axadd = fig.add_axes([0.05+0.5*nc+0.075*(1-nc), 0.07+(0.35/nrmax+0.05)*(nrmax-nr-1), 0.35, 0.35/nrmax])            

            ymin = tmintrks[ne][nt]; ymax = tmaxtrks[ne][nt]; yint = tinttrks[ne][nt]            
            if ne == 0:
                axadd.plot(vartrk[nt][0][0], vartrk[nt][0][1], '--k', label = 'LR-exp', linewidth = 2)
                axadd.plot(vartrk[nt][1][0], vartrk[nt][1][1], 'k',   label = 'HR-exp', linewidth = 2)
            elif ne == 1:
                labels = [r'$\Delta \theta$', '3D', '1D', 'Res']
                for nn in range(np.shape(dmlttMM13)[0]):                    
                    ylr = interpolate.interp1d(vartrk[nt][0][0], dmlttMM13b[nn], fill_value = 'extrapolate')(lonLI)                    
                    yhr = interpolate.interp1d(vartrk[nt][1][0],  dmlttMM13[nn], fill_value = 'extrapolate')(lonLI)

                    # if nn == 0:
                    #     axadd.plot(lonLI, yhr-ylr, cols[nn], linewidth = 2)
                    #     # ii = np.argmin(np.abs(lonLI-xmintrk))
                    #     ydini = yhr[0]-ylr[0]
                    # else:
                    #     axadd.plot(lonLI, yhr-ylr-(yhr[0]-ylr[0])+ydini, cols[nn], linewidth = 2, label = labels[nn])
                    # axadd.plot(0.5*(lonLI[:-1]+lonLI[1:]), np.diff(yhr-ylr)/dlon, cols[nn], linewidth = 2, label = labels[nn])
                    if cnrm:
                        axadd.plot(0.5*(lonLI[:-1]+lonLI[1:]), np.diff(yhr-ylr)/dlon, cols[nn], linewidth = 0.5, label = labels[nn])
                    axadd.plot(rm1d(0.5*(lonLI[:-1]+lonLI[1:]), dlon, rmx), rm1d(np.diff(yhr-ylr)/dlon, dlon, rmx), cols[nn], linewidth = 2, label = labels[nn])
                    
            # elif ne > 1:
            elif ne == 2:                
                qtl0 = np.diff(vartrk[nt][0][2][4])/vartrk[nt][0][3][1:]
                qbl0 = np.diff(vartrk[nt][0][2][5])/vartrk[nt][0][3][1:]

                qtl  = interpolate.interp1d(0.5*(vartrk[nt][0][0][:-1]+vartrk[nt][0][0][1:]), qtl0, fill_value = 'extrapolate')(0.5*(lonLI[:-1]+lonLI[1:]))
                qbl  = interpolate.interp1d(0.5*(vartrk[nt][0][0][:-1]+vartrk[nt][0][0][1:]), qbl0, fill_value = 'extrapolate')(0.5*(lonLI[:-1]+lonLI[1:]))                                        
                dxl = R0 * np.cos(np.deg2rad(0.5*(latl[:-1]+latl[1:]))) * np.deg2rad(np.diff(lonLI))
                dyl = R0 * np.deg2rad(np.diff(latl))          
                lnl = np.sqrt(dxl**2+dyl**2)
                                
                qth0 = np.diff(vartrk[nt][1][2][4])/vartrk[nt][1][3][1:]
                qbh0 = np.diff(vartrk[nt][1][2][5])/vartrk[nt][1][3][1:]                

                qth  = interpolate.interp1d(0.5*(vartrk[nt][1][0][:-1]+vartrk[nt][1][0][1:]), qth0, fill_value = 'extrapolate')(0.5*(lonLI[:-1]+lonLI[1:]))
                qbh  = interpolate.interp1d(0.5*(vartrk[nt][1][0][:-1]+vartrk[nt][1][0][1:]), qbh0, fill_value = 'extrapolate')(0.5*(lonLI[:-1]+lonLI[1:]))                                        
                dxh = R0 * np.cos(np.deg2rad(0.5*(lath[:-1]+lath[1:]))) * np.deg2rad(np.diff(lonLI))
                dyh = R0 * np.deg2rad(np.diff(lath))          
                lnh = np.sqrt(dxh**2+dyh**2)

                ylr = interpolate.interp1d(vartrk[nt][0][0], dmlttMM13b[2], fill_value = 'extrapolate')(lonLI)                    
                yhr = interpolate.interp1d(vartrk[nt][1][0],  dmlttMM13[2], fill_value = 'extrapolate')(lonLI)                
                # axadd.plot(lonLI, yhr-ylr-(yhr[0]-ylr[0])+ydini, 'k', linewidth = 2, label = '1D')
                # axadd.plot(0.5*(lonLI[:-1]+lonLI[1:]), np.diff(yhr-ylr)/dlon, 'k', linewidth = 2, label = '1D')
                if cnrm:                
                    axadd.plot(0.5*(lonLI[:-1]+lonLI[1:]), np.diff(yhr-ylr)/dlon, 'k', linewidth = 0.5)
                axadd.plot(rm1d(0.5*(lonLI[:-1]+lonLI[1:]), dlon, rmx), rm1d(np.diff(yhr-ylr)/dlon, dlon, rmx), 'k', linewidth = 2, label = '1D')                


                # for nn in range(4):
                # for nn in range(7):                    
                #     lnst = '-'
                #     if nn == 0:
                #         dydt = qth-qtl
                #         dtmp = lnl/aul
                #         col = 'r'
                #         label = 'Q'
                #     elif nn == 1:
                #         dydt = -(qbh-qbl)
                #         dtmp = lnl/aul
                #         col = 'g' 
                #         label = 'R'                       
                #     elif nn == 2:
                #         dydt = qtl-qbl
                #         dtmp = lnh/auh-lnl/aul
                #         col = 'b'
                #         label = 'dt'   
                #     elif nn == 3:
                #         dydt = qth-qtl-(qbh-qbl)
                #         dtmp = lnh/auh-lnl/aul
                #         col = 'c' 
                #         label = 'NL'                                 
                #     elif nn == 4:
                #         dydt = qtl-qbl
                #         dtmp = lnl/auh-lnl/aul
                #         col = 'b'
                #         label = 'dt'
                #         lnst = '--'                        
                #     elif nn == 5:
                #         dydt = qtl-qbl
                #         dtmp = lnh/aul-lnl/aul
                #         col = 'b'
                #         label = 'dt'
                #         lnst = ':'                          
                #     elif nn == 6:
                #         dydt = qtl-qbl
                #         dtmp = (1/auh-1/aul)*(lnh-lnl)
                #         col = 'b'
                #         label = 'dt'
                #         lnst = 'dashdot'        

                for nn in range(5):                    
                    lnst = '-'
                    if nn == 0:
                        dydt = qth-qtl
                        dtmp = lnh/auh
                        col = 'r'
                        label = 'Q'
                    elif nn == 1:
                        dydt = -(qbh-qbl)
                        dtmp = lnh/auh
                        col = 'g' 
                        label = 'R'                       
                    elif nn == 2:
                        dydt = qtl-qbl
                        dtmp = lnh/auh-lnl/aul
                        col = 'b'
                        label = 'dt'   
                    elif nn == 3:
                        dydt = qtl-qbl
                        dtmp = lnh/auh-lnh/aul
                        col = 'b'
                        label = 'dt'
                        lnst = '--'                        
                    elif nn == 4:
                        dydt = qtl-qbl
                        dtmp = lnh/aul-lnl/aul
                        col = 'b'
                        label = 'dt'
                        lnst = ':'                          
                        
                    nli = np.size(lonLI)                    
                    yy = np.zeros(nli)
                    for nl in range(nli-1):
                        yy[nl+1] = yy[nl] - dydt[nl]*dtmp[nl]
                    # axadd.plot(lonLI, yy-yy[0]+ydini, col, linewidth = 2, label = label)
                    # axadd.plot(lonLI, yy-yy[0]+ydini, col, linewidth = 2, label = label, linestyle = lnst)
                    # axadd.plot(0.5*(lonLI[:-1]+lonLI[1:]), np.diff(yy)/dlon, col, linewidth = 2, label = label, linestyle = lnst)
                    if cnrm:                    
                        axadd.plot(0.5*(lonLI[:-1]+lonLI[1:]), np.diff(yy)/dlon, col, linewidth = 0.5, linestyle = lnst)                    
                    axadd.plot(rm1d(0.5*(lonLI[:-1]+lonLI[1:]), dlon, rmx), rm1d(np.diff(yy)/dlon, dlon, rmx), col, linewidth = 2, label = label, linestyle = lnst)                              
                               
            elif ne == 3:
                labels = ['3D', 'MH', 'MV', 'ED']                       
                for nn in range(np.shape(dmlttMM1)[0]):                    
                    ylr = interpolate.interp1d(vartrk[nt][0][0], dmlttMM1b[nn], fill_value = 'extrapolate')(lonLI)                    
                    yhr = interpolate.interp1d(vartrk[nt][1][0],  dmlttMM1[nn], fill_value = 'extrapolate')(lonLI)
                    # axadd.plot(lonLI, yhr-ylr-(yhr[0]-ylr[0])+ydini, cols[nn], linewidth = 2, label = labels[nn])
                    # axadd.plot(0.5*(lonLI[:-1]+lonLI[1:]), np.diff(yhr-ylr)/dlon, cols[nn], linewidth = 2, label = labels[nn])
                    if cnrm:                    
                        axadd.plot(0.5*(lonLI[:-1]+lonLI[1:]), np.diff(yhr-ylr)/dlon, cols[nn], linewidth = 0.5)
                    axadd.plot(rm1d(0.5*(lonLI[:-1]+lonLI[1:]), dlon, rmx), rm1d(np.diff(yhr-ylr)/dlon, dlon, rmx), cols[nn], linewidth = 2, label = labels[nn])                         


            axadd.set_xlim(xmintrk, xmaxtrk)
            axadd.set_ylim(ymin, ymax)
            axadd.set_yticks(np.linspace(ymin, ymax, yint))

            axadd.text(xmintrk+0.01*(xmaxtrk-xmintrk), ymin+0.01*(ymax-ymin), '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')
            nfg += 1
            # axadd.legend()        
            # if clg:

    # for nt in range(ntrck):
    #     for ne in range(netr):            
    #         ax[nr+nt*netr+ne+1, 0].remove()
    #         ax[nr+nt*netr+ne+1,-1].remove()
    for nt in range(ntrck):
        for ne in range(int(netr/2)):            
            ax[nrows+nt*int(netr/2)+ne, 0].remove()
            ax[nrows+nt*int(netr/2)+ne,1].remove()                                                
        
    # plt.tight_layout()
    plt.savefig(pngfile)
    plt.close()        

def fig3_org(pngfile, lon, lat, varf, varfl = [], vartrk = [], lonr = [120, 240, 30], latr = [15, 45, 15], level = [''], vr=[-999,-999,21], rt = 10, lines = [0.], cmap = cmo.balance, vticklabel = [''], fsizex = 8, fsizey = 2.8, lcol = 'k', lwdth = 1, cntcol = 'k', dxc = 0.03, dyc = 0.18, dxax = 4., dyax = 1.2, ctght = False, fontsize = 10, unitcbr = r'[m]', unitx = 0.98, unity = -2.4, ncols = 3, vtrtgt = [], xmintrk = 140, xmaxtrk = 170, tmintrks = [16, 16, -.8], tmaxtrks = [21, 21, 3.2], tinttrks = [6, 6, 6], xtgt = 143, xticks = np.linspace(140, 170, 4), xticklabels = ['140E', '150E', '160E', '170E']):

    print(pngfile)
    R0 = 6.375e6
    lonmin, lonmax, lonint = lonr
    latmin, latmax, latint = latr
    nrowm = int(np.shape(varf)[0]/ncols)
    nrowl = 1
    nrows = nrowm + nrowl    

    # ntrck0 = np.shape(vartrk[0])[0]
    # ntrck  = np.shape(vartrk[1])[0]
    
    plt.rcParams['font.size'] = fontsize
    fig = plt.figure(figsize = (fsizex, fsizey))
    # plt.subplots_adjust(left=0.05, right = 0.96, top = 0.98, bottom = 0.1)
    plt.subplots_adjust(left=0.05, right = 0.96, top = 1.05, bottom = 0.1)            
    ax = mc.set_maps(fig, nrows, ncols, xlim = [lonmin, lonmax], ylim = [latmin, latmax], lon_interval = lonint, lat_interval = latint)
    
    ax, images, vticks, vticklabels = mc.imcfs(ax, lon, lat, varf, nrows, ncols, vr = vr, rt = rt, level = level, cmap = cmap, vticklabel = vticklabel)
    if np.size(varfl) > 0:
        ax, lls = mc.imcs(ax, lon, lat, varfl, nrows, ncols, level = lines, lfontsize = 8, lwidth = 1.0, cntcol = cntcol)     
    
    nfg = 0    
    for nr in range(nrowm):
        caxl = ax[nr,0].get_position()
        caxr = ax[nr,-1].get_position()
        caxv = ax[nr,0].get_position()
        # for m0 in range(ncols):
        #     ax[n1+1,m0].remove()
        #     cax = fig.add_axes([caxl.x0, 0.5*(caxv.y0+caxv.y1),caxr.x1-caxl.x0,0.01])
        # cax = fig.add_axes([caxl.x0, caxv.y0-0.02*(nrows-nr)-0.018*nr,caxr.x1-caxl.x0, 0.015])
        # cax = fig.add_axes([caxl.x0, caxv.y0-0.15,caxr.x1-caxl.x0, 0.03])
        # cax = fig.add_axes([caxl.x0, caxv.y0-0.075,caxr.x1-caxl.x0, 0.02])
        cax = fig.add_axes([caxl.x0, caxv.y0-0.13,caxr.x1-caxl.x0, 0.03])                        
        cbar = plt.colorbar(images[2*nr+1], cax = cax, orientation = 'horizontal', ticks = vticks[2*nr+1])
        if unitcbr != '':
            cax.text(unitx, unity, unitcbr, transform=cax.transAxes)    
        cbars = [cbar]
        if np.size(vticklabels) != 1:
            if vticklabels[0] != ['']:
                cbar.ax.set_xticklabels(vticklabels[0])
        
        for nc in range(ncols):
            # if np.size(vartrk) > 0:
            if len(vartrk) > 0:                
                # ntrs = np.size(vartrk[nc][0])
                ntrs = np.shape(vartrk[nc][0])[0]
                for ntr in range(ntrs):
                    ax[nr,nc].plot(vartrk[nc][0][ntr]-180, vartrk[nc][1][ntr], color = lcol, linewidth = lwdth)
                    # print(vartrk[nc][0][ntr], vartrk[nc][1][ntr])

            if nc < 2:
                # nmax = np.where((xtgt<vtrtgt[nc][0][:-1])*(vtrtgt[nc][0][1:]<=xtgt))[0][0]
                nmax = np.where((xmintrk<vtrtgt[nc][0][:-1])*(vtrtgt[nc][0][1:]<=xmintrk))[0][0]                
                ax[nr,nc].plot(vtrtgt[nc][0][:nmax]-180, vtrtgt[nc][-1][:nmax], color = 'g', linewidth = 2*lwdth)     
            # ax[nr,nc].text(lonr[0]-180+5, latr[1]-8-2, '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')
            # ax[nr,nc].text(lonr[0]-180+5, latr[1]-0.2*(latr[1]-latr[0]), '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')
            # ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')
            # ax[nr,nc].text(lonr[0]-180+0.03*(lonr[1]-lonr[0]), latr[1]-0.4*(latr[1]-latr[0]), '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom', backgroundcolor = 'w')
            # ax[nr,nc].text(lonr[0]-180+0.03*(lonr[1]-lonr[0]), latr[1]-0.2*(latr[1]-latr[0]), r'$\ \ \ \ $', ha = 'left', va = 'bottom', backgroundcolor = 'w', fontsize = 5)
            ax[nr,nc].text(lonr[0]-180+0.03*(lonr[1]-lonr[0]), latr[1]-0.3*(latr[1]-latr[0]), '     ', ha = 'left', va = 'bottom', backgroundcolor = 'w', fontsize = 6)            
            ax[nr,nc].text(lonr[0]-180+0.025*(lonr[1]-lonr[0]), latr[1]-0.35*(latr[1]-latr[0]),  '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')             
            
            nfg += 1
            for lonc in np.arange(lonr[0], lonr[1]+1, lonr[2]):
                if np.round(lonc) < 180:                    
                    txt = str(np.round(lonc))+'E'
                elif np.round(lonc) > 180:
                    txt = str(np.round(360-lonc))+'W'
                else:
                    txt = '180'                    
                # ax[nr, nc].text(lonc, latr[0], txt, ha = 'center', va = 'top')
                ax[nr,nc].text(lonc-180, latr[0]-dxax, txt, ha = 'center', va = 'top')                
            for latc in np.arange(latr[0], latr[1]+1, latr[2]):
                # ax[nr, nc].text(lonr[0], latc, str(int(latc))+'N', ha = 'right', va = 'center')
                ax[nr,nc].text(lonr[0]-180-dyax, latc, str(int(latc))+'N', ha = 'right', va = 'center')                



    dx0 = R0 * np.cos(np.deg2rad(0.5*(vtrtgt[0][4][:-1]+vtrtgt[0][4][1:]))) * np.deg2rad(np.diff(vtrtgt[0][0]))
    dy0 = R0 * np.deg2rad(np.diff(vtrtgt[0][4]))       
    ln0 = np.sqrt(dx0**2+dy0**2)                
    au0 = ln0/vtrtgt[0][3][1:]
    # aul  = interpolate.interp1d(0.5*(vtrtgt[0][0][:-1]+vtrtgt[0][0][1:]), aul0, fill_value = 'extrapolate')(0.5*(lonLI[:-1]+lonLI[1:]))
    
    dx  = R0 * np.cos(np.deg2rad(0.5*(vtrtgt[1][4][:-1]+vtrtgt[1][4][1:]))) * np.deg2rad(np.diff(vtrtgt[1][0]))
    dy  = R0 * np.deg2rad(np.diff(vtrtgt[1][4]))          
    ln  = np.sqrt(dx**2+dy**2)                
    au  = ln/vtrtgt[1][3][1:]
    
    # lath = interpolate.interp1d(vtrtgt[1][0], vtrtgt[1][4], fill_value = 'extrapolate')(lonLI)
    # auh  = interpolate.interp1d(0.5*(vtrtgt[1][0][:-1]+vtrtgt[1][0][1:]), auh0, fill_value = 'extrapolate')(0.5*(lonLI[:-1]+lonLI[1:]))        
    
        
    if np.size(vtrtgt) > 0:
        for nc in range(3):
            caxl = ax[0,nc].get_position()
            axadd = fig.add_axes([caxl.x0, 0.1, caxl.x1-caxl.x0, 0.35])
            if nc < 2:            
                axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1], 'k', linewidth = 2)
                
                i = np.argmin(np.abs(vtrtgt[nc][0]-xtgt))
                tnd = vtrtgt[nc][2][6] - vtrtgt[nc][2][1]
                axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'g', linewidth = 2)                
                # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'g', linewidth = 2, label = r'$T^\prime_{ADV}$')                                 
                tnd = vtrtgt[nc][2][7] - vtrtgt[nc][2][1]                
                axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], ':g', linewidth = 2)
                tnd = vtrtgt[nc][2][6] - vtrtgt[nc][2][7]                
                axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], '--g', linewidth = 2)                                

                if nc == 0:
                    axadd.text(xmintrk+0.01*(xmaxtrk-xmintrk), tmintrks[nc]+0.2*(tmaxtrks[nc]-tmintrks[nc]), r'$T^\prime_{ADV}$', color = 'g', fontsize = fontsize)
            
                tnd = vtrtgt[nc][2][2] - vtrtgt[nc][2][6]
                axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'r', linewidth = 2)

                # tnd = vtrtgt[nc][2][8] - vtrtgt[nc][2][9]
                # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], ':r', linewidth = 2)
                # tnd = vtrtgt[nc][2][2] - vtrtgt[nc][2][6] - (vtrtgt[nc][2][8] - vtrtgt[nc][2][9])
                # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], '--r', linewidth = 2)         

                if nc == 0:
                    axadd.text(xmintrk+0.15*(xmaxtrk-xmintrk), tmintrks[nc]+0.2*(tmaxtrks[nc]-tmintrks[nc]), r'$T_{EDD}$', color = 'r', fontsize = fontsize)
                                    
                tnd = vtrtgt[nc][2][3]                
                # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'm', linewidth = 2)
                axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'c', linewidth = 2)
                if nc == 0:
                    axadd.text(xmintrk+0.01*(xmaxtrk-xmintrk), tmintrks[nc]+0.02*(tmaxtrks[nc]-tmintrks[nc]), r'$T_{SGS}$', color = 'c', fontsize = fontsize)
                    
                tnd = vtrtgt[nc][2][4]
                axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'b', linewidth = 2)
                if nc == 0:
                    axadd.text(xmintrk+0.15*(xmaxtrk-xmintrk), tmintrks[nc]+0.02*(tmaxtrks[nc]-tmintrks[nc]), r'$T_{SFC}$', color = 'b', fontsize = fontsize)
                    
                # tnd = vtrtgt[nc][2][5]
                # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'c', linewidth = 2)                                
            else:
                vint = interpolate.interp1d(vtrtgt[0][0], vtrtgt[0][1], fill_value = 'extrapolate')(vtrtgt[1][0])
                axadd.plot(vtrtgt[1][0], vtrtgt[1][1]-vint, 'k', linewidth = 2)

                i0 = np.argmin(np.abs(vtrtgt[0][0]-xtgt))
                i  = np.argmin(np.abs(vtrtgt[1][0]-xtgt))
                dt0 = vtrtgt[1][1][i] - vtrtgt[0][1][i0]
                
                tnd0 = vtrtgt[0][2][6] - vtrtgt[0][2][1]
                tnd  = vtrtgt[1][2][6] - vtrtgt[1][2][1]                
                dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'g', linewidth = 2)

                tnd0 = vtrtgt[0][2][7] - vtrtgt[0][2][1]
                tnd  = vtrtgt[1][2][7] - vtrtgt[1][2][1]
                dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], ':g', linewidth = 2)

                tnd0 = vtrtgt[0][2][6] - vtrtgt[0][2][7]
                tnd  = vtrtgt[1][2][6] - vtrtgt[1][2][7]
                dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], '--g', linewidth = 2)

                
                tnd0 = vtrtgt[0][2][2] - vtrtgt[0][2][6]
                tnd  = vtrtgt[1][2][2] - vtrtgt[1][2][6]                
                dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'r', linewidth = 2)

                # tnd0 = vtrtgt[0][2][8] - vtrtgt[0][2][9]
                # tnd  = vtrtgt[1][2][8] - vtrtgt[1][2][9]
                # dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                # axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], ':r', linewidth = 2)

                # tnd0 = vtrtgt[0][2][2] - vtrtgt[0][2][6] - (vtrtgt[0][2][8] - vtrtgt[0][2][9])
                # tnd  = vtrtgt[1][2][2] - vtrtgt[1][2][6] - (vtrtgt[1][2][8] - vtrtgt[1][2][9])
                # dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                # axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], '--r', linewidth = 2)
                
                tnd0 = vtrtgt[0][2][3]
                tnd  = vtrtgt[1][2][3]
                dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                # axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'm', linewidth = 2)
                axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'c', linewidth = 2)                

                tnd0 = vtrtgt[0][2][4]
                tnd  = vtrtgt[1][2][4]
                dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'b', linewidth = 2)

                # tnd0 = vtrtgt[0][2][5]
                # tnd  = vtrtgt[1][2][5]
                # dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                # axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'c', linewidth = 2)


                dx0 = R0 * np.cos(np.deg2rad(0.5*(vtrtgt[0][4][:-1]+vtrtgt[0][4][1:]))) * np.deg2rad(np.diff(vtrtgt[0][0]))
                dy0 = R0 * np.deg2rad(np.diff(vtrtgt[0][4]))       
                ln0 = np.sqrt(dx0**2+dy0**2)                
                au0 = ln0/vtrtgt[0][3][1:]                
                qt0 = np.diff(vtrtgt[0][2][4])/vtrtgt[0][3][1:]

                
                dx  = R0 * np.cos(np.deg2rad(0.5*(vtrtgt[1][4][:-1]+vtrtgt[1][4][1:]))) * np.deg2rad(np.diff(vtrtgt[1][0]))
                dy  = R0 * np.deg2rad(np.diff(vtrtgt[1][4]))          
                ln  = np.sqrt(dx**2+dy**2)                
                au  = ln/vtrtgt[1][3][1:]                                
                qt  = np.diff(vtrtgt[1][2][4])/vtrtgt[1][3][1:]


                ltb = interpolate.interp1d(vtrtgt[0][0], vtrtgt[0][4], fill_value = 'extrapolate')(vtrtgt[1][0])
                dxb = R0 * np.cos(np.deg2rad(0.5*(ltb[:-1]+ltb[1:]))) * np.deg2rad(np.diff(vtrtgt[1][0]))
                dyb = R0 * np.deg2rad(np.diff(ltb))
                lnb = np.sqrt(dxb**2+dyb**2)
                aub = interpolate.interp1d(0.5*(vtrtgt[0][0][:-1]+vtrtgt[0][0][1:]), au0, fill_value = 'extrapolate')(0.5*(vtrtgt[1][0][:-1]+vtrtgt[1][0][1:]))
                qtb = interpolate.interp1d(0.5*(vtrtgt[0][0][:-1]+vtrtgt[0][0][1:]), qt0, fill_value = 'extrapolate')(0.5*(vtrtgt[1][0][:-1]+vtrtgt[1][0][1:]))
                
                dtndq = np.zeros(i+1)
                dtndu = np.zeros(i+1)
                dtndl = np.zeros(i+1)                
                for ii in range(i):
                    # dtndq[ii+1] = dtndq[ii] - (qt[i-ii-1] - qtb[i-ii-1])*lnb[i-ii-1]/aub[i-ii-1]
                    dtndq[ii+1] = dtndq[ii] - (qt[i-ii-1] - qtb[i-ii-1])*lnb[i-ii-1]/au[i-ii-1]                    
                    dtndu[ii+1] = dtndu[ii] - qtb[i-ii-1]*lnb[i-ii-1]*(1/au[i-ii-1]-1/aub[i-ii-1])
                    # dtndl[ii+1] = dtndl[ii] - qtb[i-ii-1]*(ln[i-ii-1]-lnb[i-ii-1])/aub[i-ii-1]
                    dtndl[ii+1] = dtndl[ii] - qtb[i-ii-1]*(ln[i-ii-1]-lnb[i-ii-1])/au[i-ii-1]                     

                xx = 0.5*(vtrtgt[1][0][:-1]+vtrtgt[1][0][1:])[:i+1][::-1]
                
                axadd.plot(xx, dt0+dtndq, ':b', linewidth = 2)
                axadd.plot(xx, dt0+dtndu, '--b', linewidth = 2)
                axadd.plot(xx, dt0+dtndl, 'b', linestyle = 'dashdot', linewidth = 2)                
                
                
            axadd.set_xlim(xmintrk, xmaxtrk)
            axadd.set_xticks(xticks)
            axadd.set_xticklabels(xticklabels)                        
            axadd.set_ylim(tmintrks[nc], tmaxtrks[nc])
            axadd.set_yticks(np.linspace(tmintrks[nc], tmaxtrks[nc], tinttrks[nc]))
            # axadd.text(xmintrk+dxc*(xmaxtrk-xmintrk), tmaxtrks[nc]-0.12*(tmaxtrks[nc]-tmintrks[nc]), '('+chr(ord("a")+nc+3)+')', ha = 'left', va = 'bottom')
            axadd.text(xmintrk+dxc*(xmaxtrk-xmintrk), tmaxtrks[nc]-dyc*(tmaxtrks[nc]-tmintrks[nc]), '('+chr(ord("a")+nc+3)+')', ha = 'left', va = 'bottom')            
            # axadd.text(xmintrk+dxc*(xmaxtrk-xmintrk), tmintrks[nc]+0.02*(tmaxtrks[nc]-tmintrks[nc]), '('+chr(ord("a")+nc+3)+')', ha = 'left', va = 'bottom')

            axadd.text(xmintrk-0.15*(xmaxtrk-xmintrk), tmaxtrks[nc]+0.05*(tmaxtrks[nc]-tmintrks[nc]), r'[${}^\circ$C]', ha = 'left', va = 'bottom')
            # if nc == 0:
            #     axadd.legend()
            
            
        for nc in range(3):        
            ax[nrowm,nc].remove()
            
    if ctght:
        plt.tight_layout()
    plt.savefig(pngfile)
    plt.close()        

def fig4_org(pngfile, lon, lat, varf, varfl = [], vartrk = [], lonr = [120, 240, 30], latr = [15, 45, 15], level = [''], vr=[-999,-999,21], rt = 10, lines = [0.], cmap = cmo.balance, vticklabel = [''], fsizex = 8, fsizey = 2.8, lcol = 'k', lwdth = 1, cntcol = 'k', dxc = 0.03, dyc = 0.18, dxax = 4., dyax = 1.2, ctght = False, fontsize = 10, unitcbr = r'[m]', unitx = 0.98, unity = -2.4, ncols = 3, vtrtgt = [], xmintrk = 140, xmaxtrk = 170, tmintrks = [16, 16, -.8], tmaxtrks = [21, 21, 3.2], tinttrks = [6, 6, 6], xtgt = 143, xticks = np.linspace(140, 170, 4), xticklabels = ['140E', '150E', '160E', '170E']):

    print(pngfile)
    R0 = 6.375e6
    lonmin, lonmax, lonint = lonr
    latmin, latmax, latint = latr
    nrowm = int(np.shape(varf)[0]/ncols)
    nrowl = 1
    nrows = nrowm + nrowl    

    # ntrck0 = np.shape(vartrk[0])[0]
    # ntrck  = np.shape(vartrk[1])[0]
    
    plt.rcParams['font.size'] = fontsize
    fig = plt.figure(figsize = (fsizex, fsizey))
    # plt.subplots_adjust(left=0.05, right = 0.96, top = 0.98, bottom = 0.1)
    plt.subplots_adjust(left=0.05, right = 0.96, top = 1.05, bottom = 0.1)            
    ax = mc.set_maps(fig, nrows, ncols, xlim = [lonmin, lonmax], ylim = [latmin, latmax], lon_interval = lonint, lat_interval = latint)
    
    ax, images, vticks, vticklabels = mc.imcfs(ax, lon, lat, varf, nrows, ncols, vr = vr, rt = rt, level = level, cmap = cmap, vticklabel = vticklabel)
    if np.size(varfl) > 0:
        ax, lls = mc.imcs(ax, lon, lat, varfl, nrows, ncols, level = lines, lfontsize = 8, lwidth = 1.0, cntcol = cntcol)     
    
    nfg = 0    
    for nr in range(nrowm):
        caxl = ax[nr,0].get_position()
        caxr = ax[nr,-1].get_position()
        caxv = ax[nr,0].get_position()
        # for m0 in range(ncols):
        #     ax[n1+1,m0].remove()
        #     cax = fig.add_axes([caxl.x0, 0.5*(caxv.y0+caxv.y1),caxr.x1-caxl.x0,0.01])
        # cax = fig.add_axes([caxl.x0, caxv.y0-0.02*(nrows-nr)-0.018*nr,caxr.x1-caxl.x0, 0.015])
        # cax = fig.add_axes([caxl.x0, caxv.y0-0.15,caxr.x1-caxl.x0, 0.03])
        # cax = fig.add_axes([caxl.x0, caxv.y0-0.075,caxr.x1-caxl.x0, 0.02])
        cax = fig.add_axes([caxl.x0, caxv.y0-0.13,caxr.x1-caxl.x0, 0.03])                        
        cbar = plt.colorbar(images[2*nr+1], cax = cax, orientation = 'horizontal', ticks = vticks[2*nr+1])
        if unitcbr != '':
            cax.text(unitx, unity, unitcbr, transform=cax.transAxes)    
        cbars = [cbar]
        if np.size(vticklabels) != 1:
            if vticklabels[0] != ['']:
                cbar.ax.set_xticklabels(vticklabels[0])
        
        for nc in range(ncols):
            # if np.size(vartrk) > 0:
            if len(vartrk) > 0:                
                # ntrs = np.size(vartrk[nc][0])
                ntrs = np.shape(vartrk[nc][0])[0]
                for ntr in range(ntrs):
                    ax[nr,nc].plot(vartrk[nc][0][ntr]-180, vartrk[nc][1][ntr], color = lcol, linewidth = lwdth)
                    # print(vartrk[nc][0][ntr], vartrk[nc][1][ntr])

            if nc < 2:
                # nmax = np.where((xtgt<vtrtgt[nc][0][:-1])*(vtrtgt[nc][0][1:]<=xtgt))[0][0]
                nmax = np.where((xmintrk<vtrtgt[nc][0][:-1])*(vtrtgt[nc][0][1:]<=xmintrk))[0][0]                
                ax[nr,nc].plot(vtrtgt[nc][0][:nmax]-180, vtrtgt[nc][-1][:nmax], color = 'g', linewidth = 2*lwdth)     
            # ax[nr,nc].text(lonr[0]-180+5, latr[1]-8-2, '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')
            # ax[nr,nc].text(lonr[0]-180+5, latr[1]-0.2*(latr[1]-latr[0]), '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')
            # ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')
            # ax[nr,nc].text(lonr[0]-180+0.03*(lonr[1]-lonr[0]), latr[1]-0.4*(latr[1]-latr[0]), '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom', backgroundcolor = 'w')
            # ax[nr,nc].text(lonr[0]-180+0.03*(lonr[1]-lonr[0]), latr[1]-0.2*(latr[1]-latr[0]), r'$\ \ \ \ $', ha = 'left', va = 'bottom', backgroundcolor = 'w', fontsize = 5)
            ax[nr,nc].text(lonr[0]-180+0.03*(lonr[1]-lonr[0]), latr[1]-0.3*(latr[1]-latr[0]), '     ', ha = 'left', va = 'bottom', backgroundcolor = 'w', fontsize = 6)            
            ax[nr,nc].text(lonr[0]-180+0.025*(lonr[1]-lonr[0]), latr[1]-0.35*(latr[1]-latr[0]),  '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')             
            
            nfg += 1
            for lonc in np.arange(lonr[0], lonr[1]+1, lonr[2]):
                if np.round(lonc) < 180:                    
                    txt = str(np.round(lonc))+'E'
                elif np.round(lonc) > 180:
                    txt = str(np.round(360-lonc))+'W'
                else:
                    txt = '180'                    
                # ax[nr, nc].text(lonc, latr[0], txt, ha = 'center', va = 'top')
                ax[nr,nc].text(lonc-180, latr[0]-dxax, txt, ha = 'center', va = 'top')                
            for latc in np.arange(latr[0], latr[1]+1, latr[2]):
                # ax[nr, nc].text(lonr[0], latc, str(int(latc))+'N', ha = 'right', va = 'center')
                ax[nr,nc].text(lonr[0]-180-dyax, latc, str(int(latc))+'N', ha = 'right', va = 'center')                



    dx0 = R0 * np.cos(np.deg2rad(0.5*(vtrtgt[0][4][:-1]+vtrtgt[0][4][1:]))) * np.deg2rad(np.diff(vtrtgt[0][0]))
    dy0 = R0 * np.deg2rad(np.diff(vtrtgt[0][4]))       
    ln0 = np.sqrt(dx0**2+dy0**2)                
    au0 = ln0/vtrtgt[0][3][1:]
    # aul  = interpolate.interp1d(0.5*(vtrtgt[0][0][:-1]+vtrtgt[0][0][1:]), aul0, fill_value = 'extrapolate')(0.5*(lonLI[:-1]+lonLI[1:]))
    
    dx  = R0 * np.cos(np.deg2rad(0.5*(vtrtgt[1][4][:-1]+vtrtgt[1][4][1:]))) * np.deg2rad(np.diff(vtrtgt[1][0]))
    dy  = R0 * np.deg2rad(np.diff(vtrtgt[1][4]))          
    ln  = np.sqrt(dx**2+dy**2)                
    au  = ln/vtrtgt[1][3][1:]
    
    # lath = interpolate.interp1d(vtrtgt[1][0], vtrtgt[1][4], fill_value = 'extrapolate')(lonLI)
    # auh  = interpolate.interp1d(0.5*(vtrtgt[1][0][:-1]+vtrtgt[1][0][1:]), auh0, fill_value = 'extrapolate')(0.5*(lonLI[:-1]+lonLI[1:]))        
    
        
    if np.size(vtrtgt) > 0:
        for nc in range(3):
            caxl = ax[0,nc].get_position()
            axadd = fig.add_axes([caxl.x0, 0.1, caxl.x1-caxl.x0, 0.35])
            if nc < 2:            
                axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1], 'k', linewidth = 2)
                
                i = np.argmin(np.abs(vtrtgt[nc][0]-xtgt))
                tnd = vtrtgt[nc][2][6] - vtrtgt[nc][2][1]
                axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'g', linewidth = 2)                
                # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'g', linewidth = 2, label = r'$T^\prime_{ADV}$')                                 
                tnd = vtrtgt[nc][2][7] - vtrtgt[nc][2][1]                
                axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], ':g', linewidth = 2)
                tnd = vtrtgt[nc][2][6] - vtrtgt[nc][2][7]                
                axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], '--g', linewidth = 2)                                

                if nc == 0:
                    axadd.text(xmintrk+0.01*(xmaxtrk-xmintrk), tmintrks[nc]+0.2*(tmaxtrks[nc]-tmintrks[nc]), r'$T^\prime_{ADV}$', color = 'g', fontsize = fontsize)
            
                tnd = vtrtgt[nc][2][2] - vtrtgt[nc][2][6]
                axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'r', linewidth = 2)

                # tnd = vtrtgt[nc][2][8] - vtrtgt[nc][2][9]
                # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], ':r', linewidth = 2)
                # tnd = vtrtgt[nc][2][2] - vtrtgt[nc][2][6] - (vtrtgt[nc][2][8] - vtrtgt[nc][2][9])
                # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], '--r', linewidth = 2)         

                if nc == 0:
                    axadd.text(xmintrk+0.15*(xmaxtrk-xmintrk), tmintrks[nc]+0.2*(tmaxtrks[nc]-tmintrks[nc]), r'$T_{EDD}$', color = 'r', fontsize = fontsize)
                                    
                tnd = vtrtgt[nc][2][3]                
                # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'm', linewidth = 2)
                axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'c', linewidth = 2)
                if nc == 0:
                    axadd.text(xmintrk+0.01*(xmaxtrk-xmintrk), tmintrks[nc]+0.02*(tmaxtrks[nc]-tmintrks[nc]), r'$T_{SGS}$', color = 'c', fontsize = fontsize)
                    
                tnd = vtrtgt[nc][2][4]
                axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'b', linewidth = 2)
                if nc == 0:
                    axadd.text(xmintrk+0.15*(xmaxtrk-xmintrk), tmintrks[nc]+0.02*(tmaxtrks[nc]-tmintrks[nc]), r'$T_{SFC}$', color = 'b', fontsize = fontsize)
                    
                # tnd = vtrtgt[nc][2][5]
                # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'c', linewidth = 2)                                
            else:
                vint = interpolate.interp1d(vtrtgt[0][0], vtrtgt[0][1], fill_value = 'extrapolate')(vtrtgt[1][0])
                axadd.plot(vtrtgt[1][0], vtrtgt[1][1]-vint, 'k', linewidth = 2)

                i0 = np.argmin(np.abs(vtrtgt[0][0]-xtgt))
                i  = np.argmin(np.abs(vtrtgt[1][0]-xtgt))
                dt0 = vtrtgt[1][1][i] - vtrtgt[0][1][i0]
                
                tnd0 = vtrtgt[0][2][6] - vtrtgt[0][2][1]
                tnd  = vtrtgt[1][2][6] - vtrtgt[1][2][1]                
                dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'g', linewidth = 2)

                tnd0 = vtrtgt[0][2][7] - vtrtgt[0][2][1]
                tnd  = vtrtgt[1][2][7] - vtrtgt[1][2][1]
                dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], ':g', linewidth = 2)

                tnd0 = vtrtgt[0][2][6] - vtrtgt[0][2][7]
                tnd  = vtrtgt[1][2][6] - vtrtgt[1][2][7]
                dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], '--g', linewidth = 2)

                
                tnd0 = vtrtgt[0][2][2] - vtrtgt[0][2][6]
                tnd  = vtrtgt[1][2][2] - vtrtgt[1][2][6]                
                dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'r', linewidth = 2)

                # tnd0 = vtrtgt[0][2][8] - vtrtgt[0][2][9]
                # tnd  = vtrtgt[1][2][8] - vtrtgt[1][2][9]
                # dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                # axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], ':r', linewidth = 2)

                # tnd0 = vtrtgt[0][2][2] - vtrtgt[0][2][6] - (vtrtgt[0][2][8] - vtrtgt[0][2][9])
                # tnd  = vtrtgt[1][2][2] - vtrtgt[1][2][6] - (vtrtgt[1][2][8] - vtrtgt[1][2][9])
                # dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                # axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], '--r', linewidth = 2)
                
                tnd0 = vtrtgt[0][2][3]
                tnd  = vtrtgt[1][2][3]
                dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                # axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'm', linewidth = 2)
                axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'c', linewidth = 2)                

                tnd0 = vtrtgt[0][2][4]
                tnd  = vtrtgt[1][2][4]
                dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'b', linewidth = 2)

                # tnd0 = vtrtgt[0][2][5]
                # tnd  = vtrtgt[1][2][5]
                # dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                # axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'c', linewidth = 2)


                dx0 = R0 * np.cos(np.deg2rad(0.5*(vtrtgt[0][4][:-1]+vtrtgt[0][4][1:]))) * np.deg2rad(np.diff(vtrtgt[0][0]))
                dy0 = R0 * np.deg2rad(np.diff(vtrtgt[0][4]))       
                ln0 = np.sqrt(dx0**2+dy0**2)                
                au0 = ln0/vtrtgt[0][3][1:]                
                qt0 = np.diff(vtrtgt[0][2][4])/vtrtgt[0][3][1:]

                
                dx  = R0 * np.cos(np.deg2rad(0.5*(vtrtgt[1][4][:-1]+vtrtgt[1][4][1:]))) * np.deg2rad(np.diff(vtrtgt[1][0]))
                dy  = R0 * np.deg2rad(np.diff(vtrtgt[1][4]))          
                ln  = np.sqrt(dx**2+dy**2)                
                au  = ln/vtrtgt[1][3][1:]                                
                qt  = np.diff(vtrtgt[1][2][4])/vtrtgt[1][3][1:]


                ltb = interpolate.interp1d(vtrtgt[0][0], vtrtgt[0][4], fill_value = 'extrapolate')(vtrtgt[1][0])
                dxb = R0 * np.cos(np.deg2rad(0.5*(ltb[:-1]+ltb[1:]))) * np.deg2rad(np.diff(vtrtgt[1][0]))
                dyb = R0 * np.deg2rad(np.diff(ltb))
                lnb = np.sqrt(dxb**2+dyb**2)
                aub = interpolate.interp1d(0.5*(vtrtgt[0][0][:-1]+vtrtgt[0][0][1:]), au0, fill_value = 'extrapolate')(0.5*(vtrtgt[1][0][:-1]+vtrtgt[1][0][1:]))
                qtb = interpolate.interp1d(0.5*(vtrtgt[0][0][:-1]+vtrtgt[0][0][1:]), qt0, fill_value = 'extrapolate')(0.5*(vtrtgt[1][0][:-1]+vtrtgt[1][0][1:]))
                
                dtndq = np.zeros(i+1)
                dtndu = np.zeros(i+1)
                dtndl = np.zeros(i+1)                
                for ii in range(i):
                    # dtndq[ii+1] = dtndq[ii] - (qt[i-ii-1] - qtb[i-ii-1])*lnb[i-ii-1]/aub[i-ii-1]
                    dtndq[ii+1] = dtndq[ii] - (qt[i-ii-1] - qtb[i-ii-1])*lnb[i-ii-1]/au[i-ii-1]                    
                    dtndu[ii+1] = dtndu[ii] - qtb[i-ii-1]*lnb[i-ii-1]*(1/au[i-ii-1]-1/aub[i-ii-1])
                    # dtndl[ii+1] = dtndl[ii] - qtb[i-ii-1]*(ln[i-ii-1]-lnb[i-ii-1])/aub[i-ii-1]
                    dtndl[ii+1] = dtndl[ii] - qtb[i-ii-1]*(ln[i-ii-1]-lnb[i-ii-1])/au[i-ii-1]                     

                xx = 0.5*(vtrtgt[1][0][:-1]+vtrtgt[1][0][1:])[:i+1][::-1]
                
                axadd.plot(xx, dt0+dtndq, ':b', linewidth = 2)
                axadd.plot(xx, dt0+dtndu, '--b', linewidth = 2)
                axadd.plot(xx, dt0+dtndl, 'b', linestyle = 'dashdot', linewidth = 2)                
                
                
            axadd.set_xlim(xmintrk, xmaxtrk)
            axadd.set_xticks(xticks)
            axadd.set_xticklabels(xticklabels)                        
            axadd.set_ylim(tmintrks[nc], tmaxtrks[nc])
            axadd.set_yticks(np.linspace(tmintrks[nc], tmaxtrks[nc], tinttrks[nc]))
            # axadd.text(xmintrk+dxc*(xmaxtrk-xmintrk), tmaxtrks[nc]-0.12*(tmaxtrks[nc]-tmintrks[nc]), '('+chr(ord("a")+nc+3)+')', ha = 'left', va = 'bottom')
            axadd.text(xmintrk+dxc*(xmaxtrk-xmintrk), tmaxtrks[nc]-dyc*(tmaxtrks[nc]-tmintrks[nc]), '('+chr(ord("a")+nc+3)+')', ha = 'left', va = 'bottom')            
            # axadd.text(xmintrk+dxc*(xmaxtrk-xmintrk), tmintrks[nc]+0.02*(tmaxtrks[nc]-tmintrks[nc]), '('+chr(ord("a")+nc+3)+')', ha = 'left', va = 'bottom')

            axadd.text(xmintrk-0.15*(xmaxtrk-xmintrk), tmaxtrks[nc]+0.05*(tmaxtrks[nc]-tmintrks[nc]), r'[${}^\circ$C]', ha = 'left', va = 'bottom')
            # if nc == 0:
            #     axadd.legend()
            
            
        for nc in range(3):        
            ax[nrowm,nc].remove()
            
    if ctght:
        plt.tight_layout()
    plt.savefig(pngfile)
    plt.close()        


def fig45_org(pngfile, lon, lat, varf, varfl = [], vartrk = [], lonr = [120, 240, 30], latr = [15, 45, 15], level = [''], vr=[-999,-999,21], rt = 10, lines = [0.], cmap = cmo.balance, vticklabel = [''], fsizex = 8, fsizey = 5, lcol = 'k', lwdth = 1, cntcol = 'k', dxc = 0.015, dyc = 0.15, dxax = 4., dyax = 1.2, ctght = False, fontsize = 10, unitcbr = r'[m]', unitx = 1.02, unity = -1.5, ncols = 3, vtrtgt = [], xmintrk = 140, xmaxtrk = 170, tmintrks = [16, 16, -.8], tmaxtrks = [21, 21, 3.2], tinttrks = [6, 6, 6], xtgt = 143, xticks = np.linspace(140, 170, 4), xticklabels = ['140E', '150E', '160E', '170E'], latmintrk = 34, latmaxtrk = 40, latinttrk = 4, fontsizexy = 8):

    print(pngfile)
    R0 = 6.375e6
    lonmin, lonmax, lonint = lonr
    latmin, latmax, latint = latr
    nrowm = int(np.shape(varf)[0]/ncols)
    nrowl = 2
    nrows = nrowm + nrowl    

    # ntrck0 = np.shape(vartrk[0])[0]
    # ntrck  = np.shape(vartrk[1])[0]
    
    plt.rcParams['font.size'] = fontsize
    fig = plt.figure(figsize = (fsizex, fsizey))
    # plt.subplots_adjust(left=0.05, right = 0.96, top = 0.98, bottom = 0.1)
    plt.subplots_adjust(left=0.05, right = 0.96, top = 1.05, bottom = 0.1)            
    ax = mc.set_maps(fig, nrows, ncols, xlim = [lonmin, lonmax], ylim = [latmin, latmax], lon_interval = lonint, lat_interval = latint)
    
    ax, images, vticks, vticklabels = mc.imcfs(ax, lon, lat, varf, nrows, ncols, vr = vr, rt = rt, level = level, cmap = cmap, vticklabel = vticklabel)
    if np.size(varfl) > 0:
        ax, lls = mc.imcs(ax, lon, lat, varfl, nrows, ncols, level = lines, lfontsize = 8, lwidth = 1.0, cntcol = cntcol)     

    nfg = 0    
    for nr in range(nrowm):
        caxl = ax[nr,0].get_position()
        caxr = ax[nr,-1].get_position()
        caxv = ax[nr,0].get_position()
        # for m0 in range(ncols):
        #     ax[n1+1,m0].remove()
        #     cax = fig.add_axes([caxl.x0, 0.5*(caxv.y0+caxv.y1),caxr.x1-caxl.x0,0.01])
        # cax = fig.add_axes([caxl.x0, caxv.y0-0.02*(nrows-nr)-0.018*nr,caxr.x1-caxl.x0, 0.015])
        # cax = fig.add_axes([caxl.x0, caxv.y0-0.15,caxr.x1-caxl.x0, 0.03])
        # cax = fig.add_axes([caxl.x0, caxv.y0-0.075,caxr.x1-caxl.x0, 0.02])
        cax = fig.add_axes([caxl.x0, caxv.y0-0.13,caxr.x1-caxl.x0, 0.03])                        
        cbar = plt.colorbar(images[2*nr+1], cax = cax, orientation = 'horizontal', ticks = vticks[2*nr+1])
        if unitcbr != '':
            cax.text(unitx, unity, unitcbr, transform=cax.transAxes)    
        cbars = [cbar]
        if np.size(vticklabels) != 1:
            if vticklabels[0] != ['']:
                cbar.ax.set_xticklabels(vticklabels[0])
        
        for nc in range(ncols):
            # if np.size(vartrk) > 0:
            if len(vartrk) > 0:                
                # ntrs = np.size(vartrk[nc][0])
                ntrs = np.shape(vartrk[nc][0])[0]
                for ntr in range(ntrs):
                    ax[nr,nc].plot(vartrk[nc][0][ntr]-180, vartrk[nc][1][ntr], color = lcol, linewidth = lwdth)
                    # print(vartrk[nc][0][ntr], vartrk[nc][1][ntr])

            if nc < 2:
                # nmax = np.where((xtgt<vtrtgt[nc][0][:-1])*(vtrtgt[nc][0][1:]<=xtgt))[0][0]
                nmax = np.where((xmintrk<vtrtgt[nc][0][:-1])*(vtrtgt[nc][0][1:]<=xmintrk))[0][0]                
                ax[nr,nc].plot(vtrtgt[nc][0][:nmax]-180, vtrtgt[nc][-1][:nmax], color = 'g', linewidth = 2*lwdth)     
            # ax[nr,nc].text(lonr[0]-180+5, latr[1]-8-2, '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')
            # ax[nr,nc].text(lonr[0]-180+5, latr[1]-0.2*(latr[1]-latr[0]), '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')
            # ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')
            # ax[nr,nc].text(lonr[0]-180+0.03*(lonr[1]-lonr[0]), latr[1]-0.4*(latr[1]-latr[0]), '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom', backgroundcolor = 'w')
            # ax[nr,nc].text(lonr[0]-180+0.03*(lonr[1]-lonr[0]), latr[1]-0.2*(latr[1]-latr[0]), r'$\ \ \ \ $', ha = 'left', va = 'bottom', backgroundcolor = 'w', fontsize = 5)
            ax[nr,nc].text(lonr[0]-180+0.03*(lonr[1]-lonr[0]), latr[1]-0.3*(latr[1]-latr[0]), '     ', ha = 'left', va = 'bottom', backgroundcolor = 'w', fontsize = 6)            
            ax[nr,nc].text(lonr[0]-180+0.025*(lonr[1]-lonr[0]), latr[1]-0.35*(latr[1]-latr[0]),  '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')             
            
            nfg += 1
            for lonc in np.arange(lonr[0], lonr[1]+1, lonr[2]):
                if np.round(lonc) < 180:                    
                    txt = str(np.round(lonc))+'E'
                elif np.round(lonc) > 180:
                    txt = str(np.round(360-lonc))+'W'
                else:
                    txt = '180'                    
                # ax[nr, nc].text(lonc, latr[0], txt, ha = 'center', va = 'top')
                ax[nr,nc].text(lonc-180, latr[0]-dxax, txt, ha = 'center', va = 'top', fontsize = fontsizexy) 
            for latc in np.arange(latr[0], latr[1]+1, latr[2]):
                # ax[nr, nc].text(lonr[0], latc, str(int(latc))+'N', ha = 'right', va = 'center')
                ax[nr,nc].text(lonr[0]-180-dyax, latc, str(int(latc))+'N', ha = 'right', va = 'center', fontsize = fontsizexy)                



    dx0 = R0 * np.cos(np.deg2rad(0.5*(vtrtgt[0][4][:-1]+vtrtgt[0][4][1:]))) * np.deg2rad(np.diff(vtrtgt[0][0]))
    dy0 = R0 * np.deg2rad(np.diff(vtrtgt[0][4]))       
    ln0 = np.sqrt(dx0**2+dy0**2)                
    au0 = ln0/vtrtgt[0][3][1:]
    # aul  = interpolate.interp1d(0.5*(vtrtgt[0][0][:-1]+vtrtgt[0][0][1:]), aul0, fill_value = 'extrapolate')(0.5*(lonLI[:-1]+lonLI[1:]))
    
    dx  = R0 * np.cos(np.deg2rad(0.5*(vtrtgt[1][4][:-1]+vtrtgt[1][4][1:]))) * np.deg2rad(np.diff(vtrtgt[1][0]))
    dy  = R0 * np.deg2rad(np.diff(vtrtgt[1][4]))          
    ln  = np.sqrt(dx**2+dy**2)                
    au  = ln/vtrtgt[1][3][1:]
    
    # lath = interpolate.interp1d(vtrtgt[1][0], vtrtgt[1][4], fill_value = 'extrapolate')(lonLI)
    # auh  = interpolate.interp1d(0.5*(vtrtgt[1][0][:-1]+vtrtgt[1][0][1:]), auh0, fill_value = 'extrapolate')(0.5*(lonLI[:-1]+lonLI[1:]))        
    
        
    if np.size(vtrtgt) > 0:
        for nc in range(3):
            caxl = ax[0,nc].get_position()
            axadd0 = fig.add_axes([caxl.x0, 0.4,  caxl.x1-caxl.x0, 0.25])  
            axadd  = fig.add_axes([caxl.x0, 0.05, caxl.x1-caxl.x0, 0.25])
            if nc < 2:
                axadd0.plot(vtrtgt[nc][0], vtrtgt[nc][-1], 'k', linewidth = 2)
                
                axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1], 'k', linewidth = 2)
                
                i = np.argmin(np.abs(vtrtgt[nc][0]-xtgt))
                tnd = vtrtgt[nc][2][6] - vtrtgt[nc][2][1]
                axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'g', linewidth = 2)                
                # # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'g', linewidth = 2, label = r'$T^\prime_{ADV}$')                                 
                # tnd = vtrtgt[nc][2][7] - vtrtgt[nc][2][1]                
                # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], ':g', linewidth = 2)
                # tnd = vtrtgt[nc][2][6] - vtrtgt[nc][2][7]                
                # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], '--g', linewidth = 2)                                

                if nc == 0:
                    axadd.text(xmintrk+0.01*(xmaxtrk-xmintrk), tmintrks[nc]+0.2*(tmaxtrks[nc]-tmintrks[nc]), r'$T^\prime_{ADV}$', color = 'g', fontsize = fontsize)
            
                tnd = vtrtgt[nc][2][2] - vtrtgt[nc][2][6]
                axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'r', linewidth = 2)

                # tnd = vtrtgt[nc][2][8] - vtrtgt[nc][2][9]
                # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], ':r', linewidth = 2)
                # tnd = vtrtgt[nc][2][2] - vtrtgt[nc][2][6] - (vtrtgt[nc][2][8] - vtrtgt[nc][2][9])
                # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], '--r', linewidth = 2)         

                if nc == 0:
                    axadd.text(xmintrk+0.15*(xmaxtrk-xmintrk), tmintrks[nc]+0.2*(tmaxtrks[nc]-tmintrks[nc]), r'$T_{EDD}$', color = 'r', fontsize = fontsize)
                                    
                tnd = vtrtgt[nc][2][3]                
                # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'm', linewidth = 2)
                axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'c', linewidth = 2)
                if nc == 0:
                    axadd.text(xmintrk+0.01*(xmaxtrk-xmintrk), tmintrks[nc]+0.02*(tmaxtrks[nc]-tmintrks[nc]), r'$T_{SGS}$', color = 'c', fontsize = fontsize)
                    
                tnd = vtrtgt[nc][2][4]
                axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'b', linewidth = 2)
                if nc == 0:
                    axadd.text(xmintrk+0.15*(xmaxtrk-xmintrk), tmintrks[nc]+0.02*(tmaxtrks[nc]-tmintrks[nc]), r'$T_{SFC}$', color = 'b', fontsize = fontsize)
                    
                # tnd = vtrtgt[nc][2][5]
                # axadd.plot(vtrtgt[nc][0], vtrtgt[nc][1][i]+tnd-tnd[i], 'c', linewidth = 2)                                
            else:
                vint0 = interpolate.interp1d(vtrtgt[0][0], vtrtgt[0][-1], fill_value = 'extrapolate')(vtrtgt[1][0])
                axadd0.plot(vtrtgt[1][0], vtrtgt[1][-1]-vint0, 'k', linewidth = 2)
                
                vint = interpolate.interp1d(vtrtgt[0][0], vtrtgt[0][1], fill_value = 'extrapolate')(vtrtgt[1][0])
                axadd.plot(vtrtgt[1][0], vtrtgt[1][1]-vint, 'k', linewidth = 2)

                i0 = np.argmin(np.abs(vtrtgt[0][0]-xtgt))
                i  = np.argmin(np.abs(vtrtgt[1][0]-xtgt))
                dt0 = vtrtgt[1][1][i] - vtrtgt[0][1][i0]
                
                tnd0 = vtrtgt[0][2][6] - vtrtgt[0][2][1]
                tnd  = vtrtgt[1][2][6] - vtrtgt[1][2][1]                
                dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'g', linewidth = 2)

                # tnd0 = vtrtgt[0][2][7] - vtrtgt[0][2][1]
                # tnd  = vtrtgt[1][2][7] - vtrtgt[1][2][1]
                # dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                # axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], ':g', linewidth = 2)

                # tnd0 = vtrtgt[0][2][6] - vtrtgt[0][2][7]
                # tnd  = vtrtgt[1][2][6] - vtrtgt[1][2][7]
                # dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                # axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], '--g', linewidth = 2)

                
                tnd0 = vtrtgt[0][2][2] - vtrtgt[0][2][6]
                tnd  = vtrtgt[1][2][2] - vtrtgt[1][2][6]                
                dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'r', linewidth = 2)

                # tnd0 = vtrtgt[0][2][8] - vtrtgt[0][2][9]
                # tnd  = vtrtgt[1][2][8] - vtrtgt[1][2][9]
                # dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                # axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], ':r', linewidth = 2)

                # tnd0 = vtrtgt[0][2][2] - vtrtgt[0][2][6] - (vtrtgt[0][2][8] - vtrtgt[0][2][9])
                # tnd  = vtrtgt[1][2][2] - vtrtgt[1][2][6] - (vtrtgt[1][2][8] - vtrtgt[1][2][9])
                # dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                # axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], '--r', linewidth = 2)
                
                tnd0 = vtrtgt[0][2][3]
                tnd  = vtrtgt[1][2][3]
                dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                # axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'm', linewidth = 2)
                axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'c', linewidth = 2)                

                tnd0 = vtrtgt[0][2][4]
                tnd  = vtrtgt[1][2][4]
                dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'b', linewidth = 2)

                # tnd0 = vtrtgt[0][2][5]
                # tnd  = vtrtgt[1][2][5]
                # dtnd = tnd - interpolate.interp1d(vtrtgt[0][0], tnd0, fill_value = 'extrapolate')(vtrtgt[1][0])
                # axadd.plot(vtrtgt[1][0], dt0+dtnd-dtnd[i], 'c', linewidth = 2)


                dx0 = R0 * np.cos(np.deg2rad(0.5*(vtrtgt[0][4][:-1]+vtrtgt[0][4][1:]))) * np.deg2rad(np.diff(vtrtgt[0][0]))
                dy0 = R0 * np.deg2rad(np.diff(vtrtgt[0][4]))       
                ln0 = np.sqrt(dx0**2+dy0**2)                
                au0 = ln0/vtrtgt[0][3][1:]                
                qt0 = np.diff(vtrtgt[0][2][4])/vtrtgt[0][3][1:]

                
                dx  = R0 * np.cos(np.deg2rad(0.5*(vtrtgt[1][4][:-1]+vtrtgt[1][4][1:]))) * np.deg2rad(np.diff(vtrtgt[1][0]))
                dy  = R0 * np.deg2rad(np.diff(vtrtgt[1][4]))          
                ln  = np.sqrt(dx**2+dy**2)                
                au  = ln/vtrtgt[1][3][1:]                                
                qt  = np.diff(vtrtgt[1][2][4])/vtrtgt[1][3][1:]


                ltb = interpolate.interp1d(vtrtgt[0][0], vtrtgt[0][4], fill_value = 'extrapolate')(vtrtgt[1][0])
                dxb = R0 * np.cos(np.deg2rad(0.5*(ltb[:-1]+ltb[1:]))) * np.deg2rad(np.diff(vtrtgt[1][0]))
                dyb = R0 * np.deg2rad(np.diff(ltb))
                lnb = np.sqrt(dxb**2+dyb**2)
                aub = interpolate.interp1d(0.5*(vtrtgt[0][0][:-1]+vtrtgt[0][0][1:]), au0, fill_value = 'extrapolate')(0.5*(vtrtgt[1][0][:-1]+vtrtgt[1][0][1:]))
                qtb = interpolate.interp1d(0.5*(vtrtgt[0][0][:-1]+vtrtgt[0][0][1:]), qt0, fill_value = 'extrapolate')(0.5*(vtrtgt[1][0][:-1]+vtrtgt[1][0][1:]))
                
                dtndq = np.zeros(i+1)
                dtndu = np.zeros(i+1)
                dtndl = np.zeros(i+1)                
                for ii in range(i):
                    # dtndq[ii+1] = dtndq[ii] - (qt[i-ii-1] - qtb[i-ii-1])*lnb[i-ii-1]/aub[i-ii-1]
                    dtndq[ii+1] = dtndq[ii] - (qt[i-ii-1] - qtb[i-ii-1])*lnb[i-ii-1]/au[i-ii-1]                    
                    dtndu[ii+1] = dtndu[ii] - qtb[i-ii-1]*lnb[i-ii-1]*(1/au[i-ii-1]-1/aub[i-ii-1])
                    # dtndl[ii+1] = dtndl[ii] - qtb[i-ii-1]*(ln[i-ii-1]-lnb[i-ii-1])/aub[i-ii-1]
                    dtndl[ii+1] = dtndl[ii] - qtb[i-ii-1]*(ln[i-ii-1]-lnb[i-ii-1])/au[i-ii-1]                     

                xx = 0.5*(vtrtgt[1][0][:-1]+vtrtgt[1][0][1:])[:i+1][::-1]
                
                axadd.plot(xx, dt0+dtndq, ':b', linewidth = 2)
                axadd.plot(xx, dt0+dtndu, '--b', linewidth = 2)
                axadd.plot(xx, dt0+dtndl, 'b', linestyle = 'dashdot', linewidth = 2)


                di  = np.argmin(np.abs(vtrtgt[1][0]-xmintrk)) - i
                dtndq = np.zeros(di+1)
                dtndu = np.zeros(di+1)
                dtndl = np.zeros(di+1)                
                for ii in range(di):
                    # dtndq[ii+1] = dtndq[ii] + (qt[i+ii] - qtb[i+ii])*lnb[i+ii]/aub[i+ii]
                    dtndq[ii+1] = dtndq[ii] + (qt[i+ii] - qtb[i+ii])*lnb[i+ii]/au[i+ii]                    
                    dtndu[ii+1] = dtndu[ii] + qtb[i+ii]*lnb[i+ii]*(1/au[i+ii]-1/aub[i+ii])
                    # dtndl[ii+1] = dtndl[ii] + qtb[i+ii]*(ln[i+ii]-lnb[i+ii])/aub[i+ii]
                    dtndl[ii+1] = dtndl[ii] + qtb[i+ii]*(ln[i+ii]-lnb[i+ii])/au[i+ii]                     

                xx = 0.5*(vtrtgt[1][0][:-1]+vtrtgt[1][0][1:])[i:i+di+1]
                axadd.plot(xx, dt0+dtndq, ':b', linewidth = 2)
                axadd.plot(xx, dt0+dtndu, '--b', linewidth = 2)
                axadd.plot(xx, dt0+dtndl, 'b', linestyle = 'dashdot', linewidth = 2)
                
            axadd.set_xlim(xmintrk, xmaxtrk)
            axadd.set_xticks(xticks)
            axadd.set_xticklabels(xticklabels)                        
            axadd.set_ylim(tmintrks[nc], tmaxtrks[nc])
            axadd.set_yticks(np.linspace(tmintrks[nc], tmaxtrks[nc], tinttrks[nc]))
            # axadd.text(xmintrk+dxc*(xmaxtrk-xmintrk), tmaxtrks[nc]-0.12*(tmaxtrks[nc]-tmintrks[nc]), '('+chr(ord("a")+nc+3)+')', ha = 'left', va = 'bottom')
            # axadd.text(xmintrk+dxc*(xmaxtrk-xmintrk), tmaxtrks[nc]-dyc*(tmaxtrks[nc]-tmintrks[nc]), '('+chr(ord("a")+nc+3)+')', ha = 'left', va = 'bottom')
            axadd.text(xmintrk+dxc*(xmaxtrk-xmintrk), tmaxtrks[nc]-dyc*(tmaxtrks[nc]-tmintrks[nc]), '('+chr(ord("a")+nc+6)+')', ha = 'left', va = 'bottom')                        
            # axadd.text(xmintrk+dxc*(xmaxtrk-xmintrk), tmintrks[nc]+0.02*(tmaxtrks[nc]-tmintrks[nc]), '('+chr(ord("a")+nc+3)+')', ha = 'left', va = 'bottom')
            axadd.text(xmintrk-0.15*(xmaxtrk-xmintrk), tmaxtrks[nc]+0.05*(tmaxtrks[nc]-tmintrks[nc]), r'[${}^\circ$C]', ha = 'left', va = 'bottom')

            axadd0.set_xlim(xmintrk, xmaxtrk)
            axadd0.set_xticks(xticks)
            axadd0.set_xticklabels(xticklabels)
            if nc == 2:
                ymin = -4; ymax = 2; yint = 4
            else:
                ymin = latmintrk; ymax = latmaxtrk; yint = latinttrk

            axadd0.set_ylim(ymin, ymax)
            axadd0.set_yticks(np.linspace(ymin, ymax, yint))
            if nc == 2:
                ylabel = np.linspace(ymin, ymax, yint).astype(int).astype(str).astype(object) + r'${}^\circ$'
            else:
                # ylabel = np.linspace(ymin, ymax, yint).astype(int).astype(str).astype(object) + r'${}^\circ$ N'
                ylabel = np.linspace(ymin, ymax, yint).astype(int).astype(str).astype(object) + 'N'                                
            axadd0.set_yticklabels(ylabel)
            
            axadd0.text(xmintrk+dxc*(xmaxtrk-xmintrk), ymax-dyc*(ymax-ymin), '('+chr(ord("a")+nc+3)+')', ha = 'left', va = 'bottom')            
            # axadd0.text(xmintrk-0.1*(xmaxtrk-xmintrk), ymax+0.05*(ymax-ymin), '[N]', ha = 'left', va = 'bottom')   
            # if nc == 0:
            #     axadd.legend()
            
            
        for nc in range(3):
            for nr in range(nrowl):
                ax[nrowm+nr,nc].remove()
            
    if ctght:
        plt.tight_layout()
    plt.savefig(pngfile)
    plt.close()        

    
def dh_track(pngfile, lon, lat, varf, varfl = [], vartrk = [], lonr = [120, 240, 30], latr = [20, 50, 10], level = [''], vr=[-999,-999,21], rt = 10, lines = [0.], cmap = cmo.balance, vticklabel = [''], fsizex = 8, fsizey = 2, lcol = 'k', lwdth = 1, cntcol = 'k', dxc = 0.015, dyc = 0.2, dxax = 1., dyax = 1., ctght = False, fontsize = 10, unitcbr = r'[${}^\circ$C]', unitx = 0.98, unity = -3):

    print(pngfile)
    R0 = 6.375e6
    lonmin, lonmax, lonint = lonr
    latmin, latmax, latint = latr
    nrows = int(np.shape(varf)[0]/2)
    ncols = 2
    # ntrck0 = np.shape(vartrk[0])[0]
    # ntrck  = np.shape(vartrk[1])[0]
    
    plt.rcParams['font.size'] = fontsize
    fig = plt.figure(figsize = (fsizex, fsizey))
    ax = mc.set_maps(fig, nrows, ncols, xlim = [lonmin, lonmax], ylim = [latmin, latmax], lon_interval = lonint, lat_interval = latint)
    
    ax, images, vticks, vticklabels = mc.imcfs(ax, lon, lat, varf, nrows, ncols, vr = vr, rt = rt, level = level, cmap = cmap, vticklabel = vticklabel)
    if np.size(varfl) > 0:
        ax, lls = mc.imcs(ax, lon, lat, varfl, nrows, ncols, level = lines, lfontsize = 9, lwidth = 1.0, cntcol = cntcol)     
    
    nfg = 0    
    for nr in range(nrows):
        caxl = ax[nr,0].get_position()
        caxr = ax[nr,-1].get_position()
        caxv = ax[nr,0].get_position()
        # for m0 in range(ncols):
        #     ax[n1+1,m0].remove()
        #     cax = fig.add_axes([caxl.x0, 0.5*(caxv.y0+caxv.y1),caxr.x1-caxl.x0,0.01])
        # cax = fig.add_axes([caxl.x0, caxv.y0-0.02*(nrows-nr)-0.018*nr,caxr.x1-caxl.x0, 0.015])
        cax = fig.add_axes([caxl.x0, caxv.y0-0.15,caxr.x1-caxl.x0, 0.03])        
        cbar = plt.colorbar(images[2*nr+1], cax = cax, orientation = 'horizontal', ticks = vticks[2*nr+1])
        if unitcbr != '':
            cax.text(unitx, unity, unitcbr, transform=cax.transAxes)    
        cbars = [cbar]
        if np.size(vticklabels) != 1:
            if vticklabels[0] != ['']:
                cbar.ax.set_xticklabels(vticklabels[0])
        
        for nc in range(ncols):
            # if np.size(vartrk) > 0:
            if len(vartrk) > 0:                
                # ntrs = np.size(vartrk[nc][0])
                ntrs = np.shape(vartrk[nc][0])[0]
                for ntr in range(ntrs):
                    ax[nr,nc].plot(vartrk[nc][0][ntr]-180, vartrk[nc][1][ntr], color = lcol, linewidth = lwdth)
                    # print(vartrk[nc][0][ntr], vartrk[nc][1][ntr])
            
            # ax[nr,nc].text(lonr[0]-180+5, latr[1]-8-2, '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')
            # ax[nr,nc].text(lonr[0]-180+5, latr[1]-0.2*(latr[1]-latr[0]), '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')
            ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')
            
            nfg += 1
            for lonc in np.arange(lonr[0], lonr[1]+1, lonr[2]):
                if np.round(lonc) < 180:                    
                    txt = str(np.round(lonc))+'E'
                elif np.round(lonc) > 180:
                    txt = str(np.round(360-lonc))+'W'
                else:
                    txt = '180'                    
                # ax[nr, nc].text(lonc, latr[0], txt, ha = 'center', va = 'top')
                ax[nr,nc].text(lonc-180, latr[0]-dxax, txt, ha = 'center', va = 'top')                
            for latc in np.arange(latr[0], latr[1]+1, latr[2]):
                # ax[nr, nc].text(lonr[0], latc, str(int(latc))+'N', ha = 'right', va = 'center')
                ax[nr,nc].text(lonr[0]-180-dyax, latc, str(int(latc))+'N', ha = 'right', va = 'center')                

    if ctght:
        plt.tight_layout()
    plt.savefig(pngfile)
    plt.close()        
    

def mlt_tend_maps_3rgn(pngbase, pngsuff, lon, lat, varf, nrows, ncols, rgns, varl = [], level = [''], vr=[-999,-999,21], rt = 10, cmap = cmo.balance, sngl_cbar = False, lines = [0.], lwdth = 1.0, vticklabel = [''], rnp = 3):

    nn = 0
    for rgn in rgns.keys():
        fsizey = 4 * nrows            
        if rgn == 'NP':
            fsizey = rnp * nrows
        lonmin, lonmax, lonint = rgns[rgn][0]
        latmin, latmax, latint = rgns[rgn][1]

        lonlatc = '_'+str(lonmin)+'-'+str(lonmax)+'E'+'-'+str(latmin)+'-'+str(latmax)+'N'        

        imin = np.maximum(np.argmin(np.abs(lon-0.5-lonmin)), 1); imax = np.argmin(np.abs(lon+0.5-lonmax)) + 1
        jmin = np.maximum(np.argmin(np.abs(lat-0.5-latmin)), 1); jmax = np.argmin(np.abs(lat+0.5-latmax)) + 1

        pngfile=pngbase+lonlatc+'_'+rgn+pngsuff
        print(pngfile)
        if np.size(varl) == 0:
            mc.surface_map_mc_ctp(pngfile, lon[imin-1:imax+1], lat[jmin-1:jmax+1], varf[:,jmin-1:jmax+1, imin-1:imax+1], nrows, ncols, vr=vr, rt = rt, level = level, xlim = [lonmin, lonmax], ylim = [latmin, latmax], cmap = cmap, sngl_cbar = sngl_cbar, lon_interval = lonint, lat_interval = latint, vticklabel = vticklabel, fsizey= fsizey)
        else:
            if np.size(lines[0]) > 1:
                line = lines[nn]
            else:
                line = lines
                
            mc.surface_map_mc_ctp(pngfile, lon[imin-1:imax+1], lat[jmin-1:jmax+1], varf[:,jmin-1:jmax+1, imin-1:imax+1], nrows, ncols, varl = varl[:,jmin-1:jmax+1, imin-1:imax+1],vr = vr, rt = rt, level = level, xlim = [lonmin, lonmax], ylim = [latmin, latmax], cmap = cmap, sngl_cbar = sngl_cbar, lon_interval = lonint, lat_interval = latint, linesc = True, lines = line, fsizey= fsizey, lwidth = lwdth, caxs = True)
        nn += 1
            
        
def mlt_tend_maps_ssh_track_3rgn(pngbase, pngsuff, lon, lat, varf, varfl, vartrk, nrows, ncols, rgns, level = [''], vr=[-999,-999,21], rt = 10, lines = [0.], cmap = cmo.balance, sngl_cbar = False, xmintrk = 120, xmaxtrk = 240, tmintrk = 16, tmaxtrk = 24, tinttrk = 5, cdf = False, clg = True, vticklabel = ['']):

    n = -1
    for rgn in rgns.keys():
        n += 1
        lonmin, lonmax, lonint = rgns[rgn][0]
        latmin, latmax, latint = rgns[rgn][1]

        lonlatc = '_'+str(lonmin)+'-'+str(lonmax)+'E'+'-'+str(latmin)+'-'+str(latmax)+'N'        

        imin = np.maximum(np.argmin(np.abs(lon-0.5-lonmin)), 1); imax = np.argmin(np.abs(lon+0.5-lonmax)) + 1
        jmin = np.maximum(np.argmin(np.abs(lat-0.5-latmin)), 1); jmax = np.argmin(np.abs(lat+0.5-latmax)) + 1

        pngfile=pngbase+lonlatc+'_'+rgn+pngsuff        
        plt.rcParams['font.size'] = 20
        fig = plt.figure(figsize = (11, 8))
        ax = mc.set_maps(fig, nrows, ncols, xlim = [lonmin, lonmax], ylim = [latmin, latmax], lon_interval = lonint, lat_interval = latint)
        
        
        ax, images, vticks, vticklabels = mc.imcfs(ax, lon[imin-1:imax+1], lat[jmin-1:jmax+1], varf[:,jmin-1:jmax+1,imin-1:imax+1], nrows, ncols, vr = vr, rt = rt, level = level, cmap = cmap, vticklabel = vticklabel)
        fig, ax, cbars = mc.cbs(fig, ax, images, 2, 2, vticks, vticklabels = vticklabels)   

        if np.size(np.shape(lines[0])) == 0:
            line = lines
        elif np.size(np.shape(lines[0])) == 1:
            line = lines[n]        
        
        ax[0,0], ll = mc.imc(ax[0,0], lon[imin-1:imax+1], lat[jmin-1:jmax+1], varfl[0, jmin-1:jmax+1, imin-1:imax+1], levels = line)
        ax[0,1], ll = mc.imc(ax[0,1], lon[imin-1:imax+1], lat[jmin-1:jmax+1], varfl[1, jmin-1:jmax+1, imin-1:imax+1], levels = line)
    
        data_crs = ccrs.PlateCarree()
        ax[1,0].plot(vartrk[0][0], vartrk[0][1], 'k', transform = data_crs)
        ax[1,0].plot(vartrk[1][0], vartrk[1][1], '--k', transform = data_crs)        
        
        axp = ax[1,1].get_position()
        ax[1,1].remove()
        cbars[-1].remove()
        
        # axadd = fig.add_axes([0.55, 0.1, 0.4, 0.3])
        axadd = fig.add_axes([0.55, 0.1, 0.4, 0.35])        

        dlon = 0.1
        dlonrm = 10
        # nrm = int(5/dlon)
        nrm = int(dlonrm/dlon)
        lonLI = np.min(lon) + dlon * np.arange(int((np.max(lon)-np.min(lon))/dlon)+1)
        iiminM = np.where(lonLI > np.min(vartrk[0][0]))[0][0]
        iimaxM = np.where(lonLI < np.max(vartrk[0][0]))[0][-1] + 1
        
        iiminMb = np.where(lonLI > np.min(vartrk[1][0]))[0][0]
        iimaxMb = np.where(lonLI < np.max(vartrk[1][0]))[0][-1] + 1

        if np.size(np.shape(vartrk[0][2][0])) == 0:
            nvs = 1
        else:
            nvs = np.shape(vartrk[0][2])[0]

        for nv in range(nvs):
            lbl = ''
            lblnp = ''
            lblglb = ''            
            
            mlttMM = vartrk[0][2][nv]
            mlttMMb = vartrk[1][2][nv]
            # if nv > 0:
            #     # mlttMM = mlttMM + vartrk[0][2][0][-1] - mlttMM[-1]
            #     # mlttMMb = mlttMMb + vartrk[1][2][0][-1] - mlttMMb[-1]
            #     mlttMM = mlttMM + np.mean(vartrk[0][2][0][:dlonrm] - mlttMM[:dlonrm])
            #     mlttMMb = mlttMMb + np.mean(vartrk[1][2][0][:dlonrm] - mlttMMb[:dlonrm])
                
            if nv == 0:
                if nvs == 1:
                    mlttMM = vartrk[0][2]
                    mlttMMb = vartrk[1][2]
                    if cdf:
                        lbl = 'NP-GLB'
                    else:
                        lblnp = 'NP-exp'
                        lblglb = 'GLB-exp'                        
                else:
                    if cdf:
                        lbl = 'T change'
                    else:
                        lblnp = 'T change (NP)'
                        lblglb = 'T change (GLB)'
                col = 'k'                    
            elif nv == 1:
                col = 'r'
            elif nv == 2:
                col = 'g'
            elif nv == 3:
                col = 'b'
            elif nv == 4:
                col = 'c'
            elif nv == 5:
                col = 'm'
            elif nv == 6:
                col = 'y'             
                
         
            mlttMMLI = interpolate.interp1d(vartrk[0][0], mlttMM)(lonLI[iiminM:iimaxM])
        
            mlttMMLIb = interpolate.interp1d(vartrk[1][0], mlttMMb)(lonLI[iiminMb:iimaxMb])
            if nv == 0:
                iintminM = np.maximum(np.argmin(np.abs(lonLI - xmintrk + 0.5*dlonrm)) - iiminM, 0)
                iintmaxM = np.argmin(np.abs(lonLI - xmintrk - 0.5*dlonrm)) + 1 - iiminM

                iintminMb = np.maximum(np.argmin(np.abs(lonLI - xmintrk + 0.5*dlonrm)) - iiminMb, 0)
                iintmaxMb = np.argmin(np.abs(lonLI - xmintrk - 0.5*dlonrm)) + 1 - iiminMb                
                
                mltiniMM = np.mean(mlttMMLI[iintminM:iintmaxM])
                mltiniMMb = np.mean(mlttMMLIb[iintminMb:iintmaxMb])
            else:
                mlttMMLI = mlttMMLI - np.mean(mlttMMLI[iintminM:iintmaxM]) + mltiniMM
                mlttMMLIb = mlttMMLIb - np.mean(mlttMMLIb[iintminMb:iintmaxMb]) + mltiniMMb

                
            if cdf:
                iimin = np.maximum(iiminM, iiminMb)
                iimax = np.minimum(iimaxM, iimaxMb)

                axadd.plot(lonLI[iimin:iimax], mlttMMLI[iimin-iiminM:]-mlttMMLIb[iimin-iiminMb:], col, label = lbl, linewidth = 1)
                axadd.plot(np.convolve(lonLI[iimin:iimaxM], np.ones(nrm)/nrm,mode = 'valid'),  np.convolve(mlttMMLI[iimin-iiminM:]-mlttMMLIb[iimin-iiminMb:], np.ones(nrm)/nrm,mode = 'valid'), col, linewidth = 3)   

            else:
                axadd.plot(lonLI[iiminM:iimaxM], mlttMMLI, col, label = lblnp, linewidth = 1)
                axadd.plot(lonLI[iiminMb:iimaxMb], mlttMMLIb, '--'+col, label = lblglb, linewidth = 1)
                axadd.plot(np.convolve(lonLI[iiminM:iimaxM], np.ones(nrm)/nrm,mode = 'valid'),  np.convolve(mlttMMLI, np.ones(nrm)/nrm,mode = 'valid'), col, linewidth = 3)
                axadd.plot(np.convolve(lonLI[iiminMb:iimaxMb], np.ones(nrm)/nrm,mode = 'valid'),  np.convolve(mlttMMLIb, np.ones(nrm)/nrm,mode = 'valid'), '--'+col, linewidth = 3)            
                
        axadd.set_xlim(xmintrk, xmaxtrk)
        axadd.set_ylim(tmintrk, tmaxtrk)
        axadd.set_yticks(np.linspace(tmintrk, tmaxtrk, tinttrk))        

        if clg:
            axadd.legend()
        
        plt.tight_layout()
        plt.savefig(pngfile)
        plt.close()        

def crsscts_trck(pngfile, depth, lons, varfs, nrows, ncols, vec = [], vr=[-999,-999,21], rt = 10, cmap = cm.viridis, xr = [-999, -999], yr = [-999, -999], xticks = [], yticks = [], veciint = 2, vecjint = 2, units = 'width', scale = None, scale_units = None, angles = 'uv', level = [], vticklabel = [], fsizex = 11, fsizey = 8, fontsize = 20):

    plt.rcParams['font.size'] = fontsize 
    fig = plt.figure(figsize = (fsizex, fsizey))
    ax = np.reshape(fig.subplots(nrows, ncols), (nrows, ncols))
    nm = -1
    for nr in range(nrows):
        for nc in range(ncols):
            nm += 1
            if np.size(np.shape(lons)) == 1:
                X, Y = np.meshgrid(lons, depth)
            else:
                X, Y = np.meshgrid(lons[nm], depth)                
            if np.size(cmap) == 1:
                cmptmp = cmap
            else:
                cmptmp = cmap[nm]                
            if np.size(level) == 0:
                if np.size(np.shape(vr)) == 1:
                    vr0 = vr
                else:
                    vr0 = vr[nm]                    
                image = ax[nr,nc].contourf(X, Y, varfs[nm], np.linspace(vr0[0], vr0[1], (vr0[2]-1)*rt+1), cmap = cmptmp, extend = 'both')
                cbar = plt.colorbar(image, ax = ax[nr,nc], orientation = 'horizontal', ticks = np.linspace(vr0[0],vr0[1],vr0[2]))                
            else:
                if np.size(level[0]) == 1:                    
                    image = ax[nr,nc].contourf(X, Y, varfs[nm], level, cmap = cmptmp, extend = 'both')
                    cbar = plt.colorbar(image, ax = ax[nr,nc], orientation = 'horizontal', ticks = level)                    
                    if np.size(vticklabel) != 0:
                        cbar.ax.set_xticklabels(vticklabel[nm])                    
                else:
                    image = ax[nr,nc].contourf(X, Y, varfs[nm], level[nm], cmap = cmptmp, extend = 'both')
                    cbar = plt.colorbar(image, ax = ax[nr,nc], orientation = 'horizontal', ticks = level[nm])
                    if np.size(vticklabel) != 0:
                        cbar.ax.set_xticklabels(vticklabel[nm])
                    
            ax[nr,nc].set_xlim(xr[0], xr[1])
            ax[nr,nc].set_ylim(yr[0], yr[1])
            if xticks != []:
                ax[nr,nc].set_xticks(xticks)
            if yticks != []:
                ax[nr,nc].set_yticks(yticks)                                
            
            if vec != []:
                vecmap = ax[nr,nc].quiver(X[::vecjint,::veciint], Y[::vecjint,::veciint], vec[nm][0][::vecjint,::veciint], vec[nm][1][::vecjint,::veciint], scale = scale, scale_units = scale_units, angles = angles, units = units)
            

    plt.savefig(pngfile)

def sfccs_cnt(pngfile, lon, lat, depth, var, vsfc, vvct, latcs, loncs, lonmin, lonmax, latmin, latmax, dmin = 0, dmax = 300, cmap = cmo.dense, vr = [23,27,5], rt = 10, vsr = [-1., 1., 21], viint=5, vjint=5, vkint=5, units = 'width', scale = None, scale_units = None, angles = 'uv', rto = 1.11e5, hal = 1.5, headlength= 3, headwidth=2):

    # R0 = 6.375e6
    R0 = 6.375e6 * 0.1   
    imin = np.maximum(np.argmin(np.abs(lon-0.1-lonmin)), 1); imax = np.argmin(np.abs(lon+0.1-lonmax)) + 1
    jmin = np.maximum(np.argmin(np.abs(lat-0.1-latmin)), 1); jmax = np.argmin(np.abs(lat+0.1-latmax)) + 1    
    kmin = np.maximum(np.argmin(np.abs(depth-dmin))-1, 0);   kmax = np.argmin(np.abs(depth-dmax)) + 2
    # imin = 0; imax = -1
    # jmin = 0; jmax = -1    
    # kmin = 0; kmax = -1
    
    plt.rcParams['font.size'] = 12
    nrows = int(0.5*(1+np.size(latcs)+np.size(loncs)+1))
    ncols = 2
    
    fig = plt.figure(figsize = (11, 8))    
    ax = np.reshape(fig.subplots(nrows, ncols), (nrows, ncols))
    nm = -1    
    for nr in range(nrows):
        for nc in range(ncols):
            nm += 1
            if nm == 0:                          
                X, Y = np.meshgrid(lon[imin:imax], lat[jmin:jmax])
                varf = var[0,jmin:jmax,imin:imax]
                vsf = vsfc[jmin:jmax,imin:imax]
                xmin = lonmin; xmax = lonmax
                ymin = latmin; ymax = latmax                
            elif nm < 1+np.size(latcs):
                X, Y = np.meshgrid(lon[imin:imax], depth[dmin:dmax])
                jc = np.argmin(np.abs(lat-latcs[nm-1]))
                varf = var[kmin:kmax,jc,imin:imax]
                # vvf = vvct[::2,kmin:kmax:vkint,jc,imin:imax:viint]
                # vvf = vvct[::2,kmin:kmax,jc,imin:imax]
                vvf = np.array([vvct[0],vvct[2]])[:,kmin:kmax,jc,imin:imax].copy()
                m2d = rto * np.cos(np.deg2rad(latcs[nm-1]))
                vvf[1] = m2d * vvf[1].copy()
                xmin = lonmin; xmax = lonmax
                ymin = dmax; ymax = dmin
                vhint = viint
                hmin = imin; hmax = imax; hint = viint
            else:
                X, Y = np.meshgrid(lat[jmin:jmax], depth[dmin:dmax])
                ic = np.argmin(np.abs(lon-loncs[nm-np.size(latcs)-1]))
                varf = var[kmin:kmax,jmin:jmax,ic]
                # vvf = vvct[1:,kmin:kmax:vkint,jmin:jmax:vjint,ic]
                vvf = vvct[1:,kmin:kmax,jmin:jmax,ic].copy()
                m2d = rto
                vvf[1] = m2d * vvf[1].copy()
                xmin = latmin; xmax = latmax
                ymin = dmax; ymax = dmin                
                vhint = vjint
                hmin = jmin; hmax = jmax; hint = vjint                
                
                
            image = ax[nr,nc].contourf(X, Y, varf, np.linspace(vr[0], vr[1], (vr[2]-1)*rt+1), cmap = cmap, extend = 'both')
            cbar = plt.colorbar(image, ax = ax[nr,nc], orientation = 'horizontal', ticks = np.linspace(vr[0],vr[1],vr[2]))

            if nm == 0:
                imsfc = ax[nr,nc].contour(X, Y, vsf, np.linspace(vsr[0], vsr[1], vsr[2]), colors = 'k')
                for nl in range(np.size(latcs)):
                    ax[nr,nc].plot([lonmin, lonmax], [latcs[nl], latcs[nl]], 'k')
                for nl in range(np.size(loncs)):
                    ax[nr,nc].plot([loncs[nl], loncs[nl]], [latmin, latmax], 'k')                    
            else:                
                # imvec = ax[nr,nc].quiver(X[::vkint,::vhint], Y[::vkint,::vhint], vvf[0], vvf[1], scale = scale, scale_units = scale_units, angles = angles, units = units, headaxislength = hal)
                # imvec = ax[nr,nc].quiver(X[::vkint,::vhint], Y[::vkint,::vhint], vvf[0][::vkint,::vhint], vvf[1][::vkint,::vhint], scale = scale, scale_units = scale_units, angles = angles, units = units, headaxislength = hal)                
                for k in range(kmin, kmax, vkint):
                    for h in range(hmin,hmax, hint):
                        # print(m2d, X[k,h], Y[k,h], vvf[0][k,h], vvf[1][k,h], vvf[1][k,h]/m2d)
                        ax[nr,nc].quiver(X[k,h], Y[k,h], vvf[0][k,h], vvf[1][k,h], scale = scale, scale_units = scale_units, angles = angles, units = units, headaxislength = hal, headlength= headlength, headwidth=headwidth)
                        
            
            ax[nr,nc].set_xlim(xmin,xmax)
            ax[nr,nc].set_ylim(ymin,ymax)            
                
    plt.savefig(pngfile)


def sfccs_cnt_3d(pngfile, lon, lat, depth, var, vsfc, vvct, latcs, loncs, lonmin, lonmax, latmin, latmax, dmin = 0, dmax = 300, cmap = cmo.dense, vr = [23,27,5], rt = 10, vsr = [-1., 1., 21], viint=5, vjint=5, vkint=5, units = 'width', scale = None, scale_units = None, angles = 'uv', rto = 1.11e5, arrow_length_ratio=.3, cstrm = False, nstrm = 21, vrstrm=[-0.4,0.4, 21], title = '', fontsize=20):

    # R0 = 6.375e6
    R0 = 6.375e6 
    # imin = np.maximum(np.argmin(np.abs(lon-0.1-lonmin)), 1); imax = np.argmin(np.abs(lon+0.1-lonmax)) + 1
    # jmin = np.maximum(np.argmin(np.abs(lat-0.1-latmin)), 1); jmax = np.argmin(np.abs(lat+0.1-latmax)) + 1    
    # kmin = np.maximum(np.argmin(np.abs(depth-dmin))-1, 0);   kmax = np.argmin(np.abs(depth-dmax)) + 2
    imin = np.maximum(np.argmin(np.abs(lon-lonmin))-2, 0); imax = np.minimum(np.argmin(np.abs(lon-lonmax)) + 2, np.size(lon))
    jmin = np.maximum(np.argmin(np.abs(lat-latmin))-2, 0); jmax = np.minimum(np.argmin(np.abs(lat-latmax)) + 2, np.size(lat))
    kmin = np.maximum(np.argmin(np.abs(depth-dmin))-1, 0); kmax = np.minimum(np.argmin(np.abs(depth-dmax)) + 2, np.size(depth))    
    # imin = 0; imax = -1
    # jmin = 0; jmax = -1    
    # kmin = 0; kmax = -1
    
    plt.rcParams['font.size'] = fontsize
    
    fig = plt.figure(figsize = (11, 8))    
    ax = fig.add_subplot(111, projection="3d")

    ax.set_xlim(lonmin,lonmax)
    ax.set_ylim(latmin,latmax)
    ax.set_zlim(dmax,dmin)  

    nms = 1 + np.size(latcs) + np.size(loncs)
    # nms = 1 
    for nm in range(nms):
        if nm == 0:                          
            X, Y = np.meshgrid(lon[imin:imax], lat[jmin:jmax])
            Z = var[0,jmin:jmax,imin:imax]
            Z[Z < vr[0]] = vr[0]
            Z[Z > vr[1]] = vr[1]            
            vsf = vsfc[jmin:jmax,imin:imax]
            zdir = 'z'
            offset = dmin            
        elif nm < 1+np.size(latcs):
            X, Z = np.meshgrid(lon[imin:imax], depth[kmin:kmax])
            offset = latcs[nm-1]                        
            Xv = X.copy(); Yv = offset*np.ones_like(X); Zv = Z.copy()
            jc = np.argmin(np.abs(lat-offset))
            Y = var[kmin:kmax,jc,imin:imax]
            Y[Y < vr[0]] = vr[0]
            Y[Y > vr[1]] = vr[1]                        
            if cstrm:
                vstr = vec2strm_func(vvct[0][kmin:kmax,jc,imin:imax], vvct[2][kmin:kmax,jc,imin:imax], R0 * np.deg2rad(lon[imin:imax]-lon[imin]) * np.cos(np.deg2rad(offset)), depth, dy0 = 1)
                Xs = X.copy(); Ys = vstr.copy()
                # print(np.min(vstr), np.max(vstr))
                
            vvf = vvct[:,kmin:kmax,jc,imin:imax].copy()
            m2d = rto * np.cos(np.deg2rad(latcs[nm-1]))
            vvf[2] = m2d * vvf[2].copy()
            vvf[1] = 0.
            hmin = imin; hmax = imax; hint = viint
            zdir = 'y'
        else:
            Y, Z = np.meshgrid(lat[jmin:jmax], depth[kmin:kmax])
            offset = loncs[nm-np.size(latcs)-1]            
            Xv = offset*np.ones_like(X); Yv = Y.copy(); Zv = Z.copy()
            ic = np.argmin(np.abs(lon-offset))
            X = var[kmin:kmax,jmin:jmax,ic]
            X[X < vr[0]] = vr[0]
            X[X > vr[1]] = vr[1]
            
            if cstrm:
                vstr = vec2strm_func(vvct[1][kmin:kmax,jmin:jmax,ic], vvct[2][kmin:kmax,jmin:jmax,ic], R0 * np.deg2rad(lat[imin:imax]-lat[imin]), depth, dy0 = 1)
                Xs = vstr.copy(); Ys = Y.copy()
                # print(np.min(vstr), np.max(vstr))                
                
            vvf = vvct[:,kmin:kmax,jmin:jmax,ic].copy()
            m2d = rto
            vvf[2] = m2d * vvf[2].copy()
            vvf[0] = 0.    
            vhint = vjint
            hmin = jmin; hmax = jmax; hint = vjint
            zdir = 'x'

        # print(offset, zdir)
            
        # image = ax.contourf(X, Y, varf, np.linspace(vr[0], vr[1], (vr[2]-1)*rt+1), cmap = cmap, extend = 'both', zdir = zdir, offset = offset)
        image = ax.contourf(X, Y, Z, np.linspace(vr[0], vr[1], (vr[2]-1)*rt+1), cmap = cmap, zdir = zdir, offset = offset)        
                   
        if nm == 0:
            # print(np.linspace(vsr[0], vsr[1], vsr[2]))
            vsf[vsf<vsr[0]] = vsr[0]
            vsf[vsf>vsr[1]] = vsr[1]                        
            imsfc = ax.contour(X, Y, vsf, np.linspace(vsr[0], vsr[1], vsr[2]), colors = 'k', zdir = zdir, offset = offset)
            # print(lonmin)
            # if lonmin > 145:
            #     ax.contour(X, Y, vsf, np.linspace(vsr[0], vsr[1], vsr[2]), colors = 'k', zdir = zdir, offset = offset)
            # else:
            #     hii = int(0.5 * (imax-imin))
            #     hjj = int(0.5 * (jmax-jmin))
            #     print(hii, hjj)
            #     ax.contour(X[:hjj,:hii], Y[:hjj,:hii], vsf[:hjj,:hii], np.linspace(vsr[0], vsr[1], vsr[2]), colors = 'k', zdir = zdir, offset = offset)
            #     ax.contour(X[hjj:,:hii], Y[hjj:,:hii], vsf[hjj:,:hii], np.linspace(vsr[0], vsr[1], vsr[2]), colors = 'k', zdir = zdir, offset = offset)
            #     ax.contour(X[:hjj,hii:], Y[:hjj,hii:], vsf[:hjj,hii:], np.linspace(vsr[0], vsr[1], vsr[2]), colors = 'k', zdir = zdir, offset = offset)
            #     ax.contour(X[hjj:,hii:], Y[hjj:,hii:], vsf[hjj:,hii:], np.linspace(vsr[0], vsr[1], vsr[2]), colors = 'k', zdir = zdir, offset = offset)                

                
            # imsfc = ax.contour(X, Y, vsf, vsr[2], vmin=vsr[0], vmax = vsr[1], colors = 'k', zdir = zdir, offset = offset)            
            # for nl in range(np.size(latcs)):
            #     ax.plot([lonmin, lonmax], [latcs[nl]+0.1, latcs[nl]+0.1], [0,0], 'k')
            # for nl in range(np.size(loncs)):
            #     ax.plot([loncs[nl], loncs[nl]], [latmin, latmax], [0,0], 'k')                    
        else:
            if cstrm:                
                # imsfc = ax.contour(Xs, Ys, Z, np.linspace(vsr[0], vsr[1], vsr[2]), colors = 'k', zdir = zdir, offset = offset)
                imsfc = ax.contour(Xs, Ys, Z, vrstrm[2], vmin=vrstrm[0], vmax = vrstrm[1], colors = 'k', zdir = zdir, offset = offset)                

            else:                
                # imvec = ax[nr,nc].quiver(X[::vkint,::vhint], Y[::vkint,::vhint], vvf[0], vvf[1], scale = scale, scale_units = scale_units, angles = angles, units = units, headaxislength = hal)
                # imvec = ax[nr,nc].quiver(X[::vkint,::vhint], Y[::vkint,::vhint], vvf[0][::vkint,::vhint], vvf[1][::vkint,::vhint], scale = scale, scale_units = scale_units, angles = angles, units = units, headaxislength = hal)
                
                for k in range(kmin, kmax, vkint):
                    for h in range(hmin,hmax, hint):
                        # print(m2d, X[k,h], Y[k,h], vvf[0][k,h], vvf[1][k,h], vvf[1][k,h]/m2d)
                        # ax.quiver(Xv[k,h], Yv[k,h], Zv[k,h], vvf[0][k,h], vvf[1][k,h], vvf[2][k,h], scale = scale, scale_units = scale_units, angles = angles, units = units, headaxislength = hal, headlength= headlength, headwidth=headwidth)
                        # print(Xv[k,h])
                        # print(Yv[k,h])
                        # print(Zv[k,h])
                        # # print(vvf[:,k,h])
                        # print(vvf[0][k,h])
                        # print(vvf[1][k,h])
                        # print(vvf[2][k,h])                    
                        
                        ax.quiver(Xv[k,h], Yv[k,h], Zv[k,h], vvf[0][k,h], vvf[1][k,h], vvf[2][k,h], length = scale, colors = 'k', arrow_length_ratio=arrow_length_ratio)
                    
                    # pass
            

    cbar = plt.colorbar(image, ax = ax, orientation = 'horizontal', ticks = np.linspace(vr[0],vr[1],vr[2]))
    plt.title(title)
    plt.tight_layout()
    
    fig.savefig(pngfile)
    # plt.savefig(pngfile)    

def vec2strm_func(u, v, x, y, dx0 = -999, dy0 = -999, nt = 100):
    im, jm = np.shape(u)
    if dx0 == -999:
        x0 = 0.5 * (x[:-1]+x[1:])
        x0 = np.sort(np.r_[x,x0])
        dx0 = x0[1]-x0[0]
    else:
        x0 = np.arange(np.min(x), np.max(x), dx0)
    if dy0 == -999:
        y0 = 0.5 * (y[:-1]+y[1:])
        y0 = np.sort(np.r_[y,y0])
        dy0 = y0[1]-y0[0]
    else:
        y0 = np.arange(np.min(y), np.max(y), dy0)


    u[np.abs(u)>1.e1] = 0.
    v[np.abs(v)>1.e1] = 0.
    
    ui = interpolate.interp2d(x, y, u)(x0,y0)
    vi = interpolate.interp2d(x, y, v)(x0,y0)    

    b = 0.5*(np.diff(vi[:-1]+vi[1:], axis=1)/dx0 - np.diff(ui[:,:-1]+ui[:,1:], axis=0)/dy0)
    
    p = np.zeros_like(b)

    for it in range(nt):
        pd = p.copy()

        p[1:-1,1:-1] = (((pd[1:-1, 2:] + pd[1:-1, :-2]) * dy0**2 +
                         (pd[2:, 1:-1] + pd[:-2, 1:-1]) * dx0**2 -
                         b[1:-1, 1:-1] * dx0**2 * dy0**2) / 
                        (2 * (dx0**2 + dy0**2)))        
        p[0,:] = 0
        p[-1,:] = 0
        p[:,0] = 0
        p[:,-1] = 0

    pout = interpolate.interp2d(0.5*(x0[:-1]+x0[1:]), 0.5*(y0[:-1]+y0[1:]), p)(x,y)    

    pout = pout - np.mean(pout)

    return pout


def rm1d(var0, dx0, dx):

    nn = int(dx/dx0)
    var = np.convolve(var0, np.ones(nn)/nn, mode = 'valid')
    
    return var
