import sys
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.ticker as mticker
import matplotlib.path as mpath
import cmocean.cm as cmo


def surface_map_sngle_ctp(output_file, lon, lat, var, varl = [], level = [0], vticklabel = [''], vr=[-999,-999,21], rt = 10, xlim = [0., 359.9], ylim = [-90., 90.], extend = 'both', cmap = 'jet', fsizex=6, fsizey= 4, clon = 180., clat = 90., lon_interval = 60, lat_interval = 30, fontsize = 20, projection_type='PlateCarree', ERR = -9.99e33, suptitle='', lw_ax = 1., label = '', cland = 'w', linesc = False, lines = [0.,], lwidth = 1.0, lfmt = '%1.1f', lfontsize = 11, lw_cst = 0.5):

    
    plt.rcParams['font.size'] = fontsize    
    fig = plt.figure(figsize = (fsizex, fsizey))
    ax = set_map_sngl(fig, xlim = xlim, ylim = ylim, clon = clon, clat = clat, lon_interval = lon_interval, lat_interval = lat_interval, projection_type=projection_type, lw_ax = lw_ax, label = label, cland = cland, lw_cst = lw_cst)

    vmin, vmax, vint = vrange_func(var, vr)    
    # ax, image, vtick, vticklabel = imcf(ax, lon, lat, var, level = level, vticklabel = vticklabel, vr=[vmin,vmax,vint], rt = rt, extend = extend, cmap = cmap, ERR = ERR)

    if np.size(np.shape(lon)) > 1:
        if (np.shape(var)[0] == np.shape(lat)[0]-1)*(np.shape(var)[1] == np.shape(lat)[1]-1):
            ax, image, vtick, vticklabel = imcf_pc(ax, lon, lat, var, level = level, vticklabel = vticklabel, vr=[vmin,vmax,vint], rt = rt, extend = extend, cmap = cmap, ERR = ERR)                
        else:                  
            ax, image, vtick, vticklabel = imcf(ax, lon, lat, var, level = level, vticklabel = vticklabel, vr=[vmin,vmax,vint], rt = rt, extend = extend, cmap = cmap, ERR = ERR)                                              
    else:
        ax, image, vtick, vticklabel = imcf(ax, lon, lat, var, level = level, vticklabel = vticklabel, vr=[vmin,vmax,vint], rt = rt, extend = extend, cmap = cmap, ERR = ERR)                                              

    cbar = cb_sngl(image, vtick, vticklabel = vticklabel)
    
    if linesc:
        if np.size(varl) == 0:
            ax, ll = imc(ax, lon, lat, var, levels = lines, lfmt = lfmt, lfontsize = lfontsize, lwidth = lwidth)            
        else:
            ax, ll = imc(ax, lon, lat, varl, levels = lines, lfmt = lfmt, lfontsize = lfontsize, lwidth = lwidth)


        
    plt.suptitle(suptitle)
    plt.tight_layout()
    
    if(output_file == ''):
        plt.show()
    else:
        plt.savefig(output_file)

    plt.close()

    
def surface_map_mc_ctp(output_file, lon, lat, var, nrows, ncols, varl = [], level = [0], vticklabel = [''], vr=[-999,-999,21],  rt = 10, xlim = [0, 359.9], ylim = [-90, 90], extend = 'both', cmap = 'jet', fsizex=11, fsizey= 8, clon = 180., clat = 90., lon_interval = 60, lat_interval = 30, fontsize = 20, projection_type='PlateCarree', ERR = -9.99e33, sngl_cbar = False, labels = [''], suptitle='', lw_ax = 1., cland = 'w', linesc = False, lines = [0.,], lfmt = '%1.1f', lfontsize = 11, lwidth = 1.0, skp=True, hratio = 4, ctl = False, cusrpos = False, lonv = [], latv = [], varx = [], vary = [], angles = 'uv', scale = None, scale_units = None, units = 'width', headwidth = 3, headlength = 5, headaxislength = 4.5, vcol = 'k', iint = 1, jint = 1, dx0 = 0, dx1 = 0, dy0 = 0, dy1 = 0.01, lblif = [], tbgc = '', cntcol = 'k', caxs = False, dxax = 1, dyax = 1, unitcbr = '', unitx = 0.98, unity = -3, lw_cst = 0.5):

    
    plt.rcParams['font.size'] = fontsize
    fig = plt.figure(figsize = (fsizex, fsizey))
    ax = set_maps(fig, nrows, ncols, xlim = xlim, ylim = ylim, clon = clon, clat = clat, lon_interval = lon_interval, lat_interval = lat_interval, projection_type = projection_type, sngl_cbar = sngl_cbar, labels = labels, suptitle=suptitle, lw_ax = lw_ax, cland = cland, hratio = hratio, ctl = ctl, cusrpos = cusrpos, lblif = lblif, tbgc = tbgc, caxs = caxs, dxax = dxax, dyax = dyax, lw_cst = lw_cst)    

    # if np.size(vr) == 3:
    #     vmin, vmax, vint = vrange_func(var, vr)    
    ax, images, vticks, vticklabels = imcfs(ax, lon, lat, var, nrows, ncols, level = level, vticklabel = vticklabel, vr=vr, rt = rt, extend = extend, cmap = cmap, ERR = ERR, cusrpos = cusrpos)

    fig, ax, cbars = cbs(fig, ax, images, nrows, ncols, vticks, vticklabels = vticklabels, cusrpos = cusrpos, sngl_cbar = sngl_cbar, dx0 = dx0, dx1 = dx1, dy0 = dy0, dy1 = dy1, unitcbr = unitcbr, unitx = unitx, unity = unity)   

    if linesc:
        if np.size(varl) == 0:
            ax, lls = imcs(ax, lon, lat, var, nrows, ncols, level = lines, lfmt = lfmt, lfontsize = lfontsize, cusrpos = cusrpos, lwidth = lwidth, cntcol = cntcol)
        else:
            ax, lls = imcs(ax, lon, lat, varl, nrows, ncols, level = lines, lfmt = lfmt, lfontsize = lfontsize, cusrpos = cusrpos, lwidth = lwidth, cntcol = cntcol)

    if (np.size(varx) != 0)*(np.size(vary) != 0):
        if np.size(lonv) == 0:
            lonv = lon.copy()
        if np.size(latv) == 0:
            latv = lat.copy()            
        ax = vecs(ax, lonv[::iint], latv[::jint], varx[:,::jint,::iint], vary[:,::jint,::iint], nrows, ncols, angles = angles, scale = scale, scale_units = scale_units, units = units, headwidth = headwidth, headlength = headlength, headaxislength = headaxislength, vcol = vcol, cusrpos = cusrpos)
            
    plt.suptitle(suptitle)
    if ctl:
        fig.tight_layout()
    if(output_file == ''):
        plt.show()
    else:
        plt.savefig(output_file)
    
    plt.close()

    

def set_map_sngl(fig, xlim = [0., 359.9], ylim = [-90., 90.], clon = 180., clat = 90., lon_interval = 60, lat_interval = 30, projection_type='PlateCarree', lw_ax = 1., label = '', cland = 'w', lw_cst = 0.5):
    
    projection = projection_type_ctp(projection_type, clon, clat)        
    ax = fig.add_subplot(111, projection=projection)

    ax.add_feature(cfeature.LAND, color = cland)
    ax.coastlines(lw=lw_cst)
    
    ax = ax_setgrd(ax, projection_type = projection_type, xlim = xlim, ylim = ylim, lon_interval = lon_interval, lat_interval = lat_interval, lw_ax = lw_ax)
    ax.set_title(label)
    
    return ax

