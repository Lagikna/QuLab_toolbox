import numpy as np
import copy
import matplotlib.pyplot as plt
from ._wavedata import Wavedata
from ._wd_func import *


'''Wavedata 额外的分析模块，传入Wavedata类实例，进行分析'''


def Homodyne(wd, freq=50e6, cali=None, DEG=True):
    '''把信号按一定频率旋转，得到解调的IQ'''
    if cali is None:
        cali = [[1,0,0],
                [1,0,0]]
    _cali = np.array(cali)
    _scale_I, _offset_I = _cali[0,:2]
    _scale_Q, _offset_Q = _cali[1,:2]
    if DEG:
        _phi_I, _phi_Q = _cali[:,2]*np.pi/180  #转为弧度
    else:
        _phi_I, _phi_Q = _cali[:,2]

    # 相位校准，等效于进行波形时移，时移大小由相位误差、频率等决定
    _shift_I = _phi_I/(2*np.pi*freq)
    _shift_Q = _phi_Q/(2*np.pi*freq)

    # 反向校准，与vIQmixer中carry_wave校准相反
    _wd_I=((wd.I()>>_shift_I)-_offset_I)/_scale_I
    _wd_Q=((wd.Q()>>_shift_Q)-_offset_Q)/_scale_Q

    _wd=_wd_I+1j*_wd_Q
    res_wd=_wd*Exp(-2*np.pi*freq,0,wd.len,wd.sRate)
    return res_wd

def Analyze_cali(wd, freq=50e6, DEG=True):
    '''根据IQ波形计算校正序列；
    振幅和补偿系数计算准确性好，
    相位系数准确性较差，与采样率有关，'''
    para_I=wd.I().getFFT([0,freq],mode='complex',half=True)
    para_Q=wd.Q().getFFT([0,freq],mode='complex',half=True)

    _offset_I,_offset_Q = para_I[0].real,para_Q[0].real
    amp_I,amp_Q = np.abs(para_I[1]),np.abs(para_Q[1])
    phase_I,phase_Q = np.angle(para_I[1],deg=DEG),np.angle(para_Q[1],deg=DEG)

    _scale_I, _scale_Q = 1, amp_Q/amp_I
    phi0 = 90 if DEG else np.pi/2
    _phase_I, _phase_Q = 0, phase_Q-phase_I+phi0

    cali_array = np.array([[_scale_I,_offset_I,_phase_I],
                           [_scale_Q,_offset_Q,_phase_Q]]
                          ).round(decimals=3) # 保留3位小数
    return cali_array
