import numpy as np
import copy
import matplotlib.pyplot as plt
from ._wavedata import Wavedata
from ._wd_func import *
from . import _Filter as F


'''Wavedata 额外的分析模块，传入Wavedata类实例，进行分析'''


def Analyze_cali(wd, freq=50e6, **kw):
    '''计算IQ波形的校正序列，准确性很好

    Parameters:
        wd: 包含IQ信息的Wavedata类实例
        freq: 校正的频率标准
    Return:
        cali_array: 2*3的序列，包含校正信息
    '''
    para_I=wd.I().getFFT([0,freq],mode='complex',half=False)
    para_Q=wd.Q().getFFT([0,freq],mode='complex',half=False)

    _offset_I,_offset_Q = para_I[0].real,para_Q[0].real
    amp_I,amp_Q = np.abs(para_I[1]),np.abs(para_Q[1])
    phase_I,phase_Q = np.angle(para_I[1],deg=True),np.angle(para_Q[1],deg=True)

    _scale_I, _scale_Q = 1, amp_Q/amp_I
    phi0 = 90
    # 相位范围转化为（-180，180）
    _phase_I, _phase_Q = 0, (phase_Q-phase_I+phi0+540)%360-180

    cali_array = np.array([[_scale_I,_offset_I,_phase_I],
                           [_scale_Q,_offset_Q,_phase_Q]]
                          ).round(decimals=3) # 保留3位小数
    return cali_array


def Calibrate(wd, freq=50e6, cali=None, **kw):
    '''校正波形

    Parameters:
        wd: 包含IQ信息的Wavedata类实例
        freq: 校正的频率标准
        cali: 2*3的序列，包含校正信息，可用Analyze_cali得到
    Return:
        _wd: 校正后的wd
    '''
    if cali is None:
        _wd = wd
    else:
        _cali = np.array(cali)
        _scale_I, _offset_I = _cali[0,:2]
        _scale_Q, _offset_Q = _cali[1,:2]
        #转为弧度
        _phi_I, _phi_Q = _cali[:,2]*np.pi/180

        # 相位校准，等效于进行波形时移，时移大小由相位误差、频率等决定
        shift_I = _phi_I/(2*np.pi*freq) if not freq==0 else 0
        shift_Q = _phi_Q/(2*np.pi*freq) if not freq==0 else 0

        # 相位校准，将I/Q插值函数平移后重新采样
        func_I = lambda x: wd.I().timeFunc(kind='cubic')(x-shift_I)
        _wd_I = Wavedata.init(func_I,(0,wd.len),wd.sRate)
        func_Q = lambda x: wd.Q().timeFunc(kind='cubic')(x-shift_Q)
        _wd_Q = Wavedata.init(func_Q,(0,wd.len),wd.sRate)

        # 反向校准，与vIQmixer中carry_wave校准相反
        _wd_I=(_wd_I-_offset_I)/_scale_I
        _wd_Q=(_wd_Q-_offset_Q)/_scale_Q

        _wd=_wd_I+1j*_wd_Q
    return _wd


def Homodyne(wd, freq=50e6, cali=None, **kw):
    '''把信号按一定频率旋转，得到解调的IQ

    Parameters:
        wd: 待解调Wavedata类实例
        freq: 旋转频率，正负表示不同的解调方向
        cali: 校正矩阵，默认不校正
    Return:
        res_wd: 解调后的wd
    '''
    if cali is None:
        _wd = wd
    else:
        _wd = Calibrate(wd, freq=freq, cali=cali, **kw)
    res_wd=_wd*Exp(-2*np.pi*freq,0,wd.len,wd.sRate)
    return res_wd


def filterGenerator(freqlist,bandwidth=1e6,fs=1e9):
    '''二阶IIRFilter带通滤波器的生成器

    Parameters：
        freqlist: 滤波频率列表
        bandwidth: 滤波带宽
        fs: 数字信号的采样率

    Return：
        迭代返回各频率滤波器
    '''
    for f in freqlist:
        flt=F.IIRFilter(2, [abs(f)-bandwidth/2, abs(f)+bandwidth/2], 0.01, 100, 'band', ftype='ellip', fs=fs)
        yield flt

def Demodulation(wd_raw,freqlist):
    '''解调迭代器

    Parameters：
        wd_raw: Wavedata类，待解调wd
        freqlist: 解调频率列表

    Return:
        迭代返回各频率解调后wd
    '''
    gk=F.GaussKernal(5,a=2.5)
    for f,flt in zip(freqlist,filterGenerator(freqlist)):
        iqcali = Analyze_cali(wd_raw, f)
        wd_cali = Calibrate(wd_raw, freq=f, cali=iqcali).filter(flt)
        wd_f = Homodyne(wd_cali, freq=f, cali=None).convolve(gk)
        yield wd_f

def dataMask(data,extend=0):
    '''获取数据的掩模

    Parameters:
        data: 一维数列或np.ndarray
        extend: 掩模扩展的点数
    
    Return:
        掩模数据(np.ndarray)，为0或1的二值序列
    '''
    data=np.array(data)
    maskdata=np.where(data==0,0,1)
    if extend != 0:
        k=np.ones(int(extend)*2+1)
        _data=np.convolve(maskdata,k,mode='same')
        maskdata=np.where(_data==0,0,1)
    return maskdata

def wdMask(wd,extend_len=0):
    '''获取Wavedata类实例的掩模

    Parameters:
        wd: Wavedata类的实例
        extend_len: 掩模扩展的时间长度，实际扩展点数与wd的采样率有关
    
    Return:
        掩模Wavedata类实例，data为0或1的二值序列
    '''
    assert isinstance(wd,Wavedata)
    extend = np.around(extend_len*wd.sRate).astype(int)
    maskdata = dataMask(wd.data,extend)
    return Wavedata(maskdata,wd.sRate)