def set_maps(fig, nrows, ncols, xlim = [0., 359.9], ylim = [-90., 90.], clon = 180., clat = 90., lon_interval = 60, lat_interval = 30, projection_type='PlateCarree', sngl_cbar = False, labels = [''], suptitle='', lw_ax = 1., cland = 'w', hratio = 4, ctl = False, cusrpos = False, lblif = [], tbgc = '', caxs = False, dxax = 1, dyax = 1, lw_cst = 0.5):

    nnrows = nrows
    nncols = ncols    
    projection = projection_type_ctp(projection_type, clon, clat)

    gs_kw = None    
    if sngl_cbar:
        nnrows = nrows + 1
        hratio = hratio*np.ones(nnrows); hratio[nrows] = 1
        gs_kw = dict(height_ratios = hratio)  
    elif cusrpos:
        nnrows = 2*nrows         
        hratio = hratio*np.ones(nnrows); hratio[1::2] =1     
        gs_kw = dict(height_ratios = hratio)

    ax = fig.subplots(nnrows, nncols, subplot_kw = dict(projection = projection), gridspec_kw=gs_kw).reshape(nnrows, nncols)    


    if(np.size(labels) == 1):
        labels = np.tile(labels, ncols*nrows)
        
    nm = 0    
    for n in range(nrows):
        for m in range(ncols):
            nm = nm + 1            
            n1 = n
            m1 = m            
            if cusrpos:            
                n1 = 2*n
                m1 = m                    

            ax[n1,m1].add_feature(cfeature.LAND, color = cland)
            ax[n1,m1].coastlines(lw=lw_cst)
    
            ax[n1,m1] = ax_setgrd(ax[n1,m1], projection_type = projection_type, xlim = xlim, ylim = ylim, lon_interval = lon_interval, lat_interval = lat_interval, lw_ax = lw_ax)
            if labels[nm-1] != '':            
                ax[n1,m1].set_title(labels[nm-1])

            if np.size(lblif) != 0:
                if tbgc == '':
                    ax[n1,m1].text(lblif[nm-1][0], lblif[nm-1][1], lblif[nm-1][2], ha = 'left', va = 'bottom', transform = ccrs.PlateCarree())
                else:
                    ax[n1,m1].text(lblif[nm-1][0], lblif[nm-1][1], lblif[nm-1][2], ha = 'left', va = 'bottom', transform = ccrs.PlateCarree(), backgroundcolor = tbgc)

            if caxs:
                for lonc in np.arange(xlim[0], xlim[1]+1, lon_interval):
                    if np.round(lonc) < 180:                    
                        txt = str(np.round(lonc))+'E'
                    elif np.round(lonc) > 180:
                        txt = str(np.round(360-lonc))+'W'
                    else:
                        txt = '180'                    
                    ax[n1,m1].text(lonc, ylim[0]-dxax, txt, ha = 'center', va = 'top', transform = ccrs.PlateCarree())                
                for latc in np.arange(ylim[0], ylim[1]+1, lat_interval):
                    if np.round(latc) < 0:                    
                        txt = str(np.round(-lonc))+'S'
                    elif np.round(lonc) > 0:
                        txt = str(np.round(latc))+'N'
                    else:
                        txt = '0'                    
                    
                    ax[n1,m1].text(xlim[0]-dyax, latc, txt, ha = 'right', va = 'center', transform = ccrs.PlateCarree())
                
                
    return ax


def imcfs(ax, lon, lat, var, nrows, ncols, level = [0], vr=[-999,-999,21], rt = 10, extend = 'both', cmap = 'jet', ERR = -9.99e33, vticklabel = [''], cusrpos = False):    

    nm = 0
    for n in range(nrows):
        for m in range(ncols):
            nm = nm + 1
            n1 = n
            m1 = m            
            if cusrpos:            
                n1 = 2*n
                m1 = m                    

            if np.size(cmap) == 1:
                cmap0 = cmap
            else:
                cmap0 = cmap[nm-1]

            if np.size(level[0]) > 1:
                level0 = level[nm-1]
            else:
                level0 = level

            if np.size(vticklabel[0]) > 1:
                vlabel0 = vticklabel[nm-1]
            else:
                vlabel0 = vticklabel                

            if np.size(vr[0]) > 1:
                # vr0 = vr[nm-1]
                vr0 = vrange_func(var, vr[nm-1])                
            else:
                # vr0 = vr
                vr0 = vrange_func(var, vr)                                    

            if np.size(rt) > 1:
                rt0 = rt[nm-1]
            else:
                rt0 = rt
                
                
            if nm > np.shape(var)[0]:
                continue

            if np.size(np.shape(lon)) > 1:
                if (np.shape(var[nm-1])[0] == np.shape(lat)[0]-1)*(np.shape(var[nm-1])[1] == np.shape(lat)[1]-1):
                    ax0, image0, vtick0, vticklabel0 = imcf_pc(ax[n1,m1], lon, lat, var[nm-1], level = level0, vticklabel = vlabel0, vr=[vr0[0],vr0[1],vr0[2]], rt = rt0, extend = extend, cmap = cmap0, ERR = ERR)                
                else:                                                
                    ax0, image0, vtick0, vticklabel0 = imcf(ax[n1,m1], lon, lat, var[nm-1], level = level0, vticklabel = vlabel0, vr=[vr0[0],vr0[1],vr0[2]], rt = rt0, extend = extend, cmap = cmap0, ERR = ERR)
            else:
                ax0, image0, vtick0, vticklabel0 = imcf(ax[n1,m1], lon, lat, var[nm-1], level = level0, vticklabel = vlabel0, vr=[vr0[0],vr0[1],vr0[2]], rt = rt0, extend = extend, cmap = cmap0, ERR = ERR)
                
            # ax[n1,m1], image, vtick, vticklabel = imcf(ax[n1,m1], lon, lat, var[nm-1], level = level, vticklabel = vticklabel, vr=[vmin,vmax,vint], rt = rt, extend = extend, cmap = cmaptmp, ERR = ERR)
            ax[n1,m1] = ax0
            
            if nm == 1:
                images = [image0]
                vticks = [vtick0]
                vticklabels = [vticklabel0]                                
            else:
                images.append(image0)
                vticks.append(vtick0)
                vticklabels.append(vticklabel0)                
                            
    return ax, images, vticks, vticklabels

def imcs(ax, lon, lat, var, nrows, ncols, level = [0], lfmt = '%1.1f', lfontsize = 11, cusrpos = False, lwidth = 1.0, cntcol = 'k'):    
 
    nm = 0
    for n in range(nrows):
        for m in range(ncols):
            nm = nm + 1
            n1 = n
            m1 = m            
            if cusrpos:            
                n1 = 2*n
                m1 = m                    

            if np.size(level[0]) > 1:
                level0 = level[nm-1]
            else:
                level0 = level

            ax0, ll0 = imc(ax[n1,m1], lon, lat, var[nm-1], levels = level0, lfmt = lfmt, lfontsize = lfontsize, lwidth = lwidth, cntcol = cntcol)
            
            ax[n1,m1] = ax0
            
            if nm == 1:
                lls = [ll0]
            else:
                lls.append(ll0)
                            
    return ax, lls



def cbs(fig, ax, images, nrows, ncols, vticks, sngl_cbar = False, vticklabels = [''], cusrpos = False, dx0 = 0, dx1 = 0, dy0 = 0, dy1 = 0.01, unitcbr = '', unitx = 1, unity = -3):
        
    nm = 0
    for n in range(nrows):
        for m in range(ncols):
            nm = nm + 1
            n1 = n
            m1 = m            
            if cusrpos:            
                n1 = 2*n
                m1 = m                    

                    
            if sngl_cbar:
                if (n == nrows-1)*(m == ncols -1):
                    caxl = ax[n1,0].get_position()
                    caxr = ax[n1,m1].get_position()
                    caxv = ax[n1+1,0].get_position()
                    for m0 in range(ncols):
                        ax[n1+1,m0].remove()
                    cax = fig.add_axes([caxl.x0+dx0, 0.5*(caxv.y0+caxv.y1)+dy0,caxr.x1-caxl.x0+dx1,dy1])
                    
                    # cbar = plt.colorbar(images[-1], cax = cax, orientation = 'horizontal', ticks = vticks[nm-1])
                    cbar = plt.colorbar(images[0], cax = cax, orientation = 'horizontal', ticks = vticks[0])
                    if unitcbr != '':
                        cax.text(unitx, unity, unitcbr, transform=cax.transAxes)
                        
                    cbars = [cbar]
                    # print(vticklabels)
                    # print(np.size(vticklabels))
                    # print(vticklabels[0])                    
                    if np.size(vticklabels) != 1:
                        if np.size(vticklabels[0]) != 1:
                        # if vticklabels[0] != ['']:
                            cbar.ax.set_xticklabels(vticklabels[0])
                    # if np.size(vticklabels[nm-1]) != 1:
                    #     cbar.ax.set_xticklabels(vticklabels[nm-1])
            else:
                if cusrpos:                
                    caxh = ax[n1,m1].get_position()
                    caxv = ax[n1+1,m1].get_position()
                    ax[n1+1,m1].remove()
                    cax = fig.add_axes([caxh.x0+dx0, 0.5*(caxv.y0+caxv.y1)+dy0,caxh.x1-caxh.x0+dx1,dy1])
                    cbar = plt.colorbar(images[nm-1], cax = cax, orientation = 'horizontal', ticks = vticks[nm-1])                    
                else:
                    cbar = plt.colorbar(images[nm-1], ax = ax[n1,m1], orientation = 'horizontal', ticks = vticks[nm-1])

                # if np.size(vticklabels) != 1:
                #     cbar.ax.set_xticklabels(vticklabels[nm-1])
                if np.size(vticklabels[nm-1]) != 1:
                    cbar.ax.set_xticklabels(vticklabels[nm-1])
                    

                if nm == 1:
                    cbars = [cbar]
                else:
                    cbars.append(cbar)       
                                           

    return fig, ax, cbars

    
    
