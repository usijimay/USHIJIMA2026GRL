import os
import numpy as np
import netCDF4
import sys
import calendar
import locale
import matplotlib.pyplot as plt
import cmocean.cm as cmo
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)
import map.map_cartopy as mc
import matplotlib.cm as cm
from scipy import interpolate
from scipy.interpolate import griddata
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
import matplotlib.path as mpath
from mpl_toolkits.mplot3d import Axes3D

def fig1(pngfile, lon, lat, varf, varfl = [], lonr = [120, 210, 30], latr = [20, 50, 10], level = [''], vr=[-999,-999,21], rt = 10, lines = [0.], cmap = cmo.balance, vticklabel = [''], fsizex = 8, fsizey = 3.2, lwdth = 1, cntcol = 'k', dxc = 0.04, dyc = 0.08, dxax = 3., dyax = 1.2, ctght = False, fontsize = 10, unitcbr = r'[${}^\circ$C]', unitx = 1.02, unity = -3, bgc = 'w', sngl_cbar = True, dycb = 0.08, cbt = 0.025, top = 0.96, btm = 0.18, fontsizexy = 10, flabel = [], flabelc = 'k', bbox = [], tlabel = [], dyt = 0.02, clonlatedge = True, cfig2 = False, ncols = 3, dxcb = 0., cbrf4 = False, cbrf5 = False, left = 0.05, right = 0.96, dpi = None, textzo = 30, hspace = None, wspace = None): 

    print(pngfile)
    R0 = 6.375e6
    lonmin, lonmax, lonint = lonr
    latmin, latmax, latint = latr

    nrows = int(np.shape(varf)[0]/ncols)
    
    plt.rcParams['font.size'] = fontsize
    
    fig = plt.figure(figsize = (fsizex, fsizey))
    plt.subplots_adjust(left=left, right = right, top = top, bottom = btm, hspace = hspace, wspace = wspace)                
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
                cax.text(unitx, unity, unitcbr[nr], transform=cax.transAxes, ha = 'right')
            cbars = [cbar]
            if np.size(vticklabels) != 1:
                if np.size(vticklabels[0]) > 1:                        
                    cbar.ax.set_xticklabels(vticklabels[ncols*nr])
                        
        elif cbrf5:
            if nr == nrows-1:
                for nc in range(ncols):
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
                    ax[nr,nc].text(lonc-180, latr[0]-dxax, txt, ha = 'center', va = 'top', fontsize = fontsizexy)         
                for latc in np.arange(latr[0], latr[1]+1, latr[2]):
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

    nrows = int((np.shape(models)[0]-1)/ncols)+1
    
    plt.rcParams['font.size'] = fontsize
    
    fig = plt.figure(figsize = (fsizex, fsizey))
    plt.subplots_adjust(left=left, right = right, top = top, bottom = btm)    

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
                    ax[nr,nc].text(lonc-180, latr[0]-dxax, txt, ha = 'center', va = 'top', fontsize = fontsizexy)         
                for latc in np.arange(latr[0], latr[1]+1, latr[2]):
                    ax[nr,nc].text(lonr[0]-180-dyax, latc, str(int(latc))+'N', ha = 'right', va = 'center', fontsize = fontsizexy)                
                    
    if ctght:
        plt.tight_layout()
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

    nrows = int((np.shape(models)[0]-1)/ncols)+1
    
    plt.rcParams['font.size'] = fontsize
    
    fig = plt.figure(figsize = (fsizex, fsizey))
    plt.subplots_adjust(left=left, right = right, top = top, bottom = btm)    
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
                    ax[nr,nc].text(lonc-180, latr[0]-dxax, txt, ha = 'center', va = 'top', fontsize = fontsizexy)         
                for latc in np.arange(latr[0], latr[1]+1, latr[2]):
                    ax[nr,nc].text(lonr[0]-180-dyax, latc, str(int(latc))+'N', ha = 'right', va = 'center', fontsize = fontsizexy)                
                    
    if ctght:
        plt.tight_layout()
    if dpi is None:
        plt.savefig(pngfile)
    else:
        plt.savefig(pngfile, dpi = dpi)                
    plt.close()        
    

    
