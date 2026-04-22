
def vartyp2varnames(vartyp):
    if (vartyp[0] == 'O') or (vartyp[0] == 'o'):
        varnames = ['obvfsq', 'mlotst', 'hfds','sob','hfcorr','tos', 'tosga', 'sosga', 'thetao', 
                    'volo', 'msftbarot', 'soga', 'tob', 'zos', 'wfo', 'agessc', 'pso', 'so', 
                    'masso', 'pbo', 'sfdsi', 'thetaoga', 'sos', 'zostoga', 
                    'areacello', 
                    'thetaohga', 'sohga']
    elif (vartyp[0] == 'A') or (vartyp[0] == 'a'):        
        varnames = ['rsdt', 'uas', 'ta', 'clwvi', 'tauu', 'rlutcs', 'clivi', 'hur', 'sfcWind', 
                    'tasmin', 'rsdscs', 'ccb', 'o3', 'huss', 'tas', 'cl', 'rsds', 'wap', 'rlds', 
                    'vas', 'rsus', 'rlus', 'ua', 'ch4', 'ps', 'n2o', 'prw', 'rsuscs', 'prsn', 
                    'tauv', 'prc', 'hurs', 'rsut', 'rlut', 'mc', 'ts', 'hus', 'hfls', 'cli', 'evspsbl', 
                    'clw',  'hfss', 'va', 'cct', 'rldscs', 'sbl', 'tasmax', 'rsutcs', 'pr', 'clt', 
                    'zg', 'ci', 'psl', 'co2', 
                    'tasga', 
                    'areacella']
    elif (vartyp[0] == 'S') or (vartyp[0] == 's'):        
        varnames = ['siextentn', 'siarean', 'siconca', 'sivoln', 'siextents', 'siareas', 'sivols', 'siconc', 'sithick']

    return varnames