def ax_setgrd(ax, projection_type='PlateCarree', xlim = [0., 359.9], ylim = [-90., 90.], lon_interval = 60, lat_interval = 30, lw_ax = 1.):

    gl = ax.gridlines(crs=ccrs.PlateCarree(), linewidth = lw_ax, color = 'k')

    if (xlim[0]<1.)*(xlim[1]>359.):
        gl.xlocator = mticker.FixedLocator(np.arange(-360,360.1,lon_interval))
    else:
        xticks = np.arange(xlim[0], xlim[1], lon_interval)
        xticks[xticks>180] = xticks[xticks>180]-360.                              
        gl.xlocator = mticker.FixedLocator(xticks)
        
    # gl.ylocator = mticker.FixedLocator(np.arange(-90,90.1,lat_interval))    
    yticks = np.arange(ylim[0], ylim[1]+0.1, lat_interval)
    gl.ylocator = mticker.FixedLocator(yticks)

    ax.set_extent([xlim[0], xlim[1], ylim[0], ylim[1]], crs = ccrs.PlateCarree())
    ax = ctp_set_boundary_ax(ax, projection_type)

    return ax

def imcf(ax, lon, lat, var, level = [0], vr=[-999,-999,21], rt = 10, extend = 'both', cmap = 'jet', ERR = -9.99e33, vticklabel = ['']):

    data_crs = ccrs.PlateCarree()
    if np.size(level) == 1:
        vtick = np.linspace(vr[0],vr[1],round(vr[2])) 
        image = ax.contourf(lon, lat, var, np.linspace(vr[0], vr[1], (round(vr[2])-1)*rt+1), extend = extend, cmap = cmap, transform = data_crs)
        vticklabel = ['']
    else:
        vartmp = np.zeros_like(var)
        nls = np.size(level)
        levtmp = np.arange(nls)
        vartmp[var<level[0]] = -0.5
        for nl in range(nls-1):
            vartmp[(level[nl]<=var)*(var<level[nl+1])] = nl+0.5
        vartmp[level[-1]<var] = nls - 0.5
        if 'MaskedArray' in str(type(var)):            
            vartmp[var.mask] = np.nan

        vtick = levtmp
        if np.size(vticklabel) == 1:
            vticklabel = level
        
        image = ax.contourf(lon, lat, vartmp, levtmp, extend = extend, cmap = cmap, transform = data_crs)

    return ax, image, vtick, vticklabel

def imcf_pc(ax, lon, lat, var, level = [0], vr=[-999,-999,21], rt = 10, extend = 'both', cmap = 'jet', ERR = -9.99e33, vticklabel = ['']):

    data_crs = ccrs.PlateCarree()    
    # if np.size(level) == 1:
    #     vtick = np.linspace(vr[0],vr[1],vr[2])        
    #     # image = ax.contourf(lon, lat, var, np.linspace(vr[0], vr[1], (vr[2]-1)*rt+1), extend = extend, cmap = cmap, transform = data_crs)
    #     image = ax.pcolormesh(lon, lat, var, vmin = vr[0], vmax = vr[1], extend = extend, cmap = cmap, transform = data_crs)        
    #     vticklabel = ['']
    # else:
    #     vartmp = np.zeros_like(var)
    #     nls = np.size(level)
    #     levtmp = np.arange(nls)
    #     vartmp[var<level[0]] = -0.5
    #     for nl in range(nls-1):
    #         vartmp[(level[nl]<=var)*(var<level[nl+1])] = nl+0.5
    #     vartmp[level[-1]<var] = nls - 0.5
    #     if 'MaskedArray' in str(type(var)):            
    #         vartmp[var.mask] = np.nan

    #     vtick = levtmp
    #     if np.size(vticklabel) == 1:
    #         vticklabel = level

    #     # image = ax.contourf(lon, lat, vartmp, levtmp, extend = extend, cmap = cmap, transform = data_crs)
    #     image = ax.pcolormesh(lon, lat, vartmp, vmin = levtmp[0], vmax = levtmp[-1], cmap = cmap, transform = data_crs)        

    if np.size(level) == 1:
        vtick = np.linspace(vr[0],vr[1],vr[2])
        level = np.linspace(vr[0],vr[1],(vr[2]-1)*rt+1)
        vticklabel = ['']
        # vticklabel = vtick
    vartmp = np.zeros_like(var)
    nls = np.size(level)
    levtmp = np.arange(nls)
    vartmp[var<level[0]] = -0.5
    for nl in range(nls-1):
        vartmp[(level[nl]<=var)*(var<level[nl+1])] = nl+0.5
    vartmp[level[-1]<var] = nls - 0.5
    if 'MaskedArray' in str(type(var)):            
        vartmp[var.mask] = np.nan

    vtick = levtmp
    if np.size(vticklabel) == 1:
        vticklabel = level

    # image = ax.contourf(lon, lat, vartmp, levtmp, extend = extend, cmap = cmap, transform = data_crs)
    image = ax.pcolormesh(lon, lat, vartmp, vmin = levtmp[0], vmax = levtmp[-1], cmap = cmap, transform = data_crs)        
        

    return ax, image, vtick, vticklabel


def cb_sngl(image, vtick, vticklabel = ['']):
    cbar = plt.colorbar(image, orientation = 'horizontal', ticks = vtick)        
    if np.size(vticklabel) != 1:
        cbar.ax.set_xticklabels(vticklabel)

    return cbar
        
def imc(ax, lon, lat, var, levels = [0.,], lfmt = '%1.1f', lfontsize = 11, lwidth = 1.0, cntcol = 'k'):

    data_crs = ccrs.PlateCarree()
    ll = ax.contour(lon, lat, var, levels = levels, colors = cntcol, transform = data_crs, linewidths = lwidth)
    ll.clabel(fmt=lfmt, fontsize=lfontsize)

    return ax, ll

def vec(ax, lonv, latv, varx, vary, angles = 'uv', scale = None, scale_units = None, units = 'width', headwidth = 3, headlength = 5, headaxislength = 4.5, vcol = 'k'):
    
    if (np.size(np.shape(lonv)) == 1)*(np.size(np.shape(latv)) == 1):
        X, Y = np.meshgrid(lonv, latv)
    else:
        X, Y = lonv, latv

    data_crs = ccrs.PlateCarree()
    ax.quiver(X, Y, varx, vary, angles = angles, scale = scale, scale_units = scale_units, units = units, headwidth = headwidth, headlength = headlength, headaxislength = headaxislength, color = vcol, transform = data_crs)

    return ax


def vecs(ax, lonv, latv, varx, vary, nrows, ncols, angles = 'uv', scale = None, scale_units = None, units = 'width', headwidth = 3, headlength = 5, headaxislength = 4.5, vcol = 'k', cusrpos = False):

    nm = 0
    for n in range(nrows):
        for m in range(ncols):
            nm = nm + 1
            n1 = n
            m1 = m            
            if cusrpos:            
                n1 = 2*n
                m1 = m                    

            if np.size(vcol) == 1:
                vcol0 = vcol
            else:
                vcol0 = vcol[nm-1]
                
            if np.size(scale) == 1:
                scale0 = scale
            else:
                scale0 = scale[nm-1]

            if np.size(scale_units) == 1:
                scale_units0 = scale_units
            else:
                scale_units0 = scale_units[nm-1]

            if np.size(units) == 1:
                units0 = units
            else:
                units0 = units[nm-1]
                
            if np.size(vcol) == 1:
                vcol0 = vcol
            else:
                vcol0 = vcol[nm-1]
                
                
            if nm > np.shape(varx)[0]:
                continue

            ax0 = vec(ax[n1,m1], lonv, latv, varx[nm-1], vary[nm-1], angles = angles, scale = scale0, scale_units = scale_units0, units = units0, headwidth = headwidth, headlength = headlength, headaxislength = headaxislength, vcol = vcol0)            
            ax[n1,m1] = ax0
                            
    return ax
    
    

# def surface_map_sngle_ctp(output_file, lon, lat, var, level = [0], vticklabel = [''], vr=[-999,-999,21], rt = 10, xlim = [0., 359.9], ylim = [-90., 90.], extend = 'both', cmap = 'jet', fsizex=6, fsizey= 4, clon = 180., clat = 90., lon_interval = 60, lat_interval = 30, fontsize = 20, projection_type='PlateCarree', ERR = -9.99e33, suptitle='', lw_ax = 1., label = '', cland = 'w', linesc = False, lines = [0.,], lfmt = '%1.1f', lfontsize = 11):