def fig4(pngfile, lon, lat, varf, varfl = [], vartrk = [], lonr = [120, 240, 30], latr = [15, 45, 15], level = [''], vr=[-999,-999,21], rt = 10, lines = [0.], cmap = cmo.balance, vticklabel = [''], fsizex = 8, fsizey = 5, lcol = 'k', lwdth = 1, cntcol = 'k', dxc = 0.015, dyc = 0.15, dycb = 0.08, cbt = 0.03, dxax = 4., dyax = 1.2, ctght = False, fontsize = 10, unitcbr = r'[m]', unitx = 1.02, unity = -1.5, ncols = 2, vtrtgt = [], xmintrk = 140, xmaxtrk = 170, tmintrks = [16, 16, -.8], tmaxtrks = [21, 21, 3.2], tinttrks = [6, 6, 6], xtgt = 143, xticks = np.linspace(140, 170, 4), xticklabels = ['140E', '150E', '160E', '170E'], latmintrk = 34, latmaxtrk = 40, latinttrk = 4, fontsizexy = 8, flabel = [], clonlatedge = True):

    
    print(pngfile)
    R0 = 6.375e6
    lonmin, lonmax, lonint = lonr
    latmin, latmax, latint = latr
    nrowm = int(np.shape(varf)[0]/ncols)
    nrows = nrowm
    
    plt.rcParams['font.size'] = fontsize
    fig = plt.figure(figsize = (fsizex, fsizey))
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
        
    nfg = 0    
    for nr in range(nrowm):        
        for nc in range(ncols):
            if len(vartrk) > 0:                
                ntrs = np.shape(vartrk[nfg][0])[0]
                for ntr in range(ntrs):
                    ax[nr,nc].plot(vartrk[nfg][0][ntr]-180, vartrk[nfg][1][ntr], color = lcol, linewidth = lwdth)

                nmax = np.where((xmintrk<vtrtgt[nfg][0][:-1])*(vtrtgt[nfg][0][1:]<=xmintrk))[0][0]                
                ax[nr,nc].plot(vtrtgt[nfg][0][:nmax]-180, vtrtgt[nfg][-1][:nmax], color = 'g', linewidth = 2)

            label = '('+chr(ord("a")+nfg)+')'
            if np.size(flabel) > 0:
                label = label + ' ' + flabel[nfg]
            
            ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]),  label, ha = 'left', va = 'bottom')             
            
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
                        ax[nr,nc].text(lonc-180, latr[0]-dxax, txt, ha = 'center', va = 'top', fontsize = fontsizexy)
                if nc == 0:                        
                    for latc in np.arange(latr[0], latr[1]+1, latr[2]):
                        ax[nr,nc].text(lonr[0]-180-dyax, latc, str(int(latc))+'N', ha = 'right', va = 'center', fontsize = fontsizexy)                
            else:
                for lonc in np.arange(lonr[0], lonr[1]+1, lonr[2]):
                    if np.round(lonc) < 180:                    
                        txt = str(np.round(lonc))+'E'
                    elif np.round(lonc) > 180:
                        txt = str(np.round(360-lonc))+'W'
                    else:
                        txt = '180'                    
                    ax[nr,nc].text(lonc-180, latr[0]-dxax, txt, ha = 'center', va = 'top', fontsize = fontsizexy)         
                for latc in np.arange(latr[0], latr[1]+1, latr[2]):
                    ax[nr,nc].text(lonr[0]-180-dyax, latc, str(int(latc))+'N', ha = 'right', va = 'center', fontsize = fontsizexy)                
                
            
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
        cax = fig.add_axes([caxl.x0, caxv.y0-0.15,caxr.x1-caxl.x0, 0.03])        
        cbar = plt.colorbar(images[2*nr+1], cax = cax, orientation = 'horizontal', ticks = vticks[2*nr+1])
        if unitcbr != '':
            cax.text(unitx, unity, unitcbr, transform=cax.transAxes)    
        cbars = [cbar]
        if np.size(vticklabels) != 1:
            if vticklabels[0] != ['']:
                cbar.ax.set_xticklabels(vticklabels[0])
        
        for nc in range(ncols):
            if len(vartrk) > 0:                
                ntrs = np.shape(vartrk[nc][0])[0]
                for ntr in range(ntrs):
                    ax[nr,nc].plot(vartrk[nc][0][ntr]-180, vartrk[nc][1][ntr], color = lcol, linewidth = lwdth)
            
            ax[nr,nc].text(lonr[0]-180+dxc*(lonr[1]-lonr[0]), latr[1]-dyc*(latr[1]-latr[0]), '('+chr(ord("a")+nfg)+')', ha = 'left', va = 'bottom')
            
            nfg += 1
            for lonc in np.arange(lonr[0], lonr[1]+1, lonr[2]):
                if np.round(lonc) < 180:                    
                    txt = str(np.round(lonc))+'E'
                elif np.round(lonc) > 180:
                    txt = str(np.round(360-lonc))+'W'
                else:
                    txt = '180'                    
                ax[nr,nc].text(lonc-180, latr[0]-dxax, txt, ha = 'center', va = 'top')                
            for latc in np.arange(latr[0], latr[1]+1, latr[2]):
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
        
        axadd = fig.add_axes([0.55, 0.1, 0.4, 0.35])        

        dlon = 0.1
        dlonrm = 10
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

    R0 = 6.375e6 * 0.1   
    imin = np.maximum(np.argmin(np.abs(lon-0.1-lonmin)), 1); imax = np.argmin(np.abs(lon+0.1-lonmax)) + 1
    jmin = np.maximum(np.argmin(np.abs(lat-0.1-latmin)), 1); jmax = np.argmin(np.abs(lat+0.1-latmax)) + 1    
    kmin = np.maximum(np.argmin(np.abs(depth-dmin))-1, 0);   kmax = np.argmin(np.abs(depth-dmax)) + 2
    
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
                for k in range(kmin, kmax, vkint):
                    for h in range(hmin,hmax, hint):
                        ax[nr,nc].quiver(X[k,h], Y[k,h], vvf[0][k,h], vvf[1][k,h], scale = scale, scale_units = scale_units, angles = angles, units = units, headaxislength = hal, headlength= headlength, headwidth=headwidth)
                        
            
            ax[nr,nc].set_xlim(xmin,xmax)
            ax[nr,nc].set_ylim(ymin,ymax)            
                
    plt.savefig(pngfile)


