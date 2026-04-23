import os

def figdir(dpi = None):

    date = '20260423/'
    if dpi == None:
        Res = 'ORG/'
    else:
        Res = 'High/'

    fdir =  'fig/'+date+Res

    if not os.path.isdir(fdir):
        os.makedirs(fdir)

    return fdir


def datadir():

    BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fdir = os.path.dirname(BASE)+'/Data/'

    return fdir
