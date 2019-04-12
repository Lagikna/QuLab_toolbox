import numpy as np
import copy
import matplotlib.pyplot as plt
from ._wavedata import *


'''Wavedata 额外的分析模块，传入Wavedata类实例，进行分析'''


def Homodyne(wd, freq=50e6, cali=None):
    '''把信号按一定频率旋转，得到IQ相图'''
    w = 2*np.pi*freq
    res_wd=copy.deepcopy(wd)
    _wd=wd.trans('conj')
    for i in range(wd.size):
        t=wd.x[i]
        rotate = np.array([
        np.exp(1j*w*t),
        1j*np.exp(1j*w*t)
        ])
        res_wd.data[i]=complex(*np.real(rotate*_wd.data[i]))
    return res_wd

def Homodyne2(wd, freq=50e6, cali=None):
    '''把信号按一定频率旋转，得到IQ相图'''
    amp=wd.trans('abs')
    phase=wd.trans('angle') #角度
    _func=lambda t: 360*freq*t
    _domain=(0,wd.len)
    _sRate=wd.sRate
    _rotate=Wavedata.init(_func,_domain,_sRate)
    _phase=phase-_rotate
    res_data=amp.data*np.exp(1j*2*np.pi/360*_phase.data)
    res_wd=Wavedata(res_data,wd.sRate)
    return res_wd