def sfccs_cnt_3d(pngfile, lon, lat, depth, var, vsfc, vvct, latcs, loncs, lonmin, lonmax, latmin, latmax, dmin = 0, dmax = 300, cmap = cmo.dense, vr = [23,27,5], rt = 10, vsr = [-1., 1., 21], viint=5, vjint=5, vkint=5, units = 'width', scale = None, scale_units = None, angles = 'uv', rto = 1.11e5, arrow_length_ratio=.3, cstrm = False, nstrm = 21, vrstrm=[-0.4,0.4, 21], title = '', fontsize=20):

    R0 = 6.375e6 
    imin = np.maximum(np.argmin(np.abs(lon-lonmin))-2, 0); imax = np.minimum(np.argmin(np.abs(lon-lonmax)) + 2, np.size(lon))
    jmin = np.maximum(np.argmin(np.abs(lat-latmin))-2, 0); jmax = np.minimum(np.argmin(np.abs(lat-latmax)) + 2, np.size(lat))
    kmin = np.maximum(np.argmin(np.abs(depth-dmin))-1, 0); kmax = np.minimum(np.argmin(np.abs(depth-dmax)) + 2, np.size(depth))    
    
    plt.rcParams['font.size'] = fontsize
    
    fig = plt.figure(figsize = (11, 8))    
    ax = fig.add_subplot(111, projection="3d")

    ax.set_xlim(lonmin,lonmax)
    ax.set_ylim(latmin,latmax)
    ax.set_zlim(dmax,dmin)  

    nms = 1 + np.size(latcs) + np.size(loncs)
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
                
            vvf = vvct[:,kmin:kmax,jmin:jmax,ic].copy()
            m2d = rto
            vvf[2] = m2d * vvf[2].copy()
            vvf[0] = 0.    
            vhint = vjint
            hmin = jmin; hmax = jmax; hint = vjint
            zdir = 'x'

        image = ax.contourf(X, Y, Z, np.linspace(vr[0], vr[1], (vr[2]-1)*rt+1), cmap = cmap, zdir = zdir, offset = offset)        
                   
        if nm == 0:
            vsf[vsf<vsr[0]] = vsr[0]
            vsf[vsf>vsr[1]] = vsr[1]                        
            imsfc = ax.contour(X, Y, vsf, np.linspace(vsr[0], vsr[1], vsr[2]), colors = 'k', zdir = zdir, offset = offset)

        else:
            if cstrm:                
                imsfc = ax.contour(Xs, Ys, Z, vrstrm[2], vmin=vrstrm[0], vmax = vrstrm[1], colors = 'k', zdir = zdir, offset = offset)                

            else:                
                for k in range(kmin, kmax, vkint):
                    for h in range(hmin,hmax, hint):
                        ax.quiver(Xv[k,h], Yv[k,h], Zv[k,h], vvf[0][k,h], vvf[1][k,h], vvf[2][k,h], length = scale, colors = 'k', arrow_length_ratio=arrow_length_ratio)
                    
    cbar = plt.colorbar(image, ax = ax, orientation = 'horizontal', ticks = np.linspace(vr[0],vr[1],vr[2]))
    plt.title(title)
    plt.tight_layout()
    
    fig.savefig(pngfile)

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