#     plt.rcParams['font.size'] = fontsize
#     vmin, vmax, vint = vrange_func(var, vr)
    
#     data_crs = ccrs.PlateCarree()
#     fig = plt.figure(figsize = (fsizex, fsizey))
        
#     projection = projection_type_ctp(projection_type, clon, clat)        
#     ax = fig.add_subplot(111, projection=projection)

#     ax.add_feature(cfeature.LAND, color = cland)
#     ax.coastlines(lw=0.5)
#     gl = ax.gridlines(crs=ccrs.PlateCarree(), linewidth = lw_ax, color = 'k')

#     # gl.xlocator = mticker.FixedLocator(np.arange(0,360.1,lon_interval)) 
#     # gl.xlocator = mticker.FixedLocator(np.arange(-180,180.1,lon_interval)) 
#     # gl.xlocator = mticker.FixedLocator(np.arange(-clon,360.1-clon,lon_interval)) 
#     # gl.ylocator = mticker.FixedLocator(np.arange(-90,90.1,lat_interval))

#     gl.xlocator = mticker.FixedLocator(np.arange(-360,360.1,lon_interval)) 
#     gl.ylocator = mticker.FixedLocator(np.arange(-90,90.1,lat_interval))

#     ax.set_extent([xlim[0], xlim[1], ylim[0], ylim[1]], crs = ccrs.PlateCarree())
#     ctp_set_boundary(ax, projection_type)

#     if np.size(level) == 1:
#         image = ax.contourf(lon, lat, var, np.linspace(vmin, vmax, (vint-1)*rt+1), extend = extend, cmap = cmap, transform = data_crs)
#         plt.colorbar(image, orientation = 'horizontal', ticks = np.linspace(vmin,vmax,vint))        
#     else:
#         vartmp = np.zeros_like(var)
#         nls = np.size(level)
#         levtmp = np.arange(nls)
#         vartmp[var<level[0]] = -0.5
#         for nl in range(nls-1):
#             vartmp[(level[nl]<=var)*(var<level[nl+1])] = nl+0.5
#         vartmp[level[-1]<var] = nls - 0.5
#         if 'MaskedArray' in str(type(var)):            
#             vartmp[var.mask] = np.nan            
#         image = ax.contourf(lon, lat, vartmp, levtmp, extend = extend, cmap = cmap, transform = data_crs)
#         cbar = plt.colorbar(image, orientation = 'horizontal', ticks = levtmp)
#         if np.size(vticklabel) == 1:
#             cbar.ax.set_xticklabels(level)
#         else:
#             cbar.ax.set_xticklabels(vticklabel)                                    

        
#     # lon0 = np.arange(361.)
#     # lat0 = -90.+np.arange(181)
#     # X, Y = np.meshgrid(lon0, lat0)
#     # image = ax.pcolor(X, Y, var, np.linspace(vmin, vmax, (vint-1)*rt+1), extend = extend, cmap = cmap, transform = data_crs)



#     if(linesc):
#         ll = ax.contour(lon, lat, var, levels = lines, colors = 'k', transform = data_crs)
#         ll.clabel(fmt=lfmt, fontsize=lfontsize)
        
#     ax.set_title(label)
#     plt.suptitle(suptitle)
#     plt.tight_layout()

#     if(output_file == ''):
#         plt.show()
#     else:
#         plt.savefig(output_file)

#     plt.close()


# def surface_map_mc_ctp(output_file, lon, lat, var, nrows, ncols, level = [0], vticklabel = [''], vr=[-999,-999,21],  rt = 10, xlim = [0, 359.9], ylim = [-90, 90], extend = 'both', cmap = 'jet', fsizex=11, fsizey= 8, clon = 180., clat = 90., lon_interval = 60, lat_interval = 30, fontsize = 20, projection_type='PlateCarree', ERR = -9.99e33, sngl_cbar = False, labels = [''], suptitle='', lw_ax = 1., cland = 'w', linesc = False, lines = [0.,], lfmt = '%1.1f', lfontsize = 11, skp=True, hratio = 4, ctl = False):

#     plt.rcParams['font.size'] = fontsize
#     data_crs = ccrs.PlateCarree()
#     vmin, vmax, vint = vrange_func(var, vr)

#     if(np.size(labels) == 1):
#         labels = np.tile(labels, ncols*nrows)
        
#     projection = projection_type_ctp(projection_type, clon, clat)        

#     fig = plt.figure(figsize = (fsizex, fsizey))
#     if(sngl_cbar):
#         hratio = hratio*np.ones(nrows+1); hratio[nrows] = 1
#         gs_kw = dict(height_ratios = hratio)
#         fig, ax = plt.subplots(nrows+1, ncols, figsize = (fsizex, fsizey), subplot_kw = dict(projection = projection), gridspec_kw=gs_kw)
#     else:
#         if ctl:
#             fig, ax = plt.subplots(nrows, ncols, figsize = (fsizex, fsizey), subplot_kw = dict(projection = projection))
#         else:
#             hratio = hratio*np.ones(2*nrows); hratio[1::2] =1
#             gs_kw = dict(height_ratios = hratio)
#             fig, ax = plt.subplots(2*nrows, ncols, figsize = (fsizex, fsizey), subplot_kw = dict(projection = projection), gridspec_kw=gs_kw)


#     # if(np.shape(var) != (nrows*ncols), np.size(lat), np.size(lon)):
#     #     if(np.size(lon) != np.size(lat)):
#     #         ar_shape = np.array([nrows*ncols, np.size(lon),np.size(lat)])
#     #         k = np.argmin(np.abs(np.shape(var) - ar_shape[0]))
#     #         j = np.argmin(np.abs(np.shape(var) - ar_shape[1]))
#     #         i = np.argmin(np.abs(np.shape(var) - ar_shape[2]))

#     #         var = np.transpose(var, (k,j,i))
#     #     else:
#     #         sys.exit('transpose the array to (N, lat, lon)')

#     nm = 0
#     for n in range(nrows):
#         for m in range(ncols):
#             nm = nm + 1
            
#             if(sngl_cbar):            
#                 n1 = n
#                 m1 = m
#             else:
#                 if ctl:
#                     n1 = n
#                     m1 = m
#                 else:
#                     n1 = 2*n
#                     m1 = m

#             if skp:
#                 if nm > np.shape(var)[0]:
#                     ax[n1,m1].remove()                    
#                     if(sngl_cbar):
#                         if((n == nrows-1)*(m == ncols -1)):
#                             caxl = ax[n1+1,0].get_position()
#                             caxr = ax[n1+1,m1].get_position()
#                             for m0 in range(ncols):
#                                 ax[n1+1,m0].remove()
#                             cax = fig.add_axes([caxl.x0, 0.5*(caxl.y0+caxl.y1),caxr.x1-caxl.x0,0.01])
#                             plt.colorbar(image, cax = cax, orientation = 'horizontal', ticks = np.linspace(vmin,vmax,vint))
#                     continue

#             ax[n1,m1].add_feature(cfeature.LAND, color = cland)
#             ax[n1,m1].coastlines(lw=0.5)
#             gl = ax[n1,m1].gridlines(crs=ccrs.PlateCarree(), linewidth = lw_ax, color = 'k')
#             # gl.xlocator = mticker.FixedLocator(np.arange(0,360.1,lon_interval)) 
#             # gl.xlocator = mticker.FixedLocator(np.arange(-clon,360.1-clon,lon_interval))
#             # gl.xlocator = mticker.FixedLocator(np.arange(-clon,360.1-clon,lon_interval))
#             gl.xlocator = mticker.FixedLocator(np.arange(-360,360.1,lon_interval))     
#             gl.ylocator = mticker.FixedLocator(np.arange(-90,90.1,lat_interval))

#             ax[n1,m1].set_extent([xlim[0], xlim[1], ylim[0], ylim[1]], crs = ccrs.PlateCarree())    
#             ctp_set_boundary(ax[n1,m1], projection_type)

#             if np.size(level) == 1:
#                 image = ax[n1,m1].contourf(lon, lat, var[nm-1], np.linspace(vmin, vmax, (vint-1)*rt+1), extend = extend, cmap = cmap, transform = data_crs)
#             else:
#                 vartmp = np.zeros_like(var[nm-1])
#                 if np.size(level[0]) == 1:
#                     nls = np.size(level)
#                     levtmp = np.arange(nls)
#                     vartmp[var[nm-1]<level[0]] = -0.5
#                     for nl in range(nls-1):
#                         vartmp[(level[nl]<=var[nm-1])*(var[nm-1]<level[nl+1])] = nl+0.5
#                     vartmp[level[-1]<var[nm-1]] = nls - 0.5
#                     cmaptmp = cmap                    
#                 else:
                    
