import numpy as np
from ._wavedata import Wavedata
import scipy.signal as signal
from scipy.stats import multivariate_normal
import matplotlib.pyplot as plt

'''Wavedata 滤波器模块，包含一些数字滤波器'''

class Filter(object):
    """滤波器基类，默认不处理波形，可传入一个处理函数产生相应的滤波器实例"""
    def __init__(self, process=None):
        self._process = process

    def process(self,data,sRate):
        '''Filter处理函数，输入输出都是(data,sRate)格式'''
        if self._process is not None:
            data,sRate = self._process(data,sRate)
        return data,sRate

    def filt(self,wd):
        '''传入Wavedata实例，返回滤波后的Waveda'''
        assert isinstance(wd,Wavedata)
        data,sRate = self.process(wd.data,wd.sRate)
        return Wavedata(data,sRate)


def series(*arg):
    '''串联多个Filter'''
    def process(data,sRate):
        for f in arg:
            data,sRate = f.process(data,sRate)
        return data,sRate
    F = Filter(process)
    return F


def parallel(*arg):
    '''并联多个Filter'''
    def process(data,sRate):
        d_list = [f.process(data,sRate)[0] for f in arg]
        d = np.array(d_list).sum(axis=0)/len(arg)
        return d,sRate
    F = Filter(process)
    return F


class WGN(Filter):
    '''White Gaussian Noise adder: 向波形w中添加一个信噪比为 snr dB 的高斯白噪声'''
    def __init__(self, snr):
        self.snr = snr

    def process(self,data,sRate):
        x=data
        snr = 10**(self.snr/10.0)
        xpower = np.sum(x**2)/len(x)
        npower = xpower / snr
        n = np.random.randn(len(x)) * np.sqrt(npower)
        _data = x + n
        return _data,sRate


class baFilter(Filter):
    """指定signal模块里包含的滤波器函数名,生成相关的结果为 ba 的数字滤波器."""
    def __init__(self, name='', **kw):
        # 指定signal里包含的滤波器函数名,传入相关的参数
        kw.update(output='ba',analog=False)
        self.dict=kw  # self.dict必须包含fs
        filtertype = getattr(signal,name)
        self.ba = filtertype(**self.dict)

    def process(self,data,sRate):
        assert sRate == self.dict['fs']
        b,a = self.ba
        _data = signal.filtfilt(b, a, data)
        return _data, sRate

    def freqz(self):
        '''返回数字滤波器频率响应'''
        w,h = signal.freqz(*self.ba,fs=self.dict['fs'])
        return w,h

    def plot(self):
        '''画出频率响应曲线'''
        ax=plt.gca()
        w,h=self.freqz()
        line,=ax.plot(w, np.abs(h),'r-',label='Amplitude')
        ax.set_xlabel('Frequency')
        ax.set_ylabel('Amplitude Factor')
        ax1=plt.twinx()
        line1,=ax1.plot(w, np.angle(h,deg=True),'b--',label='Phase')
        ax1.set_ylabel('Phase Factor')
        # plt.legend([line,line1],['Amplitude','Phase'],loc='best')
        return [line,line1]


class IIRFilter(baFilter):
    '''参考scipy.signal.iirfilter'''
    def __init__(self, N=2, Wn=[49e6, 51e6], rp=0.01, rs=100, btype='band',
                     ftype='ellip', fs=1e9):
        # 为避免麻烦，不继承 baFilter.__init__ 函数，只继承其他函数
        # 默认参数是一个50MHz的 ellip 滤波器
        # 配置字典, default: output='ba',analog=False,
        self.dict=dict(N=N, Wn=Wn, rp=rp, rs=rs, btype=btype,
                        analog=False, ftype=ftype, output='ba', fs=fs)
        self.ba = signal.iirfilter(**self.dict)

