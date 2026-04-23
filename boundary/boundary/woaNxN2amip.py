import os
# import sys
import re
import numpy as np
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.append(BASE)

def area(lon0, lat0, var0, RES, dblat = BASE+'/mriagcm3/grid/', ERR = -9.99e33, clatglb = True, clonglb = True):

    if RES == 'TL159':
        dlon = 1.125        
    elif RES == 'TL319':
        dlon = 0.5625                
    elif RES == 'TL959':
        dlon = 0.1875
        
    lon = np.arange(0., 360., dlon)
    lonw = lon - 0.5 * dlon
    lone = lon + 0.5 * dlon    
        
    flat = open(dblat+RES+'_lat.txt', 'r')   
    rls = flat.readlines()            
    flat.close()
    lat = np.array([])
    for rl in rls:
        lat = np.concatenate([lat,np.array(re.split(" +", rl)[1:-1]).astype(np.float)])

    im = np.size(lon); jm = np.size(lat)
    
    lonw = lon - 0.5 * dlon
    lone = lon + 0.5 * dlon        
    lats = np.zeros(jm)
    lats[0] = -90
    for j in range(jm-1):
        lats[j+1] = 2. * lat[j] - lats[j]
    latn = np.r_[lats[1:], 90.]    

    
    var0 = var0.T
    shape = np.shape(var0)    
    im0, jm0 = shape[:2]
    
    isort = np.argsort(lon0)
    lon0 = lon0[isort]
    var0 = var0[isort]
    lon0 = np.r_[lon0-360,lon0,lon0+360]
    var0 = np.ma.vstack((var0,var0,var0))

    if 'Masked' in str(type(var0)):
        if np.size(var0.mask) > im*jm-1:            
            msk = 1-var0.mask
        else:
            msk = np.abs(var0) < 0.1 * np.abs(ERR)
    else:
        msk = np.abs(var0) < 0.1 * np.abs(ERR)
    
    dlat0 = np.diff(lat0[:2])[0]
    dlon0 = np.diff(lon0[:2])[0]
    
    lon0w = lon0-0.5*dlon0
    lon0e = lon0+0.5*dlon0

    lat0s = lat0-0.5*dlat0
    lat0n = lat0+0.5*dlat0    
            
    
    # vrgd = ERR * np.ones(np.r_[im,jm,shape[2:]])
    vrgd = np.zeros(np.r_[im,jm,shape[2:]])
    area = np.zeros(np.r_[im,jm,shape[2:]])            
    for i in range(im):
        ii = np.where((lonw[i] <= lon0e)*(lon0w < lone[i]))[0]
        for j in range(jm):
            jj = np.where((lats[j] <= lat0n)*(lat0s < latn[j]))[0]

            for ni in range(np.size(ii)):
                if ni == 0:
                    dx0 = np.deg2rad(lon0e[ii[ni]] - lonw[i])
                elif ni == np.size(ii) - 1:
                    dx0 = np.deg2rad(lone[i] - lon0w[ii[ni]])
                else:
                    dx0 = np.deg2rad(lon0e[ii[ni]] - lon0w[ii[ni]])                                        
                for nj in range(np.size(jj)):
                    if nj == 0:
                        area0 = dx0 * (np.sin(np.deg2rad(lat0n[jj[nj]])) - np.sin(np.deg2rad(lats[j]))) * msk[ii[ni],jj[nj]]
                    elif nj == np.size(jj)-1:
                        area0 = dx0 * (np.sin(np.deg2rad(latn[j])) - np.sin(np.deg2rad(lat0s[jj[nj]]))) * msk[ii[ni],jj[nj]]
                    else:
                        area0 = dx0 * (np.sin(np.deg2rad(lat0n[jj[nj]])) - np.sin(np.deg2rad(lat0s[jj[nj]]))) * msk[ii[ni],jj[nj]]
                        
                    area[i,j] = area[i,j] + area0    
                    vrgd[i,j] = vrgd[i,j] + var0[ii[ni],jj[nj]] * area0

            # if area > 0.:
            #     vrgd[i,j] = vtmp/area

    vrgd[area == 0.] = ERR
    vrgd[area > 0.] = vrgd[area > 0.]/area[area > 0.]
    vrgd = np.ma.masked_array(vrgd, mask = (vrgd == ERR), fill_value = ERR)
    vrgd = vrgd.T

    return lon, lat, vrgd
