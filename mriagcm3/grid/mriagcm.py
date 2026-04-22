import re
import os
import numpy as np

    
def lonlat(RES = 'TL159'):
    
    dlon = res2dlon(RES)
    lon = np.arange(0, 360, dlon)  
    
    basedir=os.path.dirname(os.path.abspath(__file__))+'/'    
    flat = open(basedir+RES+'_lat.txt', 'r')
    rls = flat.readlines()            
    flat.close()
    lat = np.array([])
    for rl in rls:
        lat = np.concatenate([lat,np.array(re.split(" +", rl)[1:-1]).astype(np.float)])

    return lon, lat

def res2dlon(RES):
    if RES == 'TL159':
        dlon = 1.125
    elif RES == 'TL319':
        dlon = 0.5625        
    elif RES == 'TL959':
        dlon = 0.1875    

    return dlon
