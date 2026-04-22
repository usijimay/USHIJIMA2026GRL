def figdir(dpi = None):
    import os

    date = '20260422/'
    if dpi == None:
        Res = 'ORG/'
    else:
        Res = 'High/'

    fdir =  'fig/'+date+Res

    if not os.path.isdir(fdir):
        os.makedirs(fdir)

    return fdir


def datadir():
    
    fdir = '/data16/theme-C/usijimay/mrisrv/glb050/'    

    return fdir
