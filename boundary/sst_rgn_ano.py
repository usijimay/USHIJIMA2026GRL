import os
# import netCDF4
import sys
# import re
# import glob
import calendar
# import pygrib
import numpy as np
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE)
import config.config as cf
import cmip.cmip_mm as cmm
import cmip.cmip.cmip_data as cd
# homedir = os.environ['HOME']
# sys.path.append(homedir+"/anl_esm/anlpy/cmip")
# import cmip.cmip.cmip_data as cd
# sys.path.append(homedir+"/anl_esm/anlpy/remap_tools")
# import remap_tools.create_remap_table_cmip as crt
# import cmip_gn2gr as cgr
import boundary.boundary.woaNxN2amip as w2a
# sys.path.append("../obs")
import obs.read_sst_module as rs

# sys.path.append(homedir+"/anl_esm/anlpy/SHARED_SCRIPT")
# import map_cartopy as mc
# import cmocean.cm as cmo

# ybgn = 1978; yend = 2014
ybgn = 1978; yend = 2015
# ybgn = 2015; yend = 2015
# ybgn = 1978; yend = 1978

# ampmdl = os.listdir('/Public/CMIPs/CMIP6/CMIP/amip/Amon/uas/')
# cmpmdla = os.listdir('/Public/CMIPs/CMIP6/CMIP/historical/Amon/uas/')
# cmpmdlo = os.listdir('/Public/CMIPs/regrid/CMIP6/100deg-360x180/CMIP/historical/Omon/tos/')
# models = np.intersect1d(ampmdl, cmpmdla, cmpmdlo) 
# models = models['CAS-ESM2-0' != models]
# models = models['ICON-ESM-LR' != models]
# models = models['IITM-ESM' != models]
# models = models['GISS-E2-1-G' != models]

models = cmm.read_models()

RES = 'TL159'
cglbo = False
cexcl = False
areas = ['wnp', 'ceq', 'enp']
cexcl = True
areas = ['snp']

