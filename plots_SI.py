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

    
main(cintm = cintm, dpi = dpi)

