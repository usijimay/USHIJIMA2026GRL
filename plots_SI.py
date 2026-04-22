import os
import sys
import calendar
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.ticker as mticker
import cartopy.crs as ccrs
import cmocean.cm as cmo
import seaborn as sns
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE)
import mriagcm3.read_clm as mrc

sns.set_theme(style = 'whitegrid', font_scale = 1.)
import cmip.cmip_mm as cmm
import config.config as cf
import config.fig_module as fm

expid0 = 'MPE3_agcm_cntl'
exptyp = 'region'
areasns = ['glb', 'snp', 'exsnp', 'wnp', 'ceq', 'enp']
expids = np.array(list(map(lambda x: 'MPE3_agcm_EMS35_annclm_'+x, areasns))).astype(object)

ybgn = 1985; yend = 2014
cintm = False
dpi = 900
dirbase = '/data16/theme-C/usijimay'

def main(cintm = False, dpi = 900):
    global lon, lat
    global var0, varm0, varc0
    global var, varm, varc
    global varmo, varco, rvarco

    suff = '.png'    
    figdir =  cf.figdir(dpi = dpi)    
        
    R0 = 6.375e6    
    lonmin=120; lonmax=240

    lono, lato, toso = cmm.read_sst_amip(ybgn, yend, cann = True, dirbase = dirbase+'/obs')
    
    models, lonuem, latuem, levuem, lonvem, latvem, levvem, lonwem, latwem, levwem, lontem, lattem, levtem, toscfem, uacfem, uaafem, vacfem, vaafem, wacfem, waafem, tacfem, taafem, zgcfem, zgafem, dbdycfem, dbdyafem, dbdzcfem, dbdzafem, egrcfem, egrafem = cmm.read_datas_MM(ybgn, yend, am, cem = True, dirbase = dirbase)

    
    nf = 2
    pngfile=figdir+'figS'+str(nf)+suff
    fm.figS1(pngfile, models, lono, lato, toscfem, toso, lonr = [0, 359.9, 120], latr = [-90, 90, 30], vr=[-2.4, 2.4, 5], cmap = cmo.balance, tlabel = models, ncols = 4, fsizey = 10, dpi = dpi)

    ktgt0 = 9    
    nf = 1
    pngfile=figdir+'figS'+str(nf)+suff
    fm.figS2(pngfile, models, lonuem, latuem, uacfem, uaafem, ktgt0, lonr = [90, 270, 60], latr = [-20, 80, 20], vr=[-12, 12, 5], lines = np.linspace(-100, 100, 21), cmap = cmo.balance, tlabel = models, ncols = 4, fsizey = 11, dpi = dpi)
    

def am(var, axis=0):

    if np.size(var) == 0:
        varann = var
    else:
        day = np.array(calendar.mdays[1:])        
        varann = np.average(var, weights = day, axis=axis)

    return varann
    

# def am0(var, ns, axis=0):

#     if np.size(var) == 0:
#         varann = var
#     else:
#         day = np.array(calendar.mdays[1:])        
#         varann = np.average(var, weights = day, axis=axis)

#     return varann

# # Unused functions - commented out
# def plot_ulatlev(pngfile, lev, lat, varf, varl, ncols, nrows, xr = [-90,90], yr = [1000, 0], vr = [-12, 12, 5], rt = 10, level = [], levl = np.linspace(-100, 100, 101), latl = [], latf = [], fontsize = 10, fsizex = 8, fsizey = 8, cmap = cmo.balance, extend = 'both', sngl_cbar = True, vecx = [], vecy = [], levv = [], scale = 1, scale_units = 'xy', iskp = 1, jskp = 1, vcols = ['w'], unitx = 1.02, unity = -2.9, unitcbr = r'[${\rm m \ s^{-1}}$]', labels = [], bbox = dict(facecolor='white', alpha=0.7), dxc = 0.04, dyc = 0.04):
#     pass

# def read_amip2D(expid0, expids, fbase, varname, ybgn, yend, msk = []):
#     pass

# def read_amip3D(expid0, expids, fbase, varname, ybgn, yend, msk = []):
#     pass
    
# def omsk(varM, msk):
#     pass

# def ZonalMean(lon, var, axis = 0, lonmin = 120, lonmax = 240):
#     pass

# def am(var, axis=0):
#     pass

# def sm(var, axis=0, nr=1):
#     pass

# def sm0(var, nn, axis=0, nr=1):
#     pass

# def djfm(var, axis=0, nr=1):
#     pass

# def polyfit2d(x, var, axis=-1):
#     pass
            
# def each_plot_map(expid0, expids, lon, lat, var0M, varM, yearc, lonmin = 120, lonmax = 240, lonint = 30, latmin = 20, latmax = 60, latint = 10, varcM = []):
#     pass

# def plot_ulat(pngfile, expids, lat, vlatM, xmin = 0, xmax = 10, latmin = 20, latmax = 60, fontsize = 12, vlatoM = [], vlatcM = [], vlatV = [], vlatoV = [], vlatcV = [], vlatsM = []):
#     pass

# def plot_abcbar(pngfile, labels, abcs, fontsize = 12, abco = [], abcc = [], abcr = [], ymin = 0, ymax = 10):
#     pass

# def read_sst(expid0, expids, ybgn, yend, msk = []):
#     pass

    
main(cintm = cintm, dpi = dpi)

