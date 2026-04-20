# import os
# import numpy as np
# import sys
import netCDF4
# basedir=os.path.dirname(os.path.abspath(__file__))+'/'    
# sys.path.append(basedir+"../io_interface")
# import io_interface.nc_write as ncw
# sys.path.append(basedir+"../mri-agcm3")
# import extract_mnt2d as em2
# import extract_mnt3d as em3

# # idirbase = '/nas/personal/usijimay/TSE-C/AMIP/'
# expids = ['MPE4_amip_cntl', 'MPE4_amip_mri10_glb', 'MPE4_amip_mri10_tp', 'MPE4_amip_mri10_np', 'MPE4_amip_mri10_ac', 'MPE4_amip_mri10_exnptpac']
# # expids = ['MPE4_amip_cntl']

# expids = ['MPE3_agcm_cntl']
# # model0 = 'MPI-ESM-1-2-HAM'
# # areasns = ['glb', 'tpnpa', 'tpnp', 'tpna', 'npa']
# # areasns = ['glb', 'tpnpa', 'tp', 'npa']
# # expids = np.array(list(map(lambda x: 'MPE3_agcm_'+model0+'_'+x, areasns))).astype(object)

# ybgn = 1985; yend = 2014
# fbase = 'hs_ua.'
# varname = 'ua'
# nd = 3

# def main(expid, fbase, varname, nd, ybgn, yend, idirbase = '/data38/theme-C/usijimay/TSE-C/AMIP/', odirbase = '/data38/theme-C/usijimay/TSE-C/AMIP/'):


#     odir = odirbase + expid  + '/d_analy_a/'+str(ybgn)+'-'+str(yend)+'/'
#     if os.path.isdir(odir) == False:
#         os.makedirs(odir)    

#     ofile = odir+fbase+str(ybgn)+'-'+str(yend)

#     if nd == 2:
#         lon, lat, var = em2.ReadData2DY(expid, fbase, varname, ybgn, yend, dirbase = idirbase)
#         ncw.write_woa1x1_3d(ofile, np.arange(12), lon, lat, np.mean(var, axis=0), varname)       
#     elif nd == 3:
#         lon, lat, lev, var = em3.ReadData3DY(expid, fbase, varname, ybgn, yend, dirbase = idirbase)            
#         ncw.write_woa1x1_4d(ofile, np.arange(12), lev, lon, lat, np.mean(var, axis=0), varname)           
    
def ReadData3DClm(expid, fbase, varname, ybgn, yend, cann = False, dirbase = '/data38/theme-C/usijimay/TSE-C/AMIP/', dirbase0 = '/data38/theme-C/usijimay/TSE-C/AMIP/'):     

    fname = dirbase + expid + '/d_analy_a/'+str(ybgn)+'-'+str(yend)+'/'+fbase+str(ybgn)+'-'+str(yend)
    # if os.path.isfile(fname) == False:
    #     main(expid, fbase, varname, 3, ybgn, yend, idirbase = dirbase0, odirbase = dirbase)

    nc = netCDF4.Dataset(fname, 'r')
    lon = nc.variables['lon'][:]
    lat = nc.variables['lat'][:]
    lev = nc.variables['depth'][:]    
    var = nc.variables[varname][:]    

    return lon, lat, lev, var

def ReadData2DClm(expid, fbase, varname, ybgn, yend, cann = False, dirbase = '/data38/theme-C/usijimay/TSE-C/AMIP/', dirbase0 = '/data38/theme-C/usijimay/TSE-C/AMIP/'):     

    fname = dirbase + expid + '/d_analy_a/'+str(ybgn)+'-'+str(yend)+'/'+fbase+str(ybgn)+'-'+str(yend)
    if os.path.isfile(fname) == False:
        main(expid, fbase, varname, 2, ybgn, yend, idirbase = dirbase0, odirbase = dirbase)

    nc = netCDF4.Dataset(fname, 'r')
    lon = nc.variables['lon'][:]
    lat = nc.variables['lat'][:]
    var = nc.variables[varname][:]    

    return lon, lat, var



if __name__ == '__main__':
    for expid in expids:
        main(expid, fbase, varname, nd, ybgn, yend)    