class BesselFilter(baFilter):
    '''参考scipy.signal.bessel'''
    def __init__(self, N=2, Wn=100e6, btype='low',
                     norm='phase', fs=1e9):
        # 为避免麻烦，不继承 baFilter.__init__ 函数，只继承其他函数
        # 默认参数是一个100MHz的 2阶低通贝塞尔滤波器
        # 配置字典, default: output='ba',analog=False,
        self.dict=dict(N=N, Wn=Wn, btype=btype,
                        analog=False, output='ba', norm=norm, fs=fs)
        self.ba = signal.bessel(**self.dict)


def GaussKernal2D(halfsize,a=2,factor=1,xy='X',):
    '''产生二维高斯卷积核

    Parameters：
        halfsize: int, 卷积核矩阵的长度为（2 * halfsize + 1）
        a: float, 高斯分布函数的取值范围与方差的比值
        factor: float, 二维高斯函数的协方差系数因子
        xy: ['X','Y'], 控制协方差系数的模式

    Return:
        m: 二维 np.ndarray, 二维高斯卷积核
    '''
    mean=[0,0]
    if xy=='X':
        cov=[[1,0],[0,factor]]
    elif xy=='Y':
        cov=[[factor,0],[0,1]]
    else:
        cov=[[1,0],[0,1]]
    rv = multivariate_normal(mean, cov)
    x0=np.linspace(-a,a,2*halfsize+1)
    x,y=np.meshgrid(x0,x0)
    pos = np.dstack((x, y))
    _m=rv.pdf(pos)
    m=_m/np.sum(_m)
    return m

def GaussKernal(halfsize,a=2):
    '''产生一维高斯卷积核

    Parameters：
        halfsize: int, 半边长，卷积核矩阵的长度为（2 * halfsize + 1）
        a: float, 高斯分布函数的取值范围与方差的比值

    Return:
        m: 一维 np.ndarray, 一维高斯卷积核
    '''
    rv = multivariate_normal(0, 1)
    x0=np.linspace(-a,a,2*halfsize+1)
    _m=rv.pdf(x0)
    m=_m/np.sum(_m)
    return m

class GaussFilter(Filter):
    '''高斯低通数字滤波器，通过卷积实现'''
    def __init__(self,halfsize,a=2):
        self.kernal=GaussKernal(halfsize,a)

    def process(self,data,sRate):
        _data=np.convolve(data,self.kernal,mode='same')
        return _data,sRate

    def plot(self,sRate=1e9):
        ax=plt.gca()
        wd_gk_FFT = Wavedata(self.kernal,sRate).append(1000,1000).FFT()
        line1,=wd_gk_FFT.trans('amp').plot(isfft=True,fmt1='r-',label='Amplitude')
        ax.set_xlabel('Frequency')
        ax.set_ylabel('Amplitude Factor')
        # ax1=plt.twinx()
        # line2,=wd_gk_FFT.trans('phase').plot(isfft=True,fmt1='b--',label='Phase')
        # ax1.set_ylabel('Phase Factor')
        return [line1,]

def removeDC(data,sRate):
    '''去除直流成分，可以近似为扣除平均值'''
    _data=np.array(data)-np.mean(data)
    return _data,sRate

# 滤波器实例，可直接使用
DCBlock=Filter(removeDC)

def bandpass(center=None,span=None,start=None,stop=None,fs=1e9):
    '''生成IIRFilter的一个带通滤波器实例'''
    if start is not None and stop is not None:
        start,stop=start,stop
    elif center is not None and span is not None:
        start,stop=abs(center)-span/2, abs(center)+span/2
    else:
        raise('Band Frequency Setting Error!')
    flt=IIRFilter(2, [start,stop], 0.01, 100, 'band', ftype='ellip', fs=fs)
    return flt

def lowpass(freq,fs=1e9):
    '''生成IIRFilter的一个低通滤波器实例'''
    flt=IIRFilter(2, abs(freq), 0.01, 100, 'low', ftype='ellip', fs=fs)
    return flt

def highpass(freq,fs=1e9):
    '''生成IIRFilter的一个高通滤波器实例'''
    flt=IIRFilter(2, abs(freq), 0.01, 100, 'high', ftype='ellip', fs=fs)
    return flt