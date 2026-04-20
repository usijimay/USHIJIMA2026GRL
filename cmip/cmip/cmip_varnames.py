
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

def varname2vartyp(varname, interval = 'mon'):

    varnameso = ['obvfsq', 'mlotst', 'hfds','sob','hfcorr','tos', 'tosga', 'sosga', 'thetao', 
                'volo', 'msftbarot', 'soga', 'tob', 'zos', 'wfo', 'agessc', 'pso', 'so', 
                'masso', 'pbo', 'sfdsi', 'thetaoga', 'sos', 'zostoga', 
                'areacello', 
                'thetaohga', 'sohga']

    varnamesa = ['rsdt', 'uas', 'ta', 'clwvi', 'tauu', 'rlutcs', 'clivi', 'hur', 'sfcWind', 
                'tasmin', 'rsdscs', 'ccb', 'o3', 'huss', 'tas', 'cl', 'rsds', 'wap', 'rlds', 
                'vas', 'rsus', 'rlus', 'ua', 'ch4', 'ps', 'n2o', 'prw', 'rsuscs', 'prsn', 
                'tauv', 'prc', 'hurs', 'rsut', 'rlut', 'mc', 'ts', 'hus', 'hfls', 'cli', 'evspsbl', 
                'clw',  'hfss', 'va', 'cct', 'rldscs', 'sbl', 'tasmax', 'rsutcs', 'pr', 'clt', 
                'zg', 'ci', 'psl', 'co2', 
                'tasga', 
                'areacella']

    varnamess = ['siextentn', 'siarean', 'siconca', 'sivoln', 'siextents', 'siareas', 'sivols', 'siconc', 'sithick']

    if varname in varnameso:
        vartyp = 'O'+interval
    elif varname in varnamesa:
        vartyp = 'A'+interval
    elif varname in varnamess:
        vartyp = 'SI'+interval

    return vartyp


def order2varnames(order):
    if order == 0:
        varnames = ['tosga', 'sosga',  'volo', 'soga', 'masso', 'thetaoga', 'zostoga', 
                    'tasga', 
                    'siarean', 'siareas', 'sivoln', 'sivols']
    elif order == 1:
        varnames = []
    elif order == 2:
        varnames = ['mlotst', 'hfds', 'sob','hfcorr','tos', 'msftbarot', 'tob', 'zos', 'wfo', 'pso', 'pbo', 'sfdsi', 'sos', 'areacello', 
                    'uas', 'tauu', 'sfcWind', 'tasmin', 'tas', 'tasmax', 'vas', 'tauv', 'hfss',  'areacella', 
                    'siconc', 'siconca', 'sithick', 'siextentn', 'siextents']
    elif order == 3:
        varnames = ['obvfsq', 'thetao', 'agessc', 'so', 
                    'ta', 'ua', 'va']

    # elif (vartyp[0] == 'A') or (vartyp[0] == 'a'):        
    #     varnames = ['rsdt', 'uas', 'ta', 'clwvi', 'tauu', 'rlutcs', 'clivi', 'hur', 'sfcWind', 
    #                 'tasmin', 'rsdscs', 'ccb', 'o3', 'huss', 'tas', 'cl', 'rsds', 'wap', 'rlds', 
    #                 'vas', 'rsus', 'rlus', 'ua', 'ch4', 'ps', 'n2o', 'prw', 'rsuscs', 'prsn', 
    #                 'tauv', 'prc', 'hurs', 'rsut', 'rlut', 'mc', 'ts', 'hus', 'hfls', 'cli', 'evspsbl', 
    #                 'clw',  'hfss', 'va', 'cct', 'rldscs', 'sbl', 'tasmax', 'rsutcs', 'pr', 'clt', 
    #                 'zg', 'ci', 'psl', 'co2', 
    #                 'tasga', 
    #                 'areacella']

    #     varnames = ['rsdt', 'clwvi',  'rlutcs', 'clivi', 'hur', 
    #                 'rsdscs', 'ccb', 'o3', 'huss', 'cl', 'rsds', 'wap', 'rlds', 
    #                 'rsus', 'rlus', 'ch4', 'ps', 'n2o', 'prw', 'rsuscs', 'prsn', 
    #                 'prc', 'hurs', 'rsut', 'rlut', 'mc', 'ts', 'hus', 'hfls', 'cli', 'evspsbl', 
    #                 'clw',  'cct', 'rldscs', 'sbl', 'rsutcs', 'pr', 'clt', 
    #                 'zg', 'ci', 'psl', 'co2', ]


    return varnames
        