def main(areas, models, ybgn, yend, RES, ybgnc = 1985, yendc = 2014, data = cf.datadir()+'/obs/SST/input4MIPs/model/sst_TL159_CMIP6AMIP_YYYY.dat', diro = cf.datadir()+'/AGCM/CMIP_BIAS/', ERR = -9.99e33, cexcl = False):

    # for model in models:
    #     print(model)
    #     fnameins = cd.datafiles('tos', model, 'historical', ybgn = ybgnc, yend = yendc, regrid = True)
    #     lono, lato, time, sstm = cd.ReadData2d(fnameins, 'tos', ybgnc, yendc)
    #     sstm = sstm.reshape(-1,12,180,360)
    #     sstc = np.mean(sstm, axis=0)

    #     if model == models[0]:
    #         sstem = sstc[np.newaxis]
    #     else:
    #         sstem = np.ma.vstack((sstem,sstc[np.newaxis]))

    # num = np.sum(sstem.mask.astype(np.float), axis=0)
    # sstM = np.ma.masked_array(np.mean(sstem, axis=0), mask = (num > 0))
    lono, lato, sstM = cmm.ReadData2dMMClim('tos', models, 'historical', ybgnc, yendc, regrid = True, dirbase = cf.datadir())
    
    lona, lata, sstc = w2a.area(lono, lato, sstM, 'TL159')
    lona, lata, ssto = rs.read_input4MIPs(ybgnc, yendc, camip = True)    
    ssto = np.mean(ssto, axis=0) - 273.15

    im = np.size(lona); jm = np.size(lata)
    # msk = 1-sstc.mask.astype(np.float)
    # sstano = (sstc - ssto).data * msk
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

            # elif area == 'enp':                
            #     mska[sstano > 0.] = 1.
            #     mska[:int(rt*93)] = 0.
            #     mska[int(rt*150):] = 0.
            #     mska[:,:int(rt*120)] = 0.
            #     mska[:,int(rt*263):] = 0.
            #     mska[int(rt*120):int(rt*150),int(rt*120):int(rt*175)] = 0.
            #     mska[int(rt*90):int(rt*120),int(rt*120):int(rt*165)] = 0.                
            # elif area == 'esp':
            #     mska[sstano > 0.] = 1.
            #     mska[:int(rt*60)] = 0.                
            #     mska[int(rt*95):] = 0.
            #     mska[:,:int(rt*150)] = 0.
            #     mska[:,int(rt*300):] = 0.
            #     mska[int(rt*90):,:int(rt*240)] = 0.
            #     mska[:int(rt*75),:int(rt*210)] = 0.                
            #     # mska[:int(rt*105),int(rt*267):] = 0.
            # elif area == 'kos':
            #     mska[sstano > 0.] = 1.
            #     mska[:int(rt*120)] = 0.
            #     mska[int(rt*140):] = 0.
            #     mska[:,:int(rt*140)] = 0.
            #     mska[:,int(rt*160):] = 0.
            #     mska[int(rt*133):,int(rt*150):] = 0.
            #     mska[int(rt*128):,:int(rt*142)] = 0.                                
            #     # mska[int(rt*120):int(rt*150),int(rt*120):int(rt*175)] = 0.
            #     # mska[int(rt*90):int(rt*120),int(rt*120):int(rt*165)] = 0.
            # elif area == 'okh':
            #     mska[sstano < 0.] = 1.
            #     mska[:int(rt*134)] = 0.
            #     mska[int(rt*155):] = 0.
            #     mska[:,:int(rt*135)] = 0.
            #     mska[:,int(rt*165):] = 0.
            #     # mska[int(rt*133):,int(rt*150):] = 0.
            #     # mska[int(rt*128):,:int(rt*142)] = 0.
            #     jmin = int(rt*125); jmax = int(rt*150)
            #     imin = int(rt*150); imax = int(rt*165)     
            #     for j in range(jmin, jmax):
            #         for i in range(imax,imin-1,-1):
            #             mska[j,i] = 0
            #             if mskc[j,i] == 0:
            #                 break
            #             if sstano[j,i] > 0.:
            #                 break
            #     jmin = int(rt*130); jmax = int(rt*140)
            #     for j in range(jmin, jmax):
            #         imin = int(rt*135); imax0 = int(rt*145)    
            #         for i in range(imax0,imin-1,-1):
            #             imax = i
            #             if mskc[j,i] == 0:
            #                 break
            #         for i in range(imax,imin-1,-1):
            #             mska[j,i] = 0.
                                            
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

        # if cglbo:
        #     sstout.reshape(-1).astype('>f').tofile(fnameoutt)    

        if areas[0] != '':
            for na in range(nas):
                area = areas[na]
                mska = msks[na]

                fnameoutt = diro + model + '_anom/sst_TL159_CMIP6AMIP_'+str(ybgnc)+'-'+str(yendc)+'_annclm_'+area+'_anom_'+str(year)+'.dat'                  
        
                sstouta = sstout * mska + sstobs * (1-mska)
                sstouta.reshape(-1).astype('>f').tofile(fnameoutt)    

            # mska = (np.sum(msks, axis=0) > 0).astype(float)
            # area = areaadd            
            # fnameoutt = diro + model + '_anom/sst_TL159_CMIP6AMIP_'+str(ybgnc)+'-'+str(yendc)+'_annclm_'+area+'_anom_'+str(year)+'.dat'                  
        
            # sstouta = sstout * mska + sstobs * (1-mska)
            # sstouta.reshape(-1).astype('>f').tofile(fnameoutt)    

            if cexcl:
                mska = 1-mska
                area = 'ex'+areaadd 
                fnameoutt = diro + model + '_anom/sst_TL159_CMIP6AMIP_'+str(ybgnc)+'-'+str(yendc)+'_annclm_'+area+'_anom_'+str(year)+'.dat'                  
                
                sstouta = sstout * mska + sstobs * (1-mska)
                sstouta.reshape(-1).astype('>f').tofile(fnameoutt)    



if __name__ == '__main__':
    # pass
    main(areas, models, ybgn, yend, RES, cexcl = cexcl)    
