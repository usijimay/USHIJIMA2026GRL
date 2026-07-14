import os
import numpy as np
import netCDF4
import sys
import calendar
import locale
import matplotlib.pyplot as plt
import cmocean.cm as cmo
import matplotlib.cm as cm
from scipy import interpolate
from scipy.interpolate import griddata
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
import matplotlib.path as mpath
from mpl_toolkits.mplot3d import Axes3D
BASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)
import map.map_cartopy as mc


def fig1(pngfile, lon, lat, varf, varfl = [], lonr = [120, 210, 30], latr = [20, 50, 10], level = [''], vr=[-999,-999,21], rt = 10, lines = [0.], cmap = cmo.balance, vticklabel = [''], fsizex = 8, fsizey = 3.2, lwdth = 1, cntcol = 'k', dxc = 0.04, dyc = 0.08, dxax = 3., dyax = 1.2, ctght = False, fontsize = 10, unitcbr = r'[${}^\circ$C]', unitx = 1.02, unity = -3, bgc = 'w', sngl_cbar = True, dycb = 0.08, cbt = 0.025, top = 0.96, btm = 0.18, fontsizexy = 8, flabel = [], flabelc = 'k', bbox = [], tlabel = [], dyt = 0.02, clonlatedge = True, cfig2 = False, ncols = 3, dxcb = 0., cbrf4 = False, cbrf5 = False, left = 0.05, right = 0.96, dpi = None, textzo = 30, hspace = None, wspace = None): 

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


def figS1(pngfile, models, lon, lat, varf, varfl, ktgt, lonr = [90, 270, 60], latr = [-20, 80, 20], level = [''], vr=[-999,-999,21], rt = 10, lines = [0.], cmap = cmo.balance, vticklabel = [''], fsizex = 8, fsizey = 10.5, lwdth = 1, cntcol = 'k', dxc = 0.04, dyc = 0.08, dxax = 3., dyax = 1.2, ctght = False, fontsize = 10, unitcbr = r'[${\rm m \ s^{-1}}$]', unitx = 1.02, unity = -1.8, bgc = 'w', sngl_cbar = True, dycb = 0.04, cbt = 0.012, top = 0.98, btm = 0.07, fontsizexy = 8, flabel = [], flabelc = 'k', bbox = [], tlabel = [], dyt = 0.02, clonlatedge = True, cfig2 = False, ncols = 4, dxcb = 0., cbrf5 = False, left = 0.05, right = 0.96, dpi = None):

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

            ax0, ll0 = mc.imc(ax[n][m], lon[models[nm-1]], lat[models[nm-1]], varfl[models[nm-1]][ktgt], levels=lines, lfontsize = fontsizexy)            
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
        

def figS2(pngfile, models, lon, lat, varf, varfl, lonr = [0, 359.9, 120], latr = [-90, 90, 30], level = [''], vr=[-999,-999,21], rt = 10, lines = [0.], cmap = cmo.balance, vticklabel = [''], fsizex = 8, fsizey = 10, lwdth = 1, cntcol = 'k', dxc = 0.04, dyc = 0.08, dxax = 3., dyax = 1.2, ctght = False, fontsize = 10, unitcbr = r'[${}^\circ$C]', unitx = 1.03, unity = -2.0, bgc = 'w', sngl_cbar = True, dycb = 0.04, cbt = 0.012, top = 0.96, btm = 0.08, fontsizexy = 8, flabel = [], flabelc = 'k', bbox = [], tlabel = [], dyt = 0.02, clonlatedge = True, cfig2 = False, ncols = 4, dxcb = 0., cbrf5 = False, left = 0.05, right = 0.96, dpi = None): 


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
    
