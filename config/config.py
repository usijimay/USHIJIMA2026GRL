def figdir(dpi = None):
    import os

    date = '20260420/'
    if dpi == None:
        Res = 'ORG/'
    else:
        Res = 'High/'

    fdir =  'fig/'+date+Res

    if not os.path.isdir(fdir):
        os.makedirs(fdir)

    return fdir



def anldir():

    fdir = '/data16/theme-C/usijimay/mrisrv/glb287/JPN/anlpy/'    

    return fdir

def libdir():
    
    fdir = '/data16/theme-C/usijimay/mrisrv/glb287/anl_esm/anlpy/'
    # fdir = '/home/usijimay/anl_esm/anlpy/'    

    return fdir    

def datadir():
    
    # fdir = '/nas/personal/usijimay/'
    fdir = '/data16/theme-C/usijimay/mrisrv/glb050/'    

    return fdir
