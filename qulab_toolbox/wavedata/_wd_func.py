import numpy as np
# import matplotlib.pyplot as plt
from ._wavedata import *

def DRAGpulse(width=0, sRate=1e2, a=0.5, TYPE=Gaussian2, **kw):
    '''DRAG波形 a为系数'''
    I = TYPE(width, sRate, **kw)
    Q = a*I.derivative()
    return I+1j*Q

def DRAG_wd(wd, a=0.5):
    '''DRAG给定的Wavedata类波形'''
    assert isinstance(wd, Wavedata)
    assert not wd.isIQ
    I = wd
    Q = a*I.derivative()
    return I+1j*Q

def Exp(w, phi=0, width=0, sRate=1e2):
    ''''''
    timeFunc = lambda t: np.exp(1j*(w*t+phi))
    domain=(0,width)
    return Wavedata.init(timeFunc,domain,sRate)
