import os
import sys
import numpy as np
import subprocess
import shutil
BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE)
import config.config as cf
import cmip.cmip_mm as cmm
import boundary.pcmdi2mrigrd as o2m
import boundary.sst_glb_ano as sga
import boundary.sst_rgn_ano as sra
import boundary.sst_msk as smsk

ybgn = 1978; yend = 2015; RES = 'TL159'
models = cmm.read_models()
cbcs = True
# cbcs = False

print("create amip SST boundary data")
ruby_path = shutil.which("ruby")
if ruby_path is None:
    print("Ruby is not installed. Using a Python implementation instead, which may produce slightly different values.")
    o2m.main(ybgn, yend, RES)    
else:
    if cbcs:
        result = subprocess.run([ruby_path, BASE+"/boundary/sstice_linearinterp10.rb", RES, str(ybgn), str(yend), cf.datadir()+"obs/SST/input4MIPs/tosbcs_input4MIPs_SSTsAndSeaIce_CMIP_PCMDI-AMIP-1-1-0_gs1x1_187001-201512.nc", ])
    else:
        result = subprocess.run([ruby_path, BASE+"/boundary/sstice_linearinterp10.rb", RES, str(ybgn), str(yend), cf.datadir()+"obs/SST/input4MIPs/tos_input4MIPs_SSTsAndSeaIce_CMIP_PCMDI-AMIP-1-1-0_gs1x1_187001-201512.nc", ])    

print("create SST boundary data for GLB exp.")
sga.main(models, ybgn, yend, RES)


print("create SST boundary data for PAC and GLB-PAC exps.")
sra.main(['snp'], models, ybgn, yend, RES, cexcl = True)


print("create SST boundary data for WNP, EQ, and ENP exps.")
sra.main(['wnp', 'ceq', 'enp'], models, ybgn, yend, RES, cexcl = False)


print("create SST msk data")
smsk.main(models, RES)