#                     nls = np.size(level[nm-1])                    
#                     levtmp = np.arange(nls)                
#                     vartmp[var[nm-1]<level[nm-1][0]] = -0.5
#                     for nl in range(nls-1):
#                         vartmp[(level[nm-1][nl]<=var[nm-1])*(var[nm-1]<level[nm-1][nl+1])] = nl+0.5
#                     vartmp[level[nm-1][-1]<var[nm-1]] = nls - 0.5
#                     if np.size(cmap) == 1:
#                         cmaptmp = cmap
#                     else:
#                         cmaptmp = cmap[nm-1]                    
                    
#                 if 'MaskedArray' in str(type(var)):            
#                     vartmp[var[nm-1].mask] = np.nan            
#                 # image = ax[n1,m1].contourf(lon, lat, vartmp, levtmp, extend = extend, cmap = cmap, transform = data_crs)
#                 image = ax[n1,m1].contourf(lon, lat, vartmp, levtmp, extend = extend, cmap = cmaptmp, transform = data_crs)                
                
                
#             ax[n1,m1].set_title(labels[nm-1])

#             if linesc:
#                 ll = ax[n1,m1].contour(lon, lat, var[nm-1], levels = lines, colors = 'k', transform = data_crs)
#                 ll.clabel(fmt=lfmt, fontsize=lfontsize)

#             if(sngl_cbar):
#                 if((n == nrows-1)*(m == ncols -1)):
#                     caxl = ax[n1,0].get_position()
#                     caxr = ax[n1,m1].get_position()
#                     caxv = ax[n1+1,0].get_position()
#                     for m0 in range(ncols):
#                         ax[n1+1,m0].remove()
#                     cax = fig.add_axes([caxl.x0, 0.5*(caxv.y0+caxv.y1),caxr.x1-caxl.x0,0.01])
#                     if np.size(level) == 1:                    
#                         plt.colorbar(image, cax = cax, orientation = 'horizontal', ticks = np.linspace(vmin,vmax,vint))
#                     else:
#                         cbar = plt.colorbar(image, cax = cax, orientation = 'horizontal', ticks = levtmp)
#                         if np.size(vticklabel) == 1:
#                             cbar.ax.set_xticklabels(level)
#                         else:
#                             cbar.ax.set_xticklabels(vticklabel)    
#             else:
#                 if ctl == False:                
#                     caxh = ax[n1,m1].get_position()
#                     caxv = ax[n1+1,m1].get_position()
#                     ax[n1+1,m1].remove()
#                     cax = fig.add_axes([caxh.x0, 0.5*(caxv.y0+caxv.y1),caxh.x1-caxh.x0,0.01])
#                 if np.size(level) == 1:
#                     if ctl:                        
#                         plt.colorbar(image, orientation = 'horizontal', ticks = np.linspace(vmin,vmax,vint))
#                     else:
#                         plt.colorbar(image, cax = cax, orientation = 'horizontal', ticks = np.linspace(vmin,vmax,vint))                    
#                 else:
#                     if np.size(level[0])==1:
#                         if ctl:                                                
#                             cbar = plt.colorbar(image, orientation = 'horizontal', ticks = levtmp)
#                         else:
#                             cbar = plt.colorbar(image, cax = cax, orientation = 'horizontal', ticks = levtmp)                            
#                         if np.size(vticklabel) == 1:
#                             cbar.ax.set_xticklabels(level)
#                         else:                
#                             cbar.ax.set_xticklabels(vticklabel)    
#                     else:
#                         if ctl:
#                             cbar = plt.colorbar(image, ax = ax[n1,m1], orientation = 'horizontal', ticks = levtmp)
#                         else:
#                             cbar = plt.colorbar(image, cax = cax, orientation = 'horizontal', ticks = levtmp)                            
#                         if np.size(vticklabel) == 1:
#                             cbar.ax.set_xticklabels(level[nm-1])
#                         else:
#                             if np.size(vticklabel[0]) == 1:                            
#                                 cbar.ax.set_xticklabels(vticklabel)
#                             else:
#                                 cbar.ax.set_xticklabels(vticklabel[nm-1])
                            
#             if (ERR < 0.):
#                 # print(nm-1)
#                 if np.any((var[nm-1] > 1.1 * ERR)*(var[nm-1] < 0.7 * ERR)):
#                     ax[n1,m1].contourf(lon,lat,var[nm-1], levels = np.linspace(ERR*1.1, ERR*0.7, 3), cmap = "Greys")
#             else:
#                 if np.any((var[nm-1] > 0.7 * ERR)*(var[nm-1] < 1.1 * ERR)):
#                     ax[n1,m1].contourf(lon,lat,var[nm-1], levels = np.linspace(ERR*0.7, ERR*1.1, 3), cmap = "Greys")
            

            
    
#     plt.suptitle(suptitle)
#     if ctl:
#         fig.tight_layout()
#     if(output_file == ''):
#         plt.show()
#     else:
#         plt.savefig(output_file)
    
#     plt.close()

