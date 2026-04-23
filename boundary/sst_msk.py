import os
import sys
import calendar
import numpy as np
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)
import config.config as cf
import cmip.cmip_mm as cmm
import cmip.cmip.cmip_data as cd
import boundary.boundary.woaNxN2amip as w2a
import obs.read_sst_module as rs

def main(models, RES, ybgnc = 1985, yendc = 2014, diro = cf.datadir()+'/AGCM/cnst/', ERR = -9.99e33):

    lono, lato, sstM = cmm.ReadData2dMMClim('tos', models, 'historical', ybgnc, yendc, regrid = True, dirbase = cf.datadir())    
    lona, lata, sstc = w2a.area(lono, lato, sstM, 'TL159')

    im = np.size(lona); jm = np.size(lata)
    day = calendar.mdays[1:]
    sstcann = np.average(sstc, axis=0, weights = day)
    msk = 1-sstcann.mask.astype(np.float)
    
    fnameoutt = diro + '/omsk_TL159.dat'
    foutdir = os.path.dirname(fnameoutt)
    if not os.path.isdir(foutdir):
        os.makedirs(foutdir)        
    msk[::-1].reshape(-1).astype('>f').tofile(fnameoutt)    

if __name__ == '__main__':
    ybgn = 1978; yend = 2015
    models = cmm.read_models()
    RES = 'TL159'
    main(models, RES)    
