import numpy as np
import copy
import matplotlib.pyplot as plt
from ._wavedata import *
from ._wd_func import Exp


'''Wavedata 额外的分析模块，传入Wavedata类实例，进行分析'''


def Homodyne(wd, freq=50e6, cali=None):
    '''把信号按一定频率旋转，得到解调的IQ'''
    w = -2*np.pi*freq
    res_wd=wd*Exp(w,0,wd.len,wd.sRate)
    return res_wd
