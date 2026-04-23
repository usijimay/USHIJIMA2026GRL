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


def main(areas, models, ybgn, yend, RES, ybgnc = 1985, yendc = 2014, data = cf.datadir()+'/obs/SST/input4MIPs/model/sst_TL159_CMIP6AMIP_YYYY.dat', diro = cf.datadir()+'/AGCM/CMIP_BIAS/', ERR = -9.99e33, cexcl = False):

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
    if areas[0] != '':
        areaadd = 'ex'
        msk = np.zeros((jm,im))            
        for area in areas:
            mska = np.zeros((jm,im))
            if area == 'wnp':
                for i in range(int(rt*120),int(rt*230)):
                    if i < int(rt*126):
                        j0 = int(rt*110)
                        jmin0 = int(rt*95)
                        jmax0 = int(rt*140)
                        if np.any(mskc[jmin0:j0,i]==0):   
                            jjmin = jmin0+np.where(mskc[jmin0:j0,i]==0)[0][-1]
                        if np.any(mskc[j0:jmax0,i]==0):   
                            jjmax = j0+np.where(mskc[j0:jmax0,i]==0)[0][0]-1
                        mska[jjmin+1:jjmax+1,i] = 1
                        cnd = (sstano[jjmin+1:jjmax+1,i] > 0) 
                        if np.any(cnd):
                            jj = np.where(cnd)[0]
                            for j in jj:
                                mska[jjmin+1+j,i] = 0

                    elif i < int(rt*180):
                        jmin0 = int(rt*90)
                        if i < int(rt*160):
                            jmax0 = int(rt*133)
                        else:
                            jmax0 = int(rt*140)
                        j0 = jmin0+np.argmin(sstano[jmin0:jmax0,i])

                        cnd = (sstano[jmin0:j0-1,i]>0)*(sstano[jmin0+1:j0,i]<0)
                        if np.any(cnd):
                            jjmin = jmin0+np.where(cnd)[0][-1]
                        elif np.any(mskc[jmin0:j0,i]==0):   
                            jjmin = jmin0+np.where(mskc[jmin0:j0,i]==0)[0][-1]
                        else:
                            jjmin = jmin0+np.argmax(sstano[jmin0:j0,i])-1            
                        cnd = (sstano[j0:jmax0-1,i]<0)*(sstano[j0+1:jmax0,i]>0)
                        if np.any(cnd):
                            jjmax = j0+np.where(cnd)[0][0]
                        elif np.any(mskc[j0:jmax0,i]==0):   
                            jjmax = j0+np.where(mskc[j0:jmax0,i]==0)[0][0]-1
                        else:
                            jjmax = j0+np.argmax(sstano[j0:jmax0,i])
                        mska[jjmin+1:jjmax+1,i] = 1
                    elif i < int(rt*240):
                        jmin0 = int(rt*100)
                        jmax0 = int(rt*140)                        
                        cnd = (sstano[jmin0:jmax0,i] < 0.)
                        if np.any(cnd):
                            jj = jmin0+np.where(cnd)[0]
                            mska[jj[0]:jj[-1]+1,i] = 1.        
            elif area == 'ceq':
                for i in range(int(rt*135),int(rt*270)):
                    j0 = int(rt*90)
                    jmin0=int(rt*80)
                    jmax0=int(rt*100)
                    cnd = (sstano[jmin0:j0-1,i]>0)*(sstano[jmin0+1:j0,i]<0)
                    if np.any(cnd):
                        jjmin = jmin0+np.where(cnd)[0][-1]
                    elif np.any(mskc[jmin0:j0,i]==0):   
                        jjmin = jmin0+np.where(mskc[jmin0:j0,i]==0)[0][-1]
                    else:
                        jjmin = jmin0+np.argmax(sstano[jmin0:j0,i])-1            
                    cnd = (sstano[j0:jmax0-1,i]<0)*(sstano[j0+1:jmax0,i]>0)
                    if np.any(cnd):
                        jjmax = j0+np.where(cnd)[0][0]
                    elif np.any(mskc[j0:jmax0,i]==0):   
                        jjmax = j0+np.where(mskc[j0:jmax0,i]==0)[0][0]-1
                    else:
                        jjmax = j0+np.argmax(sstano[j0:jmax0,i])
                    mska[jjmin+1:jjmax+1,i] = 1
                    cnd = (sstano[jjmin+1:jjmax+1,i] > 0) 
                    if np.any(cnd):
                        jj = np.where(cnd)[0]
                        for j in jj:
                            mska[jjmin+1+j,i] = 0
                            
            elif area == 'snp':
                mska[int(rt*120):int(rt*155),int(rt*105):int(rt*265)] = 1.
                jmin = int(rt*60); jmax = int(rt*120)
                for j in range(jmin,jmax):
                    i0 = int(rt*180)
                    i = i0
                    while mskc[j,i] == 1:
                        mska[j,i] = 1.
                        i = i-1
                    i = i0
                    while mskc[j,i] == 1:
                        mska[j,i] = 1.
                        i = i+1                 
                
            if area == areas[0]:
                msks = mska[np.newaxis]
                areaadd = area
            else:
                msks = np.vstack((msks,mska[np.newaxis]))
                areaadd = areaadd + area            

    nas = np.size(areas)
    model = 'EMS'+str(np.size(models)).zfill(2)
    sstano = sstano[::-1]    
    lata = lata[::-1]    
    msks = msks[:,::-1]
    for year in range(ybgn,yend+1):
        # print(year)
        if 'YYYY' in data:
            data0 = data.replace('YYYY', str(year))
        
        sstobs = np.fromfile(data0, '>f').reshape(12,jm,im)
        sstout = sstobs + sstano        
        fnameoutt = diro + model + '_anom/sst_TL159_CMIP6AMIP_'+str(ybgnc)+'-'+str(yendc)+'_annclm_glb_anom_'+str(year)+'.dat'

        foutdir = os.path.dirname(fnameoutt)
        if not os.path.isdir(foutdir):
            os.makedirs(foutdir)

        if areas[0] != '':
            for na in range(nas):
                area = areas[na]
                mska = msks[na]

                fnameoutt = diro + model + '_anom/sst_TL159_CMIP6AMIP_'+str(ybgnc)+'-'+str(yendc)+'_annclm_'+area+'_anom_'+str(year)+'.dat'                  
        
                sstouta = sstout * mska + sstobs * (1-mska)
                sstouta.reshape(-1).astype('>f').tofile(fnameoutt)    

            if cexcl:
                mska = 1-mska
                area = 'ex'+areaadd 
                fnameoutt = diro + model + '_anom/sst_TL159_CMIP6AMIP_'+str(ybgnc)+'-'+str(yendc)+'_annclm_'+area+'_anom_'+str(year)+'.dat'                  
                
                sstouta = sstout * mska + sstobs * (1-mska)
                sstouta.reshape(-1).astype('>f').tofile(fnameoutt)    


if __name__ == '__main__':
    ybgn = 1978; yend = 2015
    models = cmm.read_models()
    RES = 'TL159'
    
    cexcl = True
    areas = ['snp']
    main(areas, models, ybgn, yend, RES, cexcl = cexcl)
    
    cexcl = False
    areas = ['wnp', 'ceq', 'enp']
    main(areas, models, ybgn, yend, RES, cexcl = cexcl)    