def surface_map_mc_2v_ctp(output_file, lon, lat, var, varl, nrows, ncols, level = [0], vticklabel = [''], vr=[-999,-999,21],  rt = 10, xlim = [0, 359.9], ylim = [-90, 90], extend = 'both', cmap = 'jet', fsizex=11, fsizey= 8, clon = 180., clat = 90., lon_interval = 60, lat_interval = 30, fontsize = 20, projection_type='PlateCarree', ERR = -9.99e33, sngl_cbar = False, labels = [''], suptitle='', lw_ax = 1., cland = 'w', linesc = False, lines = [0.,], lfmt = '%1.1f', lfontsize = 11,skp=True, hratio = 4, ctl = False):

    plt.rcParams['font.size'] = fontsize
    data_crs = ccrs.PlateCarree()
    vmin, vmax, vint = vrange_func(var, vr)

    if(np.size(labels) == 1):
        labels = np.tile(labels, ncols*nrows)
        
    projection = projection_type_ctp(projection_type, clon, clat)        

    fig = plt.figure(figsize = (fsizex, fsizey))
    if(sngl_cbar):
        hratio = hratio*np.ones(nrows+1); hratio[nrows] = 1
        gs_kw = dict(height_ratios = hratio)
        fig, ax = plt.subplots(nrows+1, ncols, figsize = (fsizex, fsizey), subplot_kw = dict(projection = projection), gridspec_kw=gs_kw)
    else:
        if ctl:
            fig, ax = plt.subplots(nrows, ncols, figsize = (fsizex, fsizey), subplot_kw = dict(projection = projection))
        else:
            hratio = hratio*np.ones(2*nrows); hratio[1::2] =1
            gs_kw = dict(height_ratios = hratio)
            fig, ax = plt.subplots(2*nrows, ncols, figsize = (fsizex, fsizey), subplot_kw = dict(projection = projection), gridspec_kw=gs_kw)


    # if(np.shape(var) != (nrows*ncols), np.size(lat), np.size(lon)):
    #     if(np.size(lon) != np.size(lat)):
    #         ar_shape = np.array([nrows*ncols, np.size(lon),np.size(lat)])
    #         k = np.argmin(np.abs(np.shape(var) - ar_shape[0]))
    #         j = np.argmin(np.abs(np.shape(var) - ar_shape[1]))
    #         i = np.argmin(np.abs(np.shape(var) - ar_shape[2]))

    #         var = np.transpose(var, (k,j,i))
    #     else:
    #         sys.exit('transpose the array to (N, lat, lon)')

    nm = 0
    for n in range(nrows):
        for m in range(ncols):
            nm = nm + 1
            
            if(sngl_cbar):            
                n1 = n
                m1 = m
            else:
                if ctl:
                    n1 = n
                    m1 = m
                else:
                    n1 = 2*n
                    m1 = m

            if skp:
                if nm > np.shape(var)[0]:
                    ax[n1,m1].remove()                    
                    if(sngl_cbar):
                        if((n == nrows-1)*(m == ncols -1)):
                            caxl = ax[n1+1,0].get_position()
                            caxr = ax[n1+1,m1].get_position()
                            for m0 in range(ncols):
                                ax[n1+1,m0].remove()
                            cax = fig.add_axes([caxl.x0, 0.5*(caxl.y0+caxl.y1),caxr.x1-caxl.x0,0.01])
                            plt.colorbar(image, cax = cax, orientation = 'horizontal', ticks = np.linspace(vmin,vmax,vint))
                    continue

            ax[n1,m1].add_feature(cfeature.LAND, color = cland)
            ax[n1,m1].coastlines(lw=0.5)
            gl = ax[n1,m1].gridlines(crs=ccrs.PlateCarree(), linewidth = lw_ax, color = 'k')
            # gl.xlocator = mticker.FixedLocator(np.arange(0,360.1,lon_interval)) 
            # gl.xlocator = mticker.FixedLocator(np.arange(-clon,360.1-clon,lon_interval))
            # gl.xlocator = mticker.FixedLocator(np.arange(-clon,360.1-clon,lon_interval))
            gl.xlocator = mticker.FixedLocator(np.arange(-360,360.1,lon_interval))     
            gl.ylocator = mticker.FixedLocator(np.arange(-90,90.1,lat_interval))

            ax[n1,m1].set_extent([xlim[0], xlim[1], ylim[0], ylim[1]], crs = ccrs.PlateCarree())    
            ctp_set_boundary(ax[n1,m1], projection_type)

            if np.size(level) == 1:
                image = ax[n1,m1].contourf(lon, lat, var[nm-1], np.linspace(vmin, vmax, (vint-1)*rt+1), extend = extend, cmap = cmap, transform = data_crs)
            else:
                # vartmp = np.zeros_like(var[nm-1])
                vartmp = np.nan*np.ones_like(var[nm-1])                
                if np.size(level[0]) == 1:
                    nls = np.size(level)
                    levtmp = np.arange(nls)
                    vartmp[var[nm-1]<level[0]] = -0.5
                    for nl in range(nls-1):
                        vartmp[(level[nl]<=var[nm-1])*(var[nm-1]<level[nl+1])] = nl+0.5
                    vartmp[level[-1]<var[nm-1]] = nls - 0.5
                    cmaptmp = cmap                    
                else:
                    
                    nls = np.size(level[nm-1])                    
                    levtmp = np.arange(nls)
                    vartmp[var[nm-1]<level[nm-1][0]] = -0.5
                    # vartmp[(var[nm-1]<level[nm-1][0])*(np.isnan(var[nm-1]) == False)] = -0.5
                    for nl in range(nls-1):
                        vartmp[(level[nm-1][nl]<=var[nm-1])*(var[nm-1]<level[nm-1][nl+1])] = nl+0.5
                        # vartmp[(level[nm-1][nl]<=var[nm-1])*(var[nm-1]<level[nm-1][nl+1])*(np.isnan(var[nm-1]) == False)] = nl+0.5                        
                        
                    vartmp[(level[nm-1][-1]<var[nm-1])] = nls - 0.5
                    # vartmp[(level[nm-1][-1]<var[nm-1])*(np.isnan(var[nm-1]) == False)] = nls - 0.5                    
                    if np.size(cmap) == 1:
                        cmaptmp = cmap
                    else:
                        cmaptmp = cmap[nm-1]                    


                if 'MaskedArray' in str(type(var)):            
                    vartmp[var[nm-1].mask] = np.nan            
                # image = ax[n1,m1].contourf(lon, lat, vartmp, levtmp, extend = extend, cmap = cmap, transform = data_crs)
                image = ax[n1,m1].contourf(lon, lat, vartmp, levtmp, extend = extend, cmap = cmaptmp, transform = data_crs)                
                
                
            ax[n1,m1].set_title(labels[nm-1])

            if linesc:
                ll = ax[n1,m1].contour(lon, lat, varl[nm-1], levels = lines, colors = 'k', transform = data_crs)
                ll.clabel(fmt=lfmt, fontsize=lfontsize)

            if(sngl_cbar):
                if((n == nrows-1)*(m == ncols -1)):
                    caxl = ax[n1,0].get_position()
                    caxr = ax[n1,m1].get_position()
                    caxv = ax[n1+1,0].get_position()
                    for m0 in range(ncols):
                        ax[n1+1,m0].remove()
                    cax = fig.add_axes([caxl.x0, 0.5*(caxv.y0+caxv.y1),caxr.x1-caxl.x0,0.01])
                    if np.size(level) == 1:                    
                        plt.colorbar(image, cax = cax, orientation = 'horizontal', ticks = np.linspace(vmin,vmax,vint))
                    else:
                        cbar = plt.colorbar(image, cax = cax, orientation = 'horizontal', ticks = levtmp)
                        if np.size(vticklabel) == 1:
                            cbar.ax.set_xticklabels(level)
                        else:
                            cbar.ax.set_xticklabels(vticklabel)    
            else:
                if ctl == False:                
                    caxh = ax[n1,m1].get_position()
                    caxv = ax[n1+1,m1].get_position()
                    ax[n1+1,m1].remove()
                    cax = fig.add_axes([caxh.x0, 0.5*(caxv.y0+caxv.y1),caxh.x1-caxh.x0,0.01])
                if np.size(level) == 1:
                    if ctl:                        
                        plt.colorbar(image, orientation = 'horizontal', ticks = np.linspace(vmin,vmax,vint))
                    else:
                        plt.colorbar(image, cax = cax, orientation = 'horizontal', ticks = np.linspace(vmin,vmax,vint))                    
                else:
                    if np.size(level[0])==1:
                        if ctl:                                                
                            cbar = plt.colorbar(image, orientation = 'horizontal', ticks = levtmp)
                        else:
                            cbar = plt.colorbar(image, cax = cax, orientation = 'horizontal', ticks = levtmp)                            
                        if np.size(vticklabel) == 1:
                            cbar.ax.set_xticklabels(level)
                        else:                
                            cbar.ax.set_xticklabels(vticklabel)    
                    else:
                        if ctl:
                            cbar = plt.colorbar(image, ax = ax[n1,m1], orientation = 'horizontal', ticks = levtmp)
                        else:
                            cbar = plt.colorbar(image, cax = cax, orientation = 'horizontal', ticks = levtmp)                            
                        if np.size(vticklabel) == 1:
                            cbar.ax.set_xticklabels(level[nm-1])
                        else:
                            if np.size(vticklabel[0]) == 1:                            
                                cbar.ax.set_xticklabels(vticklabel)
                            else:
                                cbar.ax.set_xticklabels(vticklabel[nm-1])
                            
            if (ERR < 0.):
                # print(nm-1)
                if np.any((var[nm-1] > 1.1 * ERR)*(var[nm-1] < 0.7 * ERR)):
                    ax[n1,m1].contourf(lon,lat,var[nm-1], levels = np.linspace(ERR*1.1, ERR*0.7, 3), cmap = "Greys")
            else:
                if np.any((var[nm-1] > 0.7 * ERR)*(var[nm-1] < 1.1 * ERR)):
                    ax[n1,m1].contourf(lon,lat,var[nm-1], levels = np.linspace(ERR*0.7, ERR*1.1, 3), cmap = "Greys")
            

            
    
    plt.suptitle(suptitle)
    if ctl:
        fig.tight_layout()
    if(output_file == ''):
        plt.show()
    else:
        plt.savefig(output_file)
    
    plt.close()




