import os
import sys
import calendar
import numpy as np
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)
import config.config as cf
import boundary.boundary.woaNxN2amip as w2a
import obs.read_sst_module as rs


def main(ybgn, yend, RES, data = cf.datadir()+'/obs/SST/input4MIPs/model/sst_TL159_CMIP6AMIP_YYYY.dat', diro = cf.datadir()+'/obs/SST/input4MIPs/model/', ERR = -9.99e33, cbcs = True):

    lono, lato, ssto = rs.read_input4MIPs(ybgn, yend)    
    lona, lata, ssta = w2a.area(lono, lato, ssto, 'TL159')
    
    ssta = ssta[:,:,::-1]    
    lata = lata[::-1]    
    # msks = msks[:,::-1]
    for year in range(ybgn,yend+1):
        # print(year)
        if 'YYYY' in data:
            data0 = data.replace('YYYY', str(year))
        
        fnameoutt = diro + '/sst_TL159_CMIP6AMIP_'+str(year)+'.dat'

        foutdir = os.path.dirname(fnameoutt)
        if not os.path.isdir(foutdir):
            os.makedirs(foutdir)

        np.array(ssta[year-ybgn]).reshape(-1).astype('>f').tofile(fnameoutt)            


if __name__ == '__main__':
    ybgn = 1978; yend = 2015
    RES = 'TL159'
    cbcs = False
    main(ybgn, yend, RES, cbcs = cbcs)    
