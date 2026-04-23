import os
import sys
import calendar
import numpy as np
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)
import config.config as cf
import cmip.cmip_mm as cmm
import boundary.boundary.woaNxN2amip as w2a
import obs.read_sst_module as rs

def main(models, ybgn, yend, RES, ybgnc = 1985, yendc = 2014, data = cf.datadir()+'/obs/SST/input4MIPs/model/sst_TL159_CMIP6AMIP_YYYY.dat', diro = cf.datadir()+'/AGCM/CMIP_BIAS/', ERR = -9.99e33):

    lono, lato, sstM = cmm.ReadData2dMMClim('tos', models, 'historical', ybgnc, yendc, regrid = True, dirbase = cf.datadir())
    lona, lata, sstc = w2a.area(lono, lato, sstM, 'TL159')
    lona, lata, ssto = rs.read_input4MIPs(ybgnc, yendc, camip = True)    
    ssto = np.mean(ssto, axis=0) - 273.15

    im = np.size(lona); jm = np.size(lata)
    day = calendar.mdays[1:]
    sstcann = np.average(sstc, axis=0, weights = day)
    sstoann = np.average(ssto, axis=0, weights = day)
    msk = 1-sstcann.mask.astype(np.float)
    sstano = (sstcann - sstoann).data * msk
    mskc = msk.copy()
        
    rt = 320/360 

    model = 'EMS'+str(np.size(models)).zfill(2)
    sstano = sstano[::-1]    
    lata = lata[::-1]    
    for year in range(ybgn,yend+1):
        if 'YYYY' in data:
            data0 = data.replace('YYYY', str(year))
        
        sstobs = np.fromfile(data0, '>f').reshape(12,jm,im)
        sstout = sstobs + sstano        
        fnameoutt = diro + model + '_anom/sst_TL159_CMIP6AMIP_'+str(ybgnc)+'-'+str(yendc)+'_annclm_glb_anom_'+str(year)+'.dat'

        foutdir = os.path.dirname(fnameoutt)
        if not os.path.isdir(foutdir):
            os.makedirs(foutdir)

        sstout.reshape(-1).astype('>f').tofile(fnameoutt)            

if __name__ == '__main__':
    ybgn = 1978; yend = 2015
    models = cmm.read_models()
    RES = 'TL159'
    main(models, ybgn, yend, RES)    