def surface_map_sc_ctp(output_file, lon, lat, var, nrows, ncols, level =  [0], vticklabel = [''], vr=[-999,-999,21],  rt = 10, xlim = [0, 359.9], ylim = [-90, 90], extend = 'both', cmap = 'jet', fsizex=11, fsizey= 8, clon = 180., clat = 90., lon_interval = 60, lat_interval = 30, fontsize = 20, projection_type='PlateCarree', ERR = -9.99e33, sngl_cbar = False, labels = [''], suptitle='', lw_ax = 1., cland = 'w', linesc = False, lines = [0.,], lfmt = '%1.1f', lfontsize = 11, skp=True, hratio = 4, ctl = False):

    plt.rcParams['font.size'] = fontsize
    data_crs = ccrs.PlateCarree()
    vmin, vmax, vint = vrange_func(var, vr)

    if(np.size(labels) == 1):
        labels = np.tile(labels, ncols*nrows)
        
    projection = projection_type_ctp(projection_type, clon, clat)        

    # fig = plt.figure(figsize = (fsizex, fsizey))
    if sngl_cbar:
        hratio = hratio*np.ones(nrows+1); hratio[nrows] = 1
        gs_kw = dict(height_ratios = hratio)
        fig, ax = plt.subplots(nrows+1, ncols, figsize = (fsizex, fsizey), subplot_kw = dict(projection = projection), gridspec_kw=gs_kw)
    else:
        if ctl:
            fig, ax = plt.subplots(nrows, ncols, figsize = (fsizex, fsizey), subplot_kw = dict(projection = projection))
        else:
            hratio = hratio*np.ones(2*nrows); hratio[1::2] =1
            gs_kw = dict(height_ratios = hratio)
            fig, ax = plt.subplots(2*nrows, ncols, figsize = (fsizex, fsizey), subplot_kw = dict(projection = projection), gridspec_kw=gs_kw)
  
    # if(np.shape(var) != (nrows*ncols), np.size(lat), np.size(lon)):
    #     if(np.size(lon) != np.size(lat)):
    #         ar_shape = np.array([nrows*ncols, np.size(lon),np.size(lat)])
    #         k = np.argmin(np.abs(np.shape(var) - ar_shape[0]))
    #         j = np.argmin(np.abs(np.shape(var) - ar_shape[1]))
    #         i = np.argmin(np.abs(np.shape(var) - ar_shape[2]))

    #         var = np.transpose(var, (k,j,i))
    #     else:
    #         sys.exit('transpose the array to (N, lat, lon)')

    nm = 0
    if ncols != 1:
        sys.exit('ncols should be 1')
    for n in range(nrows):
        for m in range(ncols):
            nm = nm + 1
            
            if(sngl_cbar):            
                n1 = n
                m1 = m
            else:
                n1 = 2*n
                m1 = m

            ax[n1].add_feature(cfeature.LAND, color = cland)
            ax[n1].coastlines(lw=0.5)
            gl = ax[n1].gridlines(crs=ccrs.PlateCarree(), linewidth = lw_ax, color = 'k')
            # gl.xlocator = mticker.FixedLocator(np.arange(0,360.1,lon_interval)) 
            gl.xlocator = mticker.FixedLocator(np.arange(-clon,360.1-clon,lon_interval)) 
            gl.ylocator = mticker.FixedLocator(np.arange(-90,90.1,lat_interval))

            ax[n1].set_extent([xlim[0], xlim[1], ylim[0], ylim[1]], crs = ccrs.PlateCarree())    
            ctp_set_boundary(ax[n1], projection_type)

            if np.size(level) == 1:            
                image = ax[n1].contourf(lon, lat, var[nm-1], np.linspace(vmin, vmax, (vint-1)*rt+1), extend = extend, cmap = cmap, transform = data_crs)
            else:
                vartmp = np.zeros_like(var[nm-1])
                if np.size(level[0]) == 1:
                    nls = np.size(level)
                    levtmp = np.arange(nls)
                    vartmp[var[nm-1]<level[0]] = -0.5
                    for nl in range(nls-1):
                        vartmp[(level[nl]<=var[nm-1])*(var[nm-1]<level[nl+1])] = nl+0.5
                    vartmp[level[-1]<var[nm-1]] = nls - 0.5
                    cmaptmp = cmap
                    
                else:
                    nls = np.size(level[nm-1])                    
                    levtmp = np.arange(nls)                
                    vartmp[var[nm-1]<level[nm-1][0]] = -0.5
                    for nl in range(nls-1):
                        vartmp[(level[nm-1][nl]<=var[nm-1])*(var[nm-1]<level[nm-1][nl+1])] = nl+0.5
                    vartmp[level[nm-1][-1]<var[nm-1]] = nls - 0.5
                    if np.size(cmap) == 1:
                        cmaptmp = cmap
                    else:
                        cmaptmp = cmap[nm-1]                    
                    
                if 'MaskedArray' in str(type(var)):            
                    vartmp[var[nm-1].mask] = np.nan

                image = ax[n1].contourf(lon, lat, vartmp, levtmp, extend = extend, cmap = cmaptmp, transform = data_crs)                
                
            ax[n1].set_title(labels[nm-1])

            if linesc:
                ll = ax[n1].contour(lon, lat, var[nm-1], levels = lines, colors = 'k', transform = data_crs)
                ll.clabel(fmt=lfmt, fontsize=lfontsize)

            if sngl_cbar:
                if((n == nrows-1)*(m == ncols -1)):
                    # caxl = ax[n1+1].get_position()
                    # caxr = ax[n1+1].get_position()
                    caxl = ax[n1].get_position()
                    caxr = ax[n1].get_position()                                        
                    cax0 = ax[n1+1].get_position()                    
                    for m0 in range(ncols):
                        ax[n1+1].remove()
                    # cax = fig.add_axes([cax0.x0, 0.5*(cax0.y0+cax0.y1),cax0.x1-cax0.x0,0.01])
                    cax = fig.add_axes([caxl.x0, 0.5*(cax0.y0+cax0.y1),caxr.x1-caxl.x0,0.01])                    
                    # cax = fig.add_axes([0.1, 0.5*(cax0.y0+cax0.y1),0.8,0.01])
                    # cax = fig.add_axes([caxl.x0, 0.5*(caxl.y0+caxl.y1),0.8*fsizex,0.01])

                    if np.size(level) == 1:                    
                        plt.colorbar(image, cax = cax, orientation = 'horizontal', ticks = np.linspace(vmin,vmax,vint))
                    else:
                        cbar = plt.colorbar(image, cax = cax, orientation = 'horizontal', ticks = levtmp)
                        if np.size(vticklabel) == 1:
                            cbar.ax.set_xticklabels(level)
                        else:
                            cbar.ax.set_xticklabels(vticklabel)

            else:                
                if ctl == False:                
                    caxh = ax[n1].get_position()
                    caxv = ax[n1+1].get_position()
                    ax[n1+1].remove()
                    cax = fig.add_axes([caxh.x0, 0.5*(caxv.y0+caxv.y1),caxh.x1-caxh.x0,0.01])
                if np.size(level) == 1:
                    if ctl:                        
                        plt.colorbar(image, orientation = 'horizontal', ticks = np.linspace(vmin,vmax,vint))
                    else:
                        plt.colorbar(image, cax = cax, orientation = 'horizontal', ticks = np.linspace(vmin,vmax,vint))                    
                else:
                    if np.size(level[0])==1:
                        if ctl:                                                
                            cbar = plt.colorbar(image, orientation = 'horizontal', ticks = levtmp)
                        else:
                            cbar = plt.colorbar(image, cax = cax, orientation = 'horizontal', ticks = levtmp)                            
                        if np.size(vticklabel) == 1:
                            cbar.ax.set_xticklabels(level)
                        else:                
                            cbar.ax.set_xticklabels(vticklabel)    
                    else:
                        if ctl:
                            cbar = plt.colorbar(image, ax = ax[n1], orientation = 'horizontal', ticks = levtmp)
                        else:
                            cbar = plt.colorbar(image, cax = cax, orientation = 'horizontal', ticks = levtmp)                            
                        if np.size(vticklabel) == 1:
                            cbar.ax.set_xticklabels(level[nm-1])
                        else:
                            if np.size(vticklabel[0]) == 1:                            
                                cbar.ax.set_xticklabels(vticklabel)
                            else:
                                cbar.ax.set_xticklabels(vticklabel[nm-1])
                                

            if(ERR < 0.):
                # print(nm-1)
                if np.any((var[nm-1] > 1.1 * ERR)*(var[nm-1] < 0.7 * ERR)):
                    ax[n1].contourf(lon,lat,var[nm-1], levels = np.linspace(ERR*1.1, ERR*0.7, 3), cmap = "Greys")
            else:
                if np.any((var[nm-1] > 0.7 * ERR)*(var[nm-1] < 1.1 * ERR)):
                    ax[n1].contourf(lon,lat,var[nm-1], levels = np.linspace(ERR*0.7, ERR*1.1, 3), cmap = "Greys")
            

            
    
    plt.suptitle(suptitle)
    if ctl:
        fig.tight_layout()        
    if(output_file == ''):
        plt.show()
    else:
        plt.savefig(output_file)
    
    plt.close()




def surface_map_sngle_cl_ctp(output_file, lon, lat, var, vr=[-999,-999,21], xlim = [0., 359.9], ylim = [-90., 90.], col = 'k', fsizex=6, fsizey= 4, clon = 180., clat = 90., lon_interval = 60, lat_interval = 30, fontsize = 12, projection_type='PlateCarree', ERR = -9.99e33, suptitle='', lw_ax = 1., label = '', cland = 'w', lines = [0.,], lfmt = '%1.1f', lfontsize = 11):


    plt.rcParams['font.size'] = fontsize
    vmin, vmax, vint = vrange_func(var, vr)
    
    data_crs = ccrs.PlateCarree()
    fig = plt.figure(figsize = (fsizex, fsizey))
        
    projection = projection_type_ctp(projection_type, clon, clat)        
    ax = fig.add_subplot(111, projection=projection)

    ax.add_feature(cfeature.LAND, color = cland)
    ax.coastlines(lw=0.5)
    gl = ax.gridlines(crs=ccrs.PlateCarree(), linewidth = lw_ax, color = 'k')
    # gl.xlocator = mticker.FixedLocator(np.arange(0,360.1,lon_interval)) 
    # gl.xlocator = mticker.FixedLocator(np.arange(-180,180.1,lon_interval)) 
    gl.xlocator = mticker.FixedLocator(np.arange(-clon,360.1-clon,lon_interval)) 
    gl.ylocator = mticker.FixedLocator(np.arange(-90,90.1,lat_interval))

    ax.set_extent([xlim[0], xlim[1], ylim[0], ylim[1]], crs = ccrs.PlateCarree())
    ctp_set_boundary(ax, projection_type)

    image = ax.contour(lon, lat, var, levels = np.linspace(vmin, vmax, vint), colors = col, transform = data_crs)
    
    image.clabel(fmt=lfmt, fontsize=lfontsize)
        
    ax.set_title(label)
    plt.tight_layout()

    if(output_file == ''):
        plt.show()
    else:
        plt.savefig(output_file)

    plt.close()


def surface_map_mc_cl_ctp(output_file, lon, lat, var, nrows, ncols, vr=[-999,-999,21],  xlim = [0, 359.9], ylim = [-90, 90], col = 'k', fsizex=11, fsizey= 8, clon = 180., clat = 90., lon_interval = 60, lat_interval = 30, fontsize = 12, projection_type='PlateCarree', ERR = -9.99e33, labels = [''], suptitle='', lw_ax = 1., cland = 'w', lfmt = '%1.1f', lfontsize = 11):

    plt.rcParams['font.size'] = fontsize
    data_crs = ccrs.PlateCarree()
    vmin, vmax, vint = vrange_func(var, vr)

    if(np.size(labels) == 1):
        labels = np.tile(labels, ncols*nrows)
        
    projection = projection_type_ctp(projection_type, clon, clat)        

    hratio = 4*np.ones(nrows)
    gs_kw = dict(height_ratio = hratio)
    fig, ax = plt.subplots(nrows, ncols, figsize = (fsizex, fsizey), subplot_kw = dict(projection = projection), gridspec_kw=gs_kw)

    nm = 0
    for n in range(nrows):
        for m in range(ncols):
            nm = nm + 1
            
            n1 = n
            m1 = m

            ax[n1,m1].add_feature(cfeature.LAND, color = cland)
            ax[n1,m1].coastlines(lw=0.5)
            gl = ax[n1,m1].gridlines(crs=ccrs.PlateCarree(), linewidth = lw_ax, color = 'k')
            # gl.xlocator = mticker.FixedLocator(np.arange(0,360.1,lon_interval)) 
            gl.xlocator = mticker.FixedLocator(np.arange(-clon,360.1-clon,lon_interval))
            gl.ylocator = mticker.FixedLocator(np.arange(-90,90.1,lat_interval))

            ax[n1,m1].set_extent([xlim[0], xlim[1], ylim[0], ylim[1]], crs = ccrs.PlateCarree())    
            ctp_set_boundary(ax[n1,m1], projection_type)

            image = ax[n1,m1].contour(lon, lat, var[nm-1], levels = np.linspace(vmin, vmax, vint), colors = col, transform = data_crs)
            ax[n1,m1].set_title(labels[nm-1])
            image.clabel(fmt=lfmt, fontsize=lfontsize)            
    
    plt.suptitle(suptitle)
    # fig.tight_layout()
    if(output_file == ''):
        plt.show()
    else:
        plt.savefig(output_file)
    
    plt.close()



def surface_map_sngle_ctp_wv(output_file, lon, lat, var, lonv, latv, varx, vary, vr=[-999,-999,21], rt = 10, vscl = 1., rgs=30, xlim = [0., 359.9], ylim = [-90., 90.], extend = 'both', cmap = 'jet', fsizex=6, fsizey= 4, clon = 180., clat = 90., lon_interval = 60, lat_interval = 30, fontsize = 20, projection_type='PlateCarree', ERR = -9.99e33, suptitle='', lw_ax = 1., label = '', cland = 'w', linesc = False, lines = [0.,], lfmt = '%1.1f', lfontsize = 11):


    plt.rcParams['font.size'] = fontsize
    vmin, vmax, vint = vrange_func(var, vr)
    
    data_crs = ccrs.PlateCarree()
    fig = plt.figure(figsize = (fsizex, fsizey))
        
    projection = projection_type_ctp(projection_type, clon, clat)        
    ax = fig.add_subplot(111, projection=projection)

    ax.add_feature(cfeature.LAND, color = cland)
    ax.coastlines(lw=0.5)
    gl = ax.gridlines(crs=ccrs.PlateCarree(), linewidth = lw_ax, color = 'k')

    # gl.xlocator = mticker.FixedLocator(np.arange(0,360.1,lon_interval)) 
    # gl.xlocator = mticker.FixedLocator(np.arange(-180,180.1,lon_interval)) 
    gl.xlocator = mticker.FixedLocator(np.arange(-clon,360.1-clon,lon_interval)) 
    gl.ylocator = mticker.FixedLocator(np.arange(-90,90.1,lat_interval))

    ax.set_extent([xlim[0], xlim[1], ylim[0], ylim[1]], crs = ccrs.PlateCarree())
    ctp_set_boundary(ax, projection_type)

    image = ax.contourf(lon, lat, var, np.linspace(vmin, vmax, (vint-1)*rt+1), extend = extend, cmap = cmap, transform = data_crs)
    
    # lon0 = np.arange(361.)
    # lat0 = -90.+np.arange(181)
    # X, Y = np.meshgrid(lon0, lat0)
    # image = ax.pcolor(X, Y, var, np.linspace(vmin, vmax, (vint-1)*rt+1), extend = extend, cmap = cmap, transform = data_crs)

    plt.colorbar(image, orientation = 'horizontal', ticks = np.linspace(vmin,vmax,vint))
    
    XV, YV = np.meshgrid(lonv, latv)    
    print(vscl)
    # vc = ax.quiver(XV, YV, varx/vscl, vary/vscl, transform=data_crs)
    # vc = ax.quiver(XV, YV, varx, vary, transform=data_crs, angles='xy')
    vc = ax.quiver(XV, YV, varx/vscl, vary/vscl, transform=data_crs, regrid_shape=rgs, units='xy', angles='xy', scale_units='xy', scale=1.)
    # vc = ax.quiver(XV, YV, varx, vary, transform=ccrs.NorthPolarStereo())
    
    if(linesc):
        ll = ax.contour(lon, lat, var, levels = lines, colors = 'k', transform = data_crs)
        ll.clabel(fmt=lfmt, fontsize=lfontsize)
        
    ax.set_title(label)
    plt.tight_layout()

    if(output_file == ''):
        plt.show()
    else:
        plt.savefig(output_file)

    plt.close()


def projection_type_ctp(projection_type, clon, clat):
    if(projection_type == 'PlateCarree'):
        projection = ccrs.PlateCarree(central_longitude=clon)
    elif(projection_type == 'Orthographic'):
        projection=ccrs.Orthographic(central_longitude=clon, central_latitude=clat)
    elif(projection_type == 'NorthPolarStereo'):
        projection=ccrs.NorthPolarStereo(central_longitude=clon)
    elif(projection_type == 'SouthPolarStereo'):
        projection=ccrs.SouthPolarStereo(central_longitude=clon)
    else:
        print('check projection name/add projection type in fig_module.surface_map_sngle_ctp')
        sys.exit()

    return projection


def vrange_func(var, vr):
    vmin = vr[0]; vmax = vr[1]; vint = vr[2]
    if(vr[0] == -999):
        vmin = np.min(var)
    if(vr[1] == -999):
        vmax = np.max(var)

    return vmin, vmax, vint
        
def ctp_set_boundary(ax, projection_type):
    if (projection_type == 'Orthographic') or \
       (projection_type == 'NorthPolarStereo') or \
       projection_type == 'SouthPolarStereo' :
        
        theta = np.linspace(0, 2*np.pi, 100)
        center, radius = [0.5, 0.5], 0.5
        verts = np.vstack([np.sin(theta), np.cos(theta)]).T
        circle = mpath.Path(verts * radius + center)        

        ax.set_boundary(circle, transform=ax.transAxes)

def ctp_set_boundary_ax(ax, projection_type):
    if (projection_type == 'Orthographic') or \
       (projection_type == 'NorthPolarStereo') or \
       projection_type == 'SouthPolarStereo' :
        
        theta = np.linspace(0, 2*np.pi, 100)
        center, radius = [0.5, 0.5], 0.5
        verts = np.vstack([np.sin(theta), np.cos(theta)]).T
        circle = mpath.Path(verts * radius + center)        

        ax.set_boundary(circle, transform=ax.transAxes)

    return ax


